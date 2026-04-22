from fingerprint import generate_hashes, get_freq_band
import numpy as np

# get hashes from clean file
clean_hashes = generate_hashes("songs/505 - Arctic Monkeys (youtube).wav")
clean_hash_values = set(h[0] for h in clean_hashes)

# get hashes from recording
query_hashes = generate_hashes("query_clean.wav")
query_hash_values = set(h[0] for h in query_hashes)

# compare
overlap = clean_hash_values & query_hash_values
print(f"Clean file unique hashes: {len(clean_hash_values)}")
print(f"Recording unique hashes: {len(query_hash_values)}")
print(f"Overlapping hashes: {len(overlap)}")
print(f"Overlap percentage: {len(overlap)/len(clean_hash_values)*100:.1f}%")

# check band distribution
clean_bands = [h[0][0] for h in clean_hashes]
query_bands = [h[0][0] for h in query_hashes]
print(f"\nClean file band distribution: {np.unique(clean_bands, return_counts=True)}")
print(f"Recording band distribution: {np.unique(query_bands, return_counts=True)}")