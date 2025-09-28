# Raw audio pipeline
Scripts for processing raw, untranscribed audio to time-aligned word- and segment-level annotations.

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

	* This is slow.
	* whisper.ai installation: https://github.com/openai/whisper#setup

6. Correct transcripts

7. Apply forced alignment with [run_mfa.py](Python/run_mfa.py), using the [Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/)

	* MFA installation: https://montreal-forced-aligner.readthedocs.io/en/latest/getting_started.html

8. Correct alignments

9. Analyze your data

	* For fun, let's do classic vowel space stuff (maybe for each speaker, and as a function of stress and/or duration) and see what it looks like with zero hand correction.
	
	* Use Fastrak for this? That seems good, though you want to speed it up by stripping out everything except the vowels, right? Or does Fastrak not bother with sounds it doesn't identify as vowels? See https://github.com/santiagobarreda/FastTrack/blob/master/Fast%20Track/functions/file_5_extractVowelswithTG.praat