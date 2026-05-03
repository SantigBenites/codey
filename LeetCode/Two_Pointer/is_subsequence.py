
def isSubsequence(s, t):

    if s == "" or t == "":
        return True

    sub_idx = 0
    for c in t:
        if c == s[sub_idx]:
            sub_idx += 1
        if sub_idx == len(s):
            return True
    return False



s = ""
t = "ahbgdc"

print(isSubsequence(s,t))