from string import digits


# all .c files of github.com/torvalds/linux (2020.09.03)
# characters with less than 120 occurrences removed
linux_character_counts = {  #
    ' ': 49866775, 'e': 30099828, 't': 25918994, '_': 25712106, '\t': 23574246,
    'r': 20610132, '\n': 20043514, 'i': 19497338, 's': 18471062, 'a': 17080509,
    'n': 16056115, 'c': 14722067, 'o': 14059134, 'd': 13578042, 'l': 10733633,
    'u': 10272191, 'p': 9953227, ',': 8850152, 'f': 8608475, '0': 8343971,
    'm': 7907913, ')': 7088418, '(': 7085243, ';': 6948986, '*': 5969454,
    'h': 5586269, 'v': 5403478, 'g': 5264319, 'E': 5145004, 'b': 5096143,
    '-': 5094715, 'x': 4859269, '=': 4600903, 'I': 4104984, 'T': 4034283,
    'R': 3983355, '>': 3978184, 'S': 3929666, 'A': 3861806, 'C': 3654392,
    'k': 3208236, 'N': 3176029, 'P': 3098533, '1': 3047150, 'L': 3038251,
    'D': 2962589, 'O': 2787882, 'M': 2718631, '.': 2712735, '2': 2702989,
    'w': 2669408, '/': 2546596, 'y': 2247674, '"': 2066326, 'F': 1983195,
    '{': 1900335, '}': 1900243, 'U': 1734884, '3': 1655540, 'G': 1541480,
    '&': 1509059, 'B': 1452658, '4': 1390673, 'q': 1313174, '8': 1298860,
    '6': 1181996, 'V': 1010725, '5': 1010477, 'H': 989130, 'X': 952193,
    ':': 861795, '7': 761972, '[': 759183, ']': 758629, '<': 755911,
    'K': 730538, 'z': 711602, '+': 674924, '#': 666951, 'W': 655312,
    '9': 641054, 'Y': 553121, '|': 535519, '%': 476250, '!': 473426,
    '\\': 430917, 'Q': 300716, 'j': 261037, 'Z': 197428, "'": 175740,
    '@': 164951, '?': 74934, '~': 67911, 'J': 57418, '^': 11242, '$': 3488,
    '`': 2385, '©': 589, 'ö': 178, '⎽': 120}

