from collections import defaultdict


def groupAnagrams(strs):

    code_anagrams = defaultdict(list)
    for word in strs:

        code = "".join(sorted(word))
        code_anagrams[code].append(word)

    return list(code_anagrams.values())

strs = ["eat","tea","tan","ate","nat","bat"]
print(groupAnagrams(strs))