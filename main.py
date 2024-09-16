from flask import Flask, jsonify, request
from flask_cors import CORS
from services import start_story, fetch_next_chapter

app = Flask(__name__)
CORS(app)

# Define story titles
stories = {
    1: {"title": "Lila and the Moonlight Garden"},
    2: {"title": "Oliver and the Pocket-Sized Dragon"},
    3: {"title": "The Cloud Collector"},
    4: {"title": "Benny and the Enchanted Paintbrush"},
    5: {"title": "The Whispering Woods"}
}

@app.route('/api/stories', methods=['GET'])
def get_stories():
    story_list = [{"id": id, "title": story["title"]} for id, story in stories.items()]
    return jsonify(story_list)

@app.route('/api/start_story/<int:story_id>', methods=['GET'])
def start_story_route(story_id):
    result = start_story(story_id)
    return jsonify(result)

@app.route('/api/next_chapter', methods=['POST'])
def get_next_chapter_route():
    data = request.get_json()
    result = fetch_next_chapter(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
