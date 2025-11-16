import google.generativeai as genai
from flask import current_app

def get_gemini_response(knowledge, history, question):
    """
    Gets a response from the Gemini API, using our OWN history.
    """

    api_key = current_app.config['GEMINI_API_KEY']

    if not api_key:
        return "Error: GEMINI_API_KEY is not set."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')

        # This is our new prompt. It includes HISTORY.
        prompt = f"""
        You are a helpful assistant. Answer the user's question based ONLY on the following knowledge
        and your conversation history.

        Conversation History:
        ---
        {history}
        ---

        Knowledge:
        ---
        {knowledge}
        ---

        Question:
        {question}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error: Could not connect to the AI service. {e}"