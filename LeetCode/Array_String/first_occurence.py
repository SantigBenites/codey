


def strStr(haystack, needle):

    word_lenght = len(needle)

    for idx, letter in enumerate(haystack):
        if letter == needle[0]:
            if haystack[idx:idx+word_lenght] == needle:
                return idx
    return -1


haystack = "dasdasdaleeto"
needle = "leeto"
print(strStr(haystack,needle))