import os
from fingerprint import generate_hashes
from database import create_database, add_to_database, save_database, load_database

SONGS_FOLDER = "songs/"

def build_database():
    db = load_database()

    songs = [f for f in os.listdir(SONGS_FOLDER) if f.endswith(".wav") or f.endswith(".mp3")]

    if not songs:
        print("No songs found in songs/ folder!")
        return

    print(f"Found {len(songs)} songs to process...")

    for i, filename in enumerate(songs):
        filepath = os.path.join(SONGS_FOLDER, filename)
        song_id = filename  # use filename as unique identifier

        print(f"[{i+1}/{len(songs)}] Processing: {song_id}")

        try:
            hashes = generate_hashes(filepath)
            add_to_database(db, song_id, hashes)
            print(f"   Added {len(hashes)} hashes")

        except Exception as e:
            print(f"   Failed: {e}")
            continue

    # save to disk
    save_database(db)
    print("Done! Database is ready.")

if __name__ == "__main__":
    build_database()