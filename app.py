import os

import streamlit as st
from google import genai


st.set_page_config(page_title="AI Content Generator", page_icon="✨", layout="centered")


def get_setting(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except FileNotFoundError:
        return os.getenv(name, default)


def build_prompt(content_type: str, topic: str, tone: str, audience: str) -> str:
    return f"""
You are an experienced content strategist.

Create a {content_type} about: {topic}
Audience: {audience}
Tone: {tone}

Requirements:
- Give useful, accurate, original content.
- Use simple language and a clear structure.
- Do not invent statistics, quotations, or sources.
- Return only the requested content, ready for the user to edit and publish.
""".strip()


def generate_content(prompt: str, api_key: str, model: str) -> str:
    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model=model,
        input=prompt
    )

    return interaction.output_text


st.title("✨ AI Content Generator")
st.caption("A small Generative AI application built with Streamlit and Gemini")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Gemini API key",
        value=get_setting("GEMINI_API_KEY"),
        type="password",
        help="For deployment, store this in Streamlit Secrets instead of the source code.",
    )
    model = st.text_input("Model", value=get_setting("GEMINI_MODEL", "gemini-3.8-flash"))
    st.divider()
    st.caption("Never commit API keys to GitHub.")

content_type = st.selectbox(
    "What would you like to create?",
    ["LinkedIn post", "YouTube title and description", "Blog outline", "Instagram caption"],
)
topic = st.text_area("Topic", placeholder="Example: How AI can improve learning for college students")
tone = st.selectbox("Tone", ["Professional", "Educational", "Friendly", "Creative"])
audience = st.text_input("Target audience", placeholder="Example: College students and early-career professionals")

if st.button("Generate content", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Enter your Gemini API key in the sidebar to continue.")
    elif not topic.strip():
        st.warning("Enter a topic to generate content.")
    elif not audience.strip():
        st.warning("Enter the target audience to improve the result.")
    else:
        prompt = build_prompt(content_type, topic, tone, audience)
        with st.spinner("Generating content..."):
            try:
                result = generate_content(prompt, api_key, model)
                st.subheader("Generated result")
                st.markdown(result)
                with st.expander("View prompt sent to the model"):
                    st.code(prompt, language="text")
            except Exception as error:
                st.error("The request could not be completed. Check the API key, model name, and internet connection.")
                st.caption(f"Technical details: {error}")

st.divider()
st.caption("Review AI-generated output before publishing or using it in decisions.")
