🤖 AI Medical Assistant



A comprehensive medical chatbot built with Streamlit and powered by Google's Gemini AI. This application provides reliable medical information, symptom analysis, and health guidance through an intuitive chat interface.

✨ Features
*AI-Powered Responses: Utilizes Google's Gemini 2.0 Flash model for accurate medical information
*Comprehensive Medical Data: Provides detailed information about conditions, symptoms, treatments, and prevention
Wikipedia Integration: Fallback to Wikipedia for additional medical information
*Interactive Chat Interface: Modern, responsive chat UI with message history
*Highlighted Medical Terms: Important medical terms are highlighted for better readability
*Structured Responses: Organized format covering symptoms, causes, diagnosis, treatment, and prevention
*Error Handling: Robust error handling with Wikipedia backup


Prerequisites

Python 3.8 or higher
Google Gemini API key

Installation

Clone the repository
bashgit clone https://github.com/yourusername/medical-chatbot.git
cd medical-chatbot

Install dependencies
bashpip install -r requirements.txt

Set up environment variables
Create a .streamlit/secrets.toml file:
tomlGEMINI_API_KEY = "your_google_gemini_api_key_here"

Run the application
bashstreamlit run Medical_ChatBot.py


📦 Dependencies
Create a requirements.txt file with the following dependencies:
streamlit>=1.28.0
langchain-google-genai>=1.0.0
langchain-core>=0.1.0
langchain-community>=0.0.1
beautifulsoup4>=4.12.0
requests>=2.31.0
🔧 Configuration
Getting a Gemini API Key

Visit the Google AI Studio
Create a new API key
Add it to your .streamlit/secrets.toml file

Customization
You can customize the chatbot by modifying:

System Prompt: Edit the SYS_PROMPT variable to change the AI's behavior
Highlighted Terms: Modify the highlight_terms list to highlight different medical terms
UI Styling: Update the CSS in the st.markdown section for custom styling
Model Settings: Adjust temperature and model parameters in the ChatGoogleGenerativeAI configuration

💡 Usage

Start the Application: Run streamlit run Medical_ChatBot.py
Ask Medical Questions: Type any medical condition or symptom in the chat input
Get Comprehensive Information: Receive structured information about:

Condition overview
Common symptoms
Causes and risk factors
Diagnosis methods
Treatment options
Prevention tips
When to see a doctor
