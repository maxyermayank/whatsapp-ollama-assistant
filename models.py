from pydantic import BaseModel
from typing import List, Optional

class WhatsAppMessage(BaseModel):
    messaging_product: str
    recipient_type: str
    to: str
    type: str
    text: dict

class WebhookMessage(BaseModel):
    object: str
    entry: List[dict]