# Anonymization
This repository contains two scripts for the anonymization of audio and ELAN files.

1. anonymize.praat

This Praat script takes a Praat TextGrid file with 2 tiers containing part of speech annotations and a corresponding .wav file and replaces the audio with silence for any interval with the annotation NAME (= personal name). It can be used to batch process a set of files.

In the ELIC project, we are using ELAN to annotate our data. The PoS annotations for speaker and interviewer include the label NAME for any personal names. To use the script, export the PoS tiers for both the speaker and interviewer from the annotation ELAN file as a Praat TextGrid. Put all TextGrid and .wav files to be anonymized into the same folder. The file names should be the same except for the extension (.TextGrid, .wav).

Open Praat, then open the anonymize.praat script and select Run. The script will prompt you for the path names to the input files directory, the output files directory. and the directory where the script is located. The anonymized .wav files will be saved with _anon appended to the original file name.

2. Anonymize_Elan_files.py

This Python script takes a set of annotated ELAN files with the tier names used in the ELIC project and for every instance of NAME in a PoS tier, it replaces the actual personal name in the corresponding intervals on other tiers (Text, Words, Lemma, Gloss, engTrans) with the annotation "ANONYMIZED". It also generates a list of personal names that have been anonymized as a .csv file for verification purposes.

To use the script, place all ELAN files to be anonymized in a folder named Original_Elan_files. Run the script. It will generate a file named "Names_List.csv", which will appear in the same directory, as well as a new folder named "Anonymized_Elan_files" with all the anonymized files.

To adapt this script for use with other ELAN templates, note that the tiers in this script are referenced by tier name.
