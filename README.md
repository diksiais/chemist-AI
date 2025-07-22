# AI Research Agent for Chemists

🔬 **AI Research Agent** is a Streamlit-based web app that helps chemists generate, refine, and compile research proposals using Google’s Gemini AI language model. It guides users through a multi-step workflow from idea generation to final proposal creation, with PDF export support.

---

## Features

- **Interactive Workflow:**  
  Step-by-step interface for submitting research details, reviewing AI-generated ideas, summarizing literature, predicting properties, and compiling final proposals.

- **AI-Powered Content Generation:**  
  Uses Google Gemini API to generate research ideas, literature summaries, predicted chemical properties, and comprehensive proposal overviews.

- **PDF Export:**  
  Download summaries and final proposals as PDF documents.

- **Session State Management:**  
  Retains user progress, allowing smooth navigation and iterative refinement.

---

## Project Structure

| File               | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| `app.py`           | Main Streamlit application handling UI and session state.       |
| `gemini_api.py`    | Wrapper for calling Google Gemini API with error handling.      |
| `pdf_utils.py`     | Utility for generating PDFs from text using FPDF.               |
| `prompts.py`       | Functions formatting prompts sent to the AI model.              |
| `workflow.py`      | Functions orchestrating AI calls, response parsing, and errors. |

---

## Requirements

- Python 3.7 or higher  
- Streamlit  
- Requests  
- FPDF  

Install dependencies with:

```bash
pip install streamlit requests fpdf
