import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
import numpy as np
import noisereduce as nr
from collections import defaultdict
from fingerprint import generate_hashes
from database import load_database

# recording settings
SAMPLE_RATE = 44100
DURATION = 20
FILENAME = "query.wav"
CLEAN_FILENAME = "query_clean.wav"
MIN_SCORE = 50

def record_audio():
    print("Recording... play the song now!")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    print("Done recording!")

    data = recording.flatten().astype(np.float32)

    # amplify
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val * 0.8 * 32767

    data = data.astype(np.int16)
    write(FILENAME, SAMPLE_RATE, data)

    # denoise
    noise_sample = data[:SAMPLE_RATE // 2]
    reduced = nr.reduce_noise(y=data.astype(float), sr=SAMPLE_RATE, y_noise=noise_sample.astype(float))
    reduced_int16 = np.clip(reduced, -32767, 32767).astype(np.int16)
    write(CLEAN_FILENAME, SAMPLE_RATE, reduced_int16)

    return CLEAN_FILENAME

def match(query_hashes, db):
    candidates = defaultdict(int)

    for hash_value, query_t1 in query_hashes:
        if hash_value in db:
            for song_id, db_t1 in db[hash_value]:
                delta_t = db_t1 - query_t1
                delta_t_binned = (delta_t // 100) * 100
                candidates[(song_id, delta_t_binned)] += 1

    if not candidates:
        return None, 0

    best_match, best_score = max(candidates.items(), key=lambda x: x[1])
    song_id, delta_t = best_match
    return song_id, best_score

def recognize():
    db = load_database()

    filepath = record_audio()

    print("Generating fingerprint...")
    query_hashes = generate_hashes(filepath)
    print(f"Generated {len(query_hashes)} hashes from recording")

    # DEBUG — check how many query hashes exist in db
    found_in_db = 0
    for hash_value, t1 in query_hashes:
        if hash_value in db:
            found_in_db += 1
    print(f"Hashes found in database: {found_in_db}/{len(query_hashes)}")

    # DEBUG — check db has hashes for your song
    song_name = "505-Arctic Monkeys(youtube)"  # replace with exact filename in db
    song_hashes = [(k, v) for k, vals in db.items() for v in vals if v[0] == song_name]
    print(f"Total hashes in db for {song_name}: {len(song_hashes)}")

    # match
    song_id, score = match(query_hashes, db)
    print(f"Best match: {song_id} with score: {score}")

if __name__ == "__main__":
    recognize()

