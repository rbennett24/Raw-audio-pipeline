# https://github.com/timmahrt/praatIO/blob/main/examples/split_audio_on_tier.py
"""
Praatio example of extracting a separate wav file for each labeled entry in a textgrid tier
ONLY labelled intervals will be extracted, not empty intervals.
"""
import os
from os.path import join
from praatio import praatio_scripts # praatio v6.2.0
import glob
from pydub import AudioSegment, effects # pydub v0.25.1
from pathlib import Path # pathlib v1.0.1
import shutil

####################
# Input .wav and .TextGrid files are expected in .../samples/initial_recordings/
# Output .wav files will be saved in .../samples/mfa_input/
# Amplitude normalized .wav files will be saved in .../samples/normalized/
####################

# Update path
computer = "510fu"
path = "C:/Users/%s/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/" % computer
os.chdir(path) # Set base path as working directory
outputPath = "./mfa_input/"

if not os.path.exists(outputPath):
    os.mkdir(outputPath)

if not os.path.exists("./normalized/"):
    os.mkdir("./normalized/")

wav_files = glob.glob(os.path.join("./initial_recordings/", "*.wav")) # Not case sensitive

for wav in wav_files:

    # Create normalized version of .wav
    rawsound = AudioSegment.from_file(wav)
    normalizedsound = effects.normalize(rawsound)
    normWav = "./normalized/" + Path(wav).stem + ".wav"
    normalizedsound.export(normWav, format="wav")

    praatio_scripts.splitAudioOnTier(
        normWav, # Input .wav file
        wav.replace(".wav","_diarized.TextGrid"), # Input .TextGRid file
        "DetectedSpeech", # Tier
        outputPath, # Output path
        outputTGFlag = False # We don't want chunked .TextGrids here, just the .wav files.
    )


# If you like, delete the file location with normalized .wav files
# after processing is done.
shutil.rmtree("./normalized/")