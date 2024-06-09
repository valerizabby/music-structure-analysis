**********************************************************************
Schubert Winterreise Dataset (SWD)
**********************************************************************

This is a description of

Schubert Winterreise Dataset (SWD), Version 2.0

by Christof Weiß, Frank Zalkow, Vlora Arifi-Müller, Meinard Müller,  Hendrik Vincent Koops, Anja Volk, Harald G. Grohganz

published on the Zenodo platform under: https://zenodo.org/record/3968389#.X5FctIgzZaQ

For details on the dataset content, the creation process, and potential usage, please see the accompanying journal paper:

Christof Weiß, Frank Zalkow, Vlora Arifi-Müller, Meinard Müller,  Hendrik Vincent Koops, Anja Volk, Harald G. Grohganz, "Schubert Winterreise dataset: A multimodal scenario for music analysis," ACM Journal on Computing and Cultural Heritage (JOCCH), 2020.

This README provides information about the structure of the data (zip-file), the contents of the subfolders, and the interpretation of the annotation files.

Contact:
 * christof.weiss@audiolabs-erlangen.de (primary)
 * frank.zalkow@audiolabs-erlangen.de
 * vlora.arifi-mueller@audiolabs-erlangen.de
 * meinard.mueller@audiolabs-erlangen.de
 * h.v.koops@gmail.com
 * a.volk@uu.nl
 * hg@blsq.org


**********************************************************************
License
**********************************************************************

