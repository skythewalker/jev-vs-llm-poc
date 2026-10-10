# src/test_jev.py

import asyncio
import httpx

from src.core.config import settings


async def main():
    payload = {
        "model": settings.jev_model,
        "state": "hello",
        "questions": {
            "intent": {
                "type": "choice",
                "instructions": "Classify the user intent",
                "criteria": {
                    "GREETING": "Greeting message",
                    "INCIDENT_QUERY": "Incident related query",
                    "UNKNOWN": "Other"
                }
            }
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.typesafe.ai/v1/systemone",
            headers={
                "Authorization": f"Bearer {settings.jev_api_key}",
                "Content-Type": "application/json"
            },
            json=payload
        )

        print("Status:", response.status_code)
        print(response.text)


asyncio.run(main())