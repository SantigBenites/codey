def wordPattern(pattern, s):
    words = s.split(" ")
    if len(words) != len(pattern):
        return False
    map_char_word = {}
    map_word_char = {}

    for char,word in zip(pattern,words):

        if char in map_char_word and map_char_word[char] != word:
            return False
        if word in map_word_char and map_word_char[word] != char:
            return False

        map_char_word[char] = word
        map_word_char[word] = char
    
    return True

pattern = "aaa"
s = "aa aa aa"
print(wordPattern(pattern,s))