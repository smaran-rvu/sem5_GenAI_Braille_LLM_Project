import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from gtts import gTTS
import os
import time

# Page configuration
st.set_page_config(layout="wide")

def get_device():
    """Determine the appropriate device for model loading"""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch, 'mps') and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

@st.cache_resource
def load_model():
    """Load the LLaMA model and tokenizer"""
    try:
        device = get_device()
        st.info(f"Using device: {device}")
        
        tokenizer = AutoTokenizer.from_pretrained("unsloth/Meta-Llama-3.1-8B")
        model = AutoModelForCausalLM.from_pretrained(
            "unsloth/Meta-Llama-3.1-8B",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            low_cpu_mem_usage=True
        )
        
        if device != "cuda":
            model = model.to(device)
            
        return model, tokenizer, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

def generate_text(prompt, temperature, grade):
    """Generate text using the LLaMA model"""
    model, tokenizer, device = load_model()
    if model is None or tokenizer is None:
        return "Error: Model not loaded properly"
    
    try:
        # Modify prompt based on grade
        grade_prompt = f"Generate a {grade} level response for: {prompt}"
        
        inputs = tokenizer(grade_prompt, return_tensors="pt")
        if device != "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error during generation: {str(e)}"

def text_to_speech(text):
    """Convert text to speech and save as audio file"""
    tts = gTTS(text=text, lang='en')
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

# App title
st.title("LLaMA 3.1 Text Generation App")

# System info
if st.checkbox("Show System Info"):
    st.info(f"""
    PyTorch version: {torch.__version__}
    CUDA available: {torch.cuda.is_available()}
    Current device: {get_device()}
    """)

# Create two columns for layout
left_col, right_col = st.columns(2)

# Left column elements
with left_col:
    st.subheader("Input Parameters")
    
    # Text input
    input_text = st.text_area("Enter your text:", height=150)
    
    # Grade selector
    grade = st.radio("Select Grade:", ["Grade 1", "Grade 2"])
    
    # Temperature slider
    temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
    
    # Generate button
    if st.button("Generate"):
        if input_text:
            with st.spinner("Generating..."):
                # Store the generated text in session state
                st.session_state.generated_text = generate_text(input_text, temperature, grade)
        else:
            st.error("Please enter some text first!")

# Right column elements
with right_col:
    st.subheader("Generated Output")
    
    # Output text area
    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ""
    
    st.text_area("Output:", value=st.session_state.generated_text, height=150)
    
    # Buttons row
    button_col1, button_col2 = st.columns(2)
    
    with button_col1:
        if st.button("Regenerate"):
            if input_text:
                with st.spinner("Regenerating..."):
                    st.session_state.generated_text = generate_text(input_text, temperature, grade)
            else:
                st.error("Please enter some text first!")
    
    with button_col2:
        if st.button("Read Aloud"):
            if st.session_state.generated_text:
                with st.spinner("Converting to speech..."):
                    audio_file = text_to_speech(st.session_state.generated_text)
                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    # Clean up the audio file
                    os.remove(audio_file)
            else:
                st.error("No text to read! Please generate some text first.")

# Add CSS to improve layout
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin: 5px 0;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)