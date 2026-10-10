from core.config import settings

print("GPT Model:", settings.gpt_model)
print("JEV Model:", settings.jev_model)
print("OpenAI Key Exists:", bool(settings.openai_api_key))
print("JEV Key Exists:", bool(settings.jev_api_key))