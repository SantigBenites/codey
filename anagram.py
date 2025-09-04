def isAnagram( s: str, t: str) -> bool:

    if len(s) != len(t):
        return False
    
    map_s = {}
    map_t = {}
    for s_letter,t_letter in zip(s,t):
        if s_letter in map_s.keys():
            map_s[s_letter]+= 1
        else:
            map_s[s_letter] = 0

        if t_letter in map_t.keys():
            map_t[t_letter]+= 1
        else:
            map_t[t_letter] = 0

    return True if map_s == map_t else False

s = "racecar"
t = "carrace"
print(isAnagram(s,t))