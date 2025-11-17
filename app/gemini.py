from app import mem0
from flask import current_app
from google import genai

def get_ai_response_with_memory(agent_id, knowledge, question):
    """
    Manually handles the memory cycle: Add -> Search -> Generate -> Add
    """
    try:
        # --- 1. ADD USER QUESTION TO MEMORY ---
        mem0.add(question, user_id=agent_id)

        # --- 2. SEARCH FOR RELEVANT MEMORIES ---
        previous_memories = mem0.search(question, user_id=agent_id)
        
        print(f"[DEBUG] RAW MEMORIES: {previous_memories}")

        # --- FIX: Handle the 'results' dictionary format ---
        memory_list = []
        if isinstance(previous_memories, dict) and 'results' in previous_memories:
            memory_list = previous_memories['results']
        elif isinstance(previous_memories, list):
            memory_list = previous_memories
            
        memory_text = ""
        for m in memory_list:
            if 'memory' in m:
                memory_text += f"- {m['memory']}\n"
        
        print(f"[DEBUG] FINAL CONTEXT PASSED TO AI:\n{memory_text}")

        # --- 3. GENERATE ANSWER (Using Gemini Directly) ---
        api_key = current_app.config['GEMINI_API_KEY']
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are a helpful AI agent. 
        
        [Relevant Memory]
        {memory_text}
        
        [Knowledge Base]
        {knowledge}
        
        [User Question]
        {question}
        
        Answer the question naturally. If the Memory contains the answer (like the user's name), USE IT.
        """
        
        response = client.models.generate_content(
            model='gemini-flash-latest', 
            contents=prompt
        )
        
        answer = response.text

        # --- 4. ADD AI ANSWER TO MEMORY ---
        mem0.add(answer, user_id=agent_id)
        
        return answer

    except Exception as e:
        print(f"Error in AI Logic: {e}")
        return f"I'm sorry, I encountered an error: {e}"