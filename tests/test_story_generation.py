# test_story_generation.py

import unittest
from unittest.mock import patch
from mock_responses import mock_generate_story_structure, mock_generate_next_chapter

class TestStoryGeneration(unittest.TestCase):

    @patch('backend.openai_client.generate_story_structure', side_effect=mock_generate_story_structure)
    @patch('backend.openai_client.generate_next_chapter', side_effect=mock_generate_next_chapter)
    def test_story_generation(self, mock_generate_story_structure, mock_generate_next_chapter):
        # Test the story structure generation
        system_message = {"role": "system", "content": "System message"}
        user_messages = {"role": "user", "content": "User message"}
        story_structure = mock_generate_story_structure(system_message, user_messages)
        self.assertIn("The Whispering Woods", story_structure)

        # Test the next chapter generation
        conversation_history = [{"role": "user", "content": "User message"}]
        next_chapter = mock_generate_next_chapter(conversation_history)
        self.assertIn("Luna ventured deeper into the woods", next_chapter)

if __name__ == '__main__':
    unittest.main()