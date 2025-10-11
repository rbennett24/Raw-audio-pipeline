##############
# TO DO:
# -- Speed up .TextGrid merging method.
##############

import os
import shutil
import subprocess
from pathlib import Path
import glob
from aligned_textgrid import AlignedTextGrid
from aligned_textgrid import Word, Phone
import pandas as pd

# https://fasttrackiverse.github.io/fasttrackpy/usage/getting_started.html
# fasttrackpy is intended for command line use,
# though there are more 'Pythonic' options (https://fasttrackiverse.github.io/fasttrackpy/usage/pythonic_use.html)

####################
# Input .wav and .TextGrid files are expected in .../samples/mfa_aligned/
# Output .csv file will be saved in .../samples/mfa_aligned/
####################

####################
# Parameters to set

# A regular expression telling FastTrack what vowel symbols to look for. Default is [AEIOU], i.e. English ARPABET.
# This is currently not working very well outside of English.
vlabels = "[AEIOUaeiouãẽĩõũ]"

# Update path as needed
computer = "Tiamat"
baseFileFolder = "spanish" # samples, spanish
####################
basePath = f"C:/Users/{computer}/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/{baseFileFolder}/mfa_aligned/"
os.chdir(basePath) # Set base path as working directory

# Your corpus should be in a folder *without any other subfolders*. Otherwise, some kind of weird access problems result.
# We try to guarantee that here.
inputPath = basePath + "corpus/"
if not os.path.exists(inputPath):
    os.mkdir(inputPath)
wav_files = glob.glob(os.path.join(basePath, '*.wav'))
for w in wav_files:
	copyWavTo = inputPath + Path(w).stem + ".wav"
	shutil.copy(w, copyWavTo)

	copyTGFrom = basePath + Path(w).stem + ".TextGrid"
	copyTGTo = inputPath + Path(w).stem + ".TextGrid"
	shutil.copy(copyTGFrom, copyTGTo)

outputPath = inputPath

command = f"fasttrack corpus --target-labels \"{vlabels}\" --corpus {inputPath} --output fasttrack.csv"
subprocess.Popen(["start", "cmd", "/k", command], shell=True)


###########
# Iterate over all TextGrids in inputPath and extract relevant info, to be merged via id column
# later with output of fasttrackpy
# https://forced-alignment-and-vowel-extraction.github.io/alignedTextGrid/usage/
tg_files = glob.glob("*.TextGrid") # Not case sensitive

####################
# THIS IS AN UNNECESSARILY SLOW WAY OF SAVING TEXTGRIDS,
# BECAUSE pd.concat() COPIES THE ENTIRE TEXTGRID EACH TIME
# I'VE TRIED OTHER TECHNIQUES, E.G. POPULATING A LIST IN THE LOOP,
# THEN CONVERTING THE LIST TO A PANDAS DATAFRAME AFTER THE LOOP IS OVER,
# BUT I CAN'T GET THE OUTPUT FORMATTED CORRECTLY.
####################
outputPDframe = pd.DataFrame()
for tg in tg_files:
	tgParsed = AlignedTextGrid(textgrid_path = tg, entry_classes=[Word, Phone])

	phone_tier = tgParsed.group_0.Phone

	tgPDframe = pd.DataFrame({
	  "phone":    [p.label for p in phone_tier], # This will get all annotations, not just vowels. You can filter later in R.
	  "id":       [p.id for p in phone_tier],
	  "fol":      [p.fol.label for p in phone_tier],
	  "prev":     [p.prev.label for p in phone_tier],
	  "word":     [p.within.label for p in phone_tier],
	  "start":    [p.start for p in phone_tier],
	  "end":      [p.end for p in phone_tier],
	  "file_name": tg.replace(".TextGrid","")
	})

	outputPDframe = pd.concat([outputPDframe, tgPDframe])

outputPDframe.to_csv('fasttrack_TextGrid_data.csv', index=False)


# The following doesn't currently work, because FastTrack is called from the command line, rather than in a more pythonic way.
# That causes the folder to get deleted before it's processed! 
# https://fasttrackiverse.github.io/fasttrackpy/usage/pythonic_use.html
# Get rid of the corpus folder, which is redundant.
# shutil.rmtree(inputPath) 