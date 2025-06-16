

import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Wikipedia Scraper
def get_medical_info_from_wiki(condition):
    try:
        url = f"https://en.wikipedia.org/wiki/{condition.replace(' ', '_')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        for para in paragraphs:
            text = para.get_text().strip()
            if text and not text.lower().startswith("may refer to:"):
                return text[:1000] + "..."
        return "❌ No relevant Wikipedia information found."
    except Exception as e:
        return f"⚠️ Error fetching info: {e}"


st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: #f0f2f6;
        }
        .header-title {
            font-size: 48px;
            text-align: center;
            font-weight: bold;
            background: linear-gradient(90deg, #1976d2, #ef5350);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 30px;
        }
        .header-subtitle {
            font-size: 20px;
            text-align: center;
            color: #555;
            margin-bottom: 40px;
        }
        .footer {
            text-align: center;
            padding: 15px;
            margin-top: 30px;
            background-color: #ef5350;
            color: white;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
        }
        .user-message, .ai-message {
            padding: 14px 20px;
            border-radius: 12px;
            margin: 10px 0;
            max-width: 90%;
            font-size: 16px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        .user-message {
            background: #c8e6c9;
            color: #1b5e20;
            align-self: flex-end;
        }
        .ai-message {
            background: #ffffff;
            color: #333;
            border-left: 4px solid #1976d2;
            align-self: flex-start;
        }
        .highlighted-term {
            background-color: #ff9800;
            color: white;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 600;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #90a4ae;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="header-title">🤖 AI Medical Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Built by Ayaz Khan | Powered by Gemini AI</div>', unsafe_allow_html=True)



gemini = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-001',
    temperature=0.1,
    convert_system_message_to_human=True
)

SYS_PROMPT = """
You are a medical assistant designed to provide clear, accurate, and up-to-date information about various medical conditions.

When given a medical condition, respond with the following format:

Condition Name: {{Condition Name}}
Overview: {{Brief summary of the condition}}

Common Symptoms:
{{List of common symptoms}}

Causes:
{{List of common causes or risk factors}}

Diagnosis:
{{How it is usually diagnosed}}

Treatment Options:
{{Medications, therapies, or procedures}}

Prevention Tips:
{{How to prevent it, if possible}}

When to See a Doctor:
{{Red flags or emergency signs}}

Sources:
{{Trusted source references like Mayo Clinic, WebMD, WHO}}

If the user asks about specific aspects of the condition like "Diagnosis," "Symptoms," or "Treatment," provide relevant information for those subcategories.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYS_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

llm_chain = prompt | gemini
streamlit_msg_history = StreamlitChatMessageHistory()

conversation_chain = RunnableWithMessageHistory(
    llm_chain,
    lambda session_id: streamlit_msg_history,
    input_messages_key="input",
    history_messages_key="history",
)


for msg in streamlit_msg_history.messages:
    with st.chat_message(msg.type):
        if msg.type == "human":
            st.markdown(f'<div class="user-message">{msg.content}</div>', unsafe_allow_html=True)
        else:
            response = msg.content
            terms = ["Diabetes", "Insulin", "Symptoms", "Treatment", "Diagnosis", "Hypertension", "Cancer", "Asthma"]
            for term in terms:
                response = response.replace(term, f'<span class="highlighted-term">{term}</span>')
            st.markdown(f'<div class="ai-message">{response}</div>', unsafe_allow_html=True)


user_prompt = st.chat_input("Type your medical condition here...")

if user_prompt:
    st.chat_message("human").markdown(user_prompt)
    with st.chat_message("ai"):
        try:
            config = {"configurable": {"session_id": "any"}}
            response = conversation_chain.invoke({"input": user_prompt}, config)

            if hasattr(response, "content") and response.content.strip():
                response_content = response.content
            else:
                response_content = None

            highlight_terms = ["Diabetes", "Insulin", "Symptoms", "Treatment", "Diagnosis", "Cancer", "Asthma"]
            if response_content:
                for term in highlight_terms:
                    response_content = response_content.replace(term, f'<span class="highlighted-term">{term}</span>')
                st.markdown(f'<div class="ai-message">{response_content}</div>', unsafe_allow_html=True)
            else:
                st.warning("🤖 Gemini gave no response, fetching Wikipedia info...")
                wiki_data = get_medical_info_from_wiki(user_prompt)
                st.markdown(f'<div class="ai-message">{wiki_data}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error("⚠️ Gemini failed. Fetching Wikipedia info...")
            wiki_data = get_medical_info_from_wiki(user_prompt)
            st.markdown(f'<div class="ai-message">{wiki_data}</div>', unsafe_allow_html=True)



st.markdown('<div class="footer">Developed by Ayaz Khan | Medical Assistant Chatbot | Powered by AI</div>', unsafe_allow_html=True)

