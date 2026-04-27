from pydub import AudioSegment

# Load the MP3 file
sound = AudioSegment.from_mp3("input.mp3")

# Export as WAV
sound.export("output.wav", format="wav")