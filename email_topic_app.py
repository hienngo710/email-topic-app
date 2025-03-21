import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# Use Streamlit secrets for deployment; fallback to .env for local testing
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except KeyError:
    # Fallback for local development
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Check your .env file or Streamlit secrets.")
    else:
        client = OpenAI(api_key=api_key)

def get_email_topic(email_body):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Identify the main topic of this email in 1-4 words. Use these categories if applicable: complaint, product, pricing, internal, other."},
            {"role": "user", "content": f"Email body: {email_body}"}
        ],
        max_tokens=10,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

st.title("Email Topic Classifier")

uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if "Email Body" not in df.columns:
            st.error("Excel file must contain an 'Email Body' column")
        else:
            df["Topic"] = df["Email Body"].apply(get_email_topic)
            st.write(df)
            st.download_button("Download Results", df.to_csv(index=False), "email_topics.csv")
    except Exception as e:
        st.error(f"An error occurred: {e}")


##Use these categories if applicable: pricing, cloud reporting, technical support, other.
