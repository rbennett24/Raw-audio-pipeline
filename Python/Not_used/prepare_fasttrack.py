import shutil
import os
import glob
from praatio import textgrid

# inputPath = "C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/"
inputPath = "C:/Users/510fu/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/"
os.chdir(inputPath + "/mfa_aligned/") # Set base path as working directory

# List characters which define vowel intervals
# In general, we'll look with intervals which BEGIN with these
# symbols, because that should create more robustness for
# diphthongs, diacritics, etc.
vsyms = ["A","I","E","O","U"]

# Create working folder 'sounds'
outputPath = "./sounds/"
if not os.path.exists(outputPath):
    os.mkdir(outputPath)

# Read in .TextGrids
tg_files = glob.glob(os.path.join("", "*.TextGrid")) # Not case sensitive

# Inspect TextGrids
for tgPath in tg_files:
	tg = textgrid.openTextgrid(r"%s" % tgPath, False)
	wds = tg._tierDict["words"].entries # Get all intervals
	segs = tg._tierDict["phones"].entries
	vowels = []
	for s in segs:
		if s[2][0] in vsyms: # Find intervals with labels (index 2) beginning in a licit vowel symbol
			vowels.append(s)

	# Extract .wav and .TextGrid files corresponding to each vowel, with padding for FastTrack
	for v in vowels:
		intervalCutStart = float(v[0]-0.025)
		print(intervalCutStart)
		# Make sure file name is informative

############
# HEREHERE HEREHERE
############
# Fast Track is intended to analyze sound files that contain only a single vowel sound, or vowel nucleus.
#
# So extract each vowel, surrounding sounds, and the word-level transcription, into separate .wav and .TextGrid files.
# Do you need to strip out non-vowel annotations?
#
# Which Praat utility do you want for this? praatio again?



# # Copy over .wav files
# wav_files = glob.glob(os.path.join("", "*.wav")) # Not case sensitive

# for w in wav_files:
# 	newLocation = "./sounds/" + w
# 	shutil.copy(w,newLocation)

