import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Check your .env file.")
else:
    client = OpenAI(api_key=api_key)

def get_email_topic(email_body):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Identify the main topic of this email in 1-10 words. "},
            {"role": "user", "content": f"Email body: {email_body}"}
        ],
        max_tokens=10,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

st.title("Email Topic Classifier")
uploaded_file = st.file_uploader("Upload an Excel file", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "Email Body" not in df.columns:
        st.error("Excel file must contain an 'Email Body' column")
    else:
        df["Topic"] = df["Email Body"].apply(get_email_topic)
        st.write(df)  # Display results
        st.download_button("Download Results", df.to_csv(index=False), "email_topics.csv")




##Use these categories if applicable: pricing, cloud reporting, technical support, other.
