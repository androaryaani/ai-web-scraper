# AI-Powered Web Scraper with Streamlit

A powerful web scraping application that uses Google Gemini AI to analyze and answer questions about website content.

## Features

- 🌐 Web scraping with BeautifulSoup
- 🤖 AI-powered content analysis using Google Gemini
- 🌍 Multi-language support (Hindi, English, Hinglish, and more)
- ⚙️ Customizable settings for timeout, content length, and response format
- 🎨 Clean black and white UI design
- 📱 Responsive Streamlit interface

## Deployment on Streamlit Cloud

### 1. Requirements
- Python 3.9 (specified in runtime.txt)
- Google Gemini API Key

### 2. Setup Instructions

1. **Fork/Clone this repository**
2. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
3. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set the main file path: `web-scrape.py`
   - The app will use the following configuration files:
     - `requirements.txt` - Python dependencies
     - `runtime.txt` - Python version (3.9)
     - `.streamlit/config.toml` - Streamlit configuration
     - `packages.txt` - System packages (empty for this app)
4. **Configure Secrets (Recommended)**
   - In Streamlit Cloud dashboard, go to "Manage app" → "Secrets"
   - Add your API key:
     ```toml
     GOOGLE_API_KEY = "your_api_key_here"
     ```

### 3. Troubleshooting Deployment Issues

If you encounter "Error installing requirements":

1. **Check Python Version**: Ensure runtime.txt specifies `python-3.9`
2. **Verify Requirements**: Make sure requirements.txt contains only:
   ```
   streamlit
   requests
   beautifulsoup4
   google-generativeai
   ```
3. **Clear Cache**: In Streamlit Cloud, go to "Manage app" → "Reboot app"
4. **Check Logs**: Click "Manage app" and check the terminal logs for specific errors
5. **Repository Structure**: Ensure all files are in the root directory of your repository

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run the app
streamlit run web-scrape.py
```

## Usage

1. **Configure API Key**: Enter your Google Gemini API key in the sidebar
2. **Enter Website URL**: Provide the URL you want to analyze
3. **Ask Your Question**: Type your question about the website content
4. **Get AI Response**: The app will scrape the content and provide an AI-generated answer

## Settings

- **Request Timeout**: Maximum time to wait for website response
- **Max Content Length**: Limit content sent to AI (to manage API costs)
- **Language Preference**: Choose response language (auto-detect, Hindi, English, etc.)
- **Response Format**: Professional, Simple, Bullet Points, Academic, or Conversational
- **Response Length**: Short, Medium, or Comprehensive

## Supported Languages

- English
- Hindi
- Hinglish (Hindi + English mix)
- Urdu, Bengali, Tamil, Telugu, Gujarati, Marathi, Punjabi

## Dependencies

- `streamlit>=1.28.0`
- `requests>=2.31.0`
- `beautifulsoup4>=4.12.0`
- `google-generativeai>=0.3.0`
- `python-dotenv>=1.0.0`

## License

MIT License - Feel free to use and modify as needed.