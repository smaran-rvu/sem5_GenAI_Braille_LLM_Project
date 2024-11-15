import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import tempfile
from pathlib import Path
import base64
from Grade1BrailleConverter import Grade1BrailleConverter
from Grade2BrailleConverter import Grade2BrailleConverter

os.environ["GROQ_API_KEY"] = "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"
# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def autoplay_audio(file_path: str):
    """Automatically play audio using HTML audio tag with autoplay"""
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)

def generate_text(prompt, temperature, max_tokens):
    """Generate text using Groq's LLaMA-3 8B model"""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech(text):
    """Convert text to speech using gTTS"""
    try:
        tts = gTTS(text=text, lang='en')
        # Create a temporary file to store the audio
        temp_dir = tempfile.gettempdir()
        audio_path = Path(temp_dir) / "output.mp3"
        tts.save(str(audio_path))
        return str(audio_path)
    except Exception as e:
        return f"Error in text-to-speech conversion: {str(e)}"

def convert_to_braille(text, grade_level):
    """Convert text to braille based on selected grade level"""
    if grade_level == "Grade 1":
        return Grade1BrailleConverter().to_braille(text)
    else:  # Grade 2
        return Grade2BrailleConverter().to_braille(text)

# Custom CSS for output boxes
st.markdown("""
    <style>
    .output-box {
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .output-label {
        color: #4CAF50;
        font-size: 1.1em;
        margin-bottom: 5px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("LLaMA-3 Based Braille LLM")

# Sidebar with input controls
with st.sidebar:
    st.header("Input Controls")
    
    # Text input
    input_text = st.text_area("Enter your text:", height=150)
    
    # Grade selector
    grade_level = st.radio("Select UEB Grade Level:", ["Grade 1", "Grade 2"])
    
    # Temperature and max tokens sliders
    temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.slider("Max Tokens:", min_value=50, max_value=1000, value=200, step=50)
    
    # Generate button
    generate_button = st.button("Generate")

# Initialize session states
if 'generated_text' not in st.session_state:
    st.session_state.generated_text = ""
if 'braille_text' not in st.session_state:
    st.session_state.braille_text = ""

# Generate text when button is clicked
if generate_button and input_text:
    model_output = generate_text(input_text + ". Generate the response in a concise manner.", temperature, max_tokens)
    st.session_state.generated_text = model_output
    st.session_state.braille_text = convert_to_braille(model_output, grade_level)

# Output section
st.header("Generated Output")
output_container = st.container()

with output_container:
    # Display original output in custom box
    st.markdown('<div class="output-label">Original Output:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{st.session_state.generated_text}</div>', unsafe_allow_html=True)
    
    # Display Braille output in custom box
    st.markdown('<div class="output-label">Braille Output:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{st.session_state.braille_text}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Regenerate button
    with col1:
        if st.button("Regenerate"):
            if input_text:
                model_output = generate_text(input_text, temperature, max_tokens)
                st.session_state.generated_text = model_output
                st.session_state.braille_text = convert_to_braille(model_output, grade_level)
                st.experimental_rerun()
    
    # Read aloud button with autoplay
    with col2:
        if st.button("Read Aloud"):
            if st.session_state.generated_text:
                audio_path = text_to_speech(st.session_state.generated_text)
                if not audio_path.startswith("Error"):
                    autoplay_audio(audio_path)
                else:
                    st.error(audio_path)

# Display error if no input text
if generate_button and not input_text:
    st.error("Please enter some text to generate.")