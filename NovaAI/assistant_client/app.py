from flask import Flask
from routes.chat import chat_bp
from routes.voice import voice_bp
from routes.download import dl_bp as download_bp
from routes.commands import commands_bp
from routes.ui import ui_bp
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.register_blueprint(ui_bp)
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(voice_bp, url_prefix='/api')
app.register_blueprint(download_bp, url_prefix='/api')
app.register_blueprint(commands_bp, url_prefix='/api')

if __name__ == "__main__":
    # For development only. For production wrap with a proper WSGI server.
    app.run(port=int(os.getenv("PORT", 5000)), debug=True)
