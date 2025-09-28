# Raw audio pipeline
Scripts for processing raw, untranscribed audio to time-aligned word- and segment-level annotations


**************
Goals:
* Extend beyond English
* Connect parts of the pipeline together as single-step processes whenever possible.
* Other types of flexibility?
**************

0. If needed, convert mp3 files to .wav using mp3_to_wav_converter.py

1. Get raw audio (.wav format)

2. Apply diarization.py to generate a .TextGrid delimiting regions of speech.

3. Hand correct speech detection from diarization.py

4. Apply extract_short_wavs.py to extract all labeled intervals from diarization

	=> To do: apply volume normalization first

5. Apply speech recognition to generate .txt transcripts with whisper_transcription.py

	=> This is slow.

6. Correct transcripts

(7) Apply forced alignment with run_mfa.py, using the [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/)

(8) Correct alignments

(END) Analyze your data

	=> FOR FUN, LET'S DO CLASSIC VOWEL SPACE STUFF (MAYBE FOR EACH SPEAKER, AND AS A FUNCTION OF DURATION) and see what it looks like with ZERO hand correction.
	
	=> Use Fastrak for this? That seems good, though you want to speed it up by stripping out everything except the vowels, right? Or does Fastrak not bother with sounds it doesn't identify as vowels? See https://github.com/santiagobarreda/FastTrack/blob/master/Fast%20Track/functions/file_5_extractVowelswithTG.praat