The dataset is published under a Creative Commons Attribution 3.0 Unported license (https://creativecommons.org/licenses/by/3.0/legalcode). We acknowledge the publication of the performance by baritone Randall Scarlata with pianist Jeremy Denk (denoted as SC06), published under the same license by the Isabella Stewart Gardner Museum (Boston). Please note that the audio files of this performance must not be re-distributed in modified form. All other sources for the dataset are in the Public Domain.


**********************************************************************
General conventions (filenames, musical time positions, ...)
**********************************************************************

All folder, subfolder, and file names have a modular structure of several identifiers, separated by underscores ("_").

- Folders:
The top folders refer to three different levels of the data: 01_RawData/, 02_Annotations/, and 03_ExtraMaterial/. 

- Subfolders:
The subfolders of 01_RawData/ are specified by a prefix denoting the domain (lyrics, score, audio) and by a suffix denoting the file types (txt, png, pdf, musicxml, midi, wav, ...).
The subfolders of 02_Annotations/ are specified by the prefix "ann" (for annotation) followed by the domain (score, audio) and the semantic category annotated (chord, localkey, measure, structure). The local key annotations further contain a suffix specifying the individual annotators (-ann1, -ann2, -ann3).

- Filenames:
All filenames are organized systematically using a ComposerID ("Schubert"), a hierarchical WorkID for identifying the respective song within the Winterreise cycle ("D911-06" for song No. 6), and in case of perfomance-related data and annotations a PerformanceID ("SC06" for the performance by R. Scarlata recorded in 2006). The specification of the performances can be found in the paper. IDs are separated by underscores: [ComposerID]_[WorkID]_[PerformanceID].[filetype]

- CSV files / separators:
All annotations are given as CSV files using the semicolon (;) as separator and quotation marks (" ") as delimiter for text-based annotations fields. All CSV files contain a header giving the column names. Further specification of the columns' content is given below for the different types of annotations.

- Physical/Musical time positions:
All audio-based annotations refer to physical time position given in seconds. For the symbolic/score-related annotations, time positions refer to musical time given in measures. Here, we compute beat position as fractions of a measure so that each measure obtains a total length of 1 and beat positions are relative (independet of the specific time signature), cut to three digits.
Examples:
 * 5.000: The start (beat 1) of measure 5.
 * 7.250: The second beat (in a 4/4 time signature) of measure 7.
 * 11.666: The third beat (in a 3/4 time signature) of measure 11.
 * 45.999: The end (end of the last beat) of measure 45.


**********************************************************************
01_RawData/
**********************************************************************

The "Raw Data" comprises several representations of the songs in Schubert's Winterreise in different modalities. This includes lyrics (text data), scores (image, symbolic, and MIDI data), and performances (audio data). Specifications on the file types are given below.


- audio_wav/
Audio recordings of the two published performances (HU33, SC06). The audio recordings are cut to individual songs, converted to mono wav files, and re-sampled to a sampling rate of 22050 Hz. For the first song of the Huesch performance (HU33), we additionally added an artifical repeat to account for the structural difference (see 03_ExtraMaterial).

- lyrics_txt/
Plain text files of the songs' lyrics. The text files are structured into verses (by line breaks) and musical stanzas (by blank lines). Deviating from the original poems, we account for repeated and slightly modified verses or words so that the text files exactly correspond to the scores' lyrics.

- score-IMSLP_pdf-complete.pdf
Scanned score in an edition by Peters, available as a scan at the International Music Score Library Project (IMSLP). PDF file with additional markings of the measure numbers (68 pages). Original pdf file available under http://ks4.imslp.info/files/imglnks/usimg/9/92/IMSLP00414-Schubert_-_Winterreise.pdf.

- score-IMSLP_png/
For the same scan, we provide individual PNG images of each page. The filenames consist of ComposerID, WorkID, and a three-digit page number for each song (e.g. "Schubert_D911-13_002.png").

- score_midi/
MIDI files exported from the Sibelius score (see below). Note events are rendered with a constant tempo. Voice and piano are separated into individual MIDI channels, with the voice corresponding to the male version (lower octave).

- score_musicxml/
MusicXML exports from the Sibelius score (see below) as uncompressed .xml files.

- score_pdf/
PDF exports from the Sibelius score (see below). Note that these PDF files are different from the score-IMSLP_pdf-complete.pdf mentioned above.

- score_sibelius/
Symbolic score generated by processing the scan score-IMSLP_pdf-complete.pdf (see above) with OMR software (Avid PhotoScore) and correcting using notation software (Avid Sibelius, version 8.2). In song No. 1 "Gute Nacht," the repetition is unfolded. For male singers, the treble clef is understood in a transposing way (down one octave) while for female singers, it is realized as written.


**********************************************************************
02_Annotations
**********************************************************************

This category comprises annotations of different types of musical information referring to either the score or the respective audio recordings.

- ann_audio_chord
Chord annotations for each performance specified in the syntax proposed in [Harte et al., Proc. ISMIR 2005] as "root:type/bass". Column specifications as described below.
 * start:      start time in seconds
 * end:        end time in seconds
 * shorthand:  chord label in shorthand notation ("C:maj", "C:min7/G", ...)
 * extended:   chord label in extended notation with explicit intervals ( "C:(3,5)", "C:(b3,5,b7)/G", ...)
 * majmin:     chord label reduced to major and minor triads ("C:maj", "C:min", ...)
 * majmin_inv: chord label reduced to major and minor triads with bass note ("C:maj", "C:min/G", ...)

- ann_audio_globalkey.csv
CSV file specifying the global key for each song in each performance. Note that the songs are performed in different keys across the different performances.

- ann_audio_localkey-ann1
Local key annotations by annotator 1 (ann1) for each performance specified in the syntax "root:mode". Column specifications as described below.
 * start: start time in seconds
 * end:   end time in seconds
 * key:   key label ("C:maj", "F#:min", ...)

- ann_audio_localkey-ann2
Local key annotations by annotator 2 (ann2) for each performance, as specified above.

- ann_audio_localkey-ann3
Local key annotations by annotator 3 (ann3) for each performance, as specified above.

- ann_audio_measure
Musical measure annotation (downbeat positions) for each performance. The end of the song (end of the last sounding note) is given as partial measure.
 * start:   Physical time position in the audio given in seconds
 * measure: Musical time position in the score given in measures

- ann_audio_note
Annotations of note events derived from the MIDI files (score_midi), added in Version 2.0:
 * start:      start time in seconds
 * end:        end time in seconds
 * pitch:      MIDI pitch number of the note event (60=C4)
 * pitchclass: Pitch class number of the note event (0=C)
 * instrument: Instrument label ("piano" or "voice")

- ann_audio_structure
Annotations of musical structure for each performance. Beyond the main structural parts (denoted with A, B, C,
. . . ), varied repetitions are marked with additional numbers (A1, A2, . . . ). Instrumental parts such as an introduction or interlude are denoted by specific letters (I, J, K, . . . ).
 * start:     start time in seconds
 * end:       end time in seconds
 * structure: structural part labeled as stated above ("A", "B", "A1", "I", ...)

- ann_score_chord
Chord annotations referring to the score.
 * start:      start time in measures
 * end:        end time in measures
 * shorthand:  chord label in shorthand notation ("C:maj", "C:min7/G", ...)
 * extended:   chord label in extended notation with explicit intervals ( "C:(3,5)", "C:(b3,5,b7)/G", ...)
 * majmin:     chord label reduced to major and minor triads ("C:maj", "C:min", ...)
 * majmin_inv: chord label reduced to major and minor triads with bass note ("C:maj", "C:min/G", ...)

- ann_score_globalkey.csv
CSV file specifying the global key for each song in the score.

- ann_score-IMSLP_measure
Measure positions (all three staves) given as rectangular bounding boxes indicating the coordinates of the upper left corner, the height, and the width in pixels. The positions refer to the PNG images of the IMSLP score given in 01_RawData/score-IMSLP_png/. For more information, see http://www.audiolabs-erlangen.de/resources/MIR/2019-ISMIR-LBD-Measures.
 * measure:  Measure number
 * rowindex: Row number on the score page
 * x:        horizontal position of the upper left corner in pixels
 * y:        vertical position of the upper left corner in pixels
 * height:   height of the bounding box in pixels
 * width:    width of the bounding box in pixels
 * image:    filename of the corresponding PNG image in 01_RawData/score-IMSLP_png/

- ann_score_localkey-ann1
Local key annotations by annotator 1 (ann1) referring to the score.
 * start: start time in measures
 * end:   end time in measures
 * key:   key label ("C:maj", "F#:min", ...)
 
- ann_score_localkey-ann2
Local key annotations by annotator 2 (ann2) referring to the score, as specified above.

- ann_score_localkey-ann3
Local key annotations by annotator 3 (ann3) referring to the score, as specified above.

- ann_score_structure
Annotations of musical structure referring to the score.
 * start:     start time in measures
 * end:       end time in measures
 * structure: structural part labeled as stated above ("A", "B", "A1", "I", ...)


**********************************************************************
03_ExtraMaterial
**********************************************************************

The extra material consists of the original audio recordings, which we cutted to individual songs and converted to mono wav files with a sampling rate of 22050 Hz. For song No. 1, we also add scripts and data for automatically adding the artificial repetition. Moreover, this folder contains the license files for the audio performances.

- ann_audio_globalkey-tuning.csv
CSV file specifying the key and tuning information for each song in each performance (automatically computed).

- ann_score_overview.csv
CSV file providing an overview of the Winterreise cycle (titles, keys, time signatures, length in measures) as given in the paper (Table 1).

- environment.yml
Python environment file for running the script HU33_Song01_FixRepetition.py which automatically adds the repetition to song No. 1 for the Huesch performance (HU33).

- HU33_originalShort_musopen
Variant of the raw data and annotations for the original version of the Huesch performance, where the first part is not repeated. To avoid structural inconsistencies, this version was not used in the main folders in favor of the one with artifical repetition.

- HU33_Song01_FixRepetition.py
Python script to automatically add the artificial repetition to song No. 1 in the performance by Huesch (HU33).

- HU33_Song01_WithRepetition
Output audio, measure annotations, and adapted lyrics file for song No. 1 in the performance HU33 with artifical repetition.

- license_HU33.txt
License file for the performance HU33.

- license_SC06.txt
License file for the performance SC06.

- SC06_originalStereo_IMSLP
Original audio files of the performance SC06, given as stereo MP3 files.