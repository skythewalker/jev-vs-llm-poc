from config import OPENAI_API_KEY
from config import JEV_API_KEY

print(
    {
        "openai_found": bool(OPENAI_API_KEY),
        "jev_found": bool(JEV_API_KEY),
    }
)