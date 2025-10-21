# Raw audio pipeline
Scripts for processing raw, untranscribed audio to time-aligned word- and segment-level annotations.

Presentation of sample results: https://docs.google.com/presentation/d/1PA5rW-72sAACNJwCbeuTEhJ1aXAPOB9A4i5V8oMv9j0/edit?usp=sharing

**************
Goals/to do:
* Integrate out-of-dictionary processing in the workflow, to more clearly flag words in the corpus missing from the dictionary (e.g. integrate a step which asks you to open the relevant .txt log files).
	* To address OOD words: maybe invoke grapheme-to-phoneme models, when available?

* Stress-test against a wider range of non-English languages

* Adjust workflow so that it's possible to reconstruct the original input .wav files in their entirety, including pauses and all other material which is currently excised and left untranscribed in the pipeline.

* Write scripts to help partially automate/speed up the process of hand correction.
	* E.g. scripts which iterate through files in a directory, opening them in order, maybe starting with a specific file.
	
	* Will need to be done with .wav + .txt/.TextGrid pairs.
	
	* For forced alignment in particular: some way to focus on alignments which have the lowest confidence scores (below some threshold)? Focus on alignments which are most likely to be incorrect? (E.g. vowel-glide-vowel?)
	
		* Confidence scores for pyannote.audio diarization require the precision-2 premium model – this can be used with free tokens, but right now we’re on the fully free, open version

* Speed up/improve transcription section of the pipeline (see notes below).


* Test pipeline on longer and messier files (e.g. Librivox recordings, podcasts, etc.)

* Check out [spacey-cleaner](https://github.com/Ce11an/spacy-cleaner) as a num2word alternative, and as a different method for removing punctuation and converting numerals, across .py files.

* Improve formant tracking script to implement automated formant range setting on a by-speaker basis (as you've done with Praat scripts before).

	* Following De Looze & Rauzy (2009) and Evanini et al. (2011) --- see Bennett et al. (2022) e.g.

* Improve file folder organization schemes, and update paths in scripts as appropriate.

* Make the workflow more user-friendly.
	* Maybe set it up on a server for remote access? Or on Google Colab, Jupyter Notebooks, etc.?
	
* Extend pipeline to recordings with multispeaker interactions.


<!-- **************
Goals:
* Extend beyond English
	* Partially tested.
* Connect parts of the pipeline together as single-step processes whenever possible.
* Other types of flexibility?
************** -->


**************

0. If needed, convert mp3 files to .wav using [mp3_to_wav_converter.py](Python/mp3_to_wav_converter.py)

1. Get raw audio (.wav format)

2. Apply [diarization.py](Python/diarization.py) to generate a .TextGrid delimiting regions of speech, using [pyannote.audio](https://github.com/pyannote/pyannote-audio)

	* pyannote.audio installation: https://github.com/pyannote/pyannote-audio?tab=readme-ov-file#tldr
	* You'll need a Hugging Face access token (https://huggingface.co/settings/tokens), with fine grained permissions set to approve "Read access to contents of all public gated repos you can access".

3. Hand correct speech detection from [diarization.py](Python/diarization.py)

	* Currently set up for just one speaker per file, but that could be easily changed.

4. Apply [extract_short_wavs.py](Python/extract_short_wavs.py) to extract all labeled intervals from diarization, using [praatIO](https://github.com/timmahrt/praatIO)

	* **To do**: apply volume normalization first

5. Apply speech recognition to generate .txt transcripts with [whisper_transcription.py](Python/whisper_transcription.py), using [whisper.ai](https://github.com/openai/whisper)

	* This is slow (at least when using more accurate models like large.en or turbo). We need to look into faster methods (e.g. [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)).
	
	* Also, need to **deal with punctuation and numerals in a more effective way**, since these may cause issues with forced alignment later on.
	
	* whisper.ai installation: https://github.com/openai/whisper#setup

6. Correct transcripts

7. Apply forced alignment with [run_mfa.py](Python/run_mfa.py), using the [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/)

	* MFA installation: https://montreal-forced-aligner.readthedocs.io/en/latest/getting_started.html
	* [run_mfa.py](Python/run_mfa.py) currently only works with pre-existing acoustic models. Implementation of training on transcribed data is TBD.

8. Correct alignments

9. Analyze your data

	* Here, we're doing a toy analysis of vowel spaces.
	
	* You can measure formants in this data with:
	
		* [fasttrackpy](https://github.com/FastTrackiverse/fasttrackpy), implemented in [fasttrack_alignment.py](Python/fasttrack_alignment.py)
		
			* See also https://jofrhwld.github.io/blog/posts/2024/02/2024-02-16_fs-atg/
	
		* [FastTrak](https://github.com/santiagobarreda/FastTrack) in Praat. Follow the instructions at:
			* https://github.com/santiagobarreda/FastTrack/wiki/Extract-vowels-using-TextGrids
			* https://github.com/santiagobarreda/FastTrack/wiki/How-to-analyze-a-folder
			
		* A Praat script like [formant_extraction.praat](Praat/formant_extraction.praat).
	
	* We also use the R file [formant_analysis.R](R/formant_analysis.R) to plot resulting formant values and do other analyses.