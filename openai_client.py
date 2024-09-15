# backend/openai_client.py

from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI()

def generate_initial_story(system_message, user_messages):
    """
    Sends a request to the OpenAI API to generate a part of the story.
    :param system_message: The system message setting the context for the API.
    :param user_messages: List of user messages to provide instructions and feedback.
    :return: The generated story content.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message}
        ]+ user_messages,
        temperature = 0.88,
        max_tokens = 1343,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "story_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "story_title": {
                            "type": "string"
                        },
                        "story_summary": {
                            "type": "string"
                        },
                        "full_chapter": {
                            "type": "string"
                        },
                        "chapter_number": {
                            "type": "string"
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "story_title",
                        "story_summary",
                        "full_chapter",
                        "chapter_number"
                    ]
                }
            }
        }
    )
    return response.choices[0].message.content


def generate_next_chapter(system_message, user_messages):
    """
    Function to generate the next chapter of the story using OpenAI's API.

    Args:
    system_message (str): The system-level instructions for the OpenAI model.
    user_messages (list): The list of user and assistant messages to provide context to the OpenAI API.

    Returns:
    str: The generated next chapter content.
    """
    try:
        # Call the OpenAI API with the constructed messages
        response = client.chat.completions.create(
            model="gpt-4",  # Use the appropriate model, such as GPT-4 or any specific one you have access to
            messages=[
                {"role": "system", "content": system_message},
                *user_messages  # Spread the user messages list into the messages array
            ],
        temperature = 0.88,
        max_tokens = 1343,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        response_format = {
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
        next_chapter_content = response['choices'][0]['message']['content']
        return next_chapter_content

    except Exception as e:
        print(f"Error generating the next chapter: {e}")
        return "Error: Could not generate the next chapter."