from collections import defaultdict
import pickle
import os

DB_PATH = "database.pkl"

def create_database():
    return defaultdict(list)

def add_to_database(db, song_id, hashes):
    for hash_value, t1 in hashes:
        # make sure we're appending not overwriting
        if hash_value not in db:
            db[hash_value] = []
        db[hash_value].append((song_id, t1))

def save_database(db):
    with open(DB_PATH, "wb") as f:
        pickle.dump(dict(db), f)
    print(f"Database saved! Total unique hashes: {len(db)}")

def load_database():
    if not os.path.exists(DB_PATH):
        print("No database found, creating new one...")
        return create_database()
    with open(DB_PATH, "rb") as f:
        db = pickle.load(f)
    print(f"Database loaded! Total unique hashes: {len(db)}")
    return db