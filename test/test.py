import fileIO

stop_words = fileIO.read_stop_words("../stop_words.txt")


def remove_stop_words(sentence):
    results = []
    tmp_arr = sentence.split(" ")
    sent_arr = sentence.split(" ")

    for word in tmp_arr:
        if word in stop_words:
            print(word)
            sent_arr.remove(word)
    results.append(" ".join(sent_arr))

    # for stop_word in stop_words:
    #    split_arr=sentence.split(" ")
    #    if stop_word in split_arr:
    #        sentence.remove(stop_word)
    # results.append(" ".join(sentence))

    return results


sent = "yardım etmek çok güzel bir şey".split(" ")

for i in range(len(sent) - 1):
    if (sent[i] + " " + sent[i + 1]) in ["yardım etmek"]:
        print("ege")

