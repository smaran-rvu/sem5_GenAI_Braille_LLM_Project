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
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

@st.cache_resource
def load_model():
    """Load the LLaMA model and tokenizer optimized for Apple Silicon"""
    try:
        device = get_device()
        st.info(f"Using device: {device}")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "unsloth/Meta-Llama-3.1-8B",
            use_fast=True
        )
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            "unsloth/Meta-Llama-3.1-8B",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            low_cpu_mem_usage=True
        )
        
        # Move model to appropriate device
        model = model.to(device)
        
        return model, tokenizer, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

@st.cache_data
def generate_text(prompt, temperature, grade, max_tokens=100):
    """Generate text using the LLaMA model with caching"""
    model, tokenizer, device = load_model()
    if model is None or tokenizer is None:
        return "Error: Model not loaded properly"
    
    try:
        # Modify prompt based on grade
        grade_prompt = f"Generate a {grade} level response for: {prompt}"
        
        # Tokenize with truncation
        inputs = tokenizer(
            grade_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(device)
        
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2,
                num_beams=1
            )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error during generation: {str(e)}"

@st.cache_data
def text_to_speech(text):
    """Convert text to speech with caching"""
    tts = gTTS(text=text, lang='en')
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file

# Initialize session state
if 'generated_text' not in st.session_state:
    st.session_state.generated_text = ""
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False

# App title
st.title("LLaMA 3.1 Text Generation App")

# Model loading status
with st.expander("System Information"):
    st.info(f"""
    PyTorch version: {torch.__version__}
    Device: {get_device()}
    Model loaded: {st.session_state.model_loaded}
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
    
    # Advanced settings expander
    with st.expander("Advanced Settings"):
        temperature = st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1)
        max_tokens = st.slider("Max Output Tokens:", min_value=10, max_value=200, value=100, step=10)
    
    # Generate button
    if st.button("Generate", use_container_width=True):
        if input_text:
            with st.spinner("Generating..."):
                start_time = time.time()
                st.session_state.generated_text = generate_text(
                    input_text, 
                    temperature, 
                    grade, 
                    max_tokens
                )
                end_time = time.time()
                st.session_state.generation_time = end_time - start_time
        else:
            st.error("Please enter some text first!")

# Right column elements
with right_col:
    st.subheader("Generated Output")
    
    # Output area with generation time
    st.text_area("Output:", value=st.session_state.generated_text, height=150)
    if 'generation_time' in st.session_state and st.session_state.generated_text:
        st.caption(f"Generation time: {st.session_state.generation_time:.2f} seconds")
    
    # Buttons row
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Regenerate", use_container_width=True):
            if input_text:
                with st.spinner("Regenerating..."):
                    start_time = time.time()
                    st.session_state.generated_text = generate_text(
                        input_text, 
                        temperature, 
                        grade,
                        max_tokens
                    )
                    end_time = time.time()
                    st.session_state.generation_time = end_time - start_time
            else:
                st.error("Please enter some text first!")
    
    with col2:
        if st.button("Read Aloud", use_container_width=True):
            if st.session_state.generated_text:
                with st.spinner("Converting to speech..."):
                    audio_file = text_to_speech(st.session_state.generated_text)
                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    os.remove(audio_file)
            else:
                st.error("No text to read! Please generate some text first.")

# Add CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        margin: 5px 0;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)