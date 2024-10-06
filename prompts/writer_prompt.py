# backend/writer_prompt.py


def writer_system_message():
    return """You are a writing assistant specializing in retelling classic folk tales, fairy tales, myths, and legends with an inventive twist."""


def writer_user_message(story_title, setting):
    return  f""" Take the familiar story of "{story_title}" and reimagine it in a {setting} context. 
        
            Preserve the core plot elements while adjusting the little details such as the names of characters in the story, any foods, animals or plants mentioned , the landscapes and settings etc. 
            
            You do not have to change every detail and we don't want to exaggerate stereotypes, the goal is to tell the same story in a way that is more recognisable and familiar to a {setting} reader. 

            Create an outline for the story that is split into five chapters and follows Freytag’s Pyramid structure (Exposition, Rising Action, Climax, Falling Action, Denouement). 
            
            The outline should be in the form of a short bullet point summary of each of the five chapters, explicitly showing how each chapter follows the structure of Freytag’s Pyramid. 
            
            Each bullet point should be explicit about the key events that occur in that chapter and how they contribute to the overall plot, don't leave things to interpretation here.
            
            Each chapter should also have a unique, catchy title that reflects the plot of that chapter.
            
            Example Output:
            
            Chapter 1: [Unique Title]
            
            [Introduce main character and setting, establish context and initial problem]
            
            Chapter 2: [Unique Title]
            
            [Introduce magical element and describe protagonist's decision to take action]
            
            Chapter 3: [Unique Title]
            
            [Describe protagonist's major encounter or confrontation, highlighting key tension]
            
            Chapter 4: [Unique Title]
            
            [Show protagonist dealing with consequences and addressing challenges]
            
            Chapter 5: [Unique Title]
            
            [Provide resolution and ending, showing how the protagonist's situation has changed]
            
            The goal is to maintain the spirit of the original story while infusing it with a fresh cultural context.
            
            Note your chapter summaries will contain multiple bullet points rather than the one shown in the example"""
