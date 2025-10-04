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

computer = "510fu"
basePath = "C:/Users/%s/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_aligned/" % computer
os.chdir(basePath) # Set base path as working directory

# Your corpus should be in a folder *without any other subfolders*. Otherwise, some kind of weird access problems result.
# We try to guarantee that here.
inputPath = basePath + "corpus/"
os.makedirs(inputPath, exist_ok=True)
wav_files = glob.glob(os.path.join(basePath, '*.wav'))
for w in wav_files:
	copyWavTo = inputPath + Path(w).stem + ".wav"
	copyTGTo = inputPath + Path(w).stem + ".TextGrid"
	copyTGFrom = basePath + Path(w).stem + ".TextGrid"
	shutil.copy(w, copyWavTo)
	shutil.copy(copyTGFrom, copyTGTo)

outputPath = inputPath

command = "fasttrack corpus --corpus %s --output %s" % (inputPath,"fasttrack.csv")
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