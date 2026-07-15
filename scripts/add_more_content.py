"""
Add more IELTS content to reach minimum viable levels
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsWriting, IeltsSpeaking

def add_more_writing(db: Session):
    """Add more writing tasks"""
    print("Adding more writing tasks...")
    
    new_writings = [
        {
            "task_type": "Task2",
            "category": "Health",
            "prompt": "In many countries, the average life expectancy has been increasing. What are the possible effects of this trend on individuals and society?",
            "min_words": 250,
            "duration_minutes": 40,
            "difficulty": "medium"
        },
        {
            "task_type": "Task2",
            "category": "Crime",
            "prompt": "Some people believe that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better ways to reduce crime. Discuss both views and give your own opinion.",
            "min_words": 250,
            "duration_minutes": 40,
            "difficulty": "medium"
        },
        {
            "task_type": "Task2",
            "category": "Globalization",
            "prompt": "Globalization has made the world a better place to live in. Do you agree or disagree with this statement?",
            "min_words": 250,
            "duration_minutes": 40,
            "difficulty": "medium"
        },
        {
            "task_type": "Task1",
            "category": "Line graph",
            "prompt": "The line graph shows the number of visitors to three museums in London between 2000 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "min_words": 150,
            "duration_minutes": 20,
            "difficulty": "medium"
        },
        {
            "task_type": "Task1",
            "category": "Pie chart",
            "prompt": "The pie charts show the percentage of energy produced from different sources in a country in 1990 and 2010. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
            "min_words": 150,
            "duration_minutes": 20,
            "difficulty": "medium"
        },
    ]
    
    for task_data in new_writings:
        writing = IeltsWriting(
            task_type=task_data["task_type"],
            category=task_data["category"],
            prompt=task_data["prompt"],
            image_url=None,
            min_words=task_data["min_words"],
            duration_minutes=task_data["duration_minutes"],
            difficulty=task_data["difficulty"]
        )
        db.add(writing)
        print(f"  ✓ Added writing task: {task_data['task_type']} - {task_data['category']}")
    
    db.commit()

def add_more_speaking(db: Session):
    """Add more speaking topics"""
    print("Adding more speaking topics...")
    
    new_speakings = [
        {
            "part": 1,
            "topic": "Food",
            "questions": ["What is your favorite food?", "How often do you eat out?", "Do you like cooking?", "What is a traditional dish in your country?"],
            "cue_card": None,
            "prep_seconds": None,
            "speak_seconds": None,
            "difficulty": "medium"
        },
        {
            "part": 1,
            "topic": "Weather",
            "questions": ["What is the weather like in your country?", "Do you prefer hot or cold weather?", "How does the weather affect your mood?", "What do you do on rainy days?"],
            "cue_card": None,
            "prep_seconds": None,
            "speak_seconds": None,
            "difficulty": "medium"
        },
        {
            "part": 2,
            "topic": "Describe a memorable holiday",
            "questions": ["Describe a memorable holiday you have had. You should say: where you went; who you went with; what you did; and explain why it was memorable."],
            "cue_card": "Describe a memorable holiday you have had. You should say: where you went; who you went with; what you did; and explain why it was memorable.",
            "prep_seconds": 60,
            "speak_seconds": 120,
            "difficulty": "medium"
        },
        {
            "part": 2,
            "topic": "Describe a skill you want to learn",
            "questions": ["Describe a skill you would like to learn in the future. You should say: what the skill is; why you want to learn it; how you would learn it; and explain how this skill would benefit you."],
            "cue_card": "Describe a skill you would like to learn in the future. You should say: what the skill is; why you want to learn it; how you would learn it; and explain how this skill would benefit you.",
            "prep_seconds": 60,
            "speak_seconds": 120,
            "difficulty": "medium"
        },
        {
            "part": 3,
            "topic": "Travel and Tourism",
            "questions": ["How has tourism changed in recent years?", "What are the benefits of international tourism?", "What are the disadvantages of mass tourism?", "How can tourism be made more sustainable?"],
            "cue_card": None,
            "prep_seconds": None,
            "speak_seconds": None,
            "difficulty": "medium"
        },
    ]
    
    for topic_data in new_speakings:
        speaking = IeltsSpeaking(
            part=topic_data["part"],
            topic=topic_data["topic"],
            questions=topic_data["questions"],
            cue_card=topic_data.get("cue_card"),
            prep_seconds=topic_data.get("prep_seconds"),
            speak_seconds=topic_data.get("speak_seconds"),
            difficulty=topic_data["difficulty"]
        )
        db.add(speaking)
        print(f"  ✓ Added speaking topic: Part {topic_data['part']} - {topic_data['topic']}")
    
    db.commit()

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Adding More IELTS Content")
        print("=" * 50)
        
        add_more_writing(db)
        add_more_speaking(db)
        
        print("=" * 50)
        print("Content addition complete!")
        print("=" * 50)
        
        # Show final counts
        print("\nFinal content counts:")
        print(f"  Writing: {db.query(IeltsWriting).count()} tasks")
        print(f"  Speaking: {db.query(IeltsSpeaking).count()} topics")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
