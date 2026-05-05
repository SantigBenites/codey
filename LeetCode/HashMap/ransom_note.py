from collections import Counter


def canConstruct(ransomNote, magazine):

    magazine_elems = Counter()

    for c in magazine:
        magazine_elems[c] +=1

    for c in ransomNote:
        magazine_elems[c] -=1
        if magazine_elems[c] < 0:
            return False

    return True


ransomNote = "aa"
magazine = "ab"
print(canConstruct(ransomNote,magazine))