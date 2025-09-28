# https://github.com/openai/whisper
# https://github.com/linto-ai/whisper-timestamped
import whisper_timestamped as whisper
import json
import string
import textgrid
import csv
import os
import glob
from pathlib import Path

path = "C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/"
wav_files = glob.glob(os.path.join(path+"mfa_input/", "*.wav")) # Not case sensitive

for inputWav in wav_files:
    print("Processing " + Path(inputWav).name)
    
    result = whisper.transcribe(model="base.en",audio=inputWav,vad=True,beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0))
    # Alternatively:
    # model = whisper.load_model("base.en")
    # result = model.transcribe(inputWav,word_timestamps=True)
    
    # print(result)
    
    # Strip punctuation out, make lowercase, and remove leading/trailing spaces
    outputTranscription = result["text"]
    
    translation_table = str.maketrans("","",string.punctuation)
    outputTranscription = outputTranscription.translate(translation_table).lower().strip()

    # Save unaligned transcript
    with open(inputWav.replace(".wav","").replace(".WAV","")+".txt", "w") as file:
        file.write(outputTranscription)


    ###############################
    # All of the following is commented out.
    # You can uncomment it if you'd like to save .TextGrids corresponding to where
    # whisper thinks the word boundaries are.
    # It's pretty bad, so we skip it, and allow the Montreal Forced Aligner
    # to do this instead (which is much better).
    ###############################

    # translation_table = str.maketrans("","",string.punctuation)

    # tmpCSV = inputWav.lower().replace(".wav","_temp.csv")
    # # print(tmpCSV)
    # with open(tmpCSV, "w", encoding="utf-8") as file:
    #     file.write('start_time,end_time,label\n')
    #     for segment in result['segments']:
    #         outText = ''.join(f"{word['start'].strip()},{word['end'].strip()},{word['text'].translate(translation_table)}\n" for word in segment['words'])
    #         outTextClean = outText.lower()
    #         file.write(outTextClean)

    # # Load the CSV data
    # with open(tmpCSV,
    #           "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f,
    #                             delimiter=","  # If semicolon separated, not comma
    #                             )
    #     data = [row for row in reader]

    # # Create a TextGrid object
    # # https://linguistics.stackexchange.com/questions/47676/how-to-populate-tiers-in-a-praat-textgrid-based-on-another-text-file
    # grid = textgrid.TextGrid()

    # # Create IntervalTier objects
    # wd_tier = textgrid.IntervalTier(name="words")

    # # Populate the interval tiers
    # for row in data:
    #     start_time = float(row["start_time"])
    #     end_time = float(row["end_time"])
    #     wd_tier.add(start_time, end_time, row["label"])

    # # Add the interval tiers to the TextGrid
    # grid.append(wd_tier)

    # # Write the TextGrid to a file
    # with open(inputWav.replace(".wav","").replace(".WAV","")+"_words.TextGrid", "w", encoding="utf-8") as f:
    #     grid.write(f)

    # # Check if the file exists before attempting to delete
    # if os.path.exists(tmpCSV):
    #     try:
    #         os.remove(tmpCSV)
    #         # print(f"File '{tmpCSV}' deleted successfully.") # To tamp down on the number of messages...
    #     except OSError as e:
    #         print(f"Error deleting file '{tmpCSV}': {e}")
    # else:
    #     print(f"File '{tmpCSV}' does not exist.")