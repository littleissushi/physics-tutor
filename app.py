import random
import json
import os
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "physics-tutor-secret"

PROGRESS_FILE = "progress.json"

QUESTIONS = [
    {
        "topic": "Kinematics",
        "question": "A car accelerates from rest to 20 m/s in 5 seconds. What is its acceleration?",
        "answer": "4 m/s²",
        "keywords": ["4", "m/s²", "m/s2"],
        "explanation": "Use: a = (v - u) / t → a = (20 - 0) / 5 = 4 m/s². KEY TIP: Always show your formula, substitution, and units. Examiners award marks at each step.",
    },
    {
        "topic": "Kinematics",
        "question": "A ball is dropped from rest and falls for 3 seconds. How far does it fall? (g = 10 m/s²)",
        "answer": "45 m",
        "keywords": ["45"],
        "explanation": "Use: s = ut + ½at² → s = 0 + ½(10)(9) = 45 m. KEY TIP: When dropped from rest, u = 0. State this clearly in your working.",
    },
    {
        "topic": "Energy",
        "question": "A 2 kg ball is lifted to a height of 5 m. What is its gravitational potential energy? (g = 10 m/s²)",
        "answer": "100 J",
        "keywords": ["100"],
        "explanation": "Use: GPE = mgh → GPE = 2 × 10 × 5 = 100 J. KEY TIP: Always write the formula first — examiners give a mark just for the correct formula.",
    },
    {
        "topic": "Electricity",
        "question": "A resistor has a voltage of 12V across it and a current of 3A through it. What is its resistance?",
        "answer": "4 Ω",
        "keywords": ["4"],
        "explanation": "Use Ohm's Law: R = V / I → R = 12 / 3 = 4 Ω. KEY TIP: Always rearrange the formula clearly and show each step.",
    },
    {
        "topic": "Waves",
        "question": "A wave has a frequency of 50 Hz and a wavelength of 2 m. What is its speed?",
        "answer": "100 m/s",
        "keywords": ["100"],
        "explanation": "Use: v = fλ → v = 50 × 2 = 100 m/s. KEY TIP: v = fλ is one of the most tested formulas. Memorise it.",
    },
    {
        "topic": "Pressure",
        "question": "What is the pressure at the bottom of a 4 m deep tank of water? (density = 1000 kg/m³, g = 10 m/s²)",
        "answer": "40,000 Pa",
        "keywords": ["40000", "40,000"],
        "explanation": "Use: P = ρgh → P = 1000 × 10 × 4 = 40,000 Pa. KEY TIP: Always check units — density must be in kg/m³.",
    },
    {
        "topic": "Radioactivity",
        "question": "What type of radiation is most penetrating and requires thick lead to stop it?",
        "answer": "Gamma radiation",
        "keywords": ["gamma"],
        "explanation": "Gamma is electromagnetic radiation — most penetrating. Alpha: stopped by paper. Beta: stopped by aluminium. Gamma: needs thick lead or concrete. KEY TIP: Learn the penetration order — it comes up repeatedly.",
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


def check_answer(user_answer, keywords):
    return any(kw.lower() in user_answer.lower() for kw in keywords)


def build_question_indices(progress):
    weak_topics = progress.get("weak_topics", {})
    indices = list(range(len(QUESTIONS)))
    for i, q in enumerate(QUESTIONS):
        if weak_topics.get(q["topic"], 0) > 0:
            indices.append(i)
    random.shuffle(indices)
    return indices


@app.route("/")
def home():
    progress = load_progress()
    return render_template("index.html", progress=progress)


@app.route("/start")
def start():
    progress = load_progress()
    progress["sessions"] += 1
    save_progress(progress)

    indices = build_question_indices(progress)
    session["question_indices"] = indices
    session["current"] = 0
    session["score"] = 0
    session["missed"] = []
    session["wrong_topics"] = {}

    return redirect(url_for("question"))


@app.route("/question")
def question():
    indices = session.get("question_indices", [])
    current = session.get("current", 0)

    if current >= len(indices):
        return redirect(url_for("summary"))

    q_index = indices[current]
    q = QUESTIONS[q_index]
    total = len(indices)

    return render_template("question.html", question=q, current=current + 1, total=total)


@app.route("/answer", methods=["POST"])
def answer():
    user_answer = request.form.get("answer", "").strip()
    current = session.get("current", 0)
    indices = session.get("question_indices", [])
    q_index = indices[current]
    q = QUESTIONS[q_index]

    correct = check_answer(user_answer, q["keywords"])

    if correct:
        session["score"] = session.get("score", 0) + 1
        progress = load_progress()
        if q["topic"] in progress["weak_topics"]:
            progress["weak_topics"][q["topic"]] = max(0, progress["weak_topics"][q["topic"]] - 1)
            save_progress(progress)
    else:
        missed = session.get("missed", [])
        missed.append({"topic": q["topic"], "question": q["question"], "answer": q["answer"], "explanation": q["explanation"]})
        session["missed"] = missed

        wrong_topics = session.get("wrong_topics", {})
        wrong_topics[q["topic"]] = wrong_topics.get(q["topic"], 0) + 1
        session["wrong_topics"] = wrong_topics

    session["current"] = current + 1
    total = len(indices)

    return render_template(
        "feedback.html",
        correct=correct,
        question=q,
        user_answer=user_answer,
        current=current + 1,
        total=total,
    )


@app.route("/summary")
def summary():
    score = session.get("score", 0)
    missed = session.get("missed", [])
    wrong_topics = session.get("wrong_topics", {})
    total = len(session.get("question_indices", []))

    progress = load_progress()
    for topic, count in wrong_topics.items():
        progress["weak_topics"][topic] = progress["weak_topics"].get(topic, 0) + count
    save_progress(progress)

    return render_template("summary.html", score=score, total=total, missed=missed)


if __name__ == "__main__":
    app.run(debug=True)
