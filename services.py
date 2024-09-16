import uuid
import json
from contextlib import nullcontext

from openai_client import generate_initial_story, generate_next_chapter, generate_story_structure
from prompts import generate_chapter_prompt, generate_story_structure_prompt

# In-memory store for story sessions
story_sessions = {}

def start_story(story_id):
    story_title = {
        1: "Lila and the Moonlight Garden",
        2: "Oliver and the Pocket-Sized Dragon",
        3: "The Cloud Collector",
        4: "Benny and the Enchanted Paintbrush",
        5: "The Whispering Woods"
    }.get(story_id)

    if not story_title:
        return {"error": "Story not found"}, 404

    session_id = str(uuid.uuid4())

    # Prepare messages for story structure generation
    user_messages_structure = [
        {"role": "user", "content": generate_story_structure_prompt.FIRST_USER_MESSAGE},
        {"role": "user", "content": f"The title of the story is {story_title}"},
    ]

    # Generate story structure
    story_content = generate_story_structure(generate_story_structure_prompt.SYSTEM_MESSAGE, user_messages_structure)
    print(story_content)

    try:
        story_dict = json.loads(story_content)
        story_sessions[session_id] = {
            "story_id": story_id,
            "story_title": story_dict.get("title"),
            "characters": story_dict.get('characters', []),
            "story_summary": story_dict.get('story_summary'),
            "plot_twist": story_dict.get('plot_twist'),
            "moral": story_dict.get('moral'),
            "chapters": story_dict.get('chapters', []),
        }
    except (KeyError, json.JSONDecodeError) as e:
        print("Failed to parse response:", e)
        return {"error": "Failed to generate story base"}, 404

    # Generate the first chapter
    return fetch_next_chapter({"session_id": session_id, "feedback": "just right"}, True)

def fetch_next_chapter(data, is_first_chapter):
    session_id = data.get('session_id')
    feedback_string = {"role": "user", "content":""}

    if not is_first_chapter:
        feedback_string = {"role": "user", "content":f"The previous chapter was {data.get('feedback')}. Please adjust the difficulty accordingly and write the next chapter."}

    # Retrieve the story session
    story_session = story_sessions.get(session_id)
    if not story_session:
        return {"error": "Session not found"}, 404

    user_messages_chapter = [
        {"role": "user", "content": generate_story_structure_prompt.FIRST_USER_MESSAGE},
        {"role": "user", "content": "The language is French. The reader is level A1 beginner"},
        {"role": "user", "content": json.dumps({
            "story_title": story_session["story_title"],
            "story_summary": story_session["story_summary"],
            "characters": story_session["characters"],
            "plot_twist": story_session["plot_twist"],
            "moral": story_session["moral"],
            "chapters": story_session["chapters"],
        })},
        feedback_string
    ]

    next_chapter_content = generate_next_chapter(generate_chapter_prompt.SYSTEM_MESSAGE, user_messages_chapter)
    print(next_chapter_content)

    try:
        next_chapter_dict = json.loads(next_chapter_content)
        full_chapter = next_chapter_dict.get("full_chapter")
        chapter_number = next_chapter_dict.get("chapter_number")

        story_sessions[session_id]['story_content'] = full_chapter
        story_sessions[session_id]['chapter_number'] = chapter_number

        return {"new_chapter": full_chapter}

    except (KeyError, json.JSONDecodeError) as e:
        print("Failed to parse next chapter response:", e)
        return {"error": "Failed to generate the next chapter"}, 404
