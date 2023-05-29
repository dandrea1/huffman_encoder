
def generate_frequencies(text):
    frequencies = {}

    raw_text = text.readlines()
    for line in raw_text:
        for char in line:
            if char.upper() in frequencies:
                frequencies[char.upper()] += 1
            else:
                # new character, set frequency to 1
                frequencies[char.upper()] = 1
    return frequencies
