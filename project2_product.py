import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ----------------------------------------------------
# Streamlit Configuration (Must come first)
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Copywriting & Tone Transformer",
    page_icon="✍️",
    layout="wide"
)

# ----------------------------------------------------
# Load External CSS
# ----------------------------------------------------

def load_css(file_name):
    css_path = Path(__file__).parent / file_name

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css("styles.css")

# ----------------------------------------------------
# Load API Key
# ----------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file.")
    st.stop()

# ----------------------------------------------------
# Create Gemini Client
# ----------------------------------------------------

client = genai.Client(api_key=API_KEY)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.markdown(
    """
    <div class="main-title">
        ✍️ AI Copywriting & Tone Transformer
    </div>

    <div class="subtitle">
        Powered by <b>Google Gemini 2.5 Flash</b><br>
        Generate professional marketing copy tailored to different platforms.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.header("⚙️ Generation Settings")

    platform = st.selectbox(
        "📱 Platform",
        [
            "LinkedIn",
            "Instagram",
            "Email",
            "Facebook",
            "Twitter/X"
        ]
    )

    tone = st.selectbox(
        "🎯 Tone",
        [
            "Professional",
            "Friendly",
            "Persuasive",
            "Casual",
            "Luxury",
            "Humorous"
        ]
    )

    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.8,
        step=0.1
    )

    top_p = st.slider(
        "🎲 Top-P",
        min_value=0.1,
        max_value=1.0,
        value=0.95,
        step=0.05
    )

# ----------------------------------------------------
# Main Inputs
# ----------------------------------------------------

st.subheader("📦 Product Details")

product_name = st.text_input(
    "Product Name",
    placeholder="Enter your product name..."
)

product_description = st.text_area(
    "📝 Product Description",
    height=220,
    placeholder="Describe your product here..."
)

# ----------------------------------------------------
# Generate Button
# ----------------------------------------------------

if st.button("🚀 Generate Marketing Copy", use_container_width=True):

    if not product_name.strip() or not product_description.strip():

        st.warning("⚠️ Please enter both Product Name and Product Description.")

    else:

        prompt = f"""
You are an expert marketing copywriter.

Generate high-quality marketing content.

Product Name:
{product_name}

Product Description:
{product_description}

Platform:
{platform}

Tone:
{tone}

Requirements:

- Write specifically for {platform}.
- Use a {tone} tone.
- Make the content engaging.
- Include a strong Call-to-Action.
- Add relevant emojis only when appropriate.
- Do NOT explain your answer.
"""

        try:

            with st.spinner("✍️ Generating content..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        top_p=top_p
                    )
                )

            generated_text = (
                response.text
                if response.text
                else "No content generated."
            )

            st.success("✅ Marketing copy generated successfully!")

            st.subheader("📄 Generated Copy")

            st.write(generated_text)

            st.download_button(
                label="📥 Download Copy",
                data=generated_text,
                file_name="marketing_copy.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:

                st.error(
                    "🚫 Gemini API quota exceeded.\n\n"
                    "Please wait for your free quota to reset or use another API key."
                )

            else:

                st.error(f"❌ {error}")