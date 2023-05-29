from lab3_project.node import Node
from lab3_project.huffman_tree import HuffmanTree


def get_char_freq(line):
    """
    Reads the line and returns the character and frequency
    :param line: line from csv file to read
    :return: character and its frequency
    """
    # perform error handling
    if line in ('\n', '\r\n'):
        return
    character = ''
    frequency = ''
    for item in line:
        if item in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            frequency += item
        else:
            # find the first non-space/tab character
            while character == '':
                # find (and ignore the first equal sign)
                if item not in [' ', '-', '\n']:
                    character = item
    # convert to an int
    frequency = int(frequency)
    return character, frequency


def sort_freq_table(arr):
    """
    Bubble sort to sort character frequencies in descending order
    :param arr: array of frequency Nodes
    :return: array in descending frequency order
    """
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j].frequency < arr[j + 1].frequency:
                # if left element frequency greater than right element frequency, swap
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp


def process_files(frequency_file, clear_text, coded_text, encoded_filepath, decoded_filepath):
    # Read in files
    if not frequency_file:
        exit("Frequency File is empty")
    if not clear_text:
        exit("There is no text you wish to encode")
    if not coded_text:
        exit("There is no text you wish to decode")

    frequency_table = frequency_file.readlines()
    clear_text = clear_text.readlines()
    coded_text = coded_text.readlines()

    frequencies = []

    for line in frequency_table:
        # extract frequency count for each letter and add tuple to list
        char, freq = get_char_freq(line)
        # check if character is already in frequency table
        if (char.upper(), freq) in frequencies:
            pass
        else:
            new_node = Node(char, freq)
            frequencies.append(new_node)

    # sort frequency table in ascending order
    sort_freq_table(frequencies)

    # create huffman encoder
    huffman = HuffmanTree(frequencies)
    huffman.build_huffman_tree()

    # preorder
    preorder = huffman.preorder_traversal(huffman.root)

    # encode letters
    for i in huffman.root.character:
        huffman.get_code(huffman.root, char=i, encoding="")

    # Write to files

    # encode file
    total_file_before_compression = 0
    total_file_after_compression = 0
    for line in clear_text:
        encoded_line, before_compression, after_compression = huffman.encode_message(line)
        encoded_filepath.write(f"{encoded_line}\n")
        total_file_before_compression += before_compression
        total_file_after_compression += after_compression

    # Write compression statistics
    encoded_filepath.write(f"Space usage before compression (in bits): {total_file_before_compression}\n")
    encoded_filepath.write(f"Space usage after compression (in bits): {total_file_after_compression}\n")
    encoded_filepath.write(
        f"Total Reduction: {round(((total_file_before_compression - total_file_after_compression) / total_file_before_compression) * 100)}%\n")

    # Print out preorder traversal
    encoded_filepath.write("\nPREORDER:")
    for item in preorder:
        node = f"{item.character}:{item.frequency},  "
        encoded_filepath.write(f"{node}")

    # decode file
    for line in coded_text:
        decoded_line = huffman.decode_message(line)
        decoded_filepath.write(f"{decoded_line}\n")
