import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Parameters
mfadict = "english_us_arpa" # "english_us_mfa"
mfamodel = "english_us_arpa" # "english_mfa"
spkPrefixLen = "5"
inputPath = "C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/mfa_input/"


############
# Update chosen dictionary file?
root = tk.Tk()
root.withdraw() # Hide the main window if you only want the prompt
   
result = messagebox.askyesno(title="Download dictionary file?",
								   message=("Do you want to download and update the %s dictionary model?" % mfadict))

if result == True:
	# Open command line, start conda, force download of newest version of dictionary
	command = "conda activate mfaaligner && mfa model download dictionary " + mfadict + " --ignore_cache"

	ret = subprocess.run(command, capture_output=True, shell=True)

	print(ret.stdout.decode())


############
# Update chosen acoustic model?
result = messagebox.askyesno(title="Download acoustic model?",
								   message=("Do you want to download and update the %s acoustic model?" % mfamodel))

if result == True:
	# Open command line, start conda, force download of newest version of acoustic model
	command = "conda activate mfaaligner && mfa model download acoustic " + mfamodel + " --ignore_cache"

	ret = subprocess.run(command, capture_output=True, shell=True)

	print(ret.stdout.decode())


#######################
# TO EXTEND: MODEL TRAINING
#######################


############
# Run validation?
result = messagebox.askyesno(title="Run validation?",
								   message=("Do you want to run validation before aligning"))

if result == True:
	# Open command line, start conda, force download of newest version of dictionary
	command = "conda activate mfaaligner && mfa validate --clean " + inputPath + " " + mfadict + " --speaker_characters " + spkPrefixLen

	subprocess.Popen(["start", "cmd", "/k", command], shell=True)


#######################
# TO EXTEND: deal with out of dictionary words
# https://montreal-forced-aligner.readthedocs.io/en/v3.0.7/user_guide/dictionary.html#text-normalization-and-dictionary-lookup
#######################

############
# Run alignment?
result = messagebox.askyesno(title="Run alignment?",
								   message=("Are you ready to align your data?"))

if result == True:
	outPutLoc = inputPath.replace("mfa_input","mfa_aligned")
	Path(outPutLoc).mkdir(parents=True, exist_ok=True)

	# Open command line, start conda, force download of newest version of dictionary
	command = "conda activate mfaaligner && mfa align --clean " + inputPath + " " + mfadict + " " + mfamodel + " --speaker_characters " + spkPrefixLen + " " + outPutLoc

	subprocess.Popen(["start", "cmd", "/k", command], shell=True)


# Terminate GUI
root.destroy()