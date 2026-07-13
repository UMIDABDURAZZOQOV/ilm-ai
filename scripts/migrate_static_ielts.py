"""
Migrate static IELTS content from frontend lib/ielts.ts to database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion

def migrate_reading(db: Session):
    """Migrate reading passages from lib/ielts.ts"""
    print("Migrating reading passages...")
    
    passages = [
        {
            "id": "urban-rivers",
            "title": "The Return of Urban Rivers",
            "level": "Academic",
            "minutes": 18,
            "paragraphs": [
                "For most of the twentieth century, the rivers that ran through the world's growing cities were treated as problems to be managed rather than assets to be valued. Engineers straightened their curving channels, lined the banks with concrete, and in a number of places covered the water over entirely, hiding it beneath new roads and buildings. A river that flooded after heavy rain, or that carried the smell of untreated waste, was widely regarded as an obstacle to a modern, orderly city.",
                "By the 1970s, however, a different view had begun to take hold. Researchers studying the ecology of cities argued that a living river could offer benefits that a concrete drain never could. A natural channel, with its gravel beds and overhanging plants, supported fish, insects and birds. Just as importantly, the vegetation along the banks provided shade that lowered the temperature of the surrounding streets during increasingly hot summers.",
                "The practical case for restoration grew stronger as cities faced more frequent and more intense rainfall. A straightened, concrete-lined channel moves water downstream quickly, but in doing so it can pass a sudden flood on to communities further along. A restored river, by contrast, is allowed to spread into planted areas beside the water. These spaces slow the flow and store excess water temporarily, reducing the risk of flooding in built-up districts nearby.",
                "Restoration is rarely simple. Engineers must remove old concrete, reshape the channel, and reintroduce native plants, often while managing the expectations of residents who have never seen the river uncovered. Early projects in Europe and East Asia showed that success depended less on any single technique than on patient cooperation between city authorities, ecologists and the public. Where that cooperation was absent, ambitious schemes stalled or were quietly abandoned.",
                "Today, uncovered and restored rivers are increasingly seen as symbols of a healthier city. They draw walkers and cyclists, raise the value of nearby property, and give residents daily contact with moving water and wildlife. Yet supporters caution that a restored river is not a finished monument. It is a living system that must be monitored and maintained for decades if the gains of restoration are to last.",
            ],
            "questions": [
                {"id": "ur1", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Before the 1970s, most engineers regarded urban rivers as valuable natural features.", "answer": "False"},
                {"id": "ur2", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Some city rivers were completely covered over during the twentieth century.", "answer": "True"},
                {"id": "ur3", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Concrete channels are cheaper to build than restored natural channels.", "answer": "Not Given"},
                {"id": "ur4", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Plants growing beside a restored river can help lower street temperatures.", "answer": "True"},
                {"id": "ur5", "type": "mcq", "options": ["encourages the growth of native plants.", "can pass floodwater on to communities downstream.", "is more expensive to maintain than a natural channel.", "attracts too many walkers and cyclists."], "prompt": "According to the passage, one drawback of a straightened, concrete-lined channel is that it", "answer": "can pass floodwater on to communities downstream."},
                {"id": "ur6", "type": "mcq", "options": ["the invention of a single new technique.", "generous funding from national governments.", "cooperation between authorities, ecologists and the public.", "the removal of all residents from riverside areas."], "prompt": "The writer suggests that early restoration projects succeeded mainly because of", "answer": "cooperation between authorities, ecologists and the public."},
                {"id": "ur7", "type": "completion", "hint": "ONE WORD ONLY", "prompt": "Beside a restored river, planted areas slow the flow and temporarily store excess water, reducing the risk of ______.", "answer": "flooding"},
                {"id": "ur8", "type": "completion", "hint": "ONE WORD ONLY", "prompt": "Supporters warn that a restored river must be monitored and ______ for decades.", "answer": "maintained"},
            ],
        },
        {
            "id": "bee-navigation",
            "title": "How Honeybees Find Their Way",
            "level": "Academic",
            "minutes": 18,
            "paragraphs": [
                "A honeybee that leaves its hive in search of food may travel several kilometres across a landscape of fields, hedges and buildings, and yet it returns home with remarkable accuracy. For more than a century, scientists have tried to explain how so small an animal, with a brain no larger than a grain of rice, performs a feat of navigation that would challenge a human without a map.",
                "Part of the answer lies in the sun. A foraging bee uses the position of the sun as a kind of moving compass, adjusting its course as the sun travels across the sky. On cloudy days, when the sun is hidden, the bee can still read the pattern of polarised light in patches of blue sky, information that is invisible to the human eye but clear to the specialised cells in a bee's compound eyes.",
                "The sun alone, however, cannot tell a bee how far it has flown. To measure distance, bees appear to count the movement of the landscape across their eyes as they fly, a process researchers call optic flow. A bee flying past a dense hedge, where the scene rushes by quickly, registers a greater distance than one crossing an open field, where the view changes slowly. This helps explain why bees sometimes misjudge distance over water or bare ground, where there is little detail to track.",
                "Perhaps the most famous discovery about bee navigation concerns communication. A bee that has found a rich source of food returns to the darkness of the hive and performs a series of movements, long known as the waggle dance. The direction of the dance, measured against the vertical, indicates the direction of the food relative to the sun, while the length of the central run signals how far away it lies. Other bees follow the dancer closely and then set out on the same heading.",
                "Recent research suggests that bees also build a rough mental map of familiar landmarks, allowing them to find their way even when the usual cues are disturbed. Trees, ponds and the edges of woodland all seem to act as reference points. Taken together, these overlapping systems make the honeybee one of the most sophisticated natural navigators of its size, and a continuing source of ideas for engineers designing small flying robots.",
            ],
            "questions": [
                {"id": "bn1", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "A honeybee's brain is roughly the size of a grain of rice.", "answer": "True"},
                {"id": "bn2", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Bees are unable to navigate at all when the sun is hidden by clouds.", "answer": "False"},
                {"id": "bn3", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Honeybees can see polarised light that humans cannot detect.", "answer": "True"},
                {"id": "bn4", "type": "tfng", "options": ["True", "False", "Not Given"], "prompt": "Bees find it easier to judge distance over water than over a hedge.", "answer": "False"},
                {"id": "bn5", "type": "mcq", "options": ["follow the scent of flowers to a food source.", "measure distance by the movement of the scene across their eyes.", "read the polarised light in clear blue sky.", "communicate direction inside the hive."], "prompt": "According to the passage, 'optic flow' refers to the way bees", "answer": "measure distance by the movement of the scene across their eyes."},
                {"id": "bn6", "type": "mcq", "options": ["how rich the food source is.", "the direction of the food relative to the sun.", "how far away the food source lies.", "the number of bees needed to collect it."], "prompt": "In the waggle dance, the length of the central run indicates", "answer": "how far away the food source lies."},
                {"id": "bn7", "type": "completion", "hint": "ONE WORD ONLY", "prompt": "On cloudy days, bees rely on the pattern of ______ light in the sky to hold their course.", "answer": "polarised"},
                {"id": "bn8", "type": "completion", "hint": "TWO WORDS", "prompt": "Bees appear to build a rough mental ______ of familiar landmarks such as trees and ponds.", "answer": "map"},
            ],
        },
    ]
    
    for passage_data in passages:
        # Check if already exists
        existing = db.query(IeltsReading).filter(IeltsReading.title == passage_data["title"]).first()
        if existing:
            print(f"  ✓ Skipping existing passage: {passage_data['title']}")
            continue
        
        passage = IeltsReading(
            section=1,
            title=passage_data["title"],
            passage_text="\n\n".join(passage_data["paragraphs"]),
            difficulty="medium",
            word_count=len("\n\n".join(passage_data["paragraphs"]).split())
        )
        db.add(passage)
        db.commit()
        db.refresh(passage)
        
        for i, q_data in enumerate(passage_data["questions"]):
            question = IeltsQuestion(
                skill="Reading",
                parent_id=passage.id,
                question_type=q_data["type"],
                question_text=q_data["prompt"],
                options=q_data.get("options"),
                correct_answer=q_data["answer"],
                hint=q_data.get("hint"),
                order_index=i + 1
            )
            db.add(question)
        
        db.commit()
        print(f"  ✓ Created reading passage: {passage_data['title']}")

def migrate_writing(db: Session):
    """Migrate writing tasks from lib/ielts.ts"""
    print("Migrating writing tasks...")
    
    tasks = [
        {"id": "w2-tech-1", "task": "Task2", "category": "Technology", "minWords": 250, "minutes": 40, "prompt": "Some people believe that smartphones have made communication between people worse rather than better. To what extent do you agree or disagree?"},
        {"id": "w2-edu-1", "task": "Task2", "category": "Education", "minWords": 250, "minutes": 40, "prompt": "In many countries, students are required to study subjects such as history and art even when they plan careers in science. Do the advantages of this outweigh the disadvantages?"},
        {"id": "w2-env-1", "task": "Task2", "category": "Environment", "minWords": 250, "minutes": 40, "prompt": "Some argue that individuals can do little to protect the environment and that only governments and large companies can make a real difference. Discuss both views and give your own opinion."},
        {"id": "w2-work-1", "task": "Task2", "category": "Work", "minWords": 250, "minutes": 40, "prompt": "Many people now work from home using modern technology. Do the benefits of working from home outweigh the drawbacks?"},
        {"id": "w2-society-1", "task": "Task2", "category": "Society", "minWords": 250, "minutes": 40, "prompt": "Some people think that governments should spend money on public libraries, while others believe this money would be better spent on the internet and digital services. Discuss both views and give your opinion."},
        {"id": "w2-health-1", "task": "Task2", "category": "Health", "minWords": 250, "minutes": 40, "prompt": "In some countries, the number of people who are overweight is rising. What are the causes of this, and what measures could be taken to solve the problem?"},
        {"id": "w2-culture-1", "task": "Task2", "category": "Culture", "minWords": 250, "minutes": 40, "prompt": "Some believe that international tourism creates tension rather than understanding between people from different countries. To what extent do you agree or disagree?"},
        {"id": "w2-youth-1", "task": "Task2", "category": "Youth", "minWords": 250, "minutes": 40, "prompt": "These days many young people spend a large amount of their free time on social media. Is this a positive or negative development?"},
        {"id": "w2-city-1", "task": "Task2", "category": "Urban life", "minWords": 250, "minutes": 40, "prompt": "As cities grow, more people move away from the countryside. What problems does this cause, and how might these problems be reduced?"},
        {"id": "w2-media-1", "task": "Task2", "category": "Media", "minWords": 250, "minutes": 40, "prompt": "Some people think that news organisations should report only good news. Do you agree or disagree?"},
        {"id": "w1-line-1", "task": "Task1", "category": "Line graph", "minWords": 150, "minutes": 20, "prompt": "A line graph shows the number of visitors (in millions) to three museums in one city from 2000 to 2020. Museum A rose steadily from 1 to 4 million. Museum B fell from 3 to 1 million. Museum C stayed roughly flat at 2 million. Summarise the information by selecting and reporting the main features, and make comparisons where relevant."},
        {"id": "w1-bar-1", "task": "Task1", "category": "Bar chart", "minWords": 150, "minutes": 20, "prompt": "A bar chart compares the average hours per week spent on four activities (reading, exercise, television, and social media) by two age groups: teenagers and adults over 40. Teenagers spend far more time on social media and less on reading; adults spend more on reading and television. Summarise the main features and make comparisons where relevant."},
        {"id": "w1-process-1", "task": "Task1", "category": "Process", "minWords": 150, "minutes": 20, "prompt": "A diagram shows how rainwater is collected and treated before it reaches homes: rain falls into a reservoir, passes through a filter, is stored in a tank, treated with chemicals, and finally piped to houses. Summarise the process by describing the main stages."},
    ]
    
    for task_data in tasks:
        # Check if already exists
        existing = db.query(IeltsWriting).filter(
            IeltsWriting.task_type == task_data["task"],
            IeltsWriting.category == task_data["category"]
        ).first()
        if existing:
            print(f"  ✓ Skipping existing task: {task_data['task']} - {task_data['category']}")
            continue
        
        writing = IeltsWriting(
            task_type=task_data["task"],
            category=task_data["category"],
            prompt=task_data["prompt"],
            image_url=None,
            min_words=task_data["minWords"],
            duration_minutes=task_data["minutes"],
            difficulty="medium"
        )
        db.add(writing)
        db.commit()
        print(f"  ✓ Created writing task: {task_data['task']} - {task_data['category']}")

def migrate_speaking(db: Session):
    """Migrate speaking topics from lib/ielts.ts"""
    print("Migrating speaking topics...")
    
    topics = [
        {"id": "s1-hometown", "part": 1, "topic": "Your hometown", "questions": ["Where is your hometown, and what is it known for?", "What do you like most about living there?", "Has your hometown changed much in recent years?", "Would you recommend it to a tourist? Why or why not?"]},
        {"id": "s1-work-study", "part": 1, "topic": "Work or study", "questions": ["Do you work or are you a student at the moment?", "What do you enjoy most about your work or studies?", "Is there anything you would like to change about it?", "What are your plans for the next few years?"]},
        {"id": "s1-freetime", "part": 1, "topic": "Free time", "questions": ["What do you usually do in your free time?", "Do you prefer spending free time alone or with others?", "Has the way you spend your free time changed since childhood?", "Do you think people today have enough free time?"]},
        {"id": "s1-technology", "part": 1, "topic": "Technology", "questions": ["How often do you use a smartphone during the day?", "Which app or device could you not live without?", "Do you think you spend too much time on screens?", "How did you learn to use new technology?"]},
        {"id": "s2-teacher", "part": 2, "topic": "Describe a teacher who influenced you", "questions": ["Describe a teacher who has influenced you. You should say: who this teacher was; what subject they taught; what they were like; and explain why they influenced you."], "cue_card": "Describe a teacher who has influenced you. You should say: who this teacher was; what subject they taught; what they were like; and explain why they influenced you.", "prep_seconds": 120, "speak_seconds": 120},
        {"id": "s2-place", "part": 2, "topic": "Describe a place you like to relax", "questions": ["Describe a place where you like to relax. You should say: where it is; how often you go there; what you do there; and explain why it helps you relax."], "cue_card": "Describe a place where you like to relax. You should say: where it is; how often you go there; what you do there; and explain why it helps you relax.", "prep_seconds": 120, "speak_seconds": 120},
        {"id": "s2-skill", "part": 2, "topic": "Describe a skill you would like to learn", "questions": ["Describe a skill you would like to learn. You should say: what the skill is; how you would learn it; how long it might take; and explain why you want to learn it."], "cue_card": "Describe a skill you would like to learn. You should say: what the skill is; how you would learn it; how long it might take; and explain why you want to learn it.", "prep_seconds": 120, "speak_seconds": 120},
        {"id": "s2-book", "part": 2, "topic": "Describe a book you enjoyed", "questions": ["Describe a book that you enjoyed reading. You should say: what the book was about; when you read it; why you chose it; and explain why you enjoyed it."], "cue_card": "Describe a book that you enjoyed reading. You should say: what the book was about; when you read it; why you chose it; and explain why you enjoyed it.", "prep_seconds": 120, "speak_seconds": 120},
        {"id": "s3-education", "part": 3, "topic": "Education and learning", "questions": ["How has the way people learn changed over the last twenty years?", "Do you think online learning is as effective as classroom learning?", "Should governments pay for everyone's higher education? Why or why not?", "What skills will be most important for students in the future?"]},
        {"id": "s3-technology", "part": 3, "topic": "Technology and society", "questions": ["In what ways has technology changed how families communicate?", "Do the benefits of social media outweigh its problems?", "Should there be limits on how much technology children use?", "How might technology change the workplace in the future?"]},
        {"id": "s3-environment", "part": 3, "topic": "Environment", "questions": ["Whose responsibility is it to protect the environment?", "Are people today more aware of environmental issues than in the past?", "What can ordinary people do to reduce waste?", "Do you think future generations will live in a cleaner world?"]},
    ]
    
    for topic_data in topics:
        # Check if already exists
        existing = db.query(IeltsSpeaking).filter(IeltsSpeaking.topic == topic_data["topic"]).first()
        if existing:
            print(f"  ✓ Skipping existing topic: {topic_data['topic']}")
            continue
        
        speaking = IeltsSpeaking(
            part=topic_data["part"],
            topic=topic_data["topic"],
            questions=topic_data["questions"],
            cue_card=topic_data.get("cue_card"),
            prep_seconds=topic_data.get("prep_seconds"),
            speak_seconds=topic_data.get("speak_seconds"),
            difficulty="medium"
        )
        db.add(speaking)
        db.commit()
        print(f"  ✓ Created speaking topic: {topic_data['topic']}")

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Migrating Static IELTS Content to Database")
        print("=" * 50)
        
        migrate_reading(db)
        migrate_writing(db)
        migrate_speaking(db)
        
        print("=" * 50)
        print("Migration complete!")
        print("=" * 50)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
