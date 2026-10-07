from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JEV_API_KEY = os.getenv("JEV_API_KEY")

INTENTS = [
    "GREETING",
    "RCA",
    "INCIDENT",
    "K8S",
    "SUMMARY",
]