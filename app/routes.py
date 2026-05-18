import subprocess
import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from app import db
from app.models import Agent
# Import our function that uses Mem0
from app.gemini import get_ai_response_with_memory

bp = Blueprint('main', __name__)

# --- ADMIN PANEL ---
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        agent_name = request.form.get('agent_name', '').strip()
        agent_instructions = request.form.get('agent_instructions', '').strip()

        if not agent_name or not agent_instructions:
            return "Both agent name and instructions are required.", 400

        if len(agent_name) > current_app.config['MAX_AGENT_NAME_LENGTH']:
            return "Agent name is too long.", 400

        if len(agent_instructions) > current_app.config['MAX_AGENT_INSTRUCTIONS_LENGTH']:
            return "Agent instructions are too long.", 400

        new_agent = Agent(name=agent_name, instructions=agent_instructions)
        db.session.add(new_agent)
        db.session.commit()
        return redirect(url_for('main.index'))

    all_agents = Agent.query.all()
    return render_template("admin.html", agents=all_agents)




# --- SHOW CHAT PAGE ---
@bp.route('/agent/<int:agent_id>')
def chat_page(agent_id):
    agent = db.session.get(Agent, agent_id)
    if not agent:
        return "Agent not found", 404
    return render_template("chat.html", agent=agent)

# --- HANDLE CHAT MESSAGE (API) ---
@bp.route('/chat/<int:agent_id>', methods=['POST'])
def chat_api(agent_id):
    data = request.get_json(silent=True) or {}
    user_question = data.get('question', '')

    if not isinstance(user_question, str) or not user_question.strip():
        return jsonify({"response": "Question is required."}), 400

    user_question = user_question.strip()
    if len(user_question) > current_app.config['MAX_MESSAGE_LENGTH']:
        return jsonify({"response": "Question is too long."}), 400
    
    agent = db.session.get(Agent, agent_id)
    if not agent:
        return jsonify({"response": "Agent not found"}), 404

    # Use Mem0 to get the answer
    # We use the agent's instructions as the "Knowledge" for now
    # In the next milestone, we will add the file contents here too.
    ai_response = get_ai_response_with_memory(
        agent_id=agent_id,
        knowledge=agent.instructions, 
        question=user_question
    )

    # Mem0 returns a dictionary usually, we want the string text
    if isinstance(ai_response, dict) and 'messages' in ai_response:
         # Extract the last message (the answer)
         final_answer = ai_response['messages'][-1]['content']
    elif isinstance(ai_response, str):
         final_answer = ai_response
    else:
         final_answer = str(ai_response)

    return jsonify({"response": final_answer})


# --- NEW DELETE ROUTE ---
@bp.route('/delete/<int:agent_id>', methods=['POST'])
def delete_agent(agent_id):
    agent = db.session.get(Agent, agent_id)
    if not agent:
        return "Agent not found", 404
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('main.index'))



# --- THE MAGIC DOOR (CI/CD) ---
# ... (Your existing imports)

# --- THE MAGIC DOOR (FIXED) ---
@bp.route('/update_server', methods=['POST'])
def webhook():
    deploy_secret = current_app.config.get('DEPLOY_WEBHOOK_SECRET')
    request_secret = request.headers.get('X-Deploy-Token')
    if not deploy_secret:
        current_app.logger.error("Deploy webhook secret is not configured.")
        return "Webhook is not configured.", 503
    if request_secret != deploy_secret:
        return "Unauthorized", 403

    repo_path = current_app.config.get('DEPLOY_REPO_PATH')
    wsgi_path = current_app.config.get('DEPLOY_WSGI_PATH')
    expected_remote = current_app.config.get('DEPLOY_EXPECTED_REMOTE_URL')
    expected_branch = current_app.config.get('DEPLOY_EXPECTED_BRANCH', 'main')
    if not repo_path or not wsgi_path:
        current_app.logger.error("Deploy paths are not configured.")
        return "Webhook is not configured.", 503

    try:
        if expected_remote:
            remote_result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                check=True,
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            actual_remote = remote_result.stdout.strip()
            if actual_remote != expected_remote:
                current_app.logger.error("Unexpected git remote origin configured for deploy path.")
                return "Update failed.", 500

        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        actual_branch = branch_result.stdout.strip()
        if actual_branch != expected_branch:
            current_app.logger.error("Unexpected branch checked out for deploy path.")
            return "Update failed.", 500

        subprocess.run(
            ["git", "pull", "--ff-only"],
            check=True,
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if os.path.exists(wsgi_path):
            os.utime(wsgi_path, None)
            return "Updated and reloaded successfully!", 200

        current_app.logger.error("WSGI file not found at configured path.")
        return "Update applied successfully, but server reload failed: WSGI file not found.", 500
    except subprocess.CalledProcessError:
        current_app.logger.exception("Git pull failed during deploy webhook.")
        return "Update failed.", 500
