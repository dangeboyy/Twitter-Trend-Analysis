import string
import time
import pickle
from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)


examples = ["Yrn okua gidicem",
            "Tmm, yarin havuza giricem ve aksama kadar yaticam :)",
            "ah aynen ya annemde fark ettı siz evinizden cıkmayın diyo",
            "gercek mı bu? Yuh! Artık unutulması bile beklenmiyo",
            "Hayır hayat telaşm olmasa alacam buraları gökdelen dikicem.",
            "yok hocam kesınlıkle oyle birşey yok",
            "herseyi soyle hayatında olmaması gerek bence boyle ınsanların falan baskı yapıyosa",
            "email adresim zemberek_python@loodos.com",
            "Kredi başvrusu yapmk istiyrum.",
            "Bankanizin hesp blgilerini ogrenmek istyorum."]
def remove_whitespace(x):
    try:
        x = " ".join(x.split())
    except:
        pass
    return x

morphology = TurkishMorphology.create_with_defaults()

# SENTENCE NORMALIZATION

normalizer = TurkishSentenceNormalizer(morphology)

text = "Tmm, yarin havuza giricem ve #aksama kadar yaticam arabaa arabaa aaraba aaraba     ardaba  asraba    aradba:)"
normalized_sentence = normalizer.normalize(text)
start = time.time()
normalized_sentence = remove_whitespace(normalized_sentence)
split_normalized_sentence = normalized_sentence.split()
for word in split_normalized_sentence:
    if word.startswith('#'):
        split_normalized_sentence.remove(word)

final_sentence = " ".join(split_normalized_sentence)
print(f"Normalization instance created in: {time.time() - start} s")
print(final_sentence)



# start = time.time()
# for example in examples:
#     print(example)
#     print(normalizer.normalize(example), "\n")
# print(f"Sentences normalized in: {time.time() - start} s")

# filename = "morphology"
# outfile = open(filename, "wb")
# pickle.dump(morphology,outfile)
# outfile.close()

# # SENTENCE BOUNDARY DETECTION
# start = time.time()
# extractor = TurkishSentenceExtractor()
# print("Extractor instance created in: ", time.time() - start, " s")

# text = "İnsanoğlu aslında ne para ne sevgi ne kariyer ne şöhret ne de çevre ile sonsuza dek mutlu olabilecek bir " \
#        "yapıya sahiptir. Dış kaynaklardan gelebilecek bu mutluluklar sadece belirli bir zaman için insanı mutlu " \
#        "kılıyor. Kişi bu kaynakları elde ettiği zaman belirli bir dönem için kendini iyi hissediyor, ancak alışma " \
#        "dönemine girdiği andan itibaren bu iyilik hali hızla tükeniyor. Mutlu olma sanatının özü bu değildir. Gerçek " \
#        "mutluluk, kişinin her türlü olaya ve duruma karşı kendini pozitif tutarak mutlu hissedebilmesi halidir. Bu " \
#        "davranış şeklini edinen insan, zor günlerde güçlü, mutlu günlerde zevk alan biri olur ve mutluluğu kalıcı " \
#        "kılar. "

# start = time.time()
# sentences = extractor.from_paragraph(text)
# print(f"Sentences separated in {time.time() - start}s")

# for sentence in sentences:
#     print(sentence)
# print("\n")

# SINGLE WORD MORPHOLOGICAL ANALYSIS


# sentence = 'amin'
# split_sentence = sentence.translate(str.maketrans('', '', string.punctuation)).split()

# word_to_be_analised = ""
# for word in split_sentence:
#     results = morphology.analyze(word[0])
#     for result in results:
#         print(result)
#         contains_without = False
#         for i in range(len(result.get_morphemes())):
#             if str(result.get_morphemes()[i]) == 'Without:Without' or str(result.get_morphemes()[i]) == 'Negative:Neg':
#                 contains_without = True
#                 break

#         if contains_without:
#             word_to_be_analised += word[0] + " "
#         else:
#             word_to_be_analised += result.item.lemma + " "

#         break
    
# print(word_to_be_analised.rstrip())

# # TOKENIZATION
# tokenizer = TurkishTokenizer.DEFAULT

# tokens = tokenizer.tokenize("Saat 12:00.")
# for token in tokens:
#     print('Content = ', token.content)
#     print('Type = ', token.type_.name)
#     print('Start = ', token.start)
#     print('Stop = ', token.end, '\n')