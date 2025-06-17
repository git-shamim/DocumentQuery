import os
import json

FEEDBACK_FILE = os.path.join("data", "feedback.json")


def load_feedback():
    """Loads existing feedback from JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def save_feedback(entry):
    """
    Appends a new feedback entry to the feedback.json file.

    Args:
        entry (dict): Contains keys like question, answer, feedback, notes.
    """
    data = load_feedback()
    data.append(entry)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def create_feedback_entry(question, answer, feedback, clarification=None):
    """
    Creates a structured feedback entry.

    Args:
        question (str): User's original question.
        answer (str): Initial LLM-generated answer.
        feedback (str): '👍' or '👎'.
        clarification (str): Optional notes from user.

    Returns:
        dict: Feedback record
    """
    return {
        "question": question,
        "answer": answer,
        "feedback": feedback,
        "clarification": clarification or ""
    }
