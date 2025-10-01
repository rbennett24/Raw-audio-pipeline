# https://github.com/pyannote/pyannote-audio?tab=readme-ov-file
# pip install pyannote.audio
# pip install huggingface_hub[hf_xet]
from pyannote.audio import Pipeline # pyannote v3.4.0; torch-audiomentations v0.12.0; torch_pitch_shift v1.2.5;
                                    # torchaudio v2.8.0; torchmetrics v1.8.2; torchvision v0.23.0; ffmpeg 1.4
import string
import textgrid # textgrid v1.5 and v.1.6.1 both seem to work
import csv
import os
import glob

####################
# Input .wav files are expected in .../samples/initial_recordings/
# Output .TextGrid files will be saved in .../samples/initial_recordings/
####################

# I have a Hugging Face token stored on my desktop computer as an environmental variable.
# We access it here, without publishing it in the code itself, for security reasons.
# To get an HF token, go to https://huggingface.co/settings/tokens, and set fine grained
# permissions to approve "Read access to contents of all public gated repos you can access".
# In Windows, on the command line, use <set HF_TOKEN = "YOUR_ACTUAL_TOKEN_CODE"> to store the token locally.
access_token = os.environ.get('HF_TOKEN')

# There's a problem using the access_token from some computers, I don't know what the issue is
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=access_token) # Huggingface token; make sure token has "Read access to contents of all public gated repos you can access" enabled

# send pipeline to GPU (when available)
import torch
# pipeline.to(torch.device("cuda")) # CUDA needs to be installed from NVIDIA

# Update path
computer = "510fu"
path = "C:/Users/%s/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/" % computer
os.chdir(path) # Set base path as working directory
wav_files = glob.glob(os.path.join("./initial_recordings/", "*.wav")) # Not case sensitive

for w in wav_files:
    inputWav = w

    # apply pretrained pipeline    
    # It's useful to set  the number of speakers expected in the files
    # This code assumes one speaker, but could be extended to process all speakers detected and stored in the CSV file generated below e.g. as different tiers.
    # Setting max_speakers REALLY speeds up the process!
    diarization = pipeline(inputWav,min_speakers=1, max_speakers=1) 

    tmpCSV = inputWav.lower().replace(".wav","_diarized.csv")
    # print(tmpCSV)
    with open(tmpCSV, "w", encoding="utf-8") as file:
        file.write('start_time,end_time,speaker\n')
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            outText = f"{turn.start},{turn.end},{speaker}\n"
            file.write(outText)

    # Load the CSV data
    with open(tmpCSV,
              "r", encoding="utf-8") as f:
        reader = csv.DictReader(f,
                                delimiter=","  # If semicolon separated, not comma
                                )
        data = [row for row in reader]

    # Create a TextGrid object
    # https://linguistics.stackexchange.com/questions/47676/how-to-populate-tiers-in-a-praat-textgrid-based-on-another-text-file
    grid = textgrid.TextGrid()

    # Create IntervalTier objects
    speech_tier = textgrid.IntervalTier(name="DetectedSpeech")

    # Populate the interval tiers
    for row in data:
        start_time = float(row["start_time"])
        end_time = float(row["end_time"])
        speech_tier.add(start_time, end_time, row["speaker"])

    # Add the interval tiers to the TextGrid
    grid.append(speech_tier)

    # Write the TextGrid to a file
    with open(inputWav.replace(".wav","").replace(".WAV","")+"_diarized.TextGrid", "w", encoding="utf-8") as f:
        grid.write(f)

    # Check if the file exists before attempting to delete
    if os.path.exists(tmpCSV):
        try:
            os.remove(tmpCSV)
            # print(f"File '{tmpCSV}' deleted successfully.") # Notifications not really needed.
        except OSError as e:
            print(f"Error deleting file '{tmpCSV}': {e}")
    else:
        print(f"File '{tmpCSV}' does not exist.")