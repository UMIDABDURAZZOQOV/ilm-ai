"""
skilltree_taxonomy.py -- hand-authored unit/lesson structure for the Milliy
Sertifikat skill tree (structure only, no question content -- mirrors
sat_taxonomy.py's style). scripts/seed_skilltree.py reads this to create the
SkillSubject/SkillUnit/SkillLesson/SkillLessonPrerequisite rows, then calls
Gemini per lesson to generate the actual question content.

This breakdown is a reasonable first pass at the real DTM/Milliy Sertifikat
syllabus for these two subjects -- worth a review pass by a subject-matter
reviewer before the generated question fixtures are treated as final.
"""

SKILLTREE_OUTLINE = {
    "ona_tili": {
        "name": {"uz": "Ona tili", "ru": "Родной язык", "en": "Native Language"},
        "icon": "book-open",
        "color": "#58CC02",
        "units": [
            {
                "slug": "fonetika",
                "title": {"uz": "Fonetika", "ru": "Фонетика", "en": "Phonetics"},
                "lessons": [
                    {"slug": "unli-undosh", "title": {"uz": "Unli va undosh tovushlar", "ru": "Гласные и согласные звуки", "en": "Vowels and consonants"}},
                    {"slug": "bogin", "title": {"uz": "Bo'g'in va bo'g'in ko'chirish", "ru": "Слоги и перенос слов", "en": "Syllables and hyphenation"}},
                    {"slug": "urgu", "title": {"uz": "Urg'u", "ru": "Ударение", "en": "Stress"}},
                    {"slug": "fonetik-hodisalar", "title": {"uz": "Fonetik hodisalar", "ru": "Фонетические явления", "en": "Phonetic processes"}},
                ],
            },
            {
                "slug": "leksikologiya",
                "title": {"uz": "Leksikologiya", "ru": "Лексикология", "en": "Lexicology"},
                "lessons": [
                    {"slug": "sinonim-antonim", "title": {"uz": "Sinonim, antonim, omonim", "ru": "Синонимы, антонимы, омонимы", "en": "Synonyms, antonyms, homonyms"}},
                    {"slug": "sozning-manosi", "title": {"uz": "So'zning ma'no turlari", "ru": "Значения слова", "en": "Word meanings"}},
                    {"slug": "frazeologizm", "title": {"uz": "Frazeologizmlar", "ru": "Фразеологизмы", "en": "Idioms"}},
                    {"slug": "sozlar-kelib-chiqishi", "title": {"uz": "So'zlarning kelib chiqishi", "ru": "Происхождение слов", "en": "Word origins"}},
                ],
            },
            {
                "slug": "morfologiya",
                "title": {"uz": "Morfologiya", "ru": "Морфология", "en": "Morphology"},
                "lessons": [
                    {"slug": "ot", "title": {"uz": "Ot so'z turkumi", "ru": "Имя существительное", "en": "Nouns"}},
                    {"slug": "sifat-son", "title": {"uz": "Sifat va son", "ru": "Прилагательное и числительное", "en": "Adjectives and numerals"}},
                    {"slug": "olmosh", "title": {"uz": "Olmosh", "ru": "Местоимение", "en": "Pronouns"}},
                    {"slug": "fel", "title": {"uz": "Fe'l", "ru": "Глагол", "en": "Verbs"}},
                    {"slug": "yordamchi-sozlar", "title": {"uz": "Yordamchi so'z turkumlari", "ru": "Служебные части речи", "en": "Function words"}},
                ],
            },
            {
                "slug": "sintaksis",
                "title": {"uz": "Sintaksis", "ru": "Синтаксис", "en": "Syntax"},
                "lessons": [
                    {"slug": "gap-bolaklari", "title": {"uz": "Gap bo'laklari", "ru": "Члены предложения", "en": "Sentence parts"}},
                    {"slug": "sodda-gap", "title": {"uz": "Sodda gap turlari", "ru": "Простое предложение", "en": "Simple sentences"}},
                    {"slug": "qoshma-gap", "title": {"uz": "Qo'shma gap", "ru": "Сложное предложение", "en": "Complex sentences"}},
                    {"slug": "gap-uzuvlari", "title": {"uz": "Uyushiq bo'laklar, kirish so'z", "ru": "Однородные члены, вводные слова", "en": "Coordinated parts, parenthetical words"}},
                ],
            },
            {
                "slug": "imlo-qoidalari",
                "title": {"uz": "Imlo qoidalari", "ru": "Правила орфографии", "en": "Spelling rules"},
                "lessons": [
                    {"slug": "qoshma-sozlar-imlosi", "title": {"uz": "Qo'shma so'zlar imlosi", "ru": "Правописание сложных слов", "en": "Spelling compound words"}},
                    {"slug": "qoshimcha-imlosi", "title": {"uz": "Qo'shimchalar imlosi", "ru": "Правописание суффиксов", "en": "Spelling suffixes"}},
                    {"slug": "bosh-harf", "title": {"uz": "Bosh harf bilan yozish", "ru": "Написание с большой буквы", "en": "Capitalization"}},
                    {"slug": "imlo-istisnolar", "title": {"uz": "Imlo qoidalaridagi istisnolar", "ru": "Исключения в орфографии", "en": "Spelling exceptions"}},
                ],
            },
            {
                "slug": "tinish-belgilari",
                "title": {"uz": "Tinish belgilari", "ru": "Знаки препинания", "en": "Punctuation"},
                "lessons": [
                    {"slug": "vergul", "title": {"uz": "Vergul qo'yish qoidalari", "ru": "Правила постановки запятой", "en": "Comma rules"}},
                    {"slug": "qoshma-gapda-tinish", "title": {"uz": "Qo'shma gapda tinish belgilari", "ru": "Пунктуация в сложном предложении", "en": "Punctuation in complex sentences"}},
                    {"slug": "kochirma-gap", "title": {"uz": "Ko'chirma gap va tinish belgilari", "ru": "Прямая речь и пунктуация", "en": "Direct speech punctuation"}},
                ],
            },
            {
                "slug": "nutq-madaniyati",
                "title": {"uz": "Nutq madaniyati va uslubiyat", "ru": "Культура речи и стилистика", "en": "Speech culture and stylistics"},
                "lessons": [
                    {"slug": "nutq-uslublari", "title": {"uz": "Nutq uslublari", "ru": "Стили речи", "en": "Speech styles"}},
                    {"slug": "matn-turlari", "title": {"uz": "Matn turlari", "ru": "Типы текста", "en": "Text types"}},
                    {"slug": "nutq-xatolari", "title": {"uz": "Nutqiy xatolar", "ru": "Речевые ошибки", "en": "Common speech errors"}},
                ],
            },
        ],
    },
    "matematika": {
        "name": {"uz": "Matematika", "ru": "Математика", "en": "Mathematics"},
        "icon": "calculator",
        "color": "#FF9600",
        "units": [
            {
                "slug": "sonlar-amallar",
                "title": {"uz": "Sonlar va amallar", "ru": "Числа и действия", "en": "Numbers and operations"},
                "lessons": [
                    {"slug": "natural-butun-sonlar", "title": {"uz": "Natural va butun sonlar", "ru": "Натуральные и целые числа", "en": "Natural and whole numbers"}},
                    {"slug": "oddiy-onli-kasrlar", "title": {"uz": "Oddiy va o'nli kasrlar", "ru": "Обыкновенные и десятичные дроби", "en": "Fractions and decimals"}},
                    {"slug": "foizlar", "title": {"uz": "Foizlar", "ru": "Проценты", "en": "Percentages"}},
                    {"slug": "nisbat-proporsiya", "title": {"uz": "Nisbat va proporsiya", "ru": "Отношения и пропорции", "en": "Ratios and proportions"}},
                ],
            },
            {
                "slug": "algebraik-ifodalar",
                "title": {"uz": "Algebraik ifodalar", "ru": "Алгебраические выражения", "en": "Algebraic expressions"},
                "lessons": [
                    {"slug": "darajalar-ildizlar", "title": {"uz": "Darajalar va ildizlar", "ru": "Степени и корни", "en": "Powers and roots"}},
                    {"slug": "kophadlar", "title": {"uz": "Ko'phadlar ustida amallar", "ru": "Действия с многочленами", "en": "Operations with polynomials"}},
                    {"slug": "qisqa-kopaytirish", "title": {"uz": "Qisqa ko'paytirish formulalari", "ru": "Формулы сокращённого умножения", "en": "Special products"}},
                    {"slug": "kasr-ratsional-ifodalar", "title": {"uz": "Kasr-ratsional ifodalar", "ru": "Рациональные выражения", "en": "Rational expressions"}},
                ],
            },
            {
                "slug": "tenglamalar",
                "title": {"uz": "Tenglamalar", "ru": "Уравнения", "en": "Equations"},
                "lessons": [
                    {"slug": "chiziqli-tenglamalar", "title": {"uz": "Chiziqli tenglamalar", "ru": "Линейные уравнения", "en": "Linear equations"}},
                    {"slug": "kvadrat-tenglamalar", "title": {"uz": "Kvadrat tenglamalar", "ru": "Квадратные уравнения", "en": "Quadratic equations"}},
                    {"slug": "tenglamalar-sistemasi", "title": {"uz": "Tenglamalar sistemasi", "ru": "Системы уравнений", "en": "Systems of equations"}},
                    {"slug": "matnli-masalalar", "title": {"uz": "Matnli masalalar", "ru": "Текстовые задачи", "en": "Word problems"}},
                ],
            },
            {
                "slug": "tengsizliklar-funksiyalar",
                "title": {"uz": "Tengsizliklar va funksiyalar", "ru": "Неравенства и функции", "en": "Inequalities and functions"},
                "lessons": [
                    {"slug": "chiziqli-tengsizliklar", "title": {"uz": "Chiziqli tengsizliklar", "ru": "Линейные неравенства", "en": "Linear inequalities"}},
                    {"slug": "kvadrat-tengsizliklar", "title": {"uz": "Kvadrat tengsizliklar", "ru": "Квадратные неравенства", "en": "Quadratic inequalities"}},
                    {"slug": "funksiya-grafigi", "title": {"uz": "Funksiya va uning grafigi", "ru": "Функция и её график", "en": "Functions and graphs"}},
                    {"slug": "progressiyalar", "title": {"uz": "Arifmetik va geometrik progressiya", "ru": "Арифметическая и геометрическая прогрессии", "en": "Arithmetic and geometric progressions"}},
                ],
            },
            {
                "slug": "geometriya-planimetriya",
                "title": {"uz": "Planimetriya", "ru": "Планиметрия", "en": "Plane geometry"},
                "lessons": [
                    {"slug": "uchburchaklar", "title": {"uz": "Uchburchaklar", "ru": "Треугольники", "en": "Triangles"}},
                    {"slug": "tortburchaklar", "title": {"uz": "To'rtburchaklar", "ru": "Четырёхугольники", "en": "Quadrilaterals"}},
                    {"slug": "aylana-doira", "title": {"uz": "Aylana va doira", "ru": "Окружность и круг", "en": "Circles"}},
                    {"slug": "yuza-perimetr", "title": {"uz": "Yuza va perimetr", "ru": "Площадь и периметр", "en": "Area and perimeter"}},
                ],
            },
            {
                "slug": "geometriya-stereometriya",
                "title": {"uz": "Stereometriya", "ru": "Стереометрия", "en": "Solid geometry"},
                "lessons": [
                    {"slug": "prizma-parallelepiped", "title": {"uz": "Prizma va parallelepiped", "ru": "Призма и параллелепипед", "en": "Prisms"}},
                    {"slug": "piramida-konus", "title": {"uz": "Piramida va konus", "ru": "Пирамида и конус", "en": "Pyramids and cones"}},
                    {"slug": "silindr-shar", "title": {"uz": "Silindr va shar", "ru": "Цилиндр и шар", "en": "Cylinders and spheres"}},
                ],
            },
            {
                "slug": "statistika-ehtimollik",
                "title": {"uz": "Statistika va ehtimollik", "ru": "Статистика и вероятность", "en": "Statistics and probability"},
                "lessons": [
                    {"slug": "ortacha-qiymatlar", "title": {"uz": "O'rtacha qiymatlar", "ru": "Средние значения", "en": "Averages"}},
                    {"slug": "ehtimollik-asoslari", "title": {"uz": "Ehtimollik asoslari", "ru": "Основы вероятности", "en": "Basic probability"}},
                    {"slug": "kombinatorika", "title": {"uz": "Kombinatorika elementlari", "ru": "Элементы комбинаторики", "en": "Combinatorics"}},
                ],
            },
        ],
    },
    "ingliz_tili": {
        "name": {"uz": "Ingliz tili", "ru": "Английский язык", "en": "English"},
        "icon": "languages",
        "color": "#CE82FF",
        "units": [
            {
                "slug": "parts-of-speech",
                "title": {"uz": "So'z turkumlari", "ru": "Части речи", "en": "Parts of speech"},
                "lessons": [
                    {"slug": "nouns-articles", "title": {"uz": "Otlar va artikllar (a/an/the)", "ru": "Существительные и артикли", "en": "Nouns and articles"}},
                    {"slug": "pronouns", "title": {"uz": "Olmoshlar", "ru": "Местоимения", "en": "Pronouns"}},
                    {"slug": "adjectives-adverbs", "title": {"uz": "Sifat va ravishlar", "ru": "Прилагательные и наречия", "en": "Adjectives and adverbs"}},
                    {"slug": "prepositions", "title": {"uz": "Predloglar", "ru": "Предлоги", "en": "Prepositions"}},
                ],
            },
            {
                "slug": "tenses-present-past",
                "title": {"uz": "Hozirgi va o'tgan zamonlar", "ru": "Настоящее и прошедшее время", "en": "Present and past tenses"},
                "lessons": [
                    {"slug": "present-simple-continuous", "title": {"uz": "Present Simple va Continuous", "ru": "Present Simple и Continuous", "en": "Present Simple and Continuous"}},
                    {"slug": "past-simple-continuous", "title": {"uz": "Past Simple va Continuous", "ru": "Past Simple и Continuous", "en": "Past Simple and Continuous"}},
                    {"slug": "present-perfect", "title": {"uz": "Present Perfect", "ru": "Present Perfect", "en": "Present Perfect"}},
                    {"slug": "past-perfect", "title": {"uz": "Past Perfect", "ru": "Past Perfect", "en": "Past Perfect"}},
                ],
            },
            {
                "slug": "tenses-future-modals",
                "title": {"uz": "Kelasi zamon va modal fe'llar", "ru": "Будущее время и модальные глаголы", "en": "Future and modals"},
                "lessons": [
                    {"slug": "future-forms", "title": {"uz": "Kelasi zamon shakllari (will/going to)", "ru": "Формы будущего времени", "en": "Future forms"}},
                    {"slug": "modal-verbs", "title": {"uz": "Modal fe'llar (can/must/should)", "ru": "Модальные глаголы", "en": "Modal verbs"}},
                    {"slug": "passive-voice", "title": {"uz": "Majhul nisbat (Passive Voice)", "ru": "Страдательный залог", "en": "Passive voice"}},
                ],
            },
            {
                "slug": "sentence-structure",
                "title": {"uz": "Gap tuzilishi", "ru": "Структура предложения", "en": "Sentence structure"},
                "lessons": [
                    {"slug": "questions-negatives", "title": {"uz": "So'roq va inkor gaplar", "ru": "Вопросы и отрицания", "en": "Questions and negatives"}},
                    {"slug": "conditionals", "title": {"uz": "Shart gaplar (Conditionals)", "ru": "Условные предложения", "en": "Conditionals"}},
                    {"slug": "reported-speech", "title": {"uz": "O'zlashtirma gap (Reported Speech)", "ru": "Косвенная речь", "en": "Reported speech"}},
                    {"slug": "relative-clauses", "title": {"uz": "Aniqlovchi ergash gaplar", "ru": "Определительные придаточные", "en": "Relative clauses"}},
                ],
            },
            {
                "slug": "vocabulary",
                "title": {"uz": "Lug'at boyligi", "ru": "Словарный запас", "en": "Vocabulary"},
                "lessons": [
                    {"slug": "common-verbs-collocations", "title": {"uz": "Ko'p ishlatiladigan fe'llar", "ru": "Частые глаголы и сочетания", "en": "Common verbs and collocations"}},
                    {"slug": "phrasal-verbs", "title": {"uz": "Frazeologik fe'llar (Phrasal Verbs)", "ru": "Фразовые глаголы", "en": "Phrasal verbs"}},
                    {"slug": "word-formation", "title": {"uz": "So'z yasalishi", "ru": "Словообразование", "en": "Word formation"}},
                    {"slug": "synonyms-antonyms-en", "title": {"uz": "Sinonim va antonimlar", "ru": "Синонимы и антонимы", "en": "Synonyms and antonyms"}},
                ],
            },
            {
                "slug": "reading-comprehension",
                "title": {"uz": "O'qib tushunish", "ru": "Понимание прочитанного", "en": "Reading comprehension"},
                "lessons": [
                    {"slug": "main-idea", "title": {"uz": "Asosiy g'oyani topish", "ru": "Определение главной мысли", "en": "Finding the main idea"}},
                    {"slug": "details-inference", "title": {"uz": "Tafsilotlar va xulosa chiqarish", "ru": "Детали и умозаключения", "en": "Details and inference"}},
                    {"slug": "context-vocabulary", "title": {"uz": "Kontekstdan so'z ma'nosini aniqlash", "ru": "Значение слова из контекста", "en": "Vocabulary in context"}},
                ],
            },
        ],
    },
    "biologiya": {
        "name": {"uz": "Biologiya", "ru": "Биология", "en": "Biology"},
        "icon": "leaf",
        "color": "#2FB344",
        "units": [
            {
                "slug": "sitologiya",
                "title": {"uz": "Sitologiya (hujayra)", "ru": "Цитология", "en": "Cytology"},
                "lessons": [
                    {"slug": "hujayra-tuzilishi", "title": {"uz": "Hujayra tuzilishi", "ru": "Строение клетки", "en": "Cell structure"}},
                    {"slug": "hujayra-organoidlari", "title": {"uz": "Hujayra organoidlari", "ru": "Органоиды клетки", "en": "Cell organelles"}},
                    {"slug": "hujayra-bolinishi", "title": {"uz": "Hujayra bo'linishi (mitoz, meyoz)", "ru": "Деление клетки", "en": "Cell division"}},
                    {"slug": "modda-almashinuvi", "title": {"uz": "Modda va energiya almashinuvi", "ru": "Обмен веществ", "en": "Metabolism"}},
                ],
            },
            {
                "slug": "botanika",
                "title": {"uz": "Botanika (o'simliklar)", "ru": "Ботаника", "en": "Botany"},
                "lessons": [
                    {"slug": "osimlik-organlari", "title": {"uz": "O'simlik organlari", "ru": "Органы растений", "en": "Plant organs"}},
                    {"slug": "fotosintez", "title": {"uz": "Fotosintez", "ru": "Фотосинтез", "en": "Photosynthesis"}},
                    {"slug": "osimliklar-kopayishi", "title": {"uz": "O'simliklarning ko'payishi", "ru": "Размножение растений", "en": "Plant reproduction"}},
                    {"slug": "osimliklar-sistematikasi", "title": {"uz": "O'simliklar sistematikasi", "ru": "Систематика растений", "en": "Plant classification"}},
                ],
            },
            {
                "slug": "zoologiya",
                "title": {"uz": "Zoologiya (hayvonlar)", "ru": "Зоология", "en": "Zoology"},
                "lessons": [
                    {"slug": "umurtqasizlar", "title": {"uz": "Umurtqasiz hayvonlar", "ru": "Беспозвоночные", "en": "Invertebrates"}},
                    {"slug": "umurtqalilar", "title": {"uz": "Umurtqali hayvonlar", "ru": "Позвоночные", "en": "Vertebrates"}},
                    {"slug": "hayvonlar-sistematikasi", "title": {"uz": "Hayvonlar sistematikasi", "ru": "Систематика животных", "en": "Animal classification"}},
                ],
            },
            {
                "slug": "odam-anatomiyasi",
                "title": {"uz": "Odam anatomiyasi", "ru": "Анатомия человека", "en": "Human anatomy"},
                "lessons": [
                    {"slug": "tayanch-harakat", "title": {"uz": "Tayanch-harakat sistemasi", "ru": "Опорно-двигательная система", "en": "Musculoskeletal system"}},
                    {"slug": "qon-aylanish", "title": {"uz": "Qon aylanish sistemasi", "ru": "Кровеносная система", "en": "Circulatory system"}},
                    {"slug": "nafas-ovqat-hazm", "title": {"uz": "Nafas va ovqat hazm qilish", "ru": "Дыхание и пищеварение", "en": "Respiration and digestion"}},
                    {"slug": "nerv-sezgi", "title": {"uz": "Nerv sistemasi va sezgi organlari", "ru": "Нервная система и органы чувств", "en": "Nervous system and senses"}},
                ],
            },
            {
                "slug": "genetika",
                "title": {"uz": "Genetika", "ru": "Генетика", "en": "Genetics"},
                "lessons": [
                    {"slug": "mendel-qonunlari", "title": {"uz": "Mendel qonunlari", "ru": "Законы Менделя", "en": "Mendel's laws"}},
                    {"slug": "irsiyat-ozgaruvchanlik", "title": {"uz": "Irsiyat va o'zgaruvchanlik", "ru": "Наследственность и изменчивость", "en": "Heredity and variation"}},
                    {"slug": "genetik-masalalar", "title": {"uz": "Genetik masalalar", "ru": "Генетические задачи", "en": "Genetics problems"}},
                ],
            },
            {
                "slug": "evolutsiya-ekologiya",
                "title": {"uz": "Evolutsiya va ekologiya", "ru": "Эволюция и экология", "en": "Evolution and ecology"},
                "lessons": [
                    {"slug": "evolutsiya-nazariyasi", "title": {"uz": "Evolutsion ta'limot", "ru": "Эволюционное учение", "en": "Theory of evolution"}},
                    {"slug": "ekologiya-asoslari", "title": {"uz": "Ekologiya asoslari", "ru": "Основы экологии", "en": "Basics of ecology"}},
                    {"slug": "biosfera", "title": {"uz": "Biosfera va uni muhofaza qilish", "ru": "Биосфера и её охрана", "en": "Biosphere and conservation"}},
                ],
            },
        ],
    },
    "kimyo": {
        "name": {"uz": "Kimyo", "ru": "Химия", "en": "Chemistry"},
        "icon": "flask",
        "color": "#E64980",
        "units": [
            {
                "slug": "atom-tuzilishi",
                "title": {"uz": "Atom tuzilishi", "ru": "Строение атома", "en": "Atomic structure"},
                "lessons": [
                    {"slug": "atom-molekula", "title": {"uz": "Atom va molekula", "ru": "Атом и молекула", "en": "Atoms and molecules"}},
                    {"slug": "atom-yadrosi-elektron", "title": {"uz": "Atom yadrosi va elektron qobiqlar", "ru": "Ядро и электронные оболочки", "en": "Nucleus and electron shells"}},
                    {"slug": "davriy-sistema", "title": {"uz": "Mendeleyev davriy sistemasi", "ru": "Периодическая система Менделеева", "en": "Periodic table"}},
                    {"slug": "kimyoviy-boglanish", "title": {"uz": "Kimyoviy bog'lanish", "ru": "Химическая связь", "en": "Chemical bonding"}},
                ],
            },
            {
                "slug": "kimyoviy-qonunlar",
                "title": {"uz": "Kimyoviy qonun va tushunchalar", "ru": "Химические законы и понятия", "en": "Chemical laws and concepts"},
                "lessons": [
                    {"slug": "kimyoviy-formulalar", "title": {"uz": "Kimyoviy formulalar va valentlik", "ru": "Химические формулы и валентность", "en": "Chemical formulas and valence"}},
                    {"slug": "mol-molyar-massa", "title": {"uz": "Mol va molyar massa", "ru": "Моль и молярная масса", "en": "Mole and molar mass"}},
                    {"slug": "kimyoviy-reaksiyalar", "title": {"uz": "Kimyoviy reaksiya turlari", "ru": "Типы химических реакций", "en": "Types of chemical reactions"}},
                    {"slug": "reaksiya-tenglamalari", "title": {"uz": "Reaksiya tenglamalarini tenglashtirish", "ru": "Уравнивание реакций", "en": "Balancing equations"}},
                ],
            },
            {
                "slug": "anorganik-birikmalar",
                "title": {"uz": "Anorganik birikmalar", "ru": "Неорганические соединения", "en": "Inorganic compounds"},
                "lessons": [
                    {"slug": "oksidlar", "title": {"uz": "Oksidlar", "ru": "Оксиды", "en": "Oxides"}},
                    {"slug": "kislotalar", "title": {"uz": "Kislotalar", "ru": "Кислоты", "en": "Acids"}},
                    {"slug": "asoslar", "title": {"uz": "Asoslar (ishqorlar)", "ru": "Основания", "en": "Bases"}},
                    {"slug": "tuzlar", "title": {"uz": "Tuzlar", "ru": "Соли", "en": "Salts"}},
                ],
            },
            {
                "slug": "eritmalar-reaksiyalar",
                "title": {"uz": "Eritmalar va reaksiyalar", "ru": "Растворы и реакции", "en": "Solutions and reactions"},
                "lessons": [
                    {"slug": "eritmalar-konsentratsiya", "title": {"uz": "Eritmalar va konsentratsiya", "ru": "Растворы и концентрация", "en": "Solutions and concentration"}},
                    {"slug": "elektrolitik-dissotsiatsiya", "title": {"uz": "Elektrolitik dissotsiatsiya", "ru": "Электролитическая диссоциация", "en": "Electrolytic dissociation"}},
                    {"slug": "oksidlanish-qaytarilish", "title": {"uz": "Oksidlanish-qaytarilish reaksiyalari", "ru": "Окислительно-восстановительные реакции", "en": "Redox reactions"}},
                    {"slug": "metallar-nometallar", "title": {"uz": "Metallar va nometallar", "ru": "Металлы и неметаллы", "en": "Metals and non-metals"}},
                ],
            },
            {
                "slug": "organik-kimyo",
                "title": {"uz": "Organik kimyo", "ru": "Органическая химия", "en": "Organic chemistry"},
                "lessons": [
                    {"slug": "uglevodorodlar", "title": {"uz": "Uglevodorodlar (alkanlar, alkenlar)", "ru": "Углеводороды", "en": "Hydrocarbons"}},
                    {"slug": "spirtlar-kislotalar", "title": {"uz": "Spirtlar va organik kislotalar", "ru": "Спирты и органические кислоты", "en": "Alcohols and organic acids"}},
                    {"slug": "uglevodlar-oqsillar", "title": {"uz": "Uglevodlar, yog'lar, oqsillar", "ru": "Углеводы, жиры, белки", "en": "Carbohydrates, fats, proteins"}},
                ],
            },
            {
                "slug": "kimyoviy-hisoblashlar",
                "title": {"uz": "Kimyoviy hisoblashlar", "ru": "Химические расчёты", "en": "Chemical calculations"},
                "lessons": [
                    {"slug": "formula-boyicha-hisoblash", "title": {"uz": "Formula bo'yicha hisoblashlar", "ru": "Расчёты по формуле", "en": "Calculations by formula"}},
                    {"slug": "tenglama-boyicha-hisoblash", "title": {"uz": "Reaksiya tenglamasi bo'yicha hisoblash", "ru": "Расчёты по уравнению", "en": "Calculations by equation"}},
                    {"slug": "eritma-hisoblashlari", "title": {"uz": "Eritmalarga oid hisoblashlar", "ru": "Расчёты растворов", "en": "Solution calculations"}},
                ],
            },
        ],
    },
    "fizika": {
        "name": {"uz": "Fizika", "ru": "Физика", "en": "Physics"},
        "icon": "atom",
        "color": "#4263EB",
        "units": [
            {
                "slug": "mexanika-kinematika",
                "title": {"uz": "Kinematika", "ru": "Кинематика", "en": "Kinematics"},
                "lessons": [
                    {"slug": "tekis-harakat", "title": {"uz": "Tekis va notekis harakat", "ru": "Равномерное движение", "en": "Uniform motion"}},
                    {"slug": "tezlanish", "title": {"uz": "Tezlanish va tezlanuvchan harakat", "ru": "Ускорение", "en": "Acceleration"}},
                    {"slug": "erkin-tushish", "title": {"uz": "Erkin tushish", "ru": "Свободное падение", "en": "Free fall"}},
                ],
            },
            {
                "slug": "mexanika-dinamika",
                "title": {"uz": "Dinamika", "ru": "Динамика", "en": "Dynamics"},
                "lessons": [
                    {"slug": "nyuton-qonunlari", "title": {"uz": "Nyuton qonunlari", "ru": "Законы Ньютона", "en": "Newton's laws"}},
                    {"slug": "ogirlik-ishqalanish", "title": {"uz": "Og'irlik va ishqalanish kuchi", "ru": "Сила тяжести и трения", "en": "Gravity and friction"}},
                    {"slug": "impuls-saqlanish", "title": {"uz": "Impuls va uning saqlanishi", "ru": "Импульс и его сохранение", "en": "Momentum and conservation"}},
                ],
            },
            {
                "slug": "ish-energiya",
                "title": {"uz": "Ish, quvvat, energiya", "ru": "Работа, мощность, энергия", "en": "Work, power, energy"},
                "lessons": [
                    {"slug": "mexanik-ish-quvvat", "title": {"uz": "Mexanik ish va quvvat", "ru": "Механическая работа и мощность", "en": "Work and power"}},
                    {"slug": "kinetik-potensial-energiya", "title": {"uz": "Kinetik va potensial energiya", "ru": "Кинетическая и потенциальная энергия", "en": "Kinetic and potential energy"}},
                    {"slug": "energiya-saqlanish", "title": {"uz": "Energiyaning saqlanish qonuni", "ru": "Закон сохранения энергии", "en": "Conservation of energy"}},
                ],
            },
            {
                "slug": "molekulyar-fizika",
                "title": {"uz": "Molekulyar fizika va issiqlik", "ru": "Молекулярная физика и теплота", "en": "Molecular physics and heat"},
                "lessons": [
                    {"slug": "molekulyar-tuzilish", "title": {"uz": "Moddaning molekulyar tuzilishi", "ru": "Молекулярное строение вещества", "en": "Molecular structure of matter"}},
                    {"slug": "temperatura-issiqlik", "title": {"uz": "Temperatura va issiqlik miqdori", "ru": "Температура и количество теплоты", "en": "Temperature and heat"}},
                    {"slug": "gaz-qonunlari", "title": {"uz": "Gaz qonunlari", "ru": "Газовые законы", "en": "Gas laws"}},
                    {"slug": "agregat-holatlar", "title": {"uz": "Moddaning agregat holatlari", "ru": "Агрегатные состояния", "en": "States of matter"}},
                ],
            },
            {
                "slug": "elektr",
                "title": {"uz": "Elektr va magnetizm", "ru": "Электричество и магнетизм", "en": "Electricity and magnetism"},
                "lessons": [
                    {"slug": "elektr-zaryad-maydon", "title": {"uz": "Elektr zaryadi va maydoni", "ru": "Электрический заряд и поле", "en": "Electric charge and field"}},
                    {"slug": "elektr-tok-om-qonuni", "title": {"uz": "Elektr toki va Om qonuni", "ru": "Электрический ток и закон Ома", "en": "Current and Ohm's law"}},
                    {"slug": "elektr-zanjirlar", "title": {"uz": "Elektr zanjirlar (ketma-ket, parallel)", "ru": "Электрические цепи", "en": "Electric circuits"}},
                    {"slug": "magnit-maydon", "title": {"uz": "Magnit maydon", "ru": "Магнитное поле", "en": "Magnetic field"}},
                ],
            },
            {
                "slug": "tebranish-optika",
                "title": {"uz": "Tebranish, to'lqin, optika", "ru": "Колебания, волны, оптика", "en": "Oscillations, waves, optics"},
                "lessons": [
                    {"slug": "tebranish-tolqinlar", "title": {"uz": "Mexanik tebranish va to'lqinlar", "ru": "Колебания и волны", "en": "Oscillations and waves"}},
                    {"slug": "yoruglik-qonunlari", "title": {"uz": "Yorug'likning qaytishi va sinishi", "ru": "Отражение и преломление света", "en": "Reflection and refraction"}},
                    {"slug": "linzalar", "title": {"uz": "Linzalar va optik asboblar", "ru": "Линзы и оптические приборы", "en": "Lenses and optical instruments"}},
                ],
            },
            {
                "slug": "atom-yadro-fizikasi",
                "title": {"uz": "Atom va yadro fizikasi", "ru": "Атомная и ядерная физика", "en": "Atomic and nuclear physics"},
                "lessons": [
                    {"slug": "atom-tuzilishi-fizika", "title": {"uz": "Atom tuzilishi va nurlanish", "ru": "Строение атома и излучение", "en": "Atomic structure and radiation"}},
                    {"slug": "radioaktivlik", "title": {"uz": "Radioaktivlik va yadro reaksiyalari", "ru": "Радиоактивность и ядерные реакции", "en": "Radioactivity and nuclear reactions"}},
                ],
            },
        ],
    },
    "jahon_tarixi": {
        "name": {"uz": "Jahon tarixi", "ru": "Всемирная история", "en": "World History"},
        "icon": "globe",
        "color": "#F59F00",
        "units": [
            {
                "slug": "qadimgi-dunyo",
                "title": {"uz": "Qadimgi dunyo", "ru": "Древний мир", "en": "Ancient world"},
                "lessons": [
                    {"slug": "ibtidoiy-jamiyat-jahon", "title": {"uz": "Ibtidoiy jamiyat", "ru": "Первобытное общество", "en": "Primitive society"}},
                    {"slug": "qadimgi-sharq", "title": {"uz": "Qadimgi Sharq (Misr, Bobil, Hindiston, Xitoy)", "ru": "Древний Восток", "en": "Ancient East"}},
                    {"slug": "qadimgi-yunoniston", "title": {"uz": "Qadimgi Yunoniston", "ru": "Древняя Греция", "en": "Ancient Greece"}},
                    {"slug": "qadimgi-rim", "title": {"uz": "Qadimgi Rim", "ru": "Древний Рим", "en": "Ancient Rome"}},
                ],
            },
            {
                "slug": "orta-asrlar-jahon",
                "title": {"uz": "O'rta asrlar", "ru": "Средние века", "en": "Middle Ages"},
                "lessons": [
                    {"slug": "buyuk-koch", "title": {"uz": "Xalqlarning buyuk ko'chishi", "ru": "Великое переселение народов", "en": "Migration Period"}},
                    {"slug": "vizantiya-yevropa", "title": {"uz": "Vizantiya va O'rta asr Yevropasi", "ru": "Византия и средневековая Европа", "en": "Byzantium and medieval Europe"}},
                    {"slug": "arab-xalifaligi", "title": {"uz": "Arab xalifaligi va islom dini", "ru": "Арабский халифат и ислам", "en": "Arab Caliphate and Islam"}},
                    {"slug": "salib-yurishlari", "title": {"uz": "Salib yurishlari", "ru": "Крестовые походы", "en": "The Crusades"}},
                ],
            },
            {
                "slug": "yangi-davr-boshi",
                "title": {"uz": "Yangi davr boshlanishi", "ru": "Начало Нового времени", "en": "Early modern period"},
                "lessons": [
                    {"slug": "buyuk-geografik-kashfiyotlar", "title": {"uz": "Buyuk geografik kashfiyotlar", "ru": "Великие географические открытия", "en": "Age of Discovery"}},
                    {"slug": "uygonish-reformatsiya", "title": {"uz": "Uyg'onish davri va Reformatsiya", "ru": "Возрождение и Реформация", "en": "Renaissance and Reformation"}},
                    {"slug": "ingliz-inqilobi", "title": {"uz": "Ingliz burjua inqilobi", "ru": "Английская революция", "en": "English Revolution"}},
                ],
            },
            {
                "slug": "inqiloblar-davri",
                "title": {"uz": "Inqiloblar va o'zgarishlar davri", "ru": "Эпоха революций", "en": "Age of revolutions"},
                "lessons": [
                    {"slug": "amerika-mustaqilligi", "title": {"uz": "AQSh mustaqilligi uchun urush", "ru": "Война за независимость США", "en": "American Revolution"}},
                    {"slug": "fransuz-inqilobi", "title": {"uz": "Fransuz inqilobi", "ru": "Французская революция", "en": "French Revolution"}},
                    {"slug": "sanoat-tontarishi", "title": {"uz": "Sanoat to'ntarishi", "ru": "Промышленная революция", "en": "Industrial Revolution"}},
                    {"slug": "napoleon-urushlari", "title": {"uz": "Napoleon urushlari", "ru": "Наполеоновские войны", "en": "Napoleonic Wars"}},
                ],
            },
            {
                "slug": "jahon-urushlari",
                "title": {"uz": "Jahon urushlari davri", "ru": "Эпоха мировых войн", "en": "World Wars era"},
                "lessons": [
                    {"slug": "birinchi-jahon-urushi", "title": {"uz": "Birinchi jahon urushi", "ru": "Первая мировая война", "en": "World War I"}},
                    {"slug": "ikki-urush-orasi", "title": {"uz": "Ikki urush oralig'idagi dunyo", "ru": "Мир между войнами", "en": "Interwar period"}},
                    {"slug": "ikkinchi-jahon-urushi-jahon", "title": {"uz": "Ikkinchi jahon urushi", "ru": "Вторая мировая война", "en": "World War II"}},
                ],
            },
            {
                "slug": "eng-yangi-davr",
                "title": {"uz": "Eng yangi davr", "ru": "Новейшее время", "en": "Contemporary period"},
                "lessons": [
                    {"slug": "sovuq-urush", "title": {"uz": "Sovuq urush", "ru": "Холодная война", "en": "Cold War"}},
                    {"slug": "mustamlakachilik-tugashi", "title": {"uz": "Mustamlakachilik tizimining yemirilishi", "ru": "Крушение колониальной системы", "en": "Decolonization"}},
                    {"slug": "globallashuv", "title": {"uz": "Zamonaviy dunyo va globallashuv", "ru": "Современный мир и глобализация", "en": "Modern world and globalization"}},
                ],
            },
        ],
    },
    "tarix": {
        "name": {"uz": "O'zbekiston tarixi", "ru": "История Узбекистана", "en": "History of Uzbekistan"},
        "icon": "landmark",
        "color": "#1CB0F6",
        "units": [
            {
                "slug": "qadimgi-davr",
                "title": {"uz": "Qadimgi davr", "ru": "Древний период", "en": "Ancient period"},
                "lessons": [
                    {"slug": "ibtidoiy-jamoa", "title": {"uz": "O'zbekiston hududida ibtidoiy jamoa", "ru": "Первобытное общество на территории Узбекистана", "en": "Primitive society in Uzbekistan"}},
                    {"slug": "qadimgi-davlatlar", "title": {"uz": "Qadimgi Baqtriya, So'g'd, Xorazm", "ru": "Древние Бактрия, Согд, Хорезм", "en": "Ancient Bactria, Sogdiana, Khorezm"}},
                    {"slug": "ahamoniylar-iskandar", "title": {"uz": "Ahamoniylar va Iskandar Zulqarnayn yurishlari", "ru": "Ахемениды и походы Александра", "en": "Achaemenids and Alexander's campaigns"}},
                    {"slug": "kushon-davlati", "title": {"uz": "Kushon davlati", "ru": "Кушанское государство", "en": "Kushan Empire"}},
                ],
            },
            {
                "slug": "orta-asrlar",
                "title": {"uz": "O'rta asrlar", "ru": "Средние века", "en": "Middle Ages"},
                "lessons": [
                    {"slug": "arab-istilosi", "title": {"uz": "Arab istilosi va Markaziy Osiyo", "ru": "Арабское завоевание и Средняя Азия", "en": "Arab conquest of Central Asia"}},
                    {"slug": "somoniylar", "title": {"uz": "Somoniylar davlati va Uyg'onish davri", "ru": "Государство Саманидов и эпоха Возрождения", "en": "Samanid state and the Renaissance"}},
                    {"slug": "qoraxoniylar-xorazmshohlar", "title": {"uz": "Qoraxoniylar va Xorazmshohlar davlati", "ru": "Караханиды и Хорезмшахи", "en": "Karakhanids and Khorezmshahs"}},
                    {"slug": "mugul-istilosi", "title": {"uz": "Mo'g'ul istilosi", "ru": "Монгольское завоевание", "en": "Mongol conquest"}},
                ],
            },
            {
                "slug": "amir-temur-temuriylar",
                "title": {"uz": "Amir Temur va Temuriylar", "ru": "Амир Темур и Тимуриды", "en": "Amir Temur and the Timurids"},
                "lessons": [
                    {"slug": "amir-temur-davlati", "title": {"uz": "Amir Temur davlatining tashkil topishi", "ru": "Образование государства Амира Темура", "en": "Founding of Amir Temur's state"}},
                    {"slug": "temur-yurishlari", "title": {"uz": "Amir Temurning harbiy yurishlari", "ru": "Военные походы Амира Темура", "en": "Amir Temur's military campaigns"}},
                    {"slug": "ulugbek-davri", "title": {"uz": "Mirzo Ulug'bek davri, fan va madaniyat", "ru": "Эпоха Мирзо Улугбека, наука и культура", "en": "Mirzo Ulugbek era, science and culture"}},
                    {"slug": "temuriylar-inqirozi", "title": {"uz": "Temuriylar davlatining inqirozi", "ru": "Упадок государства Тимуридов", "en": "Decline of the Timurid state"}},
                ],
            },
            {
                "slug": "xonliklar-davri",
                "title": {"uz": "Xonliklar davri", "ru": "Период ханств", "en": "The Khanates period"},
                "lessons": [
                    {"slug": "shayboniylar", "title": {"uz": "Shayboniylar davlati", "ru": "Государство Шейбанидов", "en": "Shaybanid state"}},
                    {"slug": "buxoro-xonligi", "title": {"uz": "Buxoro xonligi/amirligi", "ru": "Бухарское ханство/эмират", "en": "Bukhara Khanate/Emirate"}},
                    {"slug": "xiva-xonligi", "title": {"uz": "Xiva xonligi", "ru": "Хивинское ханство", "en": "Khiva Khanate"}},
                    {"slug": "qoqon-xonligi", "title": {"uz": "Qo'qon xonligi", "ru": "Кокандское ханство", "en": "Kokand Khanate"}},
                ],
            },
            {
                "slug": "chor-rossiyasi",
                "title": {"uz": "Chor Rossiyasi davri", "ru": "Период царской России", "en": "Tsarist Russia period"},
                "lessons": [
                    {"slug": "bosib-olinishi", "title": {"uz": "Turkistonning Rossiya tomonidan bosib olinishi", "ru": "Завоевание Туркестана Россией", "en": "Russian conquest of Turkestan"}},
                    {"slug": "turkiston-general-gubernatorligi", "title": {"uz": "Turkiston general-gubernatorligi", "ru": "Туркестанское генерал-губернаторство", "en": "Turkestan Governor-Generalship"}},
                    {"slug": "jadidchilik", "title": {"uz": "Jadidchilik harakati", "ru": "Джадидское движение", "en": "The Jadid movement"}},
                    {"slug": "1916-qozgolon", "title": {"uz": "1916-yilgi qo'zg'olon", "ru": "Восстание 1916 года", "en": "The 1916 uprising"}},
                ],
            },
            {
                "slug": "sovet-davri",
                "title": {"uz": "Sovet davri", "ru": "Советский период", "en": "Soviet period"},
                "lessons": [
                    {"slug": "sovet-hokimiyati-ornatilishi", "title": {"uz": "Sovet hokimiyatining o'rnatilishi", "ru": "Установление советской власти", "en": "Establishment of Soviet power"}},
                    {"slug": "milliy-chegaralanish", "title": {"uz": "Milliy-hududiy chegaralanish", "ru": "Национально-territориальное размежевание", "en": "National territorial delimitation"}},
                    {"slug": "kollektivlashtirish-repressiya", "title": {"uz": "Kollektivlashtirish va repressiya", "ru": "Коллективизация и репрессии", "en": "Collectivization and repression"}},
                    {"slug": "ikkinchi-jahon-urushi", "title": {"uz": "O'zbekiston Ikkinchi jahon urushi yillarida", "ru": "Узбекистан в годы Второй мировой войны", "en": "Uzbekistan during World War II"}},
                ],
            },
            {
                "slug": "mustaqillik-davri",
                "title": {"uz": "Mustaqillik davri", "ru": "Период независимости", "en": "Independence period"},
                "lessons": [
                    {"slug": "mustaqillik-elon-qilinishi", "title": {"uz": "Mustaqillikning e'lon qilinishi", "ru": "Провозглашение независимости", "en": "Declaration of independence"}},
                    {"slug": "birinchi-konstitutsiya", "title": {"uz": "O'zbekiston Respublikasi Konstitutsiyasi", "ru": "Конституция Республики Узбекистан", "en": "Constitution of the Republic of Uzbekistan"}},
                    {"slug": "islohotlar-davri", "title": {"uz": "Yangi O'zbekiston -- islohotlar davri", "ru": "Новый Узбекистан -- эпоха реформ", "en": "New Uzbekistan -- era of reforms"}},
                ],
            },
        ],
    },
    "ozbek_adabiyoti": {
        "name": {"uz": "O'zbek adabiyoti", "ru": "Узбекская литература", "en": "Uzbek Literature"},
        "icon": "feather",
        "color": "#E8590C",
        "units": [
            {
                "slug": "xalq-ogzaki-ijodi",
                "title": {"uz": "Xalq og'zaki ijodi", "ru": "Устное народное творчество", "en": "Folklore"},
                "lessons": [
                    {"slug": "dostonlar", "title": {"uz": "Xalq dostonlari (Alpomish, Go'ro'g'li)", "ru": "Народные дастаны", "en": "Folk epics"}},
                    {"slug": "ertak-maqol", "title": {"uz": "Ertak, maqol va topishmoqlar", "ru": "Сказки, пословицы, загадки", "en": "Tales, proverbs, riddles"}},
                    {"slug": "qoshiq-lapar", "title": {"uz": "Xalq qo'shiqlari va laparlar", "ru": "Народные песни", "en": "Folk songs"}},
                ],
            },
            {
                "slug": "mumtoz-adabiyot",
                "title": {"uz": "Mumtoz adabiyot", "ru": "Классическая литература", "en": "Classical literature"},
                "lessons": [
                    {"slug": "yugnakiy-yusuf", "title": {"uz": "Yusuf Xos Hojib va Ahmad Yugnakiy", "ru": "Юсуф Хос Хожиб и Ахмад Югнаки", "en": "Yusuf Khos Hojib and Ahmad Yugnakiy"}},
                    {"slug": "navoiy", "title": {"uz": "Alisher Navoiy ijodi", "ru": "Творчество Алишера Навои", "en": "Alisher Navoiy"}},
                    {"slug": "bobur", "title": {"uz": "Zahiriddin Muhammad Bobur", "ru": "Захириддин Мухаммад Бабур", "en": "Zahiriddin Muhammad Bobur"}},
                    {"slug": "mashrab-ogahiy", "title": {"uz": "Mashrab va Ogahiy", "ru": "Машраб и Огахи", "en": "Mashrab and Ogahiy"}},
                ],
            },
            {
                "slug": "jadid-adabiyoti",
                "title": {"uz": "Jadid adabiyoti", "ru": "Литература джадидов", "en": "Jadid literature"},
                "lessons": [
                    {"slug": "behbudiy-fitrat", "title": {"uz": "Behbudiy va Fitrat", "ru": "Бехбуди и Фитрат", "en": "Behbudiy and Fitrat"}},
                    {"slug": "qodiriy", "title": {"uz": "Abdulla Qodiriy va o'zbek romani", "ru": "Абдулла Кадыри", "en": "Abdulla Qodiriy"}},
                    {"slug": "cholpon", "title": {"uz": "Cho'lpon she'riyati", "ru": "Поэзия Чулпана", "en": "Cho'lpon"}},
                ],
            },
            {
                "slug": "xx-asr-adabiyoti",
                "title": {"uz": "XX asr adabiyoti", "ru": "Литература XX века", "en": "20th-century literature"},
                "lessons": [
                    {"slug": "oybek", "title": {"uz": "Oybek ijodi", "ru": "Творчество Ойбека", "en": "Oybek"}},
                    {"slug": "gafur-gulom", "title": {"uz": "G'afur G'ulom", "ru": "Гафур Гулям", "en": "Gʻafur Gʻulom"}},
                    {"slug": "abdulla-qahhor", "title": {"uz": "Abdulla Qahhor hikoyalari", "ru": "Абдулла Каххар", "en": "Abdulla Qahhor"}},
                    {"slug": "zulfiya", "title": {"uz": "Zulfiya she'riyati", "ru": "Поэзия Зульфии", "en": "Zulfiya"}},
                ],
            },
            {
                "slug": "mustaqillik-adabiyoti",
                "title": {"uz": "Mustaqillik davri adabiyoti", "ru": "Литература периода независимости", "en": "Independence-era literature"},
                "lessons": [
                    {"slug": "erkin-vohidov", "title": {"uz": "Erkin Vohidov", "ru": "Эркин Вахидов", "en": "Erkin Vohidov"}},
                    {"slug": "abdulla-oripov", "title": {"uz": "Abdulla Oripov", "ru": "Абдулла Арипов", "en": "Abdulla Oripov"}},
                    {"slug": "zamonaviy-nasr", "title": {"uz": "Zamonaviy o'zbek nasri", "ru": "Современная узбекская проза", "en": "Modern Uzbek prose"}},
                ],
            },
            {
                "slug": "adabiyot-nazariyasi-uz",
                "title": {"uz": "Adabiyot nazariyasi", "ru": "Теория литературы", "en": "Literary theory"},
                "lessons": [
                    {"slug": "adabiy-turlar", "title": {"uz": "Adabiy tur va janrlar", "ru": "Литературные роды и жанры", "en": "Literary genres"}},
                    {"slug": "sher-tuzilishi", "title": {"uz": "She'r tuzilishi: aruz va barmoq", "ru": "Строение стиха", "en": "Verse structure"}},
                    {"slug": "tasvir-vositalari", "title": {"uz": "Badiiy tasvir vositalari", "ru": "Художественные средства", "en": "Literary devices"}},
                ],
            },
        ],
    },
    "jahon_adabiyoti": {
        "name": {"uz": "Jahon adabiyoti", "ru": "Мировая литература", "en": "World Literature"},
        "icon": "globe",
        "color": "#1098AD",
        "units": [
            {
                "slug": "antik-adabiyot",
                "title": {"uz": "Antik adabiyot", "ru": "Античная литература", "en": "Ancient literature"},
                "lessons": [
                    {"slug": "qadimgi-yunon", "title": {"uz": "Qadimgi Yunon adabiyoti (Homer)", "ru": "Древнегреческая литература", "en": "Ancient Greek literature"}},
                    {"slug": "yunon-tragediyasi", "title": {"uz": "Yunon tragediyasi va teatri", "ru": "Греческая трагедия", "en": "Greek tragedy"}},
                    {"slug": "qadimgi-rim", "title": {"uz": "Qadimgi Rim adabiyoti", "ru": "Древнеримская литература", "en": "Ancient Roman literature"}},
                ],
            },
            {
                "slug": "sharq-mumtoz",
                "title": {"uz": "Sharq mumtoz adabiyoti", "ru": "Классическая литература Востока", "en": "Classical Eastern literature"},
                "lessons": [
                    {"slug": "firdavsiy", "title": {"uz": "Firdavsiy \"Shohnoma\"", "ru": "Фирдоуси «Шахнаме»", "en": "Firdavsiy's Shahnameh"}},
                    {"slug": "hofiz-sadiy", "title": {"uz": "Hofiz va Sa'diy", "ru": "Хафиз и Саади", "en": "Hafiz and Saadi"}},
                    {"slug": "umar-xayyom", "title": {"uz": "Umar Xayyom ruboiylari", "ru": "Рубаи Омара Хайяма", "en": "Omar Khayyam"}},
                ],
            },
            {
                "slug": "ortaasr-uygonish",
                "title": {"uz": "O'rta asrlar va Uyg'onish", "ru": "Средневековье и Возрождение", "en": "Medieval and Renaissance"},
                "lessons": [
                    {"slug": "dante", "title": {"uz": "Dante \"Ilohiy komediya\"", "ru": "Данте «Божественная комедия»", "en": "Dante's Divine Comedy"}},
                    {"slug": "shekspir", "title": {"uz": "Uilyam Shekspir", "ru": "Уильям Шекспир", "en": "William Shakespeare"}},
                    {"slug": "servantes", "title": {"uz": "Servantes \"Don Kixot\"", "ru": "Сервантес «Дон Кихот»", "en": "Cervantes' Don Quixote"}},
                ],
            },
            {
                "slug": "marifat-romantizm",
                "title": {"uz": "Ma'rifatparvarlik va romantizm", "ru": "Просвещение и романтизм", "en": "Enlightenment and Romanticism"},
                "lessons": [
                    {"slug": "gyote", "title": {"uz": "Gyote \"Faust\"", "ru": "Гёте «Фауст»", "en": "Goethe's Faust"}},
                    {"slug": "romantizm", "title": {"uz": "Romantizm oqimi (Bayron, Pushkin)", "ru": "Романтизм", "en": "Romanticism"}},
                    {"slug": "molyer", "title": {"uz": "Molyer komediyalari", "ru": "Комедии Мольера", "en": "Molière's comedies"}},
                ],
            },
            {
                "slug": "realizm",
                "title": {"uz": "XIX asr realizmi", "ru": "Реализм XIX века", "en": "19th-century Realism"},
                "lessons": [
                    {"slug": "tolstoy", "title": {"uz": "Lev Tolstoy", "ru": "Лев Толстой", "en": "Leo Tolstoy"}},
                    {"slug": "dostoyevskiy", "title": {"uz": "Fyodor Dostoyevskiy", "ru": "Фёдор Достоевский", "en": "Fyodor Dostoevsky"}},
                    {"slug": "balzak-dikkens", "title": {"uz": "Balzak va Dikkens", "ru": "Бальзак и Диккенс", "en": "Balzac and Dickens"}},
                ],
            },
            {
                "slug": "xx-asr-jahon",
                "title": {"uz": "XX asr jahon adabiyoti", "ru": "Мировая литература XX века", "en": "20th-century world literature"},
                "lessons": [
                    {"slug": "modernizm", "title": {"uz": "Modernizm va uning yo'nalishlari", "ru": "Модернизм", "en": "Modernism"}},
                    {"slug": "xeminguey", "title": {"uz": "Ernest Xeminguey", "ru": "Эрнест Хемингуэй", "en": "Ernest Hemingway"}},
                    {"slug": "jahon-dramaturgiyasi", "title": {"uz": "XX asr jahon dramaturgiyasi", "ru": "Драматургия XX века", "en": "20th-century drama"}},
                ],
            },
        ],
    },
    "koreys_tili": {
        "name": {"uz": "Koreys tili", "ru": "Корейский язык", "en": "Korean"},
        "icon": "languages",
        "color": "#3B5BDB",
        "units": [
            {
                "slug": "hangul",
                "title": {"uz": "Hangul alifbosi", "ru": "Алфавит хангыль", "en": "Hangul alphabet"},
                "lessons": [
                    {"slug": "unlilar", "title": {"uz": "Unli harflar", "ru": "Гласные буквы", "en": "Vowels"}},
                    {"slug": "undoshlar", "title": {"uz": "Undosh harflar", "ru": "Согласные буквы", "en": "Consonants"}},
                    {"slug": "bogin-tuzilishi", "title": {"uz": "Bo'g'in tuzilishi", "ru": "Строение слогов", "en": "Syllable structure"}},
                ],
            },
            {
                "slug": "salomlashish-ko",
                "title": {"uz": "Salomlashish va tanishuv", "ru": "Приветствие и знакомство", "en": "Greetings and introductions"},
                "lessons": [
                    {"slug": "salom-alik", "title": {"uz": "Salomlashish iboralari", "ru": "Приветствия", "en": "Greetings"}},
                    {"slug": "ozini-tanishtirish-ko", "title": {"uz": "O'zini tanishtirish", "ru": "Представление себя", "en": "Introducing yourself"}},
                    {"slug": "xushmuomalalik", "title": {"uz": "Xushmuomalalik darajalari", "ru": "Уровни вежливости", "en": "Politeness levels"}},
                ],
            },
            {
                "slug": "sonlar-vaqt-ko",
                "title": {"uz": "Sonlar va vaqt", "ru": "Числа и время", "en": "Numbers and time"},
                "lessons": [
                    {"slug": "koreys-sonlar", "title": {"uz": "Koreys va Xitoy sonlari", "ru": "Корейские и китайские числа", "en": "Native and Sino-Korean numbers"}},
                    {"slug": "vaqt-sana-ko", "title": {"uz": "Vaqt va sana", "ru": "Время и дата", "en": "Time and date"}},
                ],
            },
            {
                "slug": "grammatika-ko",
                "title": {"uz": "Grammatika asoslari", "ru": "Основы грамматики", "en": "Grammar basics"},
                "lessons": [
                    {"slug": "gap-tuzilishi-ko", "title": {"uz": "Gap tuzilishi (SOV)", "ru": "Структура предложения", "en": "Sentence structure"}},
                    {"slug": "yuklamalar-ko", "title": {"uz": "Yuklamalar (은/는, 이/가)", "ru": "Частицы", "en": "Particles"}},
                    {"slug": "fel-tugallanmalari", "title": {"uz": "Fe'l tugallanmalari", "ru": "Окончания глаголов", "en": "Verb endings"}},
                ],
            },
            {
                "slug": "kundalik-hayot-ko",
                "title": {"uz": "Kundalik hayot", "ru": "Повседневная жизнь", "en": "Daily life"},
                "lessons": [
                    {"slug": "oila-ko", "title": {"uz": "Oila va odamlar", "ru": "Семья и люди", "en": "Family and people"}},
                    {"slug": "ovqat-ko", "title": {"uz": "Ovqat va restoran", "ru": "Еда и ресторан", "en": "Food and restaurant"}},
                    {"slug": "xarid-ko", "title": {"uz": "Xarid qilish", "ru": "Покупки", "en": "Shopping"}},
                ],
            },
        ],
    },
    "fransuz_tili": {
        "name": {"uz": "Fransuz tili", "ru": "Французский язык", "en": "French"},
        "icon": "languages",
        "color": "#F03E3E",
        "units": [
            {
                "slug": "alifbo-talaffuz-fr",
                "title": {"uz": "Alifbo va talaffuz", "ru": "Алфавит и произношение", "en": "Alphabet and pronunciation"},
                "lessons": [
                    {"slug": "harflar-fr", "title": {"uz": "Harflar va tovushlar", "ru": "Буквы и звуки", "en": "Letters and sounds"}},
                    {"slug": "urgu-belgilar", "title": {"uz": "Urg'u belgilari (accents)", "ru": "Диакритические знаки", "en": "Accent marks"}},
                    {"slug": "talaffuz-qoidalari-fr", "title": {"uz": "Talaffuz qoidalari", "ru": "Правила произношения", "en": "Pronunciation rules"}},
                ],
            },
            {
                "slug": "salomlashish-fr",
                "title": {"uz": "Salomlashish va tanishuv", "ru": "Приветствие и знакомство", "en": "Greetings and introductions"},
                "lessons": [
                    {"slug": "salom-fr", "title": {"uz": "Salomlashish iboralari", "ru": "Приветствия", "en": "Greetings"}},
                    {"slug": "ozini-tanishtirish-fr", "title": {"uz": "O'zini tanishtirish", "ru": "Представление себя", "en": "Introducing yourself"}},
                ],
            },
            {
                "slug": "artikl-rod-fr",
                "title": {"uz": "Artikllar va rod", "ru": "Артикли и род", "en": "Articles and gender"},
                "lessons": [
                    {"slug": "artikllar-fr", "title": {"uz": "Aniq va noaniq artikllar", "ru": "Определённые и неопределённые артикли", "en": "Definite and indefinite articles"}},
                    {"slug": "ot-rodi-fr", "title": {"uz": "Ot rodi va ko'pligi", "ru": "Род и множественное число", "en": "Noun gender and plural"}},
                ],
            },
            {
                "slug": "fellar-fr",
                "title": {"uz": "Fe'llar", "ru": "Глаголы", "en": "Verbs"},
                "lessons": [
                    {"slug": "etre-avoir", "title": {"uz": "Être va avoir fe'llari", "ru": "Глаголы être и avoir", "en": "Être and avoir"}},
                    {"slug": "er-fellari", "title": {"uz": "Birinchi guruh (-er) fe'llari", "ru": "Глаголы на -er", "en": "-er verbs"}},
                    {"slug": "hozirgi-zamon-fr", "title": {"uz": "Hozirgi zamon (Présent)", "ru": "Настоящее время", "en": "Present tense"}},
                ],
            },
            {
                "slug": "sonlar-kundalik-fr",
                "title": {"uz": "Sonlar va kundalik muloqot", "ru": "Числа и общение", "en": "Numbers and everyday communication"},
                "lessons": [
                    {"slug": "sonlar-fr", "title": {"uz": "Sonlar", "ru": "Числа", "en": "Numbers"}},
                    {"slug": "kun-oy-fr", "title": {"uz": "Kunlar, oylar, vaqt", "ru": "Дни, месяцы, время", "en": "Days, months, time"}},
                    {"slug": "kundalik-iboralar-fr", "title": {"uz": "Kundalik iboralar va dialoglar", "ru": "Повседневные фразы", "en": "Everyday phrases"}},
                ],
            },
        ],
    },
}


# ─── Generated syllabus depth ────────────────────────────────────────────────
# The structure above is the hand-authored spine: it fixes the units and the first
# few lessons of each, and its slugs are what existing UserLessonProgress rows point
# at. It is however far too shallow to be a course -- every unit above is 3-5 lessons,
# which put the whole of Uzbek history at 27 lessons and let a learner finish a
# subject in under an hour.
#
# scripts/expand_taxonomy.py generates the rest of each unit's lesson list and writes
# services/skilltree_outline.json; it is merged in here rather than pasted above so the
# hand-authored spine stays readable and reviewable on its own. The merge only ever
# APPENDS -- an existing slug is never moved or renamed, because that would silently
# repoint somebody's completed-lesson row at a different lesson.

import json as _json  # noqa: E402
import os as _os      # noqa: E402

_EXPANSION_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                "skilltree_outline.json")


def _merge_expansion() -> None:
    if not _os.path.exists(_EXPANSION_PATH):
        return
    with open(_EXPANSION_PATH, encoding="utf-8") as fh:
        expansion = _json.load(fh)

    for subject_slug, units in expansion.items():
        subject = SKILLTREE_OUTLINE.get(subject_slug)
        if not subject:
            continue
        order = units.get("_order") or {}
        for unit in subject["units"]:
            extra = units.get(unit["slug"]) or []
            existing = {l["slug"] for l in unit["lessons"]}
            for item in extra:
                if item["slug"] in existing:
                    continue
                existing.add(item["slug"])
                unit["lessons"].append({
                    "slug": item["slug"],
                    "title": {"uz": item["uz"], "ru": item["ru"], "en": item["en"]},
                })

            # Appending kept everyone's progress safe but left each unit reading
            # "the original four, then the seven added later" — in Tarix that taught
            # the 13th century before the 5th. `_order` is a teaching sequence over
            # the same slugs; anything it does not mention keeps its place at the end.
            wanted = order.get(unit["slug"])
            if wanted:
                rank = {slug: i for i, slug in enumerate(wanted)}
                unit["lessons"].sort(key=lambda l: rank.get(l["slug"], len(rank)))


_merge_expansion()
