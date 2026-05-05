from collections import defaultdict


def isIsomorphic(s, t):

    map_s_t = {}
    map_t_s = {}

    for sc,tc in zip(s,t):

        if sc in map_s_t and map_s_t[sc] != tc:
            return False
        if tc in map_t_s and map_t_s[tc] != sc:
            return False
        map_s_t[sc] = tc
        map_t_s[tc] = sc
    
    return True



s = "paper"
t = "title"
print(isIsomorphic(s,t))