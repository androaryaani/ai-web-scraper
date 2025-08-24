import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
# Note: python-dotenv removed for Streamlit Cloud compatibility
# Environment variables will be handled through Streamlit secrets

st.set_page_config(page_title="Ariyaani-Here", layout="wide")

# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Configuration Section
    st.subheader("🔑 API Configuration")
    
    # Get current API key from Streamlit secrets, environment, or session state
    current_api_key = ""
    try:
        # Try to get from Streamlit secrets first (for Streamlit Cloud)
        current_api_key = st.secrets.get("GOOGLE_API_KEY", "")
    except:
        # Fallback to environment variable
        current_api_key = os.getenv("GOOGLE_API_KEY", "")
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = current_api_key
    
    # API Key input
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Google Gemini AI API key"
    )
    
    # Update API key button
    if st.button("💾 Save API Key"):
        if api_key_input.strip():
            # Save to session state (for Streamlit Cloud compatibility)
            st.session_state.api_key = api_key_input.strip()
            os.environ["GOOGLE_API_KEY"] = api_key_input.strip()
            st.success("✅ API Key saved for this session!")
            st.info("💡 For permanent storage on Streamlit Cloud, add your API key to Streamlit secrets.")
            st.rerun()
        else:
            st.error("❌ Please enter a valid API key")
    
    # App Configuration Section
    st.subheader("🛠️ App Configuration")
    
    # Request timeout setting
    timeout = st.slider(
        "Request Timeout (seconds)",
        min_value=5,
        max_value=30,
        value=int(os.getenv("REQUEST_TIMEOUT", "10")),
        help="Maximum time to wait for website response"
    )
    
    # Max content length setting
    max_content = st.slider(
        "Max Content Length",
        min_value=5000,
        max_value=50000,
        value=int(os.getenv("MAX_CONTENT_LENGTH", "15000")),
        step=1000,
        help="Maximum characters to send to AI"
    )
    
    # Language and Formatting Section
    st.subheader("🌐 Language & Format Settings")
    
    # Language preference
    language_options = {
        "Auto-detect from question": "auto",
        "English": "english",
        "Hindi": "hindi",
        "Hinglish (Hindi + English)": "hinglish",
        "Urdu": "urdu",
        "Bengali": "bengali",
        "Tamil": "tamil",
        "Telugu": "telugu",
        "Gujarati": "gujarati",
        "Marathi": "marathi",
        "Punjabi": "punjabi"
    }
    
    selected_language = st.selectbox(
        "Response Language",
        options=list(language_options.keys()),
        index=0,
        help="Choose the language for AI responses"
    )
    
    # Response format options
    response_format = st.selectbox(
        "Response Format",
        options=[
            "Professional & Detailed",
            "Simple & Easy to Understand",
            "Bullet Points & Summary",
            "Academic Style",
            "Conversational Style"
        ],
        index=0,
        help="Choose how you want the AI to format its responses"
    )
    
    # Response length preference
    response_length = st.selectbox(
        "Response Length",
        options=["Short & Concise", "Medium Detail", "Comprehensive & Detailed"],
        index=1,
        help="Choose the preferred length of AI responses"
    )
    
    # Save app settings
    if st.button("💾 Save App Settings"):
        # Save to session state (for Streamlit Cloud compatibility)
        st.session_state.request_timeout = timeout
        st.session_state.max_content_length = max_content
        st.session_state.preferred_language = language_options[selected_language]
        st.session_state.response_format = response_format
        st.session_state.response_length = response_length
        st.success("✅ App settings saved for this session!")
    
    # API Status
    st.subheader("📊 Status")
    if st.session_state.api_key and st.session_state.api_key.strip():
        st.success("🟢 API Key Configured")
    else:
        st.error("🔴 API Key Not Set")

# Configure Gemini AI with API key
if st.session_state.api_key and st.session_state.api_key.strip():
    try:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"❌ Error configuring Gemini AI: {str(e)}")
        model = None
else:
    model = None

# Main App Content
st.title("🌐 Web-Scraping using Gemini AI")
st.markdown("---")