# from this sanitized 5.8 GiB Wikipedia (de) corpus uploaded on 2019-06-27:
# https://github.com/t-systems-on-site-services-gmbh/german-wikipedia-text-corpus
# all characters with below 1000 were removed (mostly Chinese characters)
#
# The above corpus and the following dict is released under the
# Creative Commons Attribution-ShareAlike 3.0 Unported license:
# https://creativecommons.org/licenses/by-sa/3.0/
wikipedia_de_corpus_counts = {  #
    ' ': 368434553, 'e': 300166342, 'n': 178603293, 'i': 151015223,
    'r': 144409194, 't': 114977063, 's': 108258400, 'a': 106152475,
    'd': 87499266, 'h': 73540781, 'u': 72102903, 'l': 68937042, 'o': 53910552,
    'c': 49643493, 'g': 48788009, 'm': 45134307, 'b': 31895801, 'f': 26663250,
    'w': 22905436, '.': 22344878, 'k': 21398162, 'z': 20058308, '\n': 17685830,
    ',': 16308705, 'v': 14612696, 'p': 14423348, 'S': 13772700, 'ü': 10609540,
    '1': 10425069, 'A': 9980856, 'D': 9710417, 'ä': 9645776, 'B': 8932762,
    'M': 7487156, '"': 7196803, '0': 6862972, 'E': 6518251, 'K': 6357666,
    'G': 6283656, 'F': 5965701, '9': 5862954, 'P': 5819219, '-': 5651510,
    '2': 5075224, 'R': 5005332, 'W': 4989025, 'H': 4982157, 'ö': 4882694,
    'T': 4850573, 'L': 4654194, 'I': 4413627, 'V': 4338694, 'N': 4132678,
    'y': 3818184, 'J': 3685795, ')': 3566548, '(': 3543298, '8': 3218709,
    'C': 3159422, 'ß': 2913712, '5': 2694114, 'Z': 2657991, '3': 2583446,
    'O': 2504987, '4': 2451556, '7': 2443359, 'U': 2381022, '6': 2377859,
    'j': 2110900, ':': 1341681, 'x': 1338858, '“': 1110507, '„': 1105884,
    '/': 742362, '–': 676588, ';': 524378, 'q': 393773, 'Q': 360799,
    'é': 346767, '*': 329288, 'Ü': 313842, '?': 263252, 'Y': 224088,
    'Ö': 214404, '%': 174069, '†': 166485, "'": 164932, '_': 156664,
    'Ä': 152422, '’': 149720, '!': 130675, 'á': 130656, 'X': 124765,
    'í': 92599, '&': 85569, '[': 85072, ']': 84941, '=': 83471, 'ó': 77981,
    '>': 74640, '<': 64311, 'è': 52665, 'š': 45566, 'ō': 44859, '²': 42909,
    '°': 37816, '+': 34663, 'č': 32835, '…': 32441, 'ç': 31383, 'ł': 30793,
    '‘': 30683, '»': 29306, '«': 28431, 'ā': 26256, '‚': 25694, 'ø': 23634,
    'É': 23110, 'ř': 23018, 'ć': 22975, '§': 21427, 'ı': 21410, 'ý': 20923,
    'â': 19770, '×': 19364, 'ô': 18405, 'ã': 17679, 'ū': 17563, 'à': 17212,
    'ě': 16697, 'а': 16059, 'ú': 15905, 'ž': 15619, 'о': 15169, 'ñ': 15111,
    '³': 14459, '#': 14342, 'å': 13875, 'Š': 13835, 'ī': 13520, '”': 13506,
    '−': 13339, 'и': 12750, 'ë': 12118, 'е': 11887, 'ş': 11753, 'Č': 11647,
    '|': 11502, 'α': 10783, 'н': 10357, 'ń': 10219, 'ă': 9970, 'ș': 9709,
    'р': 9671, 'ê': 9470, 'ğ': 9071, '$': 8979, '→': 8950, '´': 8543,
    '€': 8470, 'с': 8398, '@': 8294, 'ο': 7819, 'æ': 7759, 'ʿ': 7726,
    'к': 7607, 'Ž': 7499, 'в': 7311, 'ð': 7139, 'т': 7137, 'ę': 6937,
    'л': 6784, 'ι': 5957, 'ė': 5873, 'ν': 5843, 'î': 5733, 'ś': 5550,
    'Á': 5543, 'ς': 5542, 'ą': 5490, 'ρ': 5237, 'Å': 5182, 'τ': 5098,
    'µ': 5024, 'ț': 4693, 'ů': 4564, 'Ç': 4500, 'İ': 4470, '•': 4434,
    'ε': 4419, 'λ': 4376, 'д': 4291, 'ï': 4213, 'ň': 4181, '′': 4023,
    'ż': 4001, 'Ł': 3902, '^': 3882, '~': 3846, 'σ': 3775, '·': 3768,
    'μ': 3714, 'м': 3632, 'у': 3619, 'ò': 3600, '—': 3596, 'ő': 3583,
    'κ': 3565, 'Ō': 3529, 'β': 3486, 'õ': 3123, 'й': 3077, '£': 3008,
    'Ş': 2892, '½': 2891, 'ē': 2885, 'π': 2837, 'Ś': 2831, '″': 2815,
    'г': 2801, 'я': 2775, 'Ú': 2775, 'Î': 2748, 'η': 2740, 'ə': 2659,
    'γ': 2640, '`': 2537, 'ь': 2508, 'п': 2484, 'υ': 2333, 'ί': 2249,
    'б': 2227, 'ì': 2224, 'ź': 2206, '\\': 2189, 'δ': 2181, 'ό': 2156,
    '{': 2151, 'Ø': 2114, 'С': 2105, 'ά': 2079, 'Đ': 1999, 'ا': 1961,
    'ч': 1957, 'ʻ': 1953, 'з': 1906, 'Ż': 1873, '}': 1868, 'ù': 1855,
    'œ': 1841, 'ω': 1827, 'ы': 1798, 'û': 1781, 'Í': 1722, '±': 1715,
    'Ó': 1712, 'ḫ': 1568, 'ḥ': 1537, 'ť': 1514, 'đ': 1489, 'К': 1455,
    'ų': 1431, 'В': 1400, 'М': 1379, 'ľ': 1371, 'ل': 1366, 'ή': 1363,
    'י': 1350, 'і': 1339, 'έ': 1297, 'ц': 1277, 'х': 1256, 'П': 1251,
    'Æ': 1242, 'ŏ': 1216, 'ʾ': 1203, '›': 1184, 'φ': 1180, 'θ': 1177,
    '‹': 1163, 'ύ': 1133, 'ו': 1130, 'χ': 1121, 'А': 1119, 'Р': 1116,
    'Þ': 1104, '‰': 1102, 'Т': 1077, 'Б': 1027, 'ṣ': 1022, 'Δ': 1009,
    'ш': 1001}

