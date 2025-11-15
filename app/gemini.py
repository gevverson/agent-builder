import google.generativeai as genai
from flask import current_app

def get_gemini_response(knowledge, question):
    """
    Gets a response from the Gemini API based on provided knowledge and a question.
    """
    
    # 1. Get the API Key from our app's config
    # We use current_app.config to access it from anywhere in our app
    api_key = current_app.config['GEMINI_API_KEY']
    
    if not api_key:
        return "Error: GEMINI_API_KEY is not set. Please check your .env file."

    try:
        # 2. Configure the Gemini API library with our key
        genai.configure(api_key=api_key)
        
        # 3. Create the AI model
        # We use 'gemini-pro' which is the standard, reliable model
         
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        # 4. Create the prompt for the AI
        # This is the "instruction" for the agent.
        # We tell it to *only* use the knowledge we provide.
        prompt = f"""
        You are a helpful assistant. Answer the user's question based ONLY on the following knowledge.
        If the answer is not in the knowledge, say "I do not have that information."

        Knowledge:
        ---
        {knowledge}
        ---

        Question:
        {question}
        """
        
        # 5. Send the prompt to the AI and get a response
        response = model.generate_content(prompt)
        
        # 6. Return the AI's answer as plain text
        return response.text
        
    except Exception as e:
        # Handle any errors (like a bad API key or internet issue)
        print(f"Error calling Gemini API: {e}")
        return f"Error: Could not connect to the AI service. {e}"
    




def list_available_models():
    """
    Lists all models available to the current API key.
    """
    api_key = current_app.config['GEMINI_API_KEY']
    if not api_key:
        return "Error: GEMINI_API_KEY is not set."

    try:
        genai.configure(api_key=api_key)

        models_list = []
        for m in genai.list_models():
            # We only care about models that can generate content
            if 'generateContent' in m.supported_generation_methods:
                models_list.append(m.name)

        return models_list

    except Exception as e:
        print(f"Error listing models: {e}")
        return f"Error: {e}"


















