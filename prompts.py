# prompts.py

def format_research_ideas_prompt(topic, goal, data):
    """
    Formats the user's input into a prompt for generating research ideas.
    Asks for a numbered list of ideas.
    """
    prompt_text = f"""
    You are an AI research assistant specializing in chemistry.
    Your task is to generate innovative research ideas based on the provided information.

    Research Topic: {topic}
    Research Goal: {goal}
    Existing Data: {data}

    Please provide 3-7 distinct, detailed, and actionable research ideas.
    Format your response as a numbered list.
    Example:
    1. Idea one description.
    2. Idea two description.
    3. Idea three description.
    """
    return prompt_text

def format_literature_summary_prompt(research_idea):
    """
    Formats a prompt for generating a literature summary for a given research idea.
    """
    prompt_text = f"""
    Based on the following research idea, provide a concise literature summary.
    Focus on key existing research, relevant methodologies, and potential gaps this idea addresses.
    Research Idea: {research_idea}

    Please provide a summary of approximately 200-300 words.
    """
    return prompt_text

def format_properties_prediction_prompt(research_idea):
    """
    Formats a prompt for predicting properties or suggesting experimental details for a research idea.
    """
    prompt_text = f"""
    For the following research idea, suggest potential chemical properties (e.g., CAS numbers of key compounds, predicted reactivity, stability)
    or outline a conceptual approach for performance prediction. If applicable, suggest new ligands or materials.

    Research Idea: {research_idea}

    Provide your response in a structured format, perhaps using bullet points or clear headings for different aspects.
    """
    return prompt_text

def format_final_response_prompt(idea, literature_summary, properties):
    """
    Formats a prompt to compile a final research proposal summary.
    """
    prompt_text = f"""
    Based on the following approved research idea, literature summary, and predicted properties,
    compile a concise final research proposal overview.

    Research Idea: {idea}
    Literature Summary: {literature_summary}
    Predicted Properties/Approach: {properties}

    The final response should be a comprehensive overview suitable for a preliminary proposal,
    covering the need, solution, differentiation, and benefit (NSDB).
    Also, suggest what kind of experimental details and analysis data in graphs would be relevant.
    """
    return prompt_text
