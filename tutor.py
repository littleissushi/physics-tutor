import random
import json
import os

# O-Level Physics Tutor
# Focused on highest-frequency exam topics and scoring techniques

PROGRESS_FILE = "progress.json"

QUESTIONS = [
    {
        "topic": "Kinematics",
        "question": "A car accelerates from rest to 20 m/s in 5 seconds. What is its acceleration?",
        "answer": "4 m/s²",
        "keywords": ["4", "m/s²", "m/s2"],
        "explanation": (
            "Use the formula: a = (v - u) / t\n"
            "a = (20 - 0) / 5 = 4 m/s²\n"
            "KEY EXAM TIP: Always show your formula, substitution, and units. "
            "Examiners award marks at each step."
        ),
    },
    {
        "topic": "Kinematics",
        "question": "A ball is dropped from rest and falls for 3 seconds. How far does it fall? (g = 10 m/s²)",
        "answer": "45 m",
        "keywords": ["45", "m"],
        "explanation": (
            "Use: s = ut + ½at²\n"
            "s = 0(3) + ½(10)(3²) = 45 m\n"
            "KEY EXAM TIP: When dropped from rest, u = 0. State this clearly in your working."
        ),
    },
    {
        "topic": "Energy",
        "question": "A 2 kg ball is lifted to a height of 5 m. What is its gravitational potential energy? (g = 10 m/s²)",
        "answer": "100 J",
        "keywords": ["100", "j", "joules"],
        "explanation": (
            "Use: GPE = mgh\n"
            "GPE = 2 × 10 × 5 = 100 J\n"
            "KEY EXAM TIP: Always write the formula first. The examiner gives a mark just for the correct formula."
        ),
    },
    {
        "topic": "Electricity",
        "question": "A resistor has a voltage of 12V across it and a current of 3A through it. What is its resistance?",
        "answer": "4 Ω",
        "keywords": ["4", "ohm", "ω", "Ω"],
        "explanation": (
            "Use Ohm's Law: R = V / I\n"
            "R = 12 / 3 = 4 Ω\n"
            "KEY EXAM TIP: Ohm's Law is V = IR. Rearrange clearly and show each step."
        ),
    },
    {
        "topic": "Waves",
        "question": "A wave has a frequency of 50 Hz and a wavelength of 2 m. What is its speed?",
        "answer": "100 m/s",
        "keywords": ["100", "m/s"],
        "explanation": (
            "Use: v = fλ\n"
            "v = 50 × 2 = 100 m/s\n"
            "KEY EXAM TIP: The wave equation v = fλ is one of the most tested formulas. Memorise it."
        ),
    },
    {
        "topic": "Pressure",
        "question": "What is the pressure at the bottom of a 4 m deep tank of water? (density of water = 1000 kg/m³, g = 10 m/s²)",
        "answer": "40000 Pa",
        "keywords": ["40000", "40,000", "pa", "pascal"],
        "explanation": (
            "Use: P = ρgh\n"
            "P = 1000 × 10 × 4 = 40,000 Pa\n"
            "KEY EXAM TIP: ρ (rho) is density. Always check units — density must be in kg/m³."
        ),
    },
    {
        "topic": "Radioactivity",
        "question": "What type of radiation is most penetrating and requires thick lead to stop it?",
        "answer": "Gamma radiation",
        "keywords": ["gamma"],
        "explanation": (
            "Gamma radiation is electromagnetic radiation — most penetrating.\n"
            "Alpha: stopped by paper or skin.\n"
            "Beta: stopped by a few mm of aluminium.\n"
            "Gamma: requires thick lead or concrete.\n"
            "KEY EXAM TIP: Learn the penetration order — examiners test this repeatedly."
        ),
    },
]


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"weak_topics": {}, "sessions": 0}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def build_question_list(progress):
    """Give weak topics double the questions by adding them twice."""
    weak_topics = progress.get("weak_topics", {})
    question_list = list(QUESTIONS)

    for q in QUESTIONS:
        if q["topic"] in weak_topics and weak_topics[q["topic"]] > 0:
            question_list.append(q)

    random.shuffle(question_list)
    return question_list


def show_weak_areas(progress):
    weak = progress.get("weak_topics", {})
    if not weak:
        return
    print("\n📌 WEAK AREAS FROM LAST SESSION — focus on these:")
    for topic, misses in weak.items():
        if misses > 0:
            print(f"   • {topic} ({misses} missed)")
    print()


def check_answer(user_answer, keywords):
    user_lower = user_answer.lower()
    return any(kw.lower() in user_lower for kw in keywords)


def run_quiz():
    progress = load_progress()
    progress["sessions"] += 1

    print("\n" + "="*50)
    print("   O-LEVEL PHYSICS TUTOR")
    print("   Your personal exam coach")
    print("="*50)
    print(f"\nSession #{progress['sessions']}")

    show_weak_areas(progress)

    print("Topics covered: Kinematics, Energy, Electricity, Waves, Pressure, Radioactivity")
    print("Type 'quit' at any time to exit.\n")

    questions = build_question_list(progress)
    score = 0
    total = len(questions)
    session_wrong = {}

    for i, q in enumerate(questions, 1):
        print(f"\n[Question {i}/{total}] Topic: {q['topic']}")
        print("-" * 40)
        print(q["question"])
        print()

        user_answer = input("Your answer: ").strip()

        if user_answer.lower() == "quit":
            print("\nSession ended. Keep practising!")
            break

        if check_answer(user_answer, q["keywords"]):
            print("\n✓ CORRECT! Well done.\n")
            print(f"Explanation:\n{q['explanation']}")
            score += 1
            # Reduce weak topic count if she gets it right
            if q["topic"] in progress["weak_topics"]:
                progress["weak_topics"][q["topic"]] = max(
                    0, progress["weak_topics"][q["topic"]] - 1
                )
        else:
            print(f"\n✗ Not quite. The correct answer is: {q['answer']}\n")
            print(f"Explanation:\n{q['explanation']}")
            # Track weak topics
            session_wrong[q["topic"]] = session_wrong.get(q["topic"], 0) + 1

        input("\nPress Enter to continue...")

    # Update weak topics from this session
    for topic, count in session_wrong.items():
        progress["weak_topics"][topic] = progress["weak_topics"].get(topic, 0) + count

    save_progress(progress)

    print("\n" + "="*50)
    print(f"SESSION COMPLETE: {score}/{total} correct")
    print("="*50)

    # Review section — show missed questions and explanations before closing
    missed_questions = [q for q in questions if q["topic"] in session_wrong]
    if missed_questions:
        print("\n📖 REVIEW TIME — before you go, re-read these carefully:")
        print("-" * 50)
        for q in missed_questions:
            print(f"\nTopic: {q['topic']}")
            print(f"Question: {q['question']}")
            print(f"Correct answer: {q['answer']}")
            print(f"\n{q['explanation']}")
            print("-" * 50)

        print("\n💪 Keep practising — mastery comes from repetition.")
        print("   Re-read the explanations above carefully before your next session.")
        print("   These topics will appear again next time until you've got them.")
        input("\nPress Enter once you've read through the above...")
    else:
        print("\nNo weak areas this session. Excellent work!")

    if score == total:
        print("\nPerfect score! Outstanding!")
    elif score >= total * 0.7:
        print("\nGood work! Keep drilling the weak areas.")
    else:
        print("\nKeep practising — consistency beats cramming every time.")

    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    run_quiz()
