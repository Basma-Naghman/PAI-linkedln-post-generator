# 🤖 LinkedIn Post Generator using LLM & Few-Shot Learning

A smart LinkedIn Post Generator powered by few-shot learning and large language models (LLMs). This Streamlit-based app lets users generate professional posts tailored to their preferences for topic, length, and language.

---

## 🧠 Overview

This tool uses:
- ✨ **Few-shot learning**: to guide the LLM with relevant examples
- 💬 **LLMs via Groq API**: for generating quality LinkedIn content
- 🖥️ **Streamlit**: for an easy-to-use web interface

---

## 📁 File Structure

### `few_shot.py`
Handles selection of few-shot examples from a JSON post database.

- Categorizes posts by length: Short, Medium, Long
- Filters posts by tag and language
- Provides relevant samples for LLM prompting

### `llm_helper.py`
Manages the LLM setup.

- Loads environment variables
- Initializes the Groq chat model: `meta-llama/llama-4-scout-17b-16e-instruct`

### `main.py`
Streamlit-based web interface.

- Dropdowns for:
  - Post topic (tag)
  - Length (Short / Medium / Long)
  - Language (English)
- Generate button to display AI-generated post

### `post_generator.py`
Handles post generation logic.

- Constructs the prompt using selected samples
- Sends prompt to LLM and returns the generated post

### `preprocess.py`
Prepares raw posts for few-shot training.

- Extracts metadata (line count, language, tags)
- Unifies similar tags
- Saves structured data to `processed_posts.json`

---

## 🔄 Workflow

1. **Data Preparation**
   - Use `preprocess.py` to clean and tag raw post data.
   - Save as `processed_posts.json`.

2. **User Interaction (via Streamlit)**
   - Select tag, length, and language
   - Click "Generate"

3. **Post Generation**
   - Relevant examples fetched from JSON
   - Prompt created using few-shot examples
   - Post generated using Groq's LLM
   - Displayed to user

---

## 🧪 Dependencies

Make sure you have Python 3.x installed.

Install the required packages:

```bash
pip install pandas json streamlit langchain_groq langchain_core python-dotenv
