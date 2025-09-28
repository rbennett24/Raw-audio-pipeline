# https://github.com/timmahrt/praatIO/blob/main/examples/split_audio_on_tier.py
"""
Praatio example of extracting a separate wav file for each labeled entry in a textgrid tier
ONLY labelled intervals will be extracted, not empty intervals.
"""
import os
from os.path import join
from praatio import praatio_scripts
import glob

# Update path
path = "C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/"
outputPath = join(path, "mfa_input/")

if not os.path.exists(outputPath):
    os.mkdir(outputPath)

wav_files = glob.glob(os.path.join(path+"initial_recordings/", "*.wav")) # Not case sensitive

for wav in wav_files:
    # TO DO: normalize input .wav first.
    praatio_scripts.splitAudioOnTier(
        join(path, wav), join(path, wav.replace(".wav","_diarized.TextGrid")), "DetectedSpeech", outputPath,
        # In this case, we don't actually want the .TextGrids that splitAudioOnTier generates.
        outputTGFlag = False
    )

