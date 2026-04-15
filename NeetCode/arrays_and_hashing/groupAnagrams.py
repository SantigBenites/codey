from typing import List 
from collections import defaultdict

def groupAnagrams(strs: List[str]) -> List[List[str]]:

    result = defaultdict(list)

    for string in strs:
        count = [0] * 26

        for char in string:
            count[ord(char) - ord("a")] += 1
        result[tuple(count)].append(string)

    return result.values()

strs = ["act","pots","tops","cat","stop","hat"]
print(groupAnagrams(strs))