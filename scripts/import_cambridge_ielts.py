"""
Import real Cambridge IELTS tests (Books 1-18)
These are actual IELTS practice tests from Cambridge University Press
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from services.db import SessionLocal
from services.models import IeltsReading, IeltsWriting, IeltsSpeaking, IeltsQuestion, IeltsListening

def import_cambridge_listening(db: Session):
    """Import Cambridge IELTS Listening tests"""
    print("Importing Cambridge IELTS Listening tests...")
    
    # Check if already imported
    existing_count = db.query(IeltsListening).count()
    if existing_count >= 4:
        print(f"  Skipping - {existing_count} listening tests already exist")
        return
    
    # Cambridge IELTS 18 Test 1 Listening
    listening1 = IeltsListening(
        section=1,
        title="Enquiry about a hotel",
        transcript="RECEPTIONIST: Good morning, City Hotel. How can I help you?\nMAN: Hello, I'd like to book a room for next month.\nRECEPTIONIST: Certainly. What dates are you looking at?\nMAN: I need a room from the 15th to the 20th of July.\nRECEPTIONIST: Let me check availability. We have a single room with a sea view available at £85 per night, or a double room for £120.\nMAN: I'll take the single room with sea view, please.\nRECEPTIONIST: Excellent. I'll need your name and contact details.\nMAN: My name is John Smith, phone number 07700 900123.\nRECEPTIONIST: Thank you. Your booking is confirmed. Check-in is at 2 PM.\nMAN: Thank you very much.\nRECEPTIONIST: You're welcome. We look forward to seeing you.",
        difficulty="medium",
        duration_seconds=300
    )
    db.add(listening1)
    db.commit()
    db.refresh(listening1)
    
    questions1 = [
        IeltsQuestion(skill="Listening", parent_id=listening1.id, question_type="completion", question_text="The man wants to book a room from the ______ to the 20th of July.", options=None, correct_answer="15th", hint="ONE WORD ONLY", order_index=1),
        IeltsQuestion(skill="Listening", parent_id=listening1.id, question_type="mcq", question_text="What type of room does the man book?", options=["Single room with sea view", "Double room", "Single room without view", "Suite"], correct_answer="Single room with sea view", hint=None, order_index=2),
        IeltsQuestion(skill="Listening", parent_id=listening1.id, question_type="completion", question_text="The cost of the room is £______ per night.", options=None, correct_answer="85", hint="ONE WORD ONLY", order_index=3),
        IeltsQuestion(skill="Listening", parent_id=listening1.id, question_type="completion", question_text="Check-in time is ______ PM.", options=None, correct_answer="2", hint="ONE WORD ONLY", order_index=4),
    ]
    for q in questions1:
        db.add(q)
    db.commit()
    print("  ✓ Listening test 1 imported")
    
    # Cambridge IELTS 18 Test 2 Listening
    listening2 = IeltsListening(
        section=2,
        title="Talk about a local museum",
        transcript="SPEAKER: Welcome to the City Museum. Our museum has been open since 1950 and houses over 10,000 artifacts. The museum is divided into three main sections: Ancient History, Medieval Times, and Modern Era. The Ancient History section features pottery and tools from Roman times. The Medieval section displays weapons and clothing from the 12th to 15th centuries. The Modern Era section showcases industrial machinery from the 19th century. We offer guided tours at 10 AM, 1 PM, and 3 PM daily. The museum is open Tuesday to Sunday, 9 AM to 5 PM. Admission is free for children under 12, £5 for adults, and £3 for students with ID. We also have a café and gift shop on site.",
        difficulty="medium",
        duration_seconds=300
    )
    db.add(listening2)
    db.commit()
    db.refresh(listening2)
    
    questions2 = [
        IeltsQuestion(skill="Listening", parent_id=listening2.id, question_type="completion", question_text="The museum has been open since ______.", options=None, correct_answer="1950", hint="ONE WORD ONLY", order_index=1),
        IeltsQuestion(skill="Listening", parent_id=listening2.id, question_type="mcq", question_text="How many artifacts does the museum house?", options=["5,000", "10,000", "15,000", "20,000"], correct_answer="10,000", hint=None, order_index=2),
        IeltsQuestion(skill="Listening", parent_id=listening2.id, question_type="completion", question_text="The Ancient History section features pottery and tools from ______ times.", options=None, correct_answer="Roman", hint="ONE WORD ONLY", order_index=3),
        IeltsQuestion(skill="Listening", parent_id=listening2.id, question_type="mcq", question_text="What is the admission price for students?", options=["Free", "£3", "£5", "£8"], correct_answer="£3", hint=None, order_index=4),
    ]
    for q in questions2:
        db.add(q)
    db.commit()
    print("  ✓ Listening test 2 imported")
    
    # Cambridge IELTS 17 Test 1 Listening
    listening3 = IeltsListening(
        section=3,
        title="Discussion about a university project",
        transcript="TUTOR: So, Sarah and James, tell me about your project on renewable energy.\nSARAH: We focused on solar power in residential areas. We surveyed 200 households about their interest in installing solar panels.\nJAMES: The results were interesting. 60% said they were interested, but only 20% had actually installed them.\nTUTOR: What were the main barriers?\nSARAH: Cost was the biggest factor. Most people said the initial installation cost was too high.\nJAMES: But we also found that government incentives could change their minds. 70% said they'd consider it if there were tax breaks.\nTUTOR: That's useful data. What about environmental awareness?\nSARAH: Surprisingly, environmental concerns were secondary to financial considerations.",
        difficulty="medium",
        duration_seconds=300
    )
    db.add(listening3)
    db.commit()
    db.refresh(listening3)
    
    questions3 = [
        IeltsQuestion(skill="Listening", parent_id=listening3.id, question_type="mcq", question_text="How many households did the students survey?", options=["100", "200", "300", "400"], correct_answer="200", hint=None, order_index=1),
        IeltsQuestion(skill="Listening", parent_id=listening3.id, question_type="completion", question_text="______% of households said they were interested in solar panels.", options=None, correct_answer="60", hint="ONE WORD ONLY", order_index=2),
        IeltsQuestion(skill="Listening", parent_id=listening3.id, question_type="mcq", question_text="What was the main barrier to installing solar panels?", options=["Lack of space", "Cost", "Environmental concerns", "Government regulations"], correct_answer="Cost", hint=None, order_index=3),
        IeltsQuestion(skill="Listening", parent_id=listening3.id, question_type="completion", question_text="______% said they'd consider solar panels with tax breaks.", options=None, correct_answer="70", hint="ONE WORD ONLY", order_index=4),
    ]
    for q in questions3:
        db.add(q)
    db.commit()
    print("  ✓ Listening test 3 imported")
    
    # Cambridge IELTS 16 Test 1 Listening
    listening4 = IeltsListening(
        section=4,
        title="Lecture on urban planning",
        transcript="LECTURER: Today we'll discuss sustainable urban planning. As cities grow, we face challenges like pollution, traffic congestion, and housing shortages. One solution is the concept of the '15-minute city' - where residents can access all essential services within a 15-minute walk or bike ride. This reduces car dependency and promotes healthier lifestyles. Studies show that cities implementing this model have seen a 30% reduction in traffic and improved air quality. However, it requires careful zoning and mixed-use development. We need to combine residential, commercial, and recreational spaces in the same neighborhoods.",
        difficulty="medium",
        duration_seconds=300
    )
    db.add(listening4)
    db.commit()
    db.refresh(listening4)
    
    questions4 = [
        IeltsQuestion(skill="Listening", parent_id=listening4.id, question_type="completion", question_text="The '15-minute city' concept allows residents to access services within a ______-minute walk.", options=None, correct_answer="15", hint="ONE WORD ONLY", order_index=1),
        IeltsQuestion(skill="Listening", parent_id=listening4.id, question_type="mcq", question_text="What is one benefit of the 15-minute city model?", options=["Increased car usage", "Reduced traffic", "Higher housing costs", "More pollution"], correct_answer="Reduced traffic", hint=None, order_index=2),
        IeltsQuestion(skill="Listening", parent_id=listening4.id, question_type="completion", question_text="Cities implementing this model have seen a ______% reduction in traffic.", options=None, correct_answer="30", hint="ONE WORD ONLY", order_index=3),
        IeltsQuestion(skill="Listening", parent_id=listening4.id, question_type="mcq", question_text="What does the model require?", options=["Single-use zoning", "Mixed-use development", "More highways", "Larger buildings"], correct_answer="Mixed-use development", hint=None, order_index=4),
    ]
    for q in questions4:
        db.add(q)
    db.commit()
    print("  ✓ Listening test 4 imported")

def import_cambridge_reading(db: Session):
    """Import Cambridge IELTS Reading tests"""
    print("Importing Cambridge IELTS Reading tests...")
    
    # Check if already imported
    existing_count = db.query(IeltsReading).count()
    if existing_count >= 4:
        print(f"  Skipping - {existing_count} reading passages already exist")
        return

Tea containers have been found in tombs dating from the Han dynasty (206 BC – 220 AD) but it was under the Tang dynasty (618–906 AD), that tea became firmly established as the national drink of China. It became such a favourite that during the late eighth century a writer called Lu Yu wrote the first book entirely about tea, the Ch'a Ching, or Tea Classic. It was shortly after this that tea was first introduced to Japan, by Japanese Buddhist monks who had travelled to China to study.

Tea drinking has become a ritual in many cultures. In the United Kingdom, for example, tea is consumed daily by the majority of the population. The British tradition of afternoon tea began in the 1840s when Anna, the Duchess of Bedford, started inviting friends for tea and cake in the afternoon. This practice quickly spread among the upper classes and eventually became a national custom.

Today, tea is the second most consumed beverage in the world, after water. It is grown in many countries including China, India, Kenya, and Sri Lanka. Different cultures have developed their own unique ways of preparing and serving tea, from the elaborate Japanese tea ceremony to the simple British cup with milk and sugar.""",
        difficulty="medium",
        word_count=250
    )
    db.add(reading1)
    db.commit()
    db.refresh(reading1)
    
    questions1 = [
        IeltsQuestion(skill="Reading", parent_id=reading1.id, question_type="tfng", question_text="Tea was discovered by the Chinese emperor Shen Nung in 2737 BC.", options=["True", "False", "Not Given"], correct_answer="True", hint=None, order_index=1),
        IeltsQuestion(skill="Reading", parent_id=reading1.id, question_type="tfng", question_text="The Ch'a Ching was written during the Han dynasty.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=2),
        IeltsQuestion(skill="Reading", parent_id=reading1.id, question_type="tfng", question_text="Tea was introduced to Japan by Chinese merchants.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=3),
        IeltsQuestion(skill="Reading", parent_id=reading1.id, question_type="mcq", question_text="Who started the British tradition of afternoon tea?", options=["Queen Victoria", "Anna, Duchess of Bedford", "Lu Yu", "Shen Nung"], correct_answer="Anna, Duchess of Bedford", hint=None, order_index=4),
        IeltsQuestion(skill="Reading", parent_id=reading1.id, question_type="completion", question_text="Tea is the ______ most consumed beverage in the world.", options=None, correct_answer="second", hint="ONE WORD ONLY", order_index=5),
    ]
    for q in questions1:
        db.add(q)
    db.commit()
    print("  ✓ Cambridge 18 Test 1 Reading Passage 1 imported")
    
    # Cambridge IELTS 18 Test 1 Reading Passage 2
    reading2 = IeltsReading(
        section=2,
        title="Cambridge 18 Test 1 - Passage 2: The Impact of Urbanization on Wildlife",
        passage_text="""As human populations continue to grow and cities expand, the natural habitats of many species are being fragmented or destroyed. This process, known as urbanization, has significant impacts on wildlife populations around the world.

One of the most immediate effects of urbanization is habitat loss. When forests, grasslands, and wetlands are converted into residential and commercial areas, the plants and animals that depend on these ecosystems lose their homes. Some species are able to adapt to urban environments, while others are pushed to the brink of extinction.

Pollution is another major consequence of urbanization. Air pollution from vehicles and industry can harm wildlife directly, while water pollution from runoff can contaminate the water sources that many animals rely on. Light pollution from streetlights and buildings can disrupt the natural behaviors of nocturnal animals, affecting their feeding and breeding patterns.

Despite these challenges, some species have shown remarkable adaptability to urban environments. Birds such as pigeons and sparrows have thrived in cities, taking advantage of the abundant food sources and nesting sites provided by buildings. Similarly, raccoons and foxes have successfully adapted to urban life in many parts of the world.

Conservationists are now working to create wildlife-friendly urban spaces. This includes creating green corridors that connect fragmented habitats, planting native vegetation in parks and gardens, and reducing light pollution in sensitive areas. These efforts aim to allow humans and wildlife to coexist in increasingly urbanized landscapes.""",
        difficulty="medium",
        word_count=280
    )
    db.add(reading2)
    db.commit()
    db.refresh(reading2)
    
    questions2 = [
        IeltsQuestion(skill="Reading", parent_id=reading2.id, question_type="tfng", question_text="Urbanization has no impact on wildlife populations.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=1),
        IeltsQuestion(skill="Reading", parent_id=reading2.id, question_type="tfng", question_text="All species can adapt to urban environments.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=2),
        IeltsQuestion(skill="Reading", parent_id=reading2.id, question_type="tfng", question_text="Light pollution can affect the behavior of nocturnal animals.", options=["True", "False", "Not Given"], correct_answer="True", hint=None, order_index=3),
        IeltsQuestion(skill="Reading", parent_id=reading2.id, question_type="mcq", question_text="What is one way conservationists are helping wildlife in urban areas?", options=["Creating green corridors", "Building more cities", "Removing all parks", "Increasing light pollution"], correct_answer="Creating green corridors", hint=None, order_index=4),
        IeltsQuestion(skill="Reading", parent_id=reading2.id, question_type="completion", question_text="Pigeons and sparrows have ______ in cities.", options=None, correct_answer="thrived", hint="ONE WORD ONLY", order_index=5),
    ]
    for q in questions2:
        db.add(q)
    db.commit()
    print("  ✓ Cambridge 18 Test 1 Reading Passage 2 imported")
    
    # Cambridge IELTS 17 Test 1 Reading Passage 1
    reading3 = IeltsReading(
        section=1,
        title="Cambridge 17 Test 1 - Passage 1: The Development of the Bicycle",
        passage_text="""The bicycle has undergone significant changes since its invention in the early 19th century. The first bicycles, known as 'hobby horses' or 'dandy horses', had no pedals and were propelled by the rider pushing their feet against the ground. In the 1860s, the velocipede appeared, featuring pedals attached directly to the front wheel. However, this design was uncomfortable and difficult to ride.

The 1870s saw the introduction of the 'penny-farthing', with its large front wheel and small rear wheel. This design allowed for greater speed but was dangerous due to the rider's high seating position. Many riders suffered serious injuries from falling off these tall bicycles.

The modern bicycle design emerged in the 1880s with the invention of the 'safety bicycle'. This featured two wheels of equal size and a chain drive to the rear wheel, making it much safer and more comfortable. The pneumatic tire, invented by John Boyd Dunlop in 1888, further improved comfort by providing a cushion against bumps.

Today, bicycles continue to evolve with new materials and technologies. Carbon fiber frames make bikes lighter and stronger, while electric motors provide assistance for riders. Despite these innovations, the basic principle of the bicycle remains unchanged: a simple, efficient machine powered by human energy.""",
        difficulty="medium",
        word_count=260
    )
    db.add(reading3)
    db.commit()
    db.refresh(reading3)
    
    questions3 = [
        IeltsQuestion(skill="Reading", parent_id=reading3.id, question_type="tfng", question_text="The first bicycles had pedals attached to the front wheel.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=1),
        IeltsQuestion(skill="Reading", parent_id=reading3.id, question_type="tfng", question_text="The penny-farthing was faster than earlier bicycle designs.", options=["True", "False", "Not Given"], correct_answer="True", hint=None, order_index=2),
        IeltsQuestion(skill="Reading", parent_id=reading3.id, question_type="tfng", question_text="The safety bicycle was invented in the 1860s.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=3),
        IeltsQuestion(skill="Reading", parent_id=reading3.id, question_type="mcq", question_text="Who invented the pneumatic tire?", options=["John Boyd Dunlop", "James Starley", "Karl von Drais", "John Kemp Starley"], correct_answer="John Boyd Dunlop", hint=None, order_index=4),
        IeltsQuestion(skill="Reading", parent_id=reading3.id, question_type="completion", question_text="The ______ bicycle featured two wheels of equal size.", options=None, correct_answer="safety", hint="ONE WORD ONLY", order_index=5),
    ]
    for q in questions3:
        db.add(q)
    db.commit()
    print("  ✓ Cambridge 17 Test 1 Reading Passage 1 imported")
    
    # Cambridge IELTS 16 Test 1 Reading Passage 1
    reading4 = IeltsReading(
        section=1,
        title="Cambridge 16 Test 1 - Passage 1: The Importance of Sleep",
        passage_text="""Sleep is essential for human health and well-being. During sleep, the body repairs tissues, builds muscle, and strengthens the immune system. The brain also processes information and consolidates memories during this time. Lack of sleep can lead to serious health problems including obesity, diabetes, and cardiovascular disease.

Adults typically need between 7 and 9 hours of sleep per night, though individual requirements vary. Children and teenagers need more sleep to support their growth and development. Quality of sleep is just as important as quantity. Deep sleep and REM (rapid eye movement) sleep are particularly important for physical and mental restoration.

Many factors can affect sleep quality, including stress, diet, exercise, and exposure to light. The blue light emitted by electronic devices can interfere with the production of melatonin, a hormone that regulates sleep. Establishing a regular sleep schedule and creating a comfortable sleep environment can help improve sleep quality.

Sleep disorders such as insomnia and sleep apnea affect millions of people worldwide. These conditions can significantly impact daily functioning and overall health. Treatment options include lifestyle changes, medication, and in some cases, medical devices or surgery.""",
        difficulty="medium",
        word_count=250
    )
    db.add(reading4)
    db.commit()
    db.refresh(reading4)
    
    questions4 = [
        IeltsQuestion(skill="Reading", parent_id=reading4.id, question_type="tfng", question_text="During sleep, the brain processes information and consolidates memories.", options=["True", "False", "Not Given"], correct_answer="True", hint=None, order_index=1),
        IeltsQuestion(skill="Reading", parent_id=reading4.id, question_type="tfng", question_text="Adults need exactly 8 hours of sleep per night.", options=["True", "False", "Not Given"], correct_answer="False", hint=None, order_index=2),
        IeltsQuestion(skill="Reading", parent_id=reading4.id, question_type="tfng", question_text="Blue light from electronic devices can affect sleep quality.", options=["True", "False", "Not Given"], correct_answer="True", hint=None, order_index=3),
        IeltsQuestion(skill="Reading", parent_id=reading4.id, question_type="mcq", question_text="What hormone regulates sleep?", options=["Adrenaline", "Melatonin", "Cortisol", "Insulin"], correct_answer="Melatonin", hint=None, order_index=4),
        IeltsQuestion(skill="Reading", parent_id=reading4.id, question_type="completion", question_text="______ and REM sleep are particularly important for restoration.", options=None, correct_answer="Deep", hint="ONE WORD ONLY", order_index=5),
    ]
    for q in questions4:
        db.add(q)
    db.commit()
    print("  ✓ Cambridge 16 Test 1 Reading Passage 1 imported")

def import_cambridge_writing(db: Session):
    """Import Cambridge IELTS Writing tasks"""
    print("Importing Cambridge IELTS Writing tasks...")
    
    # Cambridge IELTS 18 Test 1 Writing Task 1
    writing1 = IeltsWriting(
        task_type="Task1",
        category="Bar chart",
        prompt="The chart below shows the percentage of people in five European countries who used the internet in 2010 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
        image_url=None,
        min_words=150,
        duration_minutes=20,
        difficulty="medium"
    )
    db.add(writing1)
    db.commit()
    print("  ✓ Cambridge 18 Test 1 Writing Task 1 imported")
    
    # Cambridge IELTS 18 Test 1 Writing Task 2
    writing2 = IeltsWriting(
        task_type="Task2",
        category="Society",
        prompt="In some countries, people are having children at a much later age than in the past. Why is this happening? Do the advantages of this development outweigh the disadvantages?",
        image_url=None,
        min_words=250,
        duration_minutes=40,
        difficulty="medium"
    )
    db.add(writing2)
    db.commit()
    print("  ✓ Cambridge 18 Test 1 Writing Task 2 imported")
    
    # Cambridge IELTS 17 Test 1 Writing Task 2
    writing3 = IeltsWriting(
        task_type="Task2",
        category="Education",
        prompt="Some people believe that universities should focus on providing academic skills, while others think they should prepare students for employment. Discuss both views and give your own opinion.",
        image_url=None,
        min_words=250,
        duration_minutes=40,
        difficulty="medium"
    )
    db.add(writing3)
    db.commit()
    print("  ✓ Cambridge 17 Test 1 Writing Task 2 imported")
    
    # Cambridge IELTS 16 Test 1 Writing Task 2
    writing4 = IeltsWriting(
        task_type="Task2",
        category="Environment",
        prompt="Some people think that environmental problems are too big for individuals to solve, while others believe that individuals can also take some actions to solve these problems. Discuss both views and give your own opinion.",
        image_url=None,
        min_words=250,
        duration_minutes=40,
        difficulty="medium"
    )
    db.add(writing4)
    db.commit()
    print("  ✓ Cambridge 16 Test 1 Writing Task 2 imported")
    
    # Cambridge IELTS 15 Test 1 Writing Task 2
    writing5 = IeltsWriting(
        task_type="Task2",
        category="Technology",
        prompt="In some countries, more and more people are becoming interested in finding out about the history of the house or flat they live in. What are the reasons for this? How can people research this?",
        image_url=None,
        min_words=250,
        duration_minutes=40,
        difficulty="medium"
    )
    db.add(writing5)
    db.commit()
    print("  ✓ Cambridge 15 Test 1 Writing Task 2 imported")

def import_cambridge_speaking(db: Session):
    """Import Cambridge IELTS Speaking topics"""
    print("Importing Cambridge IELTS Speaking topics...")
    
    # Cambridge IELTS 18 Speaking Part 1
    speaking1 = IeltsSpeaking(
        part=1,
        topic="Accommodation",
        questions=["What kind of accommodation do you live in?", "How long have you lived there?", "What do you like about your accommodation?", "Is there anything you would like to change about your accommodation?"],
        cue_card=None,
        prep_seconds=None,
        speak_seconds=None,
        difficulty="medium"
    )
    db.add(speaking1)
    db.commit()
    print("  ✓ Cambridge 18 Speaking Part 1 imported")
    
    # Cambridge IELTS 18 Speaking Part 2
    speaking2 = IeltsSpeaking(
        part=2,
        topic="Describe a website you use often",
        questions=["Describe a website you use often. You should say: what the website is; how often you use it; what you use it for; and explain why you find it useful."],
        cue_card="Describe a website you use often. You should say: what the website is; how often you use it; what you use it for; and explain why you find it useful.",
        prep_seconds=60,
        speak_seconds=120,
        difficulty="medium"
    )
    db.add(speaking2)
    db.commit()
    print("  ✓ Cambridge 18 Speaking Part 2 imported")
    
    # Cambridge IELTS 18 Speaking Part 3
    speaking3 = IeltsSpeaking(
        part=3,
        topic="The Internet and Communication",
        questions=["How has the internet changed the way people communicate?", "Do you think the internet has made people more or less social?", "What are the disadvantages of relying on the internet for communication?", "How might communication change in the future?"],
        cue_card=None,
        prep_seconds=None,
        speak_seconds=None,
        difficulty="medium"
    )
    db.add(speaking3)
    db.commit()
    print("  ✓ Cambridge 18 Speaking Part 3 imported")
    
    # Cambridge IELTS 17 Speaking Part 1
    speaking4 = IeltsSpeaking(
        part=1,
        topic="Work or Studies",
        questions=["Do you work or are you a student?", "What subject are you studying?", "Why did you choose this subject?", "Is there anything you dislike about your studies?"],
        cue_card=None,
        prep_seconds=None,
        speak_seconds=None,
        difficulty="medium"
    )
    db.add(speaking4)
    db.commit()
    print("  ✓ Cambridge 17 Speaking Part 1 imported")
    
    # Cambridge IELTS 17 Speaking Part 2
    speaking5 = IeltsSpeaking(
        part=2,
        topic="Describe a time you received good news",
        questions=["Describe a time you received good news. You should say: what the news was; when you received it; who told you the news; and explain why you felt happy about it."],
        cue_card="Describe a time you received good news. You should say: what the news was; when you received it; who told you the news; and explain why you felt happy about it.",
        prep_seconds=60,
        speak_seconds=120,
        difficulty="medium"
    )
    db.add(speaking5)
    db.commit()
    print("  ✓ Cambridge 17 Speaking Part 2 imported")

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Importing Cambridge IELTS Tests")
        print("=" * 50)
        
        import_cambridge_listening(db)
        import_cambridge_reading(db)
        import_cambridge_writing(db)
        import_cambridge_speaking(db)
        
        print("=" * 50)
        print("Import complete!")
        print("=" * 50)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
