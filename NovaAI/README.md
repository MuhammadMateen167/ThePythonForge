# Nova AI Assistant

Nova AI Assistant is a desktop assistant created as a fun project.  
It can chat, open applications, report system usage, and download files.  
The project consists of a **server** (backend APIs) and a **client** (frontend + Flask server) that communicate with each other.

## Features

- Chat with Nova, a witty AI assistant.
- Open applications on your system.
- Display CPU, RAM, and disk usage.
- Download files from the internet.
- Logs all conversations to `chat_log.jsonl` for future reference.

## Project Structure

nova-ai-assistant/
├─ server/
│ └─ app.py # Backend APIs handling
├─ client/
│ └─ app.py # Frontend Flask server
├─ chat_log.jsonl # Logs user-assistant conversations
└─ README.md

## Requirements

- Python 3.8+
- OpenRouter API key (set as environment variable `OPEN_ROUTER_API`)

```bash
Setup & Usage
Set your OpenRouter API key:

bash
Copy code
export OPEN_ROUTER_API="your_api_key_here"   # Linux / macOS
setx OPEN_ROUTER_API "your_api_key_here"     # Windows
Run the server-side application:

bash
Copy code
cd server
python app.py
Run the client-side application:

bash
Copy code
cd client
python app.py
Use the frontend to chat with Nova or trigger system actions.
All chats are logged automatically in chat_log.jsonl.

Logging
All user and assistant messages are stored in chat_log.jsonl in JSON Lines format:

json
Copy code
{"timestamp": "2025-11-12T12:34:56.789Z", "user": "Hello Nova", "assistant": "Hello! How can I help today?"}
This allows easy parsing or future session replay if desired.

License
This project is open source under the MIT License.
---