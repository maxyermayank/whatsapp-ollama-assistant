# WhatsApp Ollama Assistant


# Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Create .env file with your credentials
Update the credentials in the .env file

**Note:** This is only for development purposes. Do not expose your credentials in production.


# Install Ollama from: https://ollama.ai/
# Pull the model
```
ollama pull phi4
```

# Start Ollama server
```
ollama serve
```

# Install ngrok from: https://ngrok.com/download
# Start ngrok on port 8000
```
ngrok http 8000
```

# Start the FastAPI server
```
uvicorn main:app --reload --no-server-header
```
