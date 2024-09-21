# backend/story_session.py
from conversation import Conversation
import json

class StorySession:
    def __init__(self, session_id, story_id, story_title, characters, story_summary, plot_twist, moral, chapters, conversation=None):
        self.session_id = session_id  # Unique session identifier
        self.story_id = story_id  # ID of the selected story
        self.story_title = story_title  # Title of the story
        self.characters = characters  # List of characters in the story
        self.story_summary = story_summary  # Overall summary of the story
        self.plot_twist = plot_twist  # Plot twist of the story
        self.moral = moral  # Moral of the story
        self.chapters = chapters  # List of chapters (chapter summaries)
        self.story_content = {}  # Store each chapter and its feedback
        self.chapter_number = 1  # Track the current chapter number
        self.conversation = conversation if conversation else Conversation()

    def add_chapter(self, chapter_number, chapter_content, feedback):
        """Add a new chapter with feedback to the story session."""
        self.story_content[chapter_number] = {
            "chapter": chapter_content,
            "feedback": feedback
        }

    def get_chapter(self, chapter_number):
        """Retrieve the content of a specific chapter."""
        return self.story_content.get(chapter_number)

    def get_conversation(self):
        """Retrieve the content of a specific chapter."""
        return self.conversation

    def get_all_chapters(self):
        """Retrieve all chapters and their feedback."""
        return self.story_content

    def to_json(self):
        """Return the story session object as JSON."""
        return json.dumps({
            "session_id": self.session_id,
            "story_id": self.story_id,
            "story_title": self.story_title,
            "characters": self.characters,
            "story_summary": self.story_summary,
            "plot_twist": self.plot_twist,
            "moral": self.moral,
            "chapters": self.chapters,
            "story_content": self.story_content,
            "chapter_number": self.chapter_number,
            "conversation": self.conversation.get_serialized_history()
        }, indent=4)