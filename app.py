import streamlit as st
import re # Needed for parsing ideas in workflow.py, but imported here for consistency if needed elsewhere

# Import functions from our new modules
from prompts import (
    format_research_ideas_prompt,
    format_literature_summary_prompt,
    format_properties_prediction_prompt,
    format_final_response_prompt
)
from gemini_api import query_model # Only query_model is directly used by workflow functions
from workflow import (
    generate_research_ideas_from_ai,
    generate_literature_summary_from_ai,
    generate_properties_from_ai,
    compile_final_response_from_ai
)
from pdf_utils import create_pdf_from_text # New import for PDF utility

# --- Streamlit UI and Session State Management ---

st.set_page_config(page_title="AI Research Agent", page_icon="🔬", layout="centered")

st.title("🔬 AI Research Agent for Chemists")
st.markdown("Unlock new research avenues with AI-powered idea generation and workflow management.")

# Initialize session state for flow control
if 'idea_index' not in st.session_state:
    st.session_state.idea_index = 0
if 'ideas' not in st.session_state:
    st.session_state.ideas = []
if 'approved_idea' not in st.session_state:
    st.session_state.approved_idea = None
if 'literature_summary' not in st.session_state:
    st.session_state.literature_summary = None
if 'properties' not in st.session_state:
    st.session_state.properties = None
if 'final_response' not in st.session_state:
    st.session_state.final_response = None
if 'stage' not in st.session_state:
    st.session_state.stage = 'input_details' # Initial stage for user input

# --- UI Flow based on st.session_state.stage ---

if st.session_state.stage == 'input_details':
    st.subheader("Step 1: Provide Research Details")
    topic = st.text_input(
        "🔍 Research Topic",
        placeholder="e.g., Sustainable catalysts for plastic degradation",
        key="input_topic"
    )
    goal = st.text_area(
        "🎯 Research Goal",
        placeholder="e.g., Develop a highly efficient and reusable catalyst that can break down PET plastics into their monomers at room temperature.",
        key="input_goal"
    )
    data = st.text_area(
        "🧪 Data We Already Have",
        placeholder="e.g., Initial screening results of metal-organic frameworks (MOFs) showing some catalytic activity, spectroscopic data of degraded plastic samples.",
        key="input_data"
    )

    if st.button("💡 Generate Research Ideas", help="Click to generate research ideas based on your input."):
        if not topic or not goal or not data:
            st.warning("Please fill in all fields to generate research ideas.")
        else:
            with st.spinner("Generating ideas... This might take a moment."):
                st.session_state.ideas = generate_research_ideas_from_ai(topic, goal, data)
                st.session_state.idea_index = 0
                if st.session_state.ideas:
                    st.session_state.stage = 'review_ideas'
                st.rerun()

elif st.session_state.stage == 'review_ideas':
    st.subheader(f"Step 2: Review Research Idea #{st.session_state.idea_index + 1}")

    if st.session_state.ideas and st.session_state.idea_index < len(st.session_state.ideas):
        idea = st.session_state.ideas[st.session_state.idea_index]
        st.markdown(f"**Idea:** {idea}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Approve Idea"):
                st.session_state.approved_idea = idea
                st.session_state.stage = 'literature_summary'
                st.rerun()
        with col2:
            if st.button("👎 Disapprove & Next Idea"):
                st.session_state.idea_index += 1
                if st.session_state.idea_index >= len(st.session_state.ideas):
                    st.warning("No more ideas to review. Please go back to generate new ideas.")
                    st.session_state.stage = 'input_details'
                st.rerun()
    else:
        st.warning("No ideas available. Please generate new ideas.")
        st.session_state.stage = 'input_details'

elif st.session_state.stage == 'literature_summary':
    st.subheader("Step 3: Generate Literature Summary")
    st.markdown(f"**Approved Idea:** {st.session_state.approved_idea}")

    if st.session_state.literature_summary is None:
        with st.spinner("Generating literature summary..."):
            st.session_state.literature_summary = generate_literature_summary_from_ai(st.session_state.approved_idea)

    st.markdown("---")
    st.markdown("**Generated Literature Summary:**")
    st.markdown(st.session_state.literature_summary)
    st.markdown("---")

    col1, col2, col3 = st.columns(3) # Added a column for download button
    with col1:
        if st.button("👍 Approve Summary"):
            st.session_state.stage = 'properties_prediction'
            st.rerun()
    with col2:
        if st.button("👎 Disapprove & Re-evaluate Idea"):
            st.session_state.literature_summary = None
            st.session_state.stage = 'review_ideas'
            st.session_state.idea_index += 1
            if st.session_state.idea_index >= len(st.session_state.ideas):
                st.warning("No more ideas to review. Please go back to generate new ideas.")
                st.session_state.stage = 'input_details'
            st.rerun()
    with col3:
        if st.session_state.literature_summary and "⚠️ Error:" not in st.session_state.literature_summary:
            pdf_bytes = create_pdf_from_text("Literature Summary", st.session_state.literature_summary)
            st.download_button(
                label="Download Summary as PDF",
                data=pdf_bytes,
                file_name="literature_summary.pdf",
                mime="application/pdf"
            )


elif st.session_state.stage == 'properties_prediction':
    st.subheader("Step 4: Predict Properties / Experimental Approach")
    st.markdown(f"**Approved Idea:** {st.session_state.approved_idea}")

    if st.session_state.properties is None:
        with st.spinner("Generating property predictions..."):
            st.session_state.properties = generate_properties_from_ai(st.session_state.approved_idea)

    st.markdown("---")
    st.markdown("**Generated Properties/Approach:**")
    st.markdown(st.session_state.properties)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Approve Properties"):
            st.session_state.stage = 'final_compilation'
            st.rerun()
    with col2:
        if st.button("👎 Disapprove & Re-evaluate Summary"):
            st.session_state.properties = None
            st.session_state.literature_summary = None
            st.session_state.stage = 'literature_summary'
            st.rerun()

elif st.session_state.stage == 'final_compilation':
    st.subheader("Step 5: Final Research Proposal Overview")
    st.markdown(f"**Approved Idea:** {st.session_state.approved_idea}")
    st.markdown(f"**Literature Summary:** {st.session_state.literature_summary}")
    st.markdown(f"**Properties/Approach:** {st.session_state.properties}")

    if st.session_state.final_response is None:
        with st.spinner("Compiling final response..."):
            st.session_state.final_response = compile_final_response_from_ai(
                st.session_state.approved_idea,
                st.session_state.literature_summary,
                st.session_state.properties
            )

    st.markdown("---")
    st.markdown("**Final Research Proposal Overview:**")
    st.markdown(st.session_state.final_response)
    st.markdown("---")

    st.success("Research proposal overview generated! You can copy this content for your documents.")
    col1, col2 = st.columns(2) # Added a column for download button
    with col1:
        if st.button("Start New Research"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col2:
        if st.session_state.final_response and "⚠️ Error:" not in st.session_state.final_response:
            # Combine all relevant info for the final PDF
            full_content = (
                f"Research Idea: {st.session_state.approved_idea}\n\n"
                f"Literature Summary:\n{st.session_state.literature_summary}\n\n"
                f"Properties/Approach:\n{st.session_state.properties}\n\n"
                f"Final Proposal Overview:\n{st.session_state.final_response}"
            )
            pdf_bytes = create_pdf_from_text("Final Research Proposal", full_content)
            st.download_button(
                label="Download Proposal as PDF",
                data=pdf_bytes,
                file_name="research_proposal.pdf",
                mime="application/pdf"
            )

st.markdown("---")
st.markdown("Developed with Streamlit and Google Gemini API.")
