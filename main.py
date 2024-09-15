# backend/app.py
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from openai_client import generate_initial_story, generate_next_chapter
import prompts
import json

app = Flask(__name__)
CORS(app)

story_sessions = {}  # Example: {'session_id_1': {'story_content': 'Chapter 1...', 'difficulty': 'just right'}}

# Define story titles
stories = {
    1: {"title": "Sofia and the Mysterious Key"},
}

@app.route('/api/stories', methods=['GET'])
def get_stories():
    # Provide a list of story titles and IDs
    story_list = [{"id": id, "title": story["title"]} for id, story in stories.items()]
    return jsonify(story_list)

@app.route('/api/stories/<int:story_id>', methods=['GET'])
def generate_story(story_id):
    # Get the title of the selected story
    story_title = stories.get(story_id)

    if story_title:

        session_id = str(uuid.uuid4())  # Generate a random unique session ID
        # Prepare user messages
        user_messages = [
            {"role": "user", "content": prompts.USER_INSTRUCTIONS},
            {"role": "user", "content": prompts.RULES},
            {"role": "user", "content": f"Title: {story_title}, Language: French, Level: Absolute beginner. Remember, the summary must be in English."},
        ]

        # Generate the story part using OpenAI
        story_content = generate_initial_story(prompts.SYSTEM_MESSAGE, user_messages)
        print(story_content)
        try:
            story_dict = json.loads(story_content)

            # Access the structured fields
            story_title = story_dict.get("story_title")
            story_summary = story_dict.get("story_summary")
            full_chapter = story_dict.get("full_chapter")
            chapter_number = story_dict.get("chapter_number")

            # Store the generated story content in the story_sessions dictionary
            story_sessions[session_id] = {
                "story_content": full_chapter,
                "story_summary": story_summary,
                "chapter_number": chapter_number,
                "difficulty": "just right"  # Initial difficulty can be set to "just right"
            }

            # Return the generated story and session ID as a JSON response
            return jsonify({"session_id": session_id, "title": story_title, "content": full_chapter})

        except (KeyError, json.JSONDecodeError) as e:
            print("Failed to parse response:", e)
            return jsonify({"error": "Story not found"}), 404


@app.route('/api/next_chapter', methods=['POST'])
def get_next_chapter():
    # Extract data from the request
    data = request.get_json()
    session_id = data.get('session_id')
    feedback = data.get('feedback')

    # Retrieve the current story session from the in-memory store
    story_session = story_sessions.get(session_id)

    if not story_session:
        return jsonify({"error": "Session not found"}), 404

    # Construct user messages for the OpenAI API call
    user_messages = [
        {"role": "user", "content": prompts.USER_INSTRUCTIONS},
        {"role": "user", "content": prompts.RULES},
        {"role": "user", "content": f"Title: {story_session['story_title']}, Language: French, Level: Absolute beginner. Remember, the summary must be in English."},
        {"role": "assistant", "content": json.dumps({
            "story_title": story_session["story_title"],
            "story_summary": story_session["story_summary"],
            "full_chapter": story_session["story_content"],
            "chapter_number": story_session["chapter_number"]
        })},
        {"role": "user",
         "content": f"The previous chapter was {feedback}. Please adjust the difficulty accordingly and write the next chapter."}

    ]

    # Generate the next chapter using OpenAI
    next_chapter_content = generate_next_chapter(prompts.SYSTEM_MESSAGE, user_messages)

    # Update the story session with the new chapter content
    story_sessions[session_id]['story_content'] += "\n" + next_chapter_content

    # Increment the chapter number
    story_sessions[session_id]['chapter_number'] = str(int(story_sessions[session_id]['chapter_number']) + 1)

    # Return the new chapter to the frontend
    return jsonify({"new_chapter": next_chapter_content})

if __name__ == '__main__':
    app.run(debug=True)
