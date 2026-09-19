# Seeds the database with the game's predefined words.
from backend.database.connection import SessionLocal
from backend.database.models import Word


WORDS = [
    "APPLE",
    "HOUSE",
    "MOUSE",
    "TIGER",
    "WATER",
    "WORLD",
    "PLANT",
    "TRAIN",
    "CHAIR",
    "LIGHT",
    "STONE",
    "CLOUD",
    "BRAIN",
    "GREEN",
    "BLACK",
    "SMILE",
    "DREAM",
    "RIVER",
    "MUSIC",
    "POWER",
]


def seed_words():
    db = SessionLocal()
    # this is add the unique words
    try:
        for word in WORDS:

            existing_word = (
                db.query(Word)
                .filter(Word.word == word)
                .first()
            )

            if not existing_word:
                db.add(Word(word=word))

        db.commit()

        print("Words seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_words()