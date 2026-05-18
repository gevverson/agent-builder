from flask import current_app
from google import genai
from app import db
from app.models import Conversation

def normalize_agent_id(agent_id):
    if isinstance(agent_id, int):
        return agent_id
    if isinstance(agent_id, str):
        candidate = agent_id
        if candidate.startswith("agent_"):
            candidate = candidate.split("agent_", 1)[1]
        if candidate.isdigit():
            return int(candidate)
    raise ValueError("Invalid agent ID")

def get_ai_response_with_memory(agent_id, knowledge, question):
    try:
        normalized_agent_id = normalize_agent_id(agent_id)
        max_message_length = current_app.config.get('MAX_MESSAGE_LENGTH', 2000)
        if not isinstance(question, str) or not question.strip():
            return "Please ask a valid question."

        question = question.strip()
        if len(question) > max_message_length:
            return "Question is too long."
        knowledge = (knowledge or '').strip()

        # 1. Fetch History from Database (latest 10 messages, returned oldest->newest)
        history_records = (
            Conversation.query
            .filter(
                Conversation.id.in_(
                    db.session.query(Conversation.id)
                    .filter_by(agent_id=normalized_agent_id)
                    .order_by(Conversation.timestamp.desc())
                    .limit(10)
                )
            )
            .order_by(Conversation.timestamp.asc())
            .all()
        )
        
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
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            current_app.logger.error("GEMINI_API_KEY is not configured.")
            return "AI service is not configured."

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=prompt
        )
        answer = getattr(response, 'text', None)
        if not answer:
            current_app.logger.error("Gemini returned an empty response payload.")
            answer = "I couldn't generate a response right now."

        # 4. Save New Memory (User Question + AI Answer)
        user_msg = Conversation(role="user", content=question, agent_id=normalized_agent_id)
        ai_msg = Conversation(role="model", content=answer, agent_id=normalized_agent_id)
        
        db.session.add(user_msg)
        db.session.add(ai_msg)
        db.session.commit()

        return answer

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Error generating AI response.")
        return "Sorry, something went wrong while generating a response."
