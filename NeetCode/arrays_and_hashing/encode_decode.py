from typing import List


def encode(strs: List[str]) -> str:

    output = ""
    for word in strs:
        output += f"{len(word)}#{word}"

    return output

def decode(s: str) -> List[str]:

    output  = []
    idx = 0
    while idx < len(s):
        size = ""
        while s[idx] != "#":
            size += s[idx]
            idx +=1
        # To take care of #
        idx +=1 
        # Split word
        word_length = int(size)
        current_word = s[idx:idx+word_length]
        output.append(current_word)
        idx += word_length

    return output



input = ["ababdbadbadbabdabd","code","love","you"]
encoded = encode(input)
print(f"encoded = {encoded}")
decoded = decode(encoded)
print(decoded)