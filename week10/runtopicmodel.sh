# Set input and output files
inputFile=~/path/to/input
outputBaseFile=~/path/to/output-topics-50

# Import file into mallet format
bin/mallet import-file --input $inputFile.txt --output $inputFile.mallet --keep-sequence --remove-stopwords

# Run the topic model
bin/mallet train-topics --input $inputFile.mallet --num-topics 50 --output-state $outputBaseFile-state.txt.gz --output-topic-keys $outputBaseFile-keys.txt --output-doc-topics $outputBaseFile-doc-topics.txt
