from flask import Flask, jsonify
from flask_cors import CORS
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)
client = OpenAI()

stories = {
    1: {"title": "The Brave Little Tailor", "content": "Once upon a time..."},
    2: {"title": "The Ugly Duckling", "content": "A duckling was born..."},
    3: {"title": "The Emperor's New Clothes", "content": "There once was an emperor..."}
}

@app.route('/api/stories', methods=['GET'])
def get_stories():
    # Provide a list of story titles and IDs
    story_list = [{"id": id, "title": story["title"]} for id, story in stories.items()]
    return jsonify(story_list)

@app.route('/api/stories/<int:story_id>', methods=['GET'])
def get_story(story_id):
    # Predefined story titles
    story_titles = {
        1: "The Brave Little Tailor",
        2: "The Ugly Duckling",
        3: "The Emperor's New Clothes"
    }

    # Get the title of the selected story
    story_title = story_titles.get(story_id)

    if story_title:
        # Call the OpenAI API to generate a story using the new ChatCompletion method
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content":
                    "You are a children story writer specialising in stories to help children learn languages through "
                    "comprehensible input."
                                              },
                {
                    "role": "user",
                    "content": "Write a short story about Alexander the Great in french for an A1 level learner"
                }
            ]
        )
        print(response.choices[0].message.content)

        # Extract the generated story text
        story_content = response.choices[0].message.content

        # Return the generated story as a JSON response
        return jsonify({"title": story_title, "content": story_content})
    else:
        return jsonify({"error": "Story not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)
