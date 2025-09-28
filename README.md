# Raw audio pipeline
Scripts for processing raw, untranscribed audio to time-aligned word- and segment-level annotations


**************
* Goals:
* -- Extend beyond English
* -- Connect parts of the pipeline together as single-step processes whenever possible.
* -- Other types of flexibility?
**************

(0) If needed, convert mp3 files to .wav using mp3_to_wav_converter.py

(1) Get raw audio (.wav format)

(2) Apply diarization.py to generate a .TextGrid delimiting regions of speech.

	=> MAKE THIS ITERATE OVER FILES IN A FOLDER

(3) Hand correct speech detection from diarization.py

(4) Apply extract_short_wavs.py to extract all labeled intervals from diarization

	=> APPLY VOLUME NORMALIZATION FIRST? How to do this in PraatIO?

(5) Apply speech recognition to generate .txt transcripts with whisper_transcription.py

	=> This is slow, but pretty good!

(6) Correct transcripts

(7) Apply mfa

	=> WRITE A PYTHON SCRIPT TO DO THIS.
	
	conda activate mfaaligner

	mfa model download dictionary english_us_mfa --ignore_cache

	mfa model download acoustic english_mfa --ignore_cache

	mfa validate --clean C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/mfa_input/ english_us_mfa english_mfa --speaker_characters 5
	
	mfa align --clean C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/mfa_input/ english_us_mfa english_mfa --speaker_characters 5 C:/Users/Tiamat/Dropbox/Research/Speech_corpora/charsiu_testing/mfa_aligned/

(8) Correct alignments

(END) Analyze your data

	=> FOR FUN, LET'S DO CLASSIC VOWEL SPACE STUFF (MAYBE FOR EACH SPEAKER, AND AS A FUNCTION OF DURATION) and see what it looks like with ZERO hand correction.
	
	=> Use Fastrak for this? That seems good, though you want to speed it up by stripping out everything except the vowels, right? Or does Fastrak not bother with sounds it doesn't identify as vowels? See https://github.com/santiagobarreda/FastTrack/blob/master/Fast%20Track/functions/file_5_extractVowelswithTG.praat