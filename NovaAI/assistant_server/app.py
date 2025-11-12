from flask import Flask
from routes.ai_chat import ai_bp
from routes.search import search_bp
from routes.health import health_bp

app = Flask(__name__)
app.register_blueprint(ai_bp, url_prefix='/chat')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(health_bp, url_prefix='')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
