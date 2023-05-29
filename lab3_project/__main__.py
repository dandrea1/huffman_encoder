# This file is the entry point into this program when the module is executed.

from pathlib import Path
import argparse
from lab3_project.lab3 import process_files

# Create arguments for input and output files when program is run.
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("frequency_file", type=str, help="Frequency Table PathName")
arg_parser.add_argument("clear_text_file", type=str, help="Encoded File Pathname")
arg_parser.add_argument("coded_text_file", type=str, help="Decoded File Pathname")
arg_parser.add_argument("encoded_text", type=str, help="Encoded Message Pathname")
arg_parser.add_argument("decoded_text", type=str, help="Decoded Message Pathname")
args = arg_parser.parse_args()

# Set variables to the file locations to be processed.
frequency_text = Path(args.frequency_file)
text_to_encode = Path(args.clear_text_file)
text_to_decode = Path(args.coded_text_file)
encoded_text = Path(args.encoded_text)
decoded_text = Path(args.decoded_text)

# Check that input files exist
if not frequency_text.is_file():
    exit(f"Sorry, {frequency_text} input file doesn't exist")
if not text_to_encode.is_file():
    exit(f"Sorry, {text_to_encode} file doesn't exist")
if not text_to_decode.is_file():
    exit(f"Sorry, {text_to_decode} file doesn't exist")
if not encoded_text.is_file():
    exit(f"Sorry, location to put {encoded_text} doesn't exist")
if not decoded_text.is_file():
    exit(f"Sorry, location to put {decoded_text} doesn't exist")

# Using the frequency table and files to encode/decode by the user, compress or decompress the text using a huffman tree
with frequency_text.open('r') as frequency_table, text_to_encode.open('r') as text_to_encode, text_to_decode.open(
        'r') as text_to_decode, encoded_text.open('w') as encoded_text, decoded_text.open('w') as decoded_text:
    process_files(frequency_table, text_to_encode, text_to_decode, encoded_text, decoded_text)
