from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Agent # <-- NEW: Import the Agent model
from app.gemini import get_gemini_response

bp = Blueprint('main', __name__)

# --- UPDATED ADMIN PANEL ROUTE ---
@bp.route('/', methods=['GET', 'POST']) # <-- NEW: Allow 'POST' requests
def index():
    # This part handles the "POST" request when you submit the form
    if request.method == 'POST':
        # Get the data from the form
        agent_name = request.form['agent_name']
        agent_instructions = request.form['agent_instructions']
        
        # Create a new Agent object
        new_agent = Agent(name=agent_name, instructions=agent_instructions)
        
        # Add it to the database
        db.session.add(new_agent)
        db.session.commit()
        
        # Redirect back to the same page (to clear the form)
        return redirect(url_for('main.index'))

    # This part handles the "GET" request (when you just load the page)
    # It fetches all agents from the database
    all_agents = Agent.query.all()
    
    # It passes the list of agents to the HTML page
    return render_template("admin.html", agents=all_agents)


# --- THIS IS OUR TEST ROUTE (we'll keep it for now) ---
@bp.route('/test-ai')
def test_ai():
    test_knowledge = "The company IntelliVerse is working on an AI agent builder. Gevverson is a developer helping with the project."
    test_question = "What is Gevverson's role?"
    answer = get_gemini_response(test_knowledge, test_question)
    
    return f"""
    <h1>AI Test Page</h1>
    <p><b>Knowledge:</b> {test_knowledge}</p>
    <p><b>Question:</b> {test_question}</p>
    <hr>
    <p><b>AI Answer:</b> {answer}</p>
    """