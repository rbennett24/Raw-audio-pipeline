from pydub import AudioSegment, effects # pydub v0.25.1
import glob
import os
from pathlib import Path # pathlib v1.0.1

####################
# Input .mp3 files are expected in .../samples/
# Output .wav files will be saved in .../samples/initial_recordings/
# Output .wav files will be amplitude normalized.
####################

# Update path
computer = "Tiamat"
path = "C:/Users/%s/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/" % computer
os.chdir(path) # Set base path as working directory
mp3_files = glob.glob(os.path.join("./mp3s/", "*.mp3")) # Not case sensitive

outputPath = "./initial_recordings/"
if not os.path.exists(outputPath):
    os.mkdir(outputPath)

for m in mp3_files:
	sound = AudioSegment.from_mp3(m)
	normalizedsound = effects.normalize(sound)
	normalizedsound.export(outputPath + Path(m).stem + ".wav", format="wav")
