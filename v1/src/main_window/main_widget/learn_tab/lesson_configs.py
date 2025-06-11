from data.constants import LETTER


LESSON_CONFIGS = {
    "Lesson1": {
        "question_format": "pictograph",
        "answer_format": "button",
        "quiz_description": "pictograph_to_letter",
        "question_prompt": "Choose the letter for:",
    },
    "Lesson2": {
        "question_format": LETTER,
        "answer_format": "pictograph",
        "quiz_description": "letter_to_pictograph",
        "question_prompt": "Choose the pictograph for:",
    },
    "Lesson3": {
        "question_format": "pictograph",
        "answer_format": "pictograph",
        "quiz_description": "valid_next_pictograph",
        "question_prompt": "Which pictograph can follow?",
    },
}
