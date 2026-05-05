
from collections import Counter

def isAnagram(s, t):

    if len(s) != len(t):
        return False

    s_counter = Counter()
    t_counter = Counter()

    for c_s, c_t in zip(s,t):
        s_counter[c_s] += 1
        t_counter[c_t] += 1

    return s_counter == t_counter

s = "car"
t = "rat"
print(isAnagram(s,t))