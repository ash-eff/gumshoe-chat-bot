from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chat import add_user_message, add_assistant_message, chat, calculate_token_usage

app = FastAPI(title="Gumshoe Chat Bot")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")

messages = []
total_tokens = 0

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def post_message(request: ChatRequest):
    global total_tokens

    add_user_message(messages, request.message)
    answer, in_tokens, out_tokens = chat(messages, print_output=False)
    total_tokens = calculate_token_usage(in_tokens, out_tokens, total_tokens, show_usage=False)
    add_assistant_message(messages, answer)

    return {"response": answer, "in_tokens": in_tokens, "out_tokens": out_tokens, "total_tokens": total_tokens}
