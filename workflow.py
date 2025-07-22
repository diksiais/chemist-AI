# workflow.py
import re
import streamlit as st # Used for st.warning/st.error, could be refactored for pure logic

# Import functions from other modules
from gemini_api import query_model
from prompts import (
    format_research_ideas_prompt,
    format_literature_summary_prompt,
    format_properties_prediction_prompt,
    format_final_response_prompt
)

def generate_research_ideas_from_ai(topic, goal, data):
    """
    Calls the AI model to generate research ideas and parses them into a list.
    """
    prompt = format_research_ideas_prompt(topic, goal, data)
    raw_ideas_text = query_model(prompt)

    if "⚠️ Error:" in raw_ideas_text:
        st.error(raw_ideas_text) # Display error in Streamlit UI
        return []

    # Parse the numbered list into individual ideas
    ideas_list = re.findall(r'^\d+\.\s*(.*)', raw_ideas_text, re.MULTILINE)
    if not ideas_list:
        st.warning("Could not parse ideas into a list. Displaying raw AI output.")
        return [raw_ideas_text]
    return ideas_list

def generate_literature_summary_from_ai(idea):
    """
    Calls the AI model to generate a literature summary.
    """
    prompt = format_literature_summary_prompt(idea)
    summary = query_model(prompt)
    if "⚠️ Error:" in summary:
        st.error(summary)
        return "Error generating summary."
    return summary

def generate_properties_from_ai(idea):
    """
    Calls the AI model to generate properties/predictions.
    """
    prompt = format_properties_prediction_prompt(idea)
    props = query_model(prompt)
    if "⚠️ Error:" in props:
        st.error(props)
        return "Error generating properties."
    return props

def compile_final_response_from_ai(idea, literature_summary, properties):
    """
    Calls the AI model to compile the final response.
    """
    prompt = format_final_response_prompt(idea, literature_summary, properties)
    final_response_text = query_model(prompt)
    if "⚠️ Error:" in final_response_text:
        st.error(final_response_text)
        return "Error compiling final response."
    return final_response_text