# Check if API key is configured
if not st.session_state.api_key or not st.session_state.api_key.strip():
    st.warning("⚠️ Please configure your Google Gemini API Key in the sidebar settings to use this application.")
    st.info("💡 You can get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)")
    st.stop()

url = st.text_input("🌐 Website URL", placeholder="https://example.com")
question = st.text_area("❓ Your Question", placeholder="What is this website about?", height=100)

# Action buttons
col1, col2 = st.columns([1, 4])
with col1:
    ask_button = st.button("🚀 Ask Me Dude", type="primary")
with col2:
    if st.button("🔄 Clear"):
        st.rerun()

if ask_button:
    if not url or not question:
        st.warning("⚠️ Please fill in both the URL and your question.")
    elif not model:
        st.error("❌ Gemini AI model not configured. Please check your API key.")
    else:
        try:
            # Get current settings from session state or defaults
            current_timeout = getattr(st.session_state, 'request_timeout', timeout)
            current_max_content = getattr(st.session_state, 'max_content_length', max_content)
            
            with st.spinner("🔍 Scraping website content..."):
                response = requests.get(url, timeout=current_timeout)
                soup = BeautifulSoup(response.content, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                
                if len(text) == 0:
                    st.error("❌ No content found on the page.")
                    st.stop()
                
                # Show content stats
                st.info(f"📊 Content found: {len(text)} characters")

            # Limit content based on settings
            content_to_send = text[:current_max_content]
            if len(text) > current_max_content:
                st.warning(f"⚠️ Content truncated to {current_max_content} characters (from {len(text)} total)")

            with st.spinner("🤖 Sending to Gemini AI..."):
                # Get language and formatting preferences from session state or defaults
                preferred_language = getattr(st.session_state, 'preferred_language', "auto")
                format_style = getattr(st.session_state, 'response_format', "Professional & Detailed")
                length_preference = getattr(st.session_state, 'response_length', "Medium Detail")
                
                # Language detection and instruction
                if preferred_language == "auto":
                    language_instruction = f"""CRITICAL LANGUAGE MATCHING RULE:
Analyze the user's question language pattern and respond in the EXACT SAME style:

USER QUESTION: "{question}"

LANGUAGE DETECTION RULES:
- If question contains BOTH Hindi and English words mixed together (like "mujhe website ke baare mein batao") → respond in HINGLISH (Hindi+English mix)
- If question is ONLY in Hindi script/words → respond in pure Hindi
- If question is ONLY in English → respond in pure English
- If question uses Roman script but Hindi words → respond in Hinglish

MATCH THE USER'S EXACT LANGUAGE MIXING PATTERN. Do not convert Hinglish to pure Hindi."""
                elif preferred_language == "hindi":
                    language_instruction = "Respond ONLY in Hindi (केवल हिंदी में जवाब दें)."
                elif preferred_language == "hinglish":
                    language_instruction = "Respond ONLY in Hinglish (Hindi + English words mixed together using Roman script)."
                elif preferred_language == "english":
                    language_instruction = "Respond ONLY in English."
                else:
                    language_instruction = f"Respond ONLY in {preferred_language}."
                
                # Format instruction based on selection
                format_instructions = {
                    "Professional & Detailed": "Use a professional tone with detailed explanations, proper headings, and well-structured paragraphs.",
                    "Simple & Easy to Understand": "Use simple language that anyone can understand. Avoid technical jargon and explain concepts clearly.",
                    "Bullet Points & Summary": "Format your response using bullet points, numbered lists, and clear summaries for easy reading.",
                    "Academic Style": "Use an academic writing style with proper citations, formal language, and scholarly approach.",
                    "Conversational Style": "Write in a friendly, conversational tone as if talking to a friend."
                }
                
                # Length instruction
                length_instructions = {
                    "Short & Concise": "Keep your response brief and to the point (2-3 paragraphs maximum).",
                    "Medium Detail": "Provide a moderately detailed response (4-6 paragraphs).",
                    "Comprehensive & Detailed": "Give a comprehensive and thorough response with all relevant details."
                }
                
                prompt = f"""You are an intelligent multilingual web content analyzer.

🚨 CRITICAL LANGUAGE MATCHING RULE: {language_instruction}

ANALYZE THIS QUESTION: "{question}"
→ Detect the language pattern (Hindi/English/Hinglish mix)
→ Your response MUST use the SAME language pattern

FORMAT STYLE: {format_instructions.get(format_style, format_instructions["Professional & Detailed"])}
LENGTH PREFERENCE: {length_instructions.get(length_preference, length_instructions["Medium Detail"])}

WEBSITE CONTENT:
{content_to_send}

STRICT RULES:
1. Match the user's exact language mixing style
2. Answer based ONLY on website content
3. DO NOT repeat or quote the user's question
4. Give direct answer in same language pattern
5. If Hinglish question → Hinglish answer (not pure Hindi)
6. Keep response focused and helpful
7. NO question repetition in your response

Provide direct answer now:"""
                
                result = model.generate_content(prompt)

            # Display results with clean, visible formatting
            st.success("✅ Response Generated!")
            
            # Main response display with better visibility
            st.markdown("## 🤖 AI Response")
            
            # Create a clean black and white design
            st.markdown("""
            <style>
            /* Main response container with black border and white background */
            .main-response {
                background-color: #ffffff;
                padding: 30px;
                border: 3px solid #000000;
                border-radius: 10px;
                margin: 20px 0;
                font-size: 18px;
                line-height: 1.8;
                color: #000000;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            
            /* All headings in black */
            .main-response h1, .main-response h2, .main-response h3, .main-response h4 {
                color: #000000;
                font-weight: bold;
                margin-top: 25px;
                margin-bottom: 15px;
                border-bottom: 2px solid #000000;
                padding-bottom: 5px;
            }
            
            /* Paragraphs with proper spacing */
            .main-response p {
                margin-bottom: 18px;
                color: #000000;
                text-align: justify;
            }
            
            /* Lists with black styling */
            .main-response ul, .main-response ol {
                margin-left: 25px;
                margin-bottom: 18px;
                color: #000000;
            }
            
            .main-response li {
                margin-bottom: 10px;
                color: #000000;
            }
            
            /* Strong/bold text in black */
            .main-response strong, .main-response b {
                color: #000000;
                font-weight: bold;
            }
            
            /* Links in black with underline */
            .main-response a {
                color: #000000;
                text-decoration: underline;
            }
            
            /* Code blocks with black border */
            .main-response code {
                background-color: #f5f5f5;
                color: #000000;
                padding: 2px 6px;
                border: 1px solid #000000;
                border-radius: 3px;
            }
            
            /* Blockquotes with black border */
            .main-response blockquote {
                border-left: 4px solid #000000;
                margin: 20px 0;
                padding-left: 20px;
                color: #000000;
                background-color: #f9f9f9;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display the response with enhanced visibility
            st.markdown(f'<div class="main-response">{result.text}</div>', unsafe_allow_html=True)
            
            # Copy button with black and white styling
            st.markdown("""
            <style>
            /* Black divider line */
            .black-divider {
                border: none;
                height: 3px;
                background-color: #000000;
                margin: 30px 0;
            }
            
            /* Copy section styling */
            .copy-section {
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            
            /* Footer styling */
            .footer-section {
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                text-align: center;
            }
            
            .footer-section p {
                color: #000000;
                margin: 0;
                font-weight: bold;
            }
            
            .footer-section a {
                color: #000000;
                text-decoration: underline;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Black divider
            st.markdown('<hr class="black-divider">', unsafe_allow_html=True)
            
            # Copy button
            if st.button("📋 Copy Response", type="primary"):
                st.markdown('<div class="copy-section">', unsafe_allow_html=True)
                st.code(result.text, language=None)
                st.success("✅ Response ready to copy! Select the text above and copy it.")
                st.markdown('</div>', unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.error(f"⏰ Request timed out after {current_timeout} seconds. Try increasing the timeout in settings.")
        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Network error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer with black and white theme
st.markdown('<hr class="black-divider">', unsafe_allow_html=True)
st.markdown(
    """
    <div class='footer-section'>
        <p>🚀 Built with Streamlit & Google Gemini AI |
        <a href='https://makersuite.google.com/app/apikey' target='_blank'>Get API Key</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
