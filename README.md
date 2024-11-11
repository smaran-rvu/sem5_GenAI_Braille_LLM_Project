---
base_model: unsloth/meta-llama-3.1-8b-bnb-4bit
library_name: peft
---

# LLM for Visually Impaired Users: Braille Text Summarization

This project aims to develop a Large Language Model (LLM) tailored for visually impaired users, translating outputs into Braille. It features a Streamlit app for real-time interaction and includes further development for a standalone app. The model is fine-tuned to generate summaries or other textual outputs in Braille, enhancing accessibility.

## Project Structure

- **adapter_model.safetensors**: Fine-tuned LLM model for generating Braille-ready text.
- **streamlit_app.py**: Main app file for the current interactive Streamlit deployment.
- **app.py**: A work-in-progress version for future app expansion.
- **requirements.txt**: Lists dependencies required to run the project.
- **Grade1BrailleConverter.py**: Python script to convert text into Grade 1 Braille.
- **Grade2BrailleConverter.py**: Python script to convert text into Grade 2 Braille.
- **Generative AI for Braille Text Summarization.pdf**: Project report detailing objectives, methodology, and results.
- **Llama_3_1_8b_+_Unsloth_GenAI_Project_finetuning.ipynb**: Jupyter notebook detailing the fine-tuning process for the LLM model.
- **Configuration and Tokenizer Files**:
  - `adapter_config.json`
  - `special_tokens_map.json`
  - `tokenizer_config.json`
  - `tokenizer.json`

## Getting Started

### Prerequisites

Ensure that Python and the required dependencies are installed:
```bash
pip install -r requirements.txt
```

### Running the Streamlit App

To run the interactive app locally, execute:
```bash
streamlit run streamlit_app.py
```

## Future Scope

The `app.py` file is under development to provide extended features for this application. Stay tuned for more!
