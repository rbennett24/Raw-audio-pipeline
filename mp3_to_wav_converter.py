from pydub import AudioSegment
import glob
import os
from pathlib import Path

# Update path
path = "C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/"
mp3_files = glob.glob(os.path.join(path+"mp3s/", "*.mp3")) # Not case sensitive

for m in mp3_files:
	sound = AudioSegment.from_mp3(m)
	sound.export(path + "initial_recordings/" + Path(m).stem + ".wav", format="wav")