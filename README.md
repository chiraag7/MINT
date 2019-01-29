# MINT

  We are generating a standard layout for the given resource in the dataset.

  A layout defines the physical relationship between the variables in the given resource.

  We are trying to automatically generate a stnadard layout for the inputted resource instead of manually creating them.

  Currently based on the combined heading of row and column in the first cell of CSV file, we are segregating them and describing the layout.

### Requirements

  Python3

### Procedure

  Run the program as follows: -

    python generateLayout.py -i <input_file> -o <output_file>

    <input_file> - resource file in CSV format
    <output_file> - JSON object of the layout (optional - displays on the std output if not given)