import uuid
import json
import logging
from typing import Dict

from story_session import StorySession
from openai_client import generate_story_structure, generate_next_chapter
from prompts import generate_story_structure_prompt as gssp, generate_chapter_prompt as gcp
from conversation import Conversation

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# In-memory store for story sessions
story_sessions: Dict[str, StorySession] = {}


def start_story(story_id):
    logging.info(f"Starting a new story with ID: {story_id}")

    story_title = {
        1: "Lila and the Moonlight Garden",
        2: "Oliver and the Pocket-Sized Dragon",
        3: "The Cloud Collector",
        4: "Benny and the Enchanted Paintbrush",
        5: "The Whispering Woods"
    }.get(story_id)

    if not story_title:
        logging.error("Invalid story ID provided.")
        return {"error": "Story not found"}, 404

    session_id = str(uuid.uuid4())
    logging.debug(f"Generated session ID: {session_id} for story '{story_title}'")

    # Prepare messages for story structure generation
    system_message = {"role": "system", "content": gssp.SYSTEM_MESSAGE}
    story_title_message = {"role": "user", "content": f"The title of the story is {story_title}"}
    init_story_message = {"role": "user", "content": gssp.FIRST_USER_MESSAGE}

    user_messages = [
        init_story_message,
        story_title_message,
    ]

    # Generate story structure
    logging.info("Generating story structure via OpenAI API...")
    story_content = generate_story_structure(system_message, user_messages)

    try:
        story_dict = json.loads(story_content)
        logging.debug(f"Received story structure: {story_dict}")

        story_session = StorySession(
            session_id=session_id,
            story_id=story_id,
            story_title=story_dict.get("title"),
            characters=story_dict.get("characters", []),
            story_summary=story_dict.get("story_summary"),
            plot_twist=story_dict.get("plot_twist"),
            moral=story_dict.get("moral"),
            chapters=story_dict.get("chapters", []),
            conversation=Conversation()
        )

        story_sessions[session_id] = story_session  # Store the session
        logging.info(f"Story session created and stored with session ID: {session_id}")

    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Failed to parse response: {e}")
        return {"error": "Failed to generate story base"}, 404

    # Generate the first chapter and return
    return fetch_next_chapter({"session_id": session_id, "feedback": "just right"}, True)


def fetch_next_chapter(data, is_first_chapter=False):
    session_id = data.get('session_id')
    feedback = data.get('feedback')
    logging.info(f"Fetching next chapter for session ID: {session_id}, feedback: '{feedback}'")
    # Retrieve the story session
    story_session = story_sessions.get(session_id)
    print("story session: ", story_session.to_json())

    if not story_session:
        logging.error("Story session not found.")
        return {"error": "Session not found"}, 404


    if is_first_chapter:
        conversation = Conversation()
        # Prepare messages for generating the first chapter
        logging.debug("Preparing conversation for the first chapter.")
        conversation.add_message({"role": "system", "content": gcp.SYSTEM_MESSAGE})
        conversation.add_message({"role": "user", "content": "The language is French. The reader is level A1 beginner"})
        conversation.add_message({"role": "user", "content": gcp.FIRST_USER_MESSAGE})
        conversation.add_message({"role": "assistant", "content": json.dumps({
            "story_title": story_session.story_title,
            "story_summary": story_session.story_summary,
            "characters": story_session.characters,
            "plot_twist": story_session.plot_twist,
            "moral": story_session.moral,
            "chapters": story_session.chapters})
                                  })
    else:
        conversation = story_session.get_conversation()
        logging.debug(f"Adding feedback to conversation history: '{feedback}'")
        conversation.add_message({"role": "user",
                                  "content": f"The previous chapter was {feedback}. Please adjust the difficulty accordingly and write the next chapter."})

    # Generate the next chapter and parse the response
    logging.info("Generating next chapter via OpenAI API...")
    chapter_content = generate_next_chapter(conversation.get_history())
    logging.debug(f"Received chapter content: {chapter_content}")

    try:
        next_chapter_dict = json.loads(chapter_content)
        full_chapter = next_chapter_dict.get("full_chapter")
        chapter_number = next_chapter_dict.get("chapter_number")

        logging.info(f"Chapter {chapter_number} generated successfully for session ID: {session_id}")

        # Update the conversation in the story session
        story_session.conversation = conversation
        print("story session 2: ", story_session.to_json())

        return {"new_chapter": full_chapter, "story_title": story_session.story_title, "session_id": session_id}

    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Failed to parse next chapter response: {e}")
        return {"error": "Failed to generate the next chapter"}, 404

