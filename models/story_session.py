# backend/story_session.py
from backend.conversation import Conversation
import json
from utils.db_utils import get_db_connection

class StorySession:
    def __init__(self, session_id, story_id, story_title, conversation=None, language=None, level=None, setting=None):
        self.session_id = session_id  # Unique session identifier
        self.story_id = story_id  # ID of the selected story
        self.story_title = story_title  # Title of the story
        self.conversation = conversation if conversation else Conversation()
        self.language = language
        self.level = level
        self.setting = setting


    def get_conversation(self):
        """Retrieve the content of a specific chapter."""
        return self.conversation

    def to_json(self):
        try:
            return json.dumps({
                "session_id": self.session_id,
                "story_id": self.story_id,
                "story_title": self.story_title,
                "conversation": self.conversation.get_serialized_history(),
                "language": self.language,
                "level": self.level,
                "setting": self.setting
            }, default=self._json_default)
        except TypeError as e:
            print(f"Serialization error: {e}")
            print(
                f"Types: session_id={type(self.session_id)}, story_id={type(self.story_id)}, story_title={type(self.story_title)}, conversation={type(self.conversation.get_serialized_history())}, language={type(self.language)}, level={type(self.level)}, setting={type(self.setting)}")
            raise

    def _json_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def save_to_db(self):
        conn = get_db_connection()
        with conn:
            conn.execute('''
                INSERT OR REPLACE INTO story_sessions (session_id, story_id, story_title, conversation, language, level, setting)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.session_id, self.story_id, self.story_title,
                json.dumps(self.conversation.get_serialized_history(), default=self._json_default),
                self.language, self.level, self.setting
            ))
        conn.close()

    @staticmethod
    def load_from_db(session_id):
        conn = get_db_connection()
        session = conn.execute('SELECT * FROM story_sessions WHERE session_id = ?', (session_id,)).fetchone()
        conn.close()
        if session:
            return StorySession(
                session_id=session['session_id'],
                story_id=session['story_id'],
                story_title=session['story_title'],
                conversation=Conversation.load_history_from_json(session['conversation']),
                language=session['language'],
                level=session['level'],
                setting=session['setting']
            )
        return None