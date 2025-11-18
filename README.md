"""

# 🏠 AI Property Assistant

A voice-first multimodal property assistant built with Streamlit and Gemini AI.

## Features

✅ Voice input (Speech-to-Text)
✅ Voice output (Text-to-Speech)
✅ Property evaluation with AI
✅ Weather data integration
✅ Air quality index (AQI) monitoring
✅ Nearby places information
✅ Real-time API integration

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Free API Keys

**Gemini API (Free):**

- Visit: https://makersuite.google.com/app/apikey
- Sign in with Google account
- Click "Create API Key"
- Copy your key

**OpenWeather API (Free):**

- Visit: https://openweathermap.org/api
- Sign up for free account
- Go to API keys section
- Copy your API key
- Free tier: 1000 calls/day

### 3. Configure API Keys

Enter your API keys directly in the Streamlit sidebar, or:

- Copy `.env.example` to `.env`
- Add your API keys to `.env`

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Grant Microphone Access

- Browser will ask for microphone permission
- Click "Allow" to use voice input

## Usage

### Voice Input:

1. Click "Start Voice Input" button
2. Speak your query clearly
3. Wait for AI response (text + voice)

### Text Input:

1. Type your query in the text box
2. Click "Send"

### Example Queries:

- "Tell me about property prices in Mumbai"
- "What's the weather like today?"
- "Show me air quality index"
- "What are nearby amenities for this location?"
- "Is this a good time to invest in real estate?"

## Troubleshooting

**Microphone not working:**

- Check browser permissions
- Try Chrome/Edge browsers
- Ensure microphone is connected

**API Errors:**

- Verify API keys are correct
- Check API quotas (free tier limits)
- Ensure internet connection

**PyAudio installation issues (Windows):**

```bash
pip install pipwin
pipwin install pyaudio
```

**PyAudio installation (Mac):**

```bash
brew install portaudio
pip install pyaudio
```

**PyAudio installation (Linux):**

```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Project Structure

```
property-assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment variables
└── README.md          # This file
```

## Technologies Used

- **Streamlit** - Web framework
- **Google Gemini AI** - Language model
- **SpeechRecognition** - Speech-to-text
- **gTTS** - Text-to-speech
- **OpenWeatherMap API** - Weather & pollution data

## Features Breakdown

### Voice Processing

- Real-time speech recognition
- Natural voice responses
- Multiple language support

### Property Intelligence

- AI-powered property evaluation
- Market insights
- Investment recommendations

### Location Data

- Live weather information
- Air quality monitoring
- Nearby amenities finder

## Free API Limits

- **Gemini**: 60 requests/minute
- **OpenWeather**: 1000 calls/day

## Future Enhancements

- Property database integration
- Google Maps integration
- Property comparison feature
- Save favorite properties
- Email report generation

## License

MIT License - Free to use and modify

## Support

For issues, create a GitHub issue or contact support.
"""
