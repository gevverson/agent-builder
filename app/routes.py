from flask import Blueprint, render_template
from app.gemini import get_gemini_response # Import the main function

bp = Blueprint('main', __name__)

# This is the route for your admin panel
@bp.route('/')
def index():
    return render_template("admin.html")


# --- THIS IS OUR TEST ROUTE, NOW RESTORED ---
@bp.route('/test-ai')
def test_ai():
    # We'll pretend we have this knowledge:
    test_knowledge = "The company IntelliVerse is working on an AI agent builder. Gevverson is a developer helping with the project."

    # And we'll pretend the user asked this question:
    test_question = "What is Gevverson's role?"

    # Call our AI function
    answer = get_gemini_response(test_knowledge, test_question)

    # Show the answer directly in the browser
    return f"""
    <h1>AI Test Page</h1>
    <p><b>Knowledge:</b> {test_knowledge}</p>
    <p><b>Question:</b> {test_question}</p>
    <hr>
    <p><b>AI Answer:</b> {answer}</p>
    """