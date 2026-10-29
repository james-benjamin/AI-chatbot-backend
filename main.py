import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    user_message: str

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_api(message: ChatInput):
    try:
        response = client.responses.create(
            model = "gpt-5.4-mini",
            input = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.user_message},
            ],
            temperature = 0.5,
        )

        # bot_response = response.output[0].content
        bot_response = response.output[0].content[0].text
        return {"bot_response": bot_response}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))