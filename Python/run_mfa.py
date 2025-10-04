##############
# TO DO:
# -- Deal with out of dictionary (OOV) words in the input. These can be found at C:\Users\...\Documents\MFA\mfa_input\, in the files:
# 		* oov_counts_<DICTIONARY NAME>.txt
# 	 	* utterance_oovs.txt
#		* oovs_found_<DICTIONARY NAME>.txt
##############


# This script assumes that the montreal forced aligner is set up
# as <mfaaligner> in your conda environment (<conda create -n mfaaligner -c conda-forge montreal-forced-aligner> or <mamba create -n mfaaligner -c conda-forge montreal-forced-aligner>)
#
# Follow the installation instructions here:
# https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html#general-installation
#
# On Windows, you'll also need to make sure that conda is in Path.
# You can do this in Powershell. Add the string <%USERPROFILE%\Anaconda3\condabin> to the list of locations included in the user Path variable.
# To really be thorough, you can do the same with <%USERPROFILE%\Anaconda3\>, <%USERPROFILE%\Anaconda3\Library\Bin> and <%USERPROFILE%\Anaconda3\Scripts>.
# Note: install anaconda, not miniconda.
# Also, you probably need to restart your computer after editing the Path variables.

import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import glob
import os
import shutil

# Parameters
mfadict = "english_us_arpa" # "english_us_mfa"
mfamodel = "english_us_arpa" # "english_mfa"
spkPrefixLen = "2"

####################
# Input .wav and .text files are expected in .../samples/mfa_input/
# Output .txt files will be saved in .../samples/mfa_aligned/
####################

# Update path as needed
computer = "510fu"
inputPath = "C:/Users/%s/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_input/" % computer
os.chdir(inputPath) # Set base path as working directory


# For GUI prompts
root = tk.Tk()
root.withdraw() # Hide the main window if you only want the prompt


##
# Check if dictionary is installed: if not, install it; and if it is already installed, ask if it should be updated.
# In principle you could do this by seeing what files are actually on the computer, but I'd prefer to do it 
# in such a way that we're literally asking what models the mfa aligner can find.
# Same for acoustic models below.

dictSearch = "conda activate mfaaligner && mfa model list dictionary"
dictList = subprocess.run(dictSearch, capture_output=True, shell=True)

command = "conda activate mfaaligner && mfa model download dictionary " + mfadict + " --ignore_cache"

if mfadict in dictList.stdout.decode():
	print("Dictionary found! Asking about update...")

	############
	# Update chosen dictionary file?
	result = messagebox.askyesno(title="Download dictionary file?",
								 message=("Do you want to download and update the %s dictionary model?" % mfadict))

	if result == True:
		print("Upgrading .dict file...")
		
		# Open command line, start conda, force download of newest version of dictionary
		ret = subprocess.run(command, capture_output=True, shell=True)
		print(ret.stdout.decode())
		if len(ret.stderr.decode()) > 0:
			print("Something went wrong with the dictionary download! You may want to download manually from the MFA website.")

else:
	print("Attempting to download dictionary %s from MFA website..." % mfadict)
	ret = subprocess.run(command, capture_output=True, shell=True)
	print(ret.stdout.decode())
	if len(ret.stderr.decode()) > 0:
		print("Something went wrong with the dictionary download! You may want to download manually from the MFA website.")


##
# Check if acoustic model is installed: if not, install it; and if it is already installed, ask if it should be updated.

acousticSearch = "conda activate mfaaligner && mfa model list acoustic"
acousticList = subprocess.run(acousticSearch, capture_output=True, shell=True)

command = "conda activate mfaaligner && mfa model download acoustic " + mfamodel + " --ignore_cache"

if mfamodel in acousticList.stdout.decode():
	print("Acoustic model found! Asking about update...")

	# Update chosen acoustic model?
	result = messagebox.askyesno(title="Download acoustic model?",
							     message=("Do you want to download and update the %s acoustic model?" % mfamodel))

	if result == True:
		print("Upgrading acoustic model...")
		
		# Open command line, start conda, force download of newest version of acoustic model
		ret = subprocess.run(command, capture_output=True, shell=True)
		print(ret.stdout.decode())
		if len(ret.stderr.decode()) > 0:
			print("Something went wrong with the acoustic model download! You may want to download manually from the MFA website.")

else:
	print("Attempting to download acoustic model %s from MFA website..." % mfamodel)
	ret = subprocess.run(command, capture_output=True, shell=True)
	print(ret.stdout.decode())
	if len(ret.stderr.decode()) > 0:
		print("Something went wrong with the acoustic model download! You may want to download manually from the MFA website.")


#######################
# TO EXTEND: MODEL TRAINING to languages without pre-existing acoustic models.
# We'll probably want some other tools for generating pronunciation dictionaries, like the XPF
# workflow you've used for A'ingae forced alignment.
#######################


############
# Run validation?
result = messagebox.askyesno(title="Run validation?",
								   message=("Do you want to run validation before aligning?"))

if result == True:
	print("Running validation...")
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
	print("Running alignment...")
	outPutLoc = inputPath.replace("mfa_input","mfa_aligned")
	Path(outPutLoc).mkdir(parents=True, exist_ok=True)

	# Open command line, start conda, force download of newest version of dictionary
	command = "conda activate mfaaligner && mfa align --clean " + inputPath + " " + mfadict + " " + mfamodel + " --speaker_characters " + spkPrefixLen + " " + outPutLoc

	subprocess.Popen(["start", "cmd", "/k", command], shell=True)


	############
	# Move .wav files
	resultMove = messagebox.askyesno(title="Copy .wav files?",
									   message=("Do you want to copy the input .wav files to the folder which contains the aligned .TextGrids?\n(You should wait until alignment is complete before clicking yes on this!)"))

	if resultMove == True:
		print("Copying input .wav files, and sequestering unaligned .wav files...")
		# Copy all .wav files from input directory to output directory:
		wav_files = glob.glob(os.path.join(inputPath, "*.wav")) # Not case sensitive
		for w in wav_files:
			newLocation = w.replace("mfa_input","mfa_aligned")
			shutil.copy(w,newLocation) # Change back to 'move'?

		# Sequester unaligned .wav files
		unalignedPath = inputPath.replace("mfa_input","mfa_aligned/unaligned_wavs/")
		Path(unalignedPath).mkdir(parents=True, exist_ok=True)

		wav_files = glob.glob(os.path.join(inputPath.replace("mfa_input","mfa_aligned"), "*.wav")) # Not case sensitive
		for w in wav_files:
			if os.path.exists(w.replace(".wav",".TextGrid")):
		 		pass
			else:
				print("Unaligned .wav file: " + w)
				shutil.move(w,w.replace("mfa_aligned","/mfa_aligned/unaligned_wavs/"))


# Terminate GUI
root.destroy()