import httpx
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel
from config import settings
from models import WhatsAppMessage

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self, phone_number_id: str):
        self.base_url = "https://graph.facebook.com/v17.0"
        self.phone_number_id = phone_number_id
        self.token = settings.WHATSAPP_TOKEN
        
    async def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """Send WhatsApp message using Graph API"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        message_data = WhatsAppMessage(
            messaging_product="whatsapp",
            recipient_type="individual",
            to=phone_number,
            type="text",
            text={"body": message}
        )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=message_data.dict(),
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error sending message: {str(e)}")
            raise ValueError(f"Failed to send WhatsApp message: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error sending message: {str(e)}")
            raise ValueError(f"Network error sending WhatsApp message: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending message: {str(e)}")
            raise ValueError(f"Error sending WhatsApp message: {str(e)}")