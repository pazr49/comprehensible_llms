import uuid
import json
import logging

from models.story_session import StorySession
from services.openai_client import openai_generate_story, openai_generate_chapter
from prompts import writer_prompt, language_tutor_prompt
from backend.conversation import Conversation

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_story_outline(data, story_id, story_title):
    logging.info(f"Starting a new story with ID: {story_id}")
    language = data.get('language')
    level = data.get('level')
    setting = "French"

    if not story_title:
        logging.error("Invalid story ID provided.")
        return {"error": "Story not found"}, 404

    session_id = str(uuid.uuid4())
    logging.debug(f"Generated session ID: {session_id} for story '{story_title}'")

    # Prepare messages for story structure generation
    system_message = {"role": "system", "content": writer_prompt.writer_system_message()}
    init_story_message = {"role": "user", "content": writer_prompt.writer_user_message(story_title, setting)}

    # Generate story structure
    logging.info("Generating story structure via OpenAI API...")
    print("system message: ", system_message)
    print("init story message: ", init_story_message)
    story_content = openai_generate_story(system_message, init_story_message)

    try:
        story_dict = json.loads(story_content)
        logging.debug(f"Received story structure: {story_dict}")

        story_session = StorySession(
            session_id=session_id,
            story_id=story_id,
            story_title=story_title,
            conversation=Conversation(),
            language=language,
            level=level,
            setting=setting
        )

        story_session.save_to_db()  # Save the session to the database
        logging.info(f"Story session created and stored with session ID: {session_id}")

    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Failed to parse response: {e}")
        return {"error": "Failed to generate story base"}, 404

    # Generate the first chapter and return
    return generate_next_chapter(
        {"session_id": session_id, "feedback": "just right", "story_content": story_content},
        True
    )


def generate_next_chapter(data, is_first_chapter):
    session_id = data.get('session_id')
    feedback = data.get('feedback')
    story_content = data.get('story_content')
    print("story session ID: ", session_id, feedback, story_content)

    # Retrieve the story session from the database
    story_session = StorySession.load_from_db(session_id)

    if not story_session:
        logging.error("Story session not found.")
        return {"error": "Session not found"}, 404

    language = story_session.language
    level = story_session.level
    print("language is here in session, ", language)
    logging.info(f"Fetching next chapter for session ID: {session_id}, feedback: '{feedback}', language: {language}, level: {level}")
    print("story session 1: ", story_session.to_json())

    if is_first_chapter:
        conversation = Conversation()
        # Prepare messages for generating the first chapter
        logging.debug("Preparing conversation for the first chapter.")
        conversation.add_message({"role": "system", "content": language_tutor_prompt.language_tutor_system_message(language, level)})
        conversation.add_message({"role": "user", "content": language_tutor_prompt.language_tutor_user_message(story_content, language, level)})
    else:
        conversation = story_session.get_conversation()
        logging.debug(f"Adding feedback to conversation history: '{feedback}'")
        conversation.add_message({"role": "user",
                                  "content": f"The previous chapter was {feedback}. Please adjust the difficulty accordingly and write the next chapter."})

    # Generate the next chapter and parse the response
    logging.info("Generating next chapter via OpenAI API...")
    chapter_content = openai_generate_chapter(conversation.get_history())
    conversation.add_message({"role": "assistant", "content": chapter_content})
    print("story session 2: ", story_session.to_json())
    logging.debug(f"Received chapter content: {chapter_content}")

    try:
        next_chapter_dict = json.loads(chapter_content)
        full_chapter = next_chapter_dict.get("full_chapter")
        chapter_number = next_chapter_dict.get("chapter_number")

        logging.info(f"Chapter {chapter_number} generated successfully for session ID: {session_id}")

        # Update the conversation in the story session
        story_session.conversation = conversation

        # Save the updated session to the database
        story_session.save_to_db()

        print("story session 3: ", story_session.to_json())
        return {"new_chapter": full_chapter, "story_title": story_session.story_title, "session_id": session_id}

    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Failed to parse next chapter response: {e}")
        return {"error": "Failed to generate the next chapter"}, 404

