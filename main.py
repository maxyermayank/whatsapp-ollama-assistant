from fastapi import FastAPI, Request, HTTPException, Depends
from config import settings
from whatsapp_client import WhatsAppClient
from ollama_client import OllamaClient
from models import WebhookMessage

app = FastAPI()
whatsapp_client = WhatsAppClient(settings.PHONE_NUMBER_ID)
ollama_client = OllamaClient()

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    print(f"Received webhook verification request: mode={mode}, token={token}, challenge={challenge}")
    if mode and token:
        if mode == "subscribe" and token == settings.VERIFY_TOKEN:
            return int(challenge)
        raise HTTPException(status_code=403, detail="Invalid verify token")
    raise HTTPException(status_code=400, detail="Invalid request")

@app.post("/webhook")
async def webhook_handler(message: WebhookMessage):
    try:
        # Extract the message from the webhook payload
        entry = message.entry[0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" in value:
            message_body = value["messages"][0]["text"]["body"]
            sender_id = value["messages"][0]["from"]
            
            print(f"Received message: {message_body} from {sender_id}")
            
            # Generate response using Ollama
            response = await ollama_client.generate_response(message_body)
            
            # Send response back through WhatsApp
            await whatsapp_client.send_message(sender_id, response)
            
        return {"status": "success"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)