# 6.4 GiB (compressed) corpus from https://github.com/aparrish/gutenberg-dammit
#
# The above corpus and the following dict is released under the
# Creative Commons Attribution-ShareAlike 4.0 International license:
# https://creativecommons.org/licenses/by-sa/4.0/
gutenberg_dammit_counts = {  #
    ' ': 2969202277, 'e': 1707909140, 't': 1147642559, 'a': 1064145365,
    'o': 971665128, 'n': 948005230, 'i': 906858402, 's': 842394720,
    'r': 797921192, 'h': 722805259, 'l': 555680012, 'd': 548246746,
    'u': 413096101, '\n': 360128140, 'c': 335110366, 'm': 323297639,
    'f': 279516872, ',': 250938395, 'g': 244202344, 'w': 240158628,
    'p': 233907623, 'y': 216980200, 'b': 178870661, '.': 170648498,
    'v': 142336102, 'k': 102863144, '-': 61826799, 'I': 57693877,
    '"': 56045732, "'": 46676022, 'T': 45034133, 'A': 37245243, 'S': 33959715,
    'M': 26847094, '_': 25680679, 'E': 25603497, 'H': 25383900, 'j': 24869820,
    ';': 24824458, 'q': 24654807, 'C': 23680167, 'x': 22370803, 'B': 20360174,
    'ä': 20089637, 'L': 19791354, '1': 19590978, 'z': 18356531, 'N': 17816110,
    'R': 17757856, 'P': 17317640, 'W': 17300916, 'é': 17190908, 'O': 16628786,
    'D': 15984923, 'G': 14703363, 'F': 13510986, '2': 11745128, '0': 10893072,
    '!': 10787770, '?': 10779183, ':': 10154816, '3': 9032454, 'J': 8663967,
    '8': 8376888, '4': 7945247, '5': 7906709, '6': 7236716, '7': 6907613,
    '9': 6898337, 'V': 6689043, 'Y': 6672752, ')': 6362614, '(': 6303664,
    'K': 6103145, 'U': 5625106, ']': 5181030, '[': 5178808, '>': 5125309,
    '<': 5121298, 'à': 4469649, '，': 4114151, 'α': 3778860, 'è': 3448588,
    'ν': 3197200, 'ο': 3136013, 'τ': 3067079, '/': 2998660, '|': 2980798,
    '=': 2927347, 'ö': 2718922, 'ε': 2672343, 'ι': 2475287, 'á': 2133489,
    'ü': 2089506, 'X': 1942401, '。': 1836989, 'ê': 1780355, '’': 1709697,
    'Q': 1579346, 'ς': 1570485, 'ρ': 1561214, 'σ': 1388509, 'κ': 1370698,
    'π': 1340156, '»': 1338007, '~': 1335170, '“': 1313716, 'υ': 1307635,
    'Z': 1290349, '”': 1242329, 'ó': 1202808, 'μ': 1201530, 'η': 1194422,
    'λ': 1177918, 'í': 1175602, 'ß': 1168831, '«': 1134003, 'ί': 956879,
    'ά': 913756, 'ç': 858699, '*': 844586, '}': 842026, '{': 838955,
    'ό': 799540, '+': 760859, 'â': 736993, '&': 707966, '不': 707165,
    '—': 705811, 'ω': 701960, 'δ': 696267, 'έ': 695491, 'ù': 626778,
    '\u3000': 613102, '之': 578212, 'ô': 575439, 'å': 568803, 'Ã': 563205,
    'γ': 557088, '一': 551779, 'ã': 545880, '：': 535750, 'æ': 528567,
    'î': 527712, '人': 510786, 'ύ': 509052, 'θ': 496853, 'ή': 495188,
    'ò': 441949, '了': 429778, '「': 422933, '」': 420718, 'û': 418451,
    'χ': 414845, '道': 381509, 'ñ': 379554, '是': 358440, '有': 355096,
    'φ': 346109, '的': 335146, '#': 330251, 'ώ': 329883, '來': 314475}


def get_digit_frequencies(character_counts: dict):
    digits_frequencies = {}

    for d in sorted(digits, key=lambda k: character_counts[k]):
        digits_frequencies[d] = character_counts[d]

    total_count = sum(digits_frequencies.values())
    digit_ratios = {}

    for d, counts in digits_frequencies.items():
        digit_ratios[d] = counts / total_count

    return digit_ratios


def print_digit_frequencies(character_counts: dict):
    digits_frequencies = get_digit_frequencies(character_counts)
    for d, freq in digits_frequencies.items():
        print(d, character_counts[d], "    ratio to most common =", freq)

    print()
    print("as python dict:", digits_frequencies)
    print()


def p_header(text):
    print(f"\n\n{text}\n{'-' * len(text)}")


p_header("wikipedia_de_corpus")
print_digit_frequencies(wikipedia_de_corpus_counts)

p_header("linux_character")
print_digit_frequencies(linux_character_counts)

p_header("gutenberg_dammit")
print_digit_frequencies(gutenberg_dammit_counts)

avg = {d: 0 for d in digits}

frequencies = [[] for i in range(10)]
for count_map in (wikipedia_de_corpus_counts, linux_character_counts,
                  gutenberg_dammit_counts):

    freq_map = get_digit_frequencies(count_map)
    for n, d in enumerate(digits):
        frequencies[n].append(freq_map[d])
        avg[d] += freq_map[d]

for n, f_row in enumerate(frequencies):
    print(str(n) + "\t" + ("\t".join(map(str, f_row))))

p_header("average of all three")
s = sum(avg.values())
for d in digits:
    avg[d] /= s
    print(d, avg[d])
print(avg)
