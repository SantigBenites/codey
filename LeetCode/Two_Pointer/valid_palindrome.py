import re


def isPalindrome(s):
    s = s.lower()
    s = "".join([c for c in s if c.isalnum()])
    n = len(s)-1
    for idx in range(0,n):

        
        if s[idx] != s[n-idx]:
            return False
    return True


s = "ab_a"
print(isPalindrome(s))