import IPython
from fasttrackpy import process_audio_file, \
    process_directory, \
    process_audio_textgrid,\
    process_corpus
from pathlib import Path

import polars as pl
# import plotly.express as px

import csv

###########
# TO DO: CODE THAT MOVES FILES FROM INPUT TO A "corpus" SUBFOLDER FIRST
###########

# Your corpus should be in a folder *without any other subfolders*. Otherwise, some kind of weird access problems result.
corpus_path = Path("C:/Users/Tiamat/Dropbox/GIT/Raw_audio_pipeline/Raw-audio-pipeline/samples/mfa_aligned/","corpus")

all_vowels = process_corpus(corpus_path)


big_df = pl.concat(
    [cand.to_df() for cand in all_vowels], # Should just return winners
    how = "diagonal"
    )

unique_groups = big_df \
    .select("file_name", "group", "id") \
    .unique() \
    .group_by(["file_name", "group"]) \
    .count()

# print(big_df[0:5])
# print(unique_groups[0:5])

# with open(Path(corpus_path,'fasttrack.csv'), 'w', newline='') as csvfile:
# 	writer = csv.writer(csvfile)
# 	writer.writerows(big_df)