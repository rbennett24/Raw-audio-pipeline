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
inputPath = "C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_input/"
# os.chdir(inputPath) # Set base path as working directory


############
# Update chosen dictionary file?
root = tk.Tk()
root.withdraw() # Hide the main window if you only want the prompt
   
result = messagebox.askyesno(title="Download dictionary file?",
								   message=("Do you want to download and update the %s dictionary model?" % mfadict))

if result == True:
	print("Upgrading .dict file...")
	# Open command line, start conda, force download of newest version of dictionary
	command = "conda activate mfaaligner && mfa model download dictionary " + mfadict + " --ignore_cache"

	ret = subprocess.run(command, capture_output=True, shell=True)

	print(ret.stdout.decode())


############
# Update chosen acoustic model?
result = messagebox.askyesno(title="Download acoustic model?",
								   message=("Do you want to download and update the %s acoustic model?" % mfamodel))

if result == True:
	print("Upgrading acoustic model...")
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
								   message=("Do you want to run validation before aligning?"))

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


	############
	# Move .wav files
	resultMove = messagebox.askyesno(title="Move .wav files?",
									   message=("Do you want to move the input .wav files to the folder which contains the aligned .TextGrids?"))

	if resultMove == True:
		# Copy all .wav files from input directory to output directory:
		wav_files = glob.glob(os.path.join(inputPath, "*.wav")) # Not case sensitive
		for w in wav_files:
			newLocation = w.replace("mfa_input","mfa_aligned")
			shutil.move(w,newLocation)

		# Sequester unaligned .wav files
		unalignedPath = "./mfa_aligned/unaligned_wavs/"
		Path(unalignedPath).mkdir(parents=True, exist_ok=True)

		wav_files = glob.glob(os.path.join(inputPath.replace("mfa_input","mfa_aligned"), "*.wav")) # Not case sensitive
		for w in wav_files:
			if os.path.exists(w.replace(".wav",".TextGrid")):
				pass
			else: 
				print("Unaligned .wav file: " + w)
				shutil.move(w,w.replace("mfa_aligned","/mfa_aligned/unaligned/"))


# Terminate GUI
root.destroy()