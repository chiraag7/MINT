# MINT

  We are generating a standard layout for the given resource in the dataset.

  A layout defines the physical relationship between the variables in the given resource.

  We are trying to automatically generate a stnadard layout for the inputted resource instead of manually creating them.

  Currently based on the combined heading of row and column in the first cell of CSV file, we are segregating them and describing the layout.

### Requirements

  Python3

  Install pyyaml using

      pip install pyyaml

### Procedure

  Run the program as follows: -

    python generateLayout.py -i <input_file> -o <output_file>

    <input_file> - resource file in CSV format
    <output_file> - JSON object of the layout (optional - displays on the std output if not given)

## Annotated Resource Files

  Resource files chosen for annotation:

  https://docs.google.com/document/d/1T4b26yjxTw5u7IPfw7lp4Zg46Bi_vD_10w6gZ1gFQSM/edit?usp=sharing

  Actual resource files can be found in the Dataset directory.

  ( Data source: https://www.dropbox.com/sh/e43uo5iuwupkmsj/AAAzrTJI5UPAKqlQOm_W2bXya?dl=0 )