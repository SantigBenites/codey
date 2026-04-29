
def reverseWords(s):
    """
    :type s: str
    :rtype: str
    """
    
    s = [x for x in s.split(" ") if x != ""]
    s = s[::-1]

    return " ".join(s).strip()


s = "a good   example"
print(reverseWords(s))