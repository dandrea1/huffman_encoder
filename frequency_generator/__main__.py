# This file is the entry point into this program when the module is executed.

from pathlib import Path
import argparse
from frequency_generator.frequency_table import generate_frequencies

# Create arguments for input and output files when program is run.
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("clear_text", type=str, help="Text File PathName")
arg_parser.add_argument("freq_table", type=str, help="Frequency File Pathname")

args = arg_parser.parse_args()

# Set variables to the file locations to be processed.
clear_text = Path(args.clear_text)
frequency_table = Path(args.freq_table)

# Check that input files exist
if not clear_text.is_file():
    exit(f"Sorry, {clear_text} input file doesn't exist")
if not frequency_table.is_file():
    exit(f"Sorry, {frequency_table} file doesn't exist")

# Using the frequency table and files to encode/decode by the user, compress or decompress the text using a huffman tree
with clear_text.open('r') as text, frequency_table.open('w') as freq_table:
    frequencies_dict = generate_frequencies(text)
    for key, value in frequencies_dict.items():
        freq_table.write(f"{key}:{value}\n")
