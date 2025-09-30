import os 
import subprocess
from pathlib import Path

# https://fasttrackiverse.github.io/fasttrackpy/usage/getting_started.html
# fasttrackpy is intended for command line use,
# though there are more 'Pythonic' options (https://fasttrackiverse.github.io/fasttrackpy/usage/pythonic_use.html)

###########
# TO DO: CODE THAT MOVES FILES FROM INPUT TO A "corpus" SUBFOLDER FIRST, so that input files are successfully isolated from the subfolder problem?
###########

# Your corpus should be in a folder *without any other subfolders*. Otherwise, some kind of weird access problems result.
inputPath = "C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_aligned/corpus/"
os.chdir(inputPath) # Set base path as working directory


outputPath = inputPath

command = "fasttrack corpus --corpus %s --output %s" % (inputPath,"fasttrack.csv")

subprocess.Popen(["start", "cmd", "/k", command], shell=True)