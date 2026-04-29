def fullJustify(words, maxWidth):

    final_test = [""]
    for word in words :
        if len(final_test[-1]) + len(word) < maxWidth:
            final_test[-1] += word + " "
        else:
            idx = 0
            while len(final_test[-1]) <= maxWidth:

                if final_test[-1][idx] == " ":
                    final_test[-1] = final_test[-1][0:idx] + " " + final_test[-1][idx:]  
                    while final_test[-1][idx] == " ":
                        idx +=1
                idx +=1
                idx = idx % maxWidth
                print(f"{final_test[-1]} : {len(final_test[-1])}")
            final_test.append(f"{word}")

    print(final_test)

    for x in final_test[0:-1]:
        x = x.center(maxWidth)

    final_test[-1] = final_test[-1].ljust(maxWidth)

        

    return final_test

words = ["This", "is", "an", "example", "of", "text", "justification."]
maxWidth = 16
print(fullJustify(words,maxWidth))