from flask import current_app
from google import genai
from app import db
from app.models import Conversation

def get_ai_response_with_memory(agent_id, knowledge, question):
    try:
        # 1. Fetch History from Database
        # We get the last 10 messages to keep context
        history_records = Conversation.query.filter_by(agent_id=agent_id).order_by(Conversation.timestamp.asc()).limit(10).all()
        
        history_text = ""
        for record in history_records:
            history_text += f"{record.role}: {record.content}\n"

        # 2. Build Prompt
        prompt = f"""
        You are a helpful AI agent.
        
        [Instructions & Knowledge]
        {knowledge}
        
        [Conversation History]
        {history_text}
        
        [User Question]
        {question}
        
        Answer the question based on the history and knowledge.
        """

        # 3. Call Gemini
        api_key = current_app.config['GEMINI_API_KEY']
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=prompt
        )
        answer = response.text

        # 4. Save New Memory (User Question + AI Answer)
        user_msg = Conversation(role="user", content=question, agent_id=agent_id)
        ai_msg = Conversation(role="model", content=answer, agent_id=agent_id)
        
        db.session.add(user_msg)
        db.session.add(ai_msg)
        db.session.commit()

        return answer

    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"