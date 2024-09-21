# backend/generate_story_structure_prompt.py

SYSTEM_MESSAGE = """
You help authors come up with new structures and plots for short stories aimed at teenagers"""


FIRST_USER_MESSAGE = """
Help me with the base of my new book. I'll only give you a random title to start with, from that I just need the basic outline of the book and I will fill in all the details. 

It will be a short book aimed at teenagers, only 5 chapters long. The plot needs to be engaging, but at the same time easy to follow and understand. 

Generate for me 

1. The main characters of the book (max 2-3). Their names and a short summary about them. Are they a boy/girl? are they a cat/dog/dragon/chicken/banana? Do they live in a house/a shoe/an orange? Make up anything relevant, please do not only stick to these examples. You can leave a short summary about each character and any interesting details about them you like. 

2. A two sentence summary of the story of the book 

3. What's the big plot twist in the story? 

4. What's the moral of the story?

5. Finally, a two/three sentence summary of each of the 5 chapters
"""

