
def is_digit(c):
    return (ord('A') <= ord(c) <= ord('Z') or
            ord('a') <= ord(c) <= ord('z') or
            ord('0') <= ord(c) <= ord('9'))

def isPalindrome(s: str) -> bool:

    s = ''.join(c.lower() for c in s if is_digit(c))
    start = 0
    end = len(s)-1

    while start < end:
        
        if s[start] != s[end]:
            return False

        start +=1
        end -=1

    return True 


s = "Was it a car or a cat I saw?"
s2 = "tab a cat"
print(isPalindrome(s))
print(isPalindrome(s2))