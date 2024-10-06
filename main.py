# backend/main.py

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.story_manager import generate_next_chapter
from backend.story_manager import generate_story_outline
from dotenv import load_dotenv
import os
from utils.db_utils import init_db

# Load environment variables from .env file only if not already set
if not os.getenv('MODE'):
    load_dotenv()

app = Flask(__name__)
CORS(app)

stories = {
    1: {"title": "Jack and the Beanstalk"},
    2: {"title": "Cinderella"},
    3: {"title": "Little Red Riding Hood"},
    4: {"title": "Hansel and Gretel"},
    5: {"title": "The Three Little Pigs"}
}

# Initialize the database
init_db()

@app.route('/api/stories', methods=['GET'])
def get_stories():
    story_list = [{"id": id, "title": story["title"]} for id, story in stories.items()]
    return jsonify(story_list)

@app.route('/api/story/<int:story_id>', methods=['GET'])
def get_story_by_id(story_id):
    story = stories.get(story_id)
    return jsonify(story)

@app.route('/api/start_story/<int:story_id>', methods=['POST'])
def generate_story(story_id):
    data = request.get_json()
    result = generate_story_outline(data, story_id, stories.get(story_id)["title"])
    return jsonify(result)

@app.route('/api/next_chapter', methods=['POST'])
def get_next_chapter():
    data = request.get_json()
    result = generate_next_chapter(data, False)
    return jsonify(result)

def test_database():
    from models.story_session import StorySession
    session = StorySession("test_session", 1, "Test Story")
    session.save_to_db()
    loaded_session = StorySession.load_from_db("test_session")
    print(loaded_session.to_json())

if __name__ == '__main__':
   app.run(debug=os.getenv('MODE') == 'staging')

