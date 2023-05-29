from lab3_project.node import Node


class HuffmanTree:
    def __init__(self, frequency_table):
        self.freq = frequency_table
        self.codes = {}  # store encoding
        self.root = None

    def sort_freq_table(self):
        """
        Bubble sort to sort character frequencies in descending order and resolve tiebreakers
        Updates freq attribute to ordered array.
        """
        n = len(self.freq)
        for i in range(n):
            for j in range(n - i - 1):
                # tiebreaker logic
                if self.freq[j].frequency == self.freq[j + 1].frequency:  # if frequencies are equal
                    # if left item is a single letter and right is multi, don't swap
                    if len(self.freq[j].character) == 1 and len(self.freq[j + 1].character) > 1:
                        temp = self.freq[j]
                        self.freq[j] = self.freq[j + 1]
                        self.freq[j + 1] = temp
                    # if left is multi and right is single letter, swap
                    elif len(self.freq[j].character) > 1 and len(self.freq[j + 1].character) == 1:
                        pass
                    # if both are multi letters or both are single, put the letter closest to beginning of alphabet
                    # to the left
                    else:
                        if self.freq[j + 1].character[0] > self.freq[j].character[0]:
                            temp = self.freq[j]
                            self.freq[j] = self.freq[j + 1]
                            self.freq[j + 1] = temp
                # non tiebreaker logic
                elif self.freq[j].frequency < self.freq[j + 1].frequency:
                    # if left element frequency greater than right element frequency, swap
                    temp = self.freq[j]
                    self.freq[j] = self.freq[j + 1]
                    self.freq[j + 1] = temp

    @staticmethod
    def alphabetize(node_string):
        """
        Takes a string of characters and put them in alphabetical order.
        :return: Returned an alphabetized version of the string
        """
        char_list = []
        for char in node_string:
            char_list.append(char)

        for i in range(0, len(node_string)):
            for j in range(0, len(node_string)):
                if char_list[i] < char_list[j]:
                    temp = char_list[i]
                    char_list[i] = char_list[j]
                    char_list[j] = temp
        alphabetized_node_characters = ""
        for i in range(0, len(node_string)):
            alphabetized_node_characters = alphabetized_node_characters + char_list[i]

        return alphabetized_node_characters

    def build_huffman_tree(self):
        """
        Takes the frequency table that is stored in the freq attribute and converts it to a huffman tree.
        Once the huffman tree is built, the self.root is set to the only item left in self.freq.
        """
        while len(self.freq) > 1:
            key1 = self.freq.pop()
            key2 = self.freq.pop()
            freq_sum = key1.frequency + key2.frequency
            combined_char = key1.character + key2.character
            # alphabetize the combined string to aid in tiebreaker logic.
            combined_char = self.alphabetize(node_string=combined_char)
            parent = Node(character=combined_char, frequency=freq_sum)
            parent.left = key1
            parent.right = key2
            self.freq.append(parent)
            # resort the parent into the frequency
            self.sort_freq_table()
        # after building the tree, set root node
        self.root = self.freq[0]

    def get_code(self, current_node, char, encoding):
        """
        Takes in a character and ads its encoding to the codes dictionary.
        :param current_node: starts as root and then updates as huffman tree is traversed
        :param char: the character that needs to be encoded ex. 'A'
        :param encoding: The string of 0s and 1s that represent that character according to the huffman tree
        :return: character and encoding are added to self.codes dictionary
        """
        if current_node.left is None and current_node.right is None:
            self.codes[char] = encoding
        else:
            if char in current_node.left.character:
                new_encode = encoding + '0'
                self.get_code(current_node.left, char, new_encode)
            if char in current_node.right.character:
                new_encode = encoding + '1'
                self.get_code(current_node.right, char, new_encode)

    def encode_message(self, line):
        """
        Takes a line from a file and encodes it using the self.codes dictionary. If any character is not in the codes
        dictionary, that character is simply added directly to the encoded line. For example, punctuation or numbers
        are not encoded.
        :param line: A string to be encoded
        :return: the string in its encoded form
        """
        before_compression = 0
        after_compression = 0
        encoded_line = ""
        for char in line:
            if char.upper() not in self.codes:
                encoded_line += char
                before_compression += 8
                after_compression += 8
            else:
                char = char.upper()
                encoded_char = self.codes[char]
                encoded_line += encoded_char
                before_compression += 8
                after_compression += int(len(self.codes[char]))
        return encoded_line, before_compression, after_compression

    def decode_message(self, line):
        """
        Takes a line from a file and decodes it by traversing the Huffman tree. If any character is not a 1 or 0,
        that character is simply added directly to the decoded line. For example, punctuation or spaces
        are not do not need to be decoded.
        :param line: A string to be encoded
        :return: the string in its encoded form
        """
        current_node = self.root
        decoded_line = ""
        for char in line:
            if char != '1' and char != '0':
                decoded_line += char
            if char == '0':
                current_node = current_node.left
            if char == '1':
                current_node = current_node.right
            if current_node.left is None and current_node.right is None:
                decoded_line += current_node.character
                current_node = self.root
        return decoded_line

    def preorder_traversal(self, root):
        """
        Traverses huffman tree in preorder and returns the preorder nodes in a list.
        :param root: the node from which the preorder traversal should start
        :return: Returns a list of the preorder nodes with character and frequencies.
        """
        res = []
        if root:
            res.append(root)
            res = res + self.preorder_traversal(root.left)
            res = res + self.preorder_traversal(root.right)
        return res
