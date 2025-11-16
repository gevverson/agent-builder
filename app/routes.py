from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Agent, Conversation # Import Conversation
from app.gemini import get_gemini_response

bp = Blueprint('main', __name__)

# --- ADMIN PANEL ROUTE ---
# This is the code from Milestone 3
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


# --- TEST ROUTE ---
@bp.route('/test-ai')
def test_ai():
    # Let's use the Agent with ID=1 for this test
    # (Make sure you have created at least one agent in the admin panel!)
    agent = db.session.get(Agent, 1)
    if not agent:
        return "Error: Please go to the <a href='/'>Admin Page</a> and create an agent first."

    # 1. CREATE KNOWLEDGE AND QUESTION
    test_knowledge = "Gevverson is a developer."
    test_question = "What is Gevverson's role?"

    # 2. GET HISTORY FROM OUR *OWN* DATABASE
    history_tuples = db.session.query(Conversation.role, Conversation.content).filter_by(agent_id=agent.id).all()
    history = "\n".join([f"{role}: {content}" for role, content in history_tuples])

    # 3. GET AI RESPONSE
    answer = get_gemini_response(test_knowledge, history, test_question)

    # 4. SAVE TO MEMORY (OUR DATABASE)
    user_message = Conversation(role="user", content=test_question, agent_id=agent.id)
    model_message = Conversation(role="model", content=answer, agent_id=agent.id)
    db.session.add_all([user_message, model_message])
    db.session.commit()

    return f"""
    <h1>AI Test Page (With *Reliable* Memory)</h1>
    <p><b>Agent:</b> {agent.name}</p>
    <p><b>History:</b> {history}</p>
    <p><b>Knowledge:</b> {test_knowledge}</p>
    <p><b>Question:</b> {test_question}</p>
    <hr>
    <p><b>AI Answer:</b> {answer}</p>
    <hr>
    <a href="/test-memory">Click here to test memory</a>
    """

# --- TEST MEMORY ROUTE ---
@bp.route('/test-memory')
def test_memory():
    agent = db.session.get(Agent, 1)
    if not agent:
        return "Error: Please go to the <a href='/'>Admin Page</a> and create an agent first."

    # 1. NO KNOWLEDGE
    test_knowledge = "Nothing."
    test_question = "What role did I just ask about?" # Ask about the memory

    # 2. GET HISTORY FROM OUR *OWN* DATABASE
    history_tuples = db.session.query(Conversation.role, Conversation.content).filter_by(agent_id=agent.id).all()
    history = "\n".join([f"{role}: {content}" for role, content in history_tuples])

    # 3. GET AI RESPONSE
    answer = get_gemini_response(test_knowledge, history, test_question)

    # 4. SAVE TO MEMORY
    user_message = Conversation(role="user", content=test_question, agent_id=agent.id)
    model_message = Conversation(role="model", content=answer, agent_id=agent.id)
    db.session.add_all([user_message, model_message])
    db.session.commit()

    return f"""
    <h1>AI Test Page (Memory Check)</h1>
    <p><b>Agent:</b> {agent.name}</p>
    <p><b>History:</b> {history}</p>
    <p><b>Knowledge:</b> {test_knowledge}</p>
    <p><b>Question:</b> {test_question}</p>
    <hr>
    <p><b>AI Answer:</b> {answer}</p>
    <hr>
    <p><i>(If the AI answered, it's because it read from our database!)</i></p>
    <a href="/">Go Home</a>
    """