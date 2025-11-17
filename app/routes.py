from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Agent
# Import our function that uses Mem0
from app.gemini import get_ai_response_with_memory

bp = Blueprint('main', __name__)

# --- ADMIN PANEL ---
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        agent_name = request.form['agent_name']
        agent_instructions = request.form['agent_instructions']
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
    data = request.get_json()
    user_question = data.get('question')
    
    agent = db.session.get(Agent, agent_id)
    if not agent:
        return jsonify({"response": "Agent not found"}), 404

    # Use Mem0 to get the answer
    # We use the agent's instructions as the "Knowledge" for now
    # In the next milestone, we will add the file contents here too.
    ai_response = get_ai_response_with_memory(
        agent_id=f"agent_{agent_id}", # Unique ID for Mem0 memory
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
    if agent:
        db.session.delete(agent)
        db.session.commit()
    return redirect(url_for('main.index'))