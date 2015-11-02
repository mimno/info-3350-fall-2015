REM Base variables - don't give an extension
set InputFile=C:\Users\your\path\to\file
set OutputBaseFile=C:\Users\your\path\to\output-topics-50

REM import the file into mallet format
call bin\mallet.bat import-file --input %InputFile%.txt --output %InputFile%.mallet --keep-sequence --remove-stopwords

REM run the topic model
call bin\mallet.bat train-topics --input %InputFile%.mallet --num-topics 50 --output-state %OutputBaseFile%-state.txt.gz --output-topic-keys %OutputBaseFile%-keys.txt --output-doc-topics %OutputBaseFile%-doc-topics.txt