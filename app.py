
import streamlit as st
import google.generativeai as genai
import requests
import json
from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import base64

# Page config
st.set_page_config(
    page_title="AI Property Assistant",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: #000000;  /* ADD THIS LINE - makes text black */
    }
    .info-card {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
        color: #000000;  /* ADD THIS LINE TOO - makes text black */
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

# Functions
def get_weather_data(city):
    """Get weather data using free OpenWeatherMap API"""
    try:
        # Free API - No key needed for basic data
        api_key = st.session_state.get('weather_api_key', '')
        if not api_key:
            return {"error": "Weather API key not configured"}
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity'],
                "description": data['weather'][0]['description'],
                "city": city
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unable to fetch weather data"}

def get_pollution_data(city):
    """Get air quality data"""
    try:
        api_key = st.session_state.get('weather_api_key', '')
        if not api_key:
            return {"error": "API key not configured"}
        
        # First get coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url, timeout=5)
        
        if geo_response.status_code == 200 and len(geo_response.json()) > 0:
            lat = geo_response.json()[0]['lat']
            lon = geo_response.json()[0]['lon']
            
            # Get pollution data
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            pollution_response = requests.get(pollution_url, timeout=5)
            
            if pollution_response.status_code == 200:
                data = pollution_response.json()
                aqi = data['list'][0]['main']['aqi']
                components = data['list'][0]['components']
                
                aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
                
                return {
                    "aqi": aqi,
                    "aqi_label": aqi_labels.get(aqi, "Unknown"),
                    "pm2_5": components.get('pm2_5', 'N/A'),
                    "pm10": components.get('pm10', 'N/A'),
                    "city": city
                }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Unable to fetch pollution data"}

def get_nearby_places(location):
    """Simulate nearby places - In production, use Google Places API"""
    places = {
        "railway_stations": ["Central Station (2 km)", "Metro Station (1.5 km)"],
        "schools": ["ABC International School (800m)", "XYZ Public School (1.2 km)"],
        "hospitals": ["City Hospital (1 km)", "Care Medical Center (2.5 km)"],
        "restaurants": ["Food Plaza (500m)", "Cafe Corner (300m)"],
        "parks": ["Green Park (600m)", "Community Garden (1 km)"]
    }
    return places

def process_with_gemini(query, context=""):
    """Process query using Gemini AI"""
    try:
        api_key = st.session_state.get('gemini_api_key', '')
        if not api_key:
            return "Please configure your Gemini API key in the sidebar."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Enhanced prompt for property assistant
        system_prompt = f"""You are an AI Property Assistant. Help users with:
1. Property details and evaluation
2. Location analysis and nearby amenities
3. Real estate market insights
4. Property investment advice

Current context: {context}

User query: {query}

Provide detailed, helpful responses about properties, locations, and real estate.

THE GENERATED RESULTS SHOULD BE VERY CRISP AND CLEAN.
"""

        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Error processing query: {str(e)}"

def speech_to_text():
    """Convert speech to text using speech_recognition"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
        st.info("🔄 Processing your speech...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        return "No speech detected. Please try again."
    except sr.UnknownValueError:
        return "Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech(text):
    """Convert text to speech using gTTS"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def autoplay_audio(file_path):
    """Auto-play audio file"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
        os.unlink(file_path)
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")

# Main App
st.markdown("<h1 class='main-header'>🏠 AI Property Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Your voice-first property evaluation companion</p>", unsafe_allow_html=True)

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    gemini_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get('gemini_api_key', ''))
    if gemini_key:
        st.session_state.gemini_api_key = gemini_key
        st.session_state.api_key_set = True
    
    weather_key = st.text_input("OpenWeather API Key", type="password", value=st.session_state.get('weather_api_key', ''))
    if weather_key:
        st.session_state.weather_api_key = weather_key
    
    st.markdown("---")
    st.markdown("""
    ### 📝 How to get API Keys:
    
    **Gemini API:**
    1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Create API key (Free)
    
    **OpenWeather API:**
    1. Visit [OpenWeatherMap](https://openweathermap.org/api)
    2. Sign up for free tier
    """)
    
    st.markdown("---")
    if st.button("Clear History"):
        st.session_state.conversation_history = []
        st.rerun()

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 🎤 Voice Input")
    
    if st.button("🎙️ Start Voice Input", use_container_width=True, type="primary"):
        if not st.session_state.api_key_set:
            st.error("⚠️ Please configure your Gemini API key in the sidebar first!")
        else:
            with st.spinner("Listening..."):
                user_input = speech_to_text()
                
                if user_input and not user_input.startswith("Error") and not user_input.startswith("No speech") and not user_input.startswith("Could not"):
                    st.success(f"📝 You said: **{user_input}**")
                    
                    # Store in session
                    st.session_state.conversation_history.append({
                        "role": "user",
                        "content": user_input,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    
                    # Process query
                    with st.spinner("🤔 Thinking..."):
                        # Extract location from query for weather/pollution
                        location = "Mumbai"  # Default, should be extracted from query
                        
                        context = ""
                        if any(word in user_input.lower() for word in ['weather', 'temperature', 'climate']):
                            weather_data = get_weather_data(location)
                            if 'error' not in weather_data:
                                context += f"\nWeather in {location}: {weather_data['temperature']}°C, {weather_data['description']}, Humidity: {weather_data['humidity']}%"
                        
                        if any(word in user_input.lower() for word in ['pollution', 'air quality', 'aqi']):
                            pollution_data = get_pollution_data(location)
                            if 'error' not in pollution_data:
                                context += f"\nAir Quality: {pollution_data['aqi_label']} (AQI: {pollution_data['aqi']}), PM2.5: {pollution_data['pm2_5']}, PM10: {pollution_data['pm10']}"
                        
                        if any(word in user_input.lower() for word in ['nearby', 'places', 'amenities', 'facilities']):
                            places = get_nearby_places(location)
                            context += f"\nNearby places: {json.dumps(places, indent=2)}"
                        
                        # Get AI response
                        response = process_with_gemini(user_input, context)
                        
                        st.session_state.conversation_history.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                        
                        # Display response
                        st.markdown("<div class='response-box'>", unsafe_allow_html=True)
                        st.markdown(f"**🤖 Assistant:** {response}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Generate and play speech
                        with st.spinner("🔊 Generating voice response..."):
                            audio_file = text_to_speech(response)
                            if audio_file:
                                autoplay_audio(audio_file)
                                st.success("✅ Voice response played!")
                else:
                    st.error(user_input)

# Text input alternative
st.markdown("---")
st.markdown("### ⌨️ Or Type Your Query")

text_input = st.text_input("Ask about properties, locations, weather, or amenities:", key="text_query")

if st.button("Send", use_container_width=True):
    if text_input:
        if not st.session_state.api_key_set:
            st.error("⚠️ Please configure your Gemini API key in the sidebar first!")
        else:
            st.session_state.conversation_history.append({
                "role": "user",
                "content": text_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            with st.spinner("Processing..."):
                location = "Mumbai"
                context = ""
                
                if any(word in text_input.lower() for word in ['weather', 'temperature', 'climate']):
                    weather_data = get_weather_data(location)
                    if 'error' not in weather_data:
                        context += f"\nWeather: {weather_data['temperature']}°C, {weather_data['description']}"
                
                if any(word in text_input.lower() for word in ['pollution', 'air quality', 'aqi']):
                    pollution_data = get_pollution_data(location)
                    if 'error' not in pollution_data:
                        context += f"\nAir Quality: {pollution_data['aqi_label']}"
                
                response = process_with_gemini(text_input, context)
                
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                st.rerun()

# Display conversation history
if st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("### 💬 Conversation History")
    
    for msg in reversed(st.session_state.conversation_history[-6:]):
        if msg['role'] == 'user':
            st.markdown(f"<div class='info-card'>👤 **You** ({msg['timestamp']}): {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='response-box'>🤖 **Assistant** ({msg['timestamp']}): {msg['content']}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏠 AI Property Assistant | Built with Streamlit & Gemini AI</p>
    <p><small>Voice-first property evaluation system with real-time data</small></p>
</div>
""", unsafe_allow_html=True)