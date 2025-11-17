from app import mem0

def get_ai_response_with_memory(agent_id, knowledge, question):
    """
    Uses Mem0 to store memory and Gemini to answer.
    """
    # 1. Construct the prompt
    prompt = f"""
    Knowledge Base:
    {knowledge}
    
    User Question:
    {question}
    """

    # 2. Add the USER interaction to memory
    # This saves "What is Gevverson's role?" to the database
    mem0.add(question, user_id=agent_id)

    # 3. Retrieve relevant memories (The "Search" part)
    # Mem0 finds old facts related to this question
    memories = mem0.search(question, user_id=agent_id)
    
    # 4. Create a context string from memories
    memory_context = ""
    for m in memories:
        # Extract the 'memory' text from the result dictionary
        if 'memory' in m:
            memory_context += f"- {m['memory']}\n"

    # 5. Send everything to the Chat (Mem0 handles the LLM call if configured,
    # but for total control, we can also just use the context).
    # BUT, since we configured LLM in init.py, we can let Mem0 handle the chat generation:
    
    # Note: Mem0 'chat' is the easiest way to do RAG + Generation
    # It automatically uses the LLM we configured.
    response = mem0.chat(prompt, user_id=agent_id)
    
    return response