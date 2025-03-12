import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
from openai import OpenAI

## api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key='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')

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