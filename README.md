# leanread
A Tkinter-based application for learning foreign words and pronunciation by reading articles and selecting words to learn

## English Learning Tool

Features:
- Open and save text files (R-8, R-9, R-10).
- Display file path in a label.
- Text-to-speech conversion with gTTS and playback via pygame (R-11, R-12).
- Vocabulary dictionary with translations using deep-translator (R-20, R-21).
- Status bar for user feedback (R-50 to R-53).
- Vertical scrollbar for text area (R-101).
- Word/phrase cleanup before adding to dictionary (R-61, R-62).

---------------------

## Requirements

#### text
R-1. On the left side an edit control where I can display text of an article
R-101. The edit control shall have vertical scroll bar
R-2. I can open a text file or just paste a text.

#### words to learn
R-4. On the right side I have a table of words I did not know or wanted to learn.
R-5. I can select a word in the edit control and press Add button, this will add the word into the table of words to learn
R-6. In the list table I wanted to learn the left column shall contain the words I added, and the right column shall contain the translation to german language
R-61. Before a single word was added, it shall be stripped from whitespace and punktuation.
R-62. If a phrase was selected, it shall be stripped from starting and ending punktuation.


#### status bar
R-50. Need status bar between the button bar and progress bar.
R-51. If the same word is selected and Add button clicked the status bar displays "already in the Dictionary"
R-52. The table of words to learn shall be in groupbox  saying "Dictionary to learn"
R-53. All button actions shall end with a corresponding status message displayed in the status bar.

#### text file management
R-8. When I open file the file name with path appears in the label above the Open button
R-9. Add "Save" button which saves the file to either the file which was open or to a file "text.txt" if nothing was selected before
R-10. At program start the last file selected or saved shall be reopened.
R-81. When the "Save" button pressed, the current dictionary of words shall be saved to a file with the same name as the opened file with extension json
R-82. If no file was saved/selected, then the dictionary is saved to text.json
R-83. The dictionary is saved in json format.
R-84. If a new text file is opened and the dictionary json with the same exists, the dictionary is loaded from the file to the table of words to learn

#### play text
R-11. The conversion to text lasts a while, so a progress bar shall be displayed to the right of the buttons panel showing conversion in progress
R-12. Stop button shall stop reading a long text.
R-13. Move TKinter GUI setup in own function

#### word to play conversion
R-3. I can press play button and the app shall convert text to speech using gTTS, save it to output.mp3 and then play it using pygame sound output
R-20. As soon as word adds to the table of words to learn, the app starts a process to convert the (name of the word) to mp3 file called (name of the word).mp3, so that for each word we have its audio representation in the mp3 file named the same as the word itself
R-21. If I click on a word entry (showing "the content of the word entry") in the table of words I wanted to learn, the app plays the related mp3 file using pygame sound output
