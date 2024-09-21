# mock_responses.py
import json

def mock_generate_story_structure(system_message, user_messages):
    return json.dumps({
        "title": "The Whispering Woods",
        "characters": [
            {"character_name": "Luna", "character_summary": "A brave young girl with a curious mind and a heart full of adventure."},
            {"character_name": "Eldric", "character_summary": "A wise old owl who guides Luna through the mystical woods."}
        ],
        "story_summary": "A tale of adventure in the mystical woods where Luna discovers the secrets of the talking trees and learns valuable life lessons.",
        "plot_twist": "The trees can talk and they hold the memories of the forest.",
        "moral": "Courage, kindness, and curiosity can lead to great discoveries.",
        "chapters": [
            {"chapter_title": "The Beginning", "chapter_summary": "Luna enters the woods and meets Eldric, the wise old owl."},
            {"chapter_title": "The Talking Trees", "chapter_summary": "Luna discovers that the trees can talk and learns about their ancient wisdom."},
            {"chapter_title": "The Hidden Path", "chapter_summary": "Luna and Eldric find a hidden path that leads to a secret part of the forest."},
            {"chapter_title": "The Forest's Secret", "chapter_summary": "Luna uncovers the secret of the forest and learns a valuable lesson about courage and kindness."}
        ]
    })

def mock_generate_next_chapter(conversation_history):
    return json.dumps({
        "full_chapter": "Luna ventured deeper into the woods, where she met talking trees that shared their ancient wisdom. Eldric, the wise old owl, guided her to a hidden path that led to a secret part of the forest. There, Luna discovered a magical clearing where the trees revealed the forest's deepest secrets. She learned that courage and kindness could unlock the mysteries of the world around her.",
        "chapter_number": "2"
    })