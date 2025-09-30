# Raw audio pipeline
Scripts for processing raw, untranscribed audio to time-aligned word- and segment-level annotations.

**************
To do right now:
* Remove FastTrack from the Praat pipeline, and replace it with the new fasttrackpy package (possibly in conjunction with aligned-textgrid), which is MUCH faster and better integrated. This has now been implemented as a command line call in [fasttrack_alignment.py](Python/fasttrack_alignment.py)

	* https://fasttrackiverse.github.io/fasttrackpy/
	* https://jofrhwld.github.io/blog/posts/2024/02/2024-02-16_fs-atg/

* Integrate out of dictionary processing, maybe with g2p?
	* Relatedly, deal with .wav files that have not been successfully aligned. These will probably have to be moved to a separate folder so that they don't cause problems (this is now implemented).

* Check out [spacey-cleaner](https://github.com/Ce11an/spacy-cleaner) as a num2word alternative, and as a different method for removing punctuation, across .py files.

* Test pipeline on longer and messier files (e.g. Librivox recordings)

* Improve file folder organization schemes, and update scripts as appropriate.

**************

**************
Goals:
* Extend beyond English
* Connect parts of the pipeline together as single-step processes whenever possible.
* Other types of flexibility?
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

	* This is slow. We need to look into faster methods (e.g. [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper)).
	
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
	
		* [FastTrak](https://github.com/santiagobarreda/FastTrack) in Praat. Follow the instructions at:
			* https://github.com/santiagobarreda/FastTrack/wiki/Extract-vowels-using-TextGrids
			* https://github.com/santiagobarreda/FastTrack/wiki/How-to-analyze-a-folder
			
		* A Praat script like [formant_extraction.praat](Praat/formant_extraction.praat).
	
	* We also use the R file [formant_analysis.R](R/formant_analysis.R) to plot resulting formant values and do other analyses.