# backend/openai_client.py

from openai import OpenAI
import os
from tests.mock_responses import mock_generate_story_structure, mock_generate_next_chapter

# Initialize the OpenAI client
client = OpenAI()

def openai_generate_story(system_message, user_message):
    if os.getenv('MODE') == 'staging':
        return mock_generate_story_structure(system_message, user_message)
    try:
        # Call the OpenAI API with the constructed messages
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                system_message,
                user_message
            ],
            temperature=1,
            max_tokens=1343,
            top_p=1,
            frequency_penalty=0.29,
            presence_penalty=0.35,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "story_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string"
                            },
                            "chapters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "chapter_title": {
                                            "type": "string"
                                        },
                                        "chapter_summary": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "chapter_title",
                                        "chapter_summary"
                                    ],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "additionalProperties": False,
                        "required": [
                            "title",
                            "chapters"
                        ]
                    }
                }
            }
        )
        print(response.choices[0].message.content)
        # Extract the generated text from the response
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating the story structure: {e}")
        return "Error: Could not generate the story structure."

def openai_generate_chapter(conversation_history):
    if os.getenv('MODE') == 'staging':
        return mock_generate_next_chapter(conversation_history)
    try:
        # Call the OpenAI API with the constructed messages
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use the appropriate model, such as GPT-4 or any specific one you have access to
            messages=conversation_history,
            temperature=0.88,
            max_tokens=1343,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "story_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "full_chapter": {
                                "type": "string"
                            },
                            "chapter_number": {
                                "type": "string"
                            }
                        },
                        "additionalProperties": False,
                        "required": [
                            "full_chapter",
                            "chapter_number"
                        ]
                    }
                }
            }
        )

        # Extract the generated text from the response
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating the next chapter: {e}")
        return "Error: Could not generate the next chapter."