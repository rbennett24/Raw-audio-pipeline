from pydub import AudioSegment
import glob
import os
from pathlib import Path

# Update path
path = "C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/"
os.chdir(path) # Set base path as working directory
mp3_files = glob.glob(os.path.join("./mp3s/", "*.mp3")) # Not case sensitive

outputPath = "./initial_recordings/"
if not os.path.exists(outputPath):
    os.mkdir(outputPath)

for m in mp3_files:
	sound = AudioSegment.from_mp3(m)
	sound.export(outputPath + Path(m).stem + ".wav", format="wav")