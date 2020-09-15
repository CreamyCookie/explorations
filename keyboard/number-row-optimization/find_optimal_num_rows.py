from itertools import permutations
from string import digits


# Tracks how comfortable and quick each key is to press (from pinky to the two
# index finger rows). Even if all keys are in the home row, you might still
# want to give your pinky less work and thus a lower value.
LEFT_KEYS_POSITION_RATING = [0.55, 0.7, 1, 0.98, 0.8]

# if this is 0, balance between left and right hand keys is ignored
# if this is 1 the rating equals the smallest 'value' of both sides
BALANCE_FACTOR = 0.65

# How Zipfian do we want the distribution to be.
# The closer this is to zero, the more we will modify the frequency value of 0
# to fit with the real world data from Wikipedia and Gutenberg.
# Increase (to up to 1) if you want to optimize for programming.
# If USE_REAL_WORLD_AVERAGE is set true, we will instead smooth between the
# Zipfian and the real world distribution using this value.
ZIPF_FACTOR = 0.7

# ratio for zero from real world data (wiki + gutenberg)
# if this was 0.5 it would imply half of all digits are zero
RW_0_VALUE = 0.134418127182388

# I'd recommend against enabling this, as Wikipedia and Gutenberg both are
# biased by, among others, how much data there is for certain years (1800-1999)
# Similarly, I'd leave the ZIPF_FACTOR relatively high, unless you don't code.
USE_REAL_WORLD_AVERAGE = False

CURRENT = '12345 67890'
LEFT = CURRENT[:5]

# @formatter:off
MANUAL_DIGIT_PERMUTATIONS = [
    CURRENT,
    # left side: rotate right twice, right side: move 0 in the middle
    '45123 67089',

    # reverse left half and move 0 to before 6
    # relative simple change that's easy to remember and keeps numbers on their
    # side but muscle memory for every number but 3 needs to be retrained
    '54321 06789',

    # switch 1 with 4 and 7 with 0 - pretty unintuitive change, but only 4 keys
    # to relearn and numbers stay on their side
    '42315 60897',
]
# @formatter:on

MAX_PERMUTATIONS_COUNT = 10

# to find the best arrangement with at most this many swaps
MAX_N_SWAPS = 2

NUM_FMT = '.2f'

# -----------------------------------------------------------------------------


digit_frequency = {d: 1 / (n + 1) for n, d in enumerate(digits)}

print()
print(f'\nzipf digit frequency: {digit_frequency}')

if USE_REAL_WORLD_AVERAGE:
    # linux c files
    code_digit_frequency = {  #
        '9': 0.02909295446151662, '7': 0.034580576202551956,
        '5': 0.04585847891973208, '6': 0.05364252590529784,
        '8': 0.058946164959403545, '4': 0.06311291445004744,
        '3': 0.07513337383312362, '2': 0.12266975307381336,
        '1': 0.13828881215531044, '0': 0.3786744460392031}

    # assume zipf = digit frequencies in code
    code_digit_frequency = digit_frequency

    # 1/2 gutenberg, 1/2 wikipedia
    digit_frequency = {  #
        '0': 0.13441812718238821, '1': 0.2199522594323372,
        '2': 0.1185139034025656, '3': 0.0761447147048975,
        '4': 0.0690145404114608, '5': 0.07157156795805049,
        '6': 0.06450709962180562, '7': 0.06354688650306475,
        '8': 0.07996884100271787, '9': 0.10236205978071194}

    for d, f in digit_frequency.items():
        cf = code_digit_frequency[d]
        digit_frequency[d] = ZIPF_FACTOR * cf + (1 - ZIPF_FACTOR) * f
else:
    d0 = digit_frequency['0']
    digit_frequency['0'] = ZIPF_FACTOR * d0 + (1 - ZIPF_FACTOR) * RW_0_VALUE

print(f'\nused digit frequency: {digit_frequency}')

# normalize
s = sum(digit_frequency.values())
for d, freq in digit_frequency.items():
    digit_frequency[d] = freq / s

print(f'\nused digit_frequency (normalized): {digit_frequency}')

# We normalize to a total of 100
s = sum(LEFT_KEYS_POSITION_RATING) / 100
LEFT_KEYS_POSITION_RATING = [i / s for i in LEFT_KEYS_POSITION_RATING]


def value_per_side_and_rating(perm: str):
    av, bv = value_per_side(perm)

    # simple measure for how good this number arrangement is
    rating = (av + bv) - abs(av - bv) * BALANCE_FACTOR

    return av, bv, rating


def value_per_side(perm: str):
    a, b = perm.split()
    return value_for_left_side(a), value_for_left_side(b[::-1])


def value_for_left_side(perm: str):
    # value depends on how often digit appears and which key position
    # keys easier, faster, more comfortable to hit = more valuable
    return sum(LEFT_KEYS_POSITION_RATING[pos] * digit_frequency[d]  #
               for pos, d in enumerate(perm))


def print_column_header():
    print_columns("arrangment", "rating / side", "rating")
    print()


def print_columns(perm, balance, rating):
    print(f"{perm:<14}{balance:<16}{rating:<16}")


current_rating = value_per_side_and_rating(CURRENT)[2]


def print_perm_with_rating(s: str, fmt=NUM_FMT):
    av, bv, rating = value_per_side_and_rating(s)
    improvement_percentage = 100 * ((rating / current_rating) - 1)
    increase = ''
    if improvement_percentage != 0:
        increase = f' ({improvement_percentage:+{fmt}}% compared to current)'
    if s == CURRENT:
        increase = ' (current)'

    balance = f"({av:{fmt}}, {bv:{fmt}})"
    rating_text = f"{rating:{fmt}}{increase}"

    print_columns(s, balance, rating_text)


def print_header(text):
    print(f"\n\n{text}\n{'-' * len(text)}")


def get_swaps(a, target=CURRENT):
    len_target = len(target)
    if len(a) != len_target:
        raise ValueError("both arguments must have the same length")

    swaps = []
    n = 0
    arr = list(a)
    while n < len_target:
        cn = target.index(arr[n])
        if cn == n:
            n += 1
        else:
            arr[cn], arr[n] = arr[n], arr[cn]
            swaps.append((arr[n], arr[cn]))
    return swaps


def count_swaps(arrangement, current=CURRENT):
    """
    >>> current = "12345 67890"
    >>> count_swaps(current, current)
    0
    >>> count_swaps("54321 67890", current)
    2
    >>> count_swaps("67890 12345", current)
    5
    >>> count_swaps("42315 60897", current)
    2
    >>> count_swaps("12345 60897", current)
    1
    >>> count_swaps("12345 60987", current)
    2
    >>> count_swaps("23145 67890", current)
    2
    >>> count_swaps("82315 67094", current)  # 1 with 4, 0 with 8, 8 with 4
    3
    """
    len_current = len(current)
    if len(arrangement) != len_current:
        raise ValueError("both arguments must have the same length")

    swaps = 0
    n = 0
    arr = list(arrangement)
    while n < len_current:
        cn = current.index(arr[n])
        if cn == n:
            n += 1
        else:
            swaps += 1
            arr[cn], arr[n] = arr[n], arr[cn]

    return swaps


# -----------------------------------------------------------------------------


print_header("Entered permutations")
print_column_header()
for ds in MANUAL_DIGIT_PERMUTATIONS:
    print_perm_with_rating(ds)

max_permutations = [('', 0) for _ in range(MAX_PERMUTATIONS_COUNT)]

max_keep_sides_perm = None
max_keep_sides_perm_rating = 0

max_only_n_swaps_perm = None
max_only_n_swaps_perm_rating = 0

min_perm = None
min_perm_rating = float("inf")

# 10! = 3628800 - will take a bit (could be optimized if sides are mirrored)
for p in permutations(digits):
    p = ''.join(p)
    p = p[:5] + ' ' + p[5:]

    rating = value_per_side_and_rating(p)[2]

    if rating < min_perm_rating:
        min_perm_rating = rating
        min_perm = p

    if rating > max_only_n_swaps_perm_rating and count_swaps(p) <= MAX_N_SWAPS:
        max_only_n_swaps_perm_rating = rating
        max_only_n_swaps_perm = p

    if rating > max_keep_sides_perm_rating and all(d in p[:5] for d in LEFT):
        max_keep_sides_perm_rating = rating
        max_keep_sides_perm = p

    for i in range(MAX_PERMUTATIONS_COUNT):
        cur = max_permutations[i]

        if cur[1] < rating:
            max_permutations[i] = (p, rating)
            break

print_header("Worst permutation")
print_perm_with_rating(min_perm)

print_header("Best permutations")
print_column_header()
for s, rating in max_permutations:
    print_perm_with_rating(s)

print()
print()
print("Best where digits stay on their current side:")
print_perm_with_rating(max_keep_sides_perm)

print()
print(f"Best with at most {MAX_N_SWAPS} swaps:")
print_perm_with_rating(max_only_n_swaps_perm)

how_swap = ", ".join(
        f'{a} with {b}' for a, b in get_swaps(max_only_n_swaps_perm))
print(" -- " + how_swap)
