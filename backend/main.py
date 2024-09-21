# backend/main.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from story_manager import start_story, fetch_next_chapter
from dotenv import load_dotenv
import os

# Load environment variables from .env file only if not already set
if not os.getenv('MODE'):
    load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/stories', methods=['GET'])
def get_stories():
    stories = {
        1: {"title": "Lila and the Moonlight Garden"},
        2: {"title": "Oliver and the Pocket-Sized Dragon"},
        3: {"title": "The Cloud Collector"},
        4: {"title": "Benny and the Enchanted Paintbrush"},
        5: {"title": "The Whispering Woods"}
    }
    story_list = [{"id": id, "title": story["title"]} for id, story in stories.items()]
    return jsonify(story_list)

@app.route('/api/start_story/<int:story_id>', methods=['POST'])
def generate_story(story_id):
    data = request.get_json()
    result = start_story(data, story_id)
    return jsonify(result)

@app.route('/api/next_chapter', methods=['POST'])
def get_next_chapter():
    data = request.get_json()
    result = fetch_next_chapter(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=os.getenv('MODE') == 'staging')