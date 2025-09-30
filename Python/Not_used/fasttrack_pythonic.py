import IPython
from fasttrackpy import process_audio_file, \
    process_directory, \
    process_audio_textgrid,\
    process_corpus
from pathlib import Path

import polars as pl
# import plotly.express as px

import pandas as pd

###########
# TO DO: CODE THAT MOVES FILES FROM INPUT TO A "corpus" SUBFOLDER FIRST
###########

# Your corpus should be in a folder *without any other subfolders*. Otherwise, some kind of weird access problems result.
corpus_path = Path("C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_aligned/","corpus")

all_vowels = process_corpus(corpus_path)

###########
# To do: improve formatting of output before saving. Right now it's not functional.
###########

big_df = pl.concat(
    [cand.to_df() for cand in all_vowels], # Should just return winners
    how = "diagonal"
    )

unique_groups = big_df \
    .select("file_name", "group", "id") \
    .unique() \
    .group_by(["file_name", "group"]) \
    .count()

outputPDframe = pd.DataFrame(big_df)

# print(outputPDframe)
# print(unique_groups)
###########
# To do: change save location
###########
outputPDframe.to_csv('fasttrack.csv', index=False)