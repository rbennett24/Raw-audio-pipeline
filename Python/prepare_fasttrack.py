import shutil
import os
import glob

inputPath = "C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/"
os.chdir(inputPath + "/mfa_aligned/") # Set base path as working directory

# Create working folder 'sounds'
outputPath = "./sounds/"
if not os.path.exists(outputPath):
    os.mkdir(outputPath)


# Copy over .wav files
wav_files = glob.glob(os.path.join("", "*.wav")) # Not case sensitive

for w in wav_files:
	newLocation = "./sounds/" + w
	shutil.move(w,newLocation)


############
# HEREHERE HEREHERE
############

# Load TextGrids, strip them of all intervals *except* vowel intervals, then
# copy them over.