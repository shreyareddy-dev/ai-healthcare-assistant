from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import os

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
load_dotenv()

# ==========================================
# CONFIGURE GEMINI API
# ==========================================
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# LOAD GEMINI MODEL
# ==========================================
model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

# ==========================================
# MONGODB CONNECTION
# ==========================================
client = MongoClient(os.getenv("MONGO_URL"))

db = client["ai_healthcare_assistant"]

chat_collection = db["chat_history"]

# ==========================================
# CREATE FASTAPI APP
# ==========================================
app = FastAPI(
    title="AI Healthcare Assistant API",
    description="AI-powered Healthcare Assistant using FastAPI + Gemini AI",
    version="1.0.0"
)

# ==========================================
# ENABLE CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# REQUEST MODEL
# ==========================================
class ChatRequest(BaseModel):
    message: str

# ==========================================
# HOME ROUTE
# ==========================================
@app.get("/")
def home():

    return {
        "message": "AI Healthcare Assistant Backend Running Successfully"
    }

# ==========================================
# HEALTH CHECK ROUTE
# ==========================================
@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

# ==========================================
# AI CHAT ENDPOINT
# ==========================================
@app.post("/chat")
async def chat(request: ChatRequest):

    user_message = request.message.lower()

    # ==========================================
    # EMERGENCY DETECTION
    # ==========================================
    emergency_keywords = [
        "chest pain",
        "difficulty breathing",
        "heart attack",
        "stroke",
        "severe bleeding",
        "unconscious",
        "fainting",
        "seizure",
        "blood vomiting",
        "suicidal",
        "cannot breathe",
        "severe chest pain",
        "heavy bleeding",
        "loss of consciousness"
    ]

    emergency_detected = any(
        keyword in user_message
        for keyword in emergency_keywords
    )

    # ==========================================
    # GEMINI PROMPT
    # ==========================================
    healthcare_prompt = f"""
    You are an AI Healthcare Assistant.

    Rules:
    - Provide safe healthcare guidance
    - Never prescribe medicines
    - Suggest doctor consultation if needed
    - Keep responses short and professional
    - Mention emergency care if symptoms are severe

    User Symptoms:
    {request.message}
    """

    try:

        # ==========================================
        # GENERATE AI RESPONSE
        # ==========================================
        response = model.generate_content(
            healthcare_prompt
        )

        ai_response = response.text

    except Exception:

        # ==========================================
        # EMERGENCY
        # ==========================================
        if emergency_detected:

            ai_response = (
                "Possible medical emergency detected. "
                "Please seek immediate medical attention immediately."
            )

        # ==========================================
        # FEVER / FLU / VIRAL
        # ==========================================
        elif any(word in user_message for word in [
            "fever",
            "cold",
            "flu",
            "viral",
            "temperature",
            "chills",
            "infection",
            "high temperature"
        ]):

            ai_response = (
                "Your symptoms may indicate viral infection or flu. "
                "Stay hydrated, rest properly, and monitor your temperature carefully."
            )

        # ==========================================
        # HEAD / BRAIN / STRESS
        # ==========================================
        elif any(word in user_message for word in [
            "headache",
            "migraine",
            "head pain",
            "brain",
            "pressure",
            "stress",
            "confusion",
            "mental pressure",
            "dizziness",
            "dizzy",
            "heavy head"
        ]):

            ai_response = (
                "Head or brain-related symptoms may occur due to stress, migraine, "
                "dehydration, or lack of sleep. Rest properly and stay hydrated."
            )

        # ==========================================
        # STOMACH / DIGESTION
        # ==========================================
        elif any(word in user_message for word in [
            "stomach",
            "abdominal",
            "abdomen",
            "gastric",
            "acidity",
            "digestion",
            "stomach ache",
            "hurting",
            "gas",
            "indigestion"
        ]):

            ai_response = (
                "Your symptoms may indicate indigestion, acidity, or stomach infection. "
                "Avoid oily and spicy food and drink enough water."
            )

        # ==========================================
        # COUGH / THROAT
        # ==========================================
        elif any(word in user_message for word in [
            "cough",
            "throat",
            "sore throat",
            "throat pain",
            "dry cough",
            "throat infection"
        ]):

            ai_response = (
                "Your symptoms may indicate throat irritation or infection. "
                "Drink warm fluids and avoid cold beverages."
            )

        # ==========================================
        # BREATHING / LUNGS
        # ==========================================
        elif any(word in user_message for word in [
            "lungs",
            "breathing",
            "breath",
            "breathlessness",
            "heavy lungs",
            "heavy chest",
            "shortness of breath",
            "respiratory"
        ]):

            ai_response = (
                "Breathing-related symptoms may indicate respiratory infection, "
                "allergy, or lung irritation. Monitor symptoms carefully."
            )

        # ==========================================
        # BODY PAIN / FATIGUE
        # ==========================================
        elif any(word in user_message for word in [
            "fatigue",
            "weakness",
            "body pain",
            "body ache",
            "tired",
            "exhausted",
            "low energy"
        ]):

            ai_response = (
                "Fatigue and body pain may occur due to stress, viral infection, "
                "or insufficient rest. Ensure proper sleep and hydration."
            )

        # ==========================================
        # VOMITING / NAUSEA
        # ==========================================
        elif any(word in user_message for word in [
            "vomiting",
            "vomit",
            "nausea",
            "throwing up"
        ]):

            ai_response = (
                "Vomiting or nausea may occur due to food poisoning, acidity, "
                "or infection. Stay hydrated and avoid heavy meals."
            )

        # ==========================================
        # HEART RELATED
        # ==========================================
        elif any(word in user_message for word in [
            "heart",
            "palpitations",
            "heart racing",
            "heartbeat"
        ]):

            ai_response = (
                "Heart-related symptoms should be monitored carefully. "
                "Avoid stress and consult a healthcare professional if symptoms continue."
            )

        # ==========================================
        # SKIN RELATED
        # ==========================================
        elif any(word in user_message for word in [
            "rash",
            "skin",
            "itching",
            "allergy",
            "red spots"
        ]):

            ai_response = (
                "Skin irritation or allergy symptoms detected. "
                "Avoid allergens and consult a doctor if symptoms worsen."
            )

        # ==========================================
        # SLEEP RELATED
        # ==========================================
        elif any(word in user_message for word in [
            "sleep",
            "insomnia",
            "unable to sleep",
            "sleeping problem"
        ]):

            ai_response = (
                "Sleep-related issues may occur due to stress or irregular routines. "
                "Maintain proper sleep hygiene and reduce screen time before bed."
            )

        # ==========================================
        # DEFAULT RESPONSE
        # ==========================================
        else:

            ai_response = (
                "Symptoms detected. "
                "Please consult a healthcare professional "
                "for proper medical guidance."
            )

    # ==========================================
    # SAVE CHAT TO DATABASE
    # ==========================================
    chat_data = {
        "user_input": request.message,
        "response": ai_response,
        "emergency": emergency_detected,
        "timestamp": datetime.utcnow()
    }

    chat_collection.insert_one(chat_data)

    # ==========================================
    # FINAL RESPONSE
    # ==========================================
    return {
        "success": True,
        "emergency": emergency_detected,
        "user_input": request.message,
        "response": ai_response
    }

# ==========================================
# GET CHAT HISTORY
# ==========================================
@app.get("/chat-history")
def get_chat_history():

    chats = []

    for chat in chat_collection.find({}, {"_id": 0}):

        chats.append(chat)

    return {
        "success": True,
        "chat_history": chats
    }