import sys
from itertools import permutations
from string import digits


# Tracks how comfortable and quick each key is to press (from pinky to the two
# index finger rows). Even if all keys are in the home row, you might still
# want to give your pinky less work and thus a lower value.
LEFT_KEYS_POSITION_RATING = [0.55, 0.8, 1, 0.98, 0.72]

# By default, the same ratings are mirrored for the right side.
RIGHT_KEYS_POSITION_RATING = LEFT_KEYS_POSITION_RATING[::-1]

# Defines the maximum percentage that can be removed from total rating. The
# actual value depends on how much the average frequency of each side differs.
# If this is 0, balance between left and right hand keys is ignored.
# If this is 1, the final rating will be 0 if all the digits with the highest
# frequency are on the same side.
IMBALANCE_PENALTY_FACTOR = 0.38

# How Zipfian do we want the distribution to be.
# The closer this is to zero, the more we will modify the frequency value of 0
# to fit with the real world data from Wikipedia and Gutenberg.
# Increase (to up to 1) if you want to optimize for programming.
# If USE_REAL_WORLD_AVERAGE is set true, we will instead smooth between the
# Zipfian and the real world distribution using this value.
ZIPF_FACTOR = 0.6

# frequency for zero from real world data (wiki + gutenberg)
# If this was 0.5 it would imply half of all digits are zero.
RW_0_FREQ = 0.134418127182388

# I'd recommend against enabling this, as Wikipedia and Gutenberg both are
# biased by, among others, how much data there is for certain years (1800-1999)
# Similarly, I'd not set the ZIPF_FACTOR to below 0.4 if you program regularly.
USE_REAL_WORLD_AVERAGE = False

CURRENT = '12345 67890'
LEFT = CURRENT[:5]

# @formatter:off
MANUAL_DIGIT_PERMUTATIONS = [
    # left side: rotate right twice, right side: move 0 in the middle
    '45123 67089',

    # reverse left half and move 0 to before 6
    # relative simple change that's easy to remember and keeps numbers on their
    # side but muscle memory for every number but 3 needs to be retrained
    '54321 06789',

    # left side: reverse left and move 5 to end, right side: rotate right twice
    # or: highest digit on outer index key, rest increase outwards from there
    # relatively easy to remember and digits stay on current side
    '43215 90678',
]
# @formatter:on

CHECK_ALL_PERMUTATIONS = True

BEST_PERMUTATIONS_COUNT = 10

# to find the best arrangement with at most this many swaps
MAX_N_SWAPS = 2

NUM_FMT = '.2f'


# -----------------------------------------------------------------------------


def normalize(items, target_sum=1):
    s = sum(items) / target_sum
    for n in range(len(items)):
        items[n] = items[n] / s


def normalize_dict_values(mapping, target_sum=1):
    s = sum(mapping.values()) / target_sum

    for k, v in mapping.items():
        mapping[k] = v / s


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
    digit_frequency['0'] = ZIPF_FACTOR * d0 + (1 - ZIPF_FACTOR) * RW_0_FREQ

print(f'\nused digit frequency: {digit_frequency}')

normalize_dict_values(digit_frequency)

print(f'\nused digit frequency (normalized): {digit_frequency}')

# We normalize to a total of 100 to make things easier to read
normalize(LEFT_KEYS_POSITION_RATING, 100)
normalize(RIGHT_KEYS_POSITION_RATING, 100)

dfs = sorted(digit_frequency.values())
max_frequency_delta_between_sides = sum(dfs[5:]) / 5 - sum(dfs[:5]) / 5


class RatingResult:
    def __init__(self, left, right, total, imbalance_penalty):
        self.left = left
        self.right = right
        self.total = total
        self.imbalance_penalty = imbalance_penalty


def rating_per_side_and_total(perm):
    left, right = rating_per_side(perm)
    total = left + right

    laf, raf = average_frequency_per_side(perm)
    norm_frequency_delta = abs(laf - raf) / max_frequency_delta_between_sides
    imbalance_penalty = total * norm_frequency_delta * IMBALANCE_PENALTY_FACTOR
    total -= imbalance_penalty

    return RatingResult(left, right, total, imbalance_penalty)


def average_frequency_per_side(perm):
    left, right = perm.split()
    return average_frequency_of_side(left), average_frequency_of_side(right)


def average_frequency_of_side(perm):
    return sum(digit_frequency[d] for d in perm) / 5


def rating_per_side(perm):
    left, right = perm.split()

    left_rating = rating_for_one_side(left, LEFT_KEYS_POSITION_RATING)
    right_rating = rating_for_one_side(right, RIGHT_KEYS_POSITION_RATING)

    return left_rating, right_rating


def rating_for_one_side(perm, rating):
    # depends on how often a digit appears and in which key position
    return sum(rating[pos] * digit_frequency[d] for pos, d in enumerate(perm))


current_rating = rating_per_side_and_total(CURRENT).total


def print_perm_with_rating(perm, fmt=NUM_FMT):
    result = rating_per_side_and_total(perm)

    improvement_percentage = 100 * ((result.total / current_rating) - 1)
    increase = ''
    if improvement_percentage != 0:
        increase = f'{improvement_percentage:+{fmt}}%'

    left_text = f"{result.left:{fmt}}"
    right_text = f"{result.right:{fmt}}"
    total_text = f"{result.total:{fmt}}"
    imbalance_penalty_text = f"{result.imbalance_penalty:.5f}"

    print_columns(perm, imbalance_penalty_text, left_text, right_text,
                  total_text, increase)


def print_columns(perm, imbalance_penalty, left, right, total, change):
    if change:
        change = f"    {change}"
    print(f"{perm}{imbalance_penalty:>10}"
          f"{left:>8}{right:>8}{total:>8}{change}")


# uncomment if you want to create markdown tables
# base_print_columns = print_columns
# def print_columns(*args):
#     base_print_columns(*[f"| {i}" for i in args])
# print_columns("", "", "", "", "")


def print_header(text, is_current=False):
    print(f"\n\n{text}\n{'-' * len(text)}")

    change = ''
    if not is_current:
        change = "change from current"

    print_columns("arrangement", "penalty", "left", "right", "total", change)
    print()


def get_swaps(a, target=CURRENT):
    len_target = len(target)
    if len(a) != len_target:
        raise ValueError("both arguments must have the same length")

    char_to_current_index = {c: n for n, c in enumerate(target)}
    swaps = []
    n = 0
    arr = list(a)
    while n < len_target - 1:
        cn = char_to_current_index[arr[n]]
        if cn == n:
            n += 1
        else:
            arr[cn], arr[n] = arr[n], arr[cn]
            swaps.append((target[n], target[cn]))
    return swaps


def count_swaps(arrangement, target=CURRENT):
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
    len_current = len(target)
    if len(arrangement) != len_current:
        raise ValueError("both arguments must have the same length")

    char_to_current_index = {c: n for n, c in enumerate(target)}

    swaps = 0
    n = 0
    arr = list(arrangement)
    while n < len_current - 1:
        cn = char_to_current_index[arr[n]]
        if cn == n:
            n += 1
        else:
            swaps += 1
            # move current character to it's target place
            arr[cn], arr[n] = arr[n], arr[cn]

    return swaps


# -----------------------------------------------------------------------------

print_header("Current layout", is_current=True)
print_perm_with_rating(CURRENT)

print_header("Entered permutations")
for ds in MANUAL_DIGIT_PERMUTATIONS:
    print_perm_with_rating(ds)

if not CHECK_ALL_PERMUTATIONS:
    sys.exit()

best_permutations = [('', 0) for _ in range(BEST_PERMUTATIONS_COUNT)]

best_keep_sides_perm = None
best_keep_sides_perm_rating = 0

best_n_swaps_perm = None
best_n_swaps_perm_rating = 0

worst_perm = None
worst_perm_rating = float("inf")

most_balanced_perm = None
most_balanced_imbalance_penalty = float("inf")

# 10! / 2 = 1 814 400 - will take a bit
for p in permutations(digits):
    p = ''.join(p[:5]) + ' ' + ''.join(p[5:])

    result = rating_per_side_and_total(p)
    rating = result.total

    if result.imbalance_penalty < most_balanced_imbalance_penalty:
        most_balanced_imbalance_penalty = result.imbalance_penalty
        most_balanced_perm = p

    if rating < worst_perm_rating:
        worst_perm_rating = rating
        worst_perm = p

    if rating > best_n_swaps_perm_rating and count_swaps(p) <= MAX_N_SWAPS:
        best_n_swaps_perm_rating = rating
        best_n_swaps_perm = p

    if rating > best_keep_sides_perm_rating and all(d in p[:5] for d in LEFT):
        best_keep_sides_perm_rating = rating
        best_keep_sides_perm = p

    for i in range(BEST_PERMUTATIONS_COUNT):
        cur = best_permutations[i]

        if cur[1] < rating:
            best_permutations[i] = (p, rating)
            break

print_header("Worst permutation")
print_perm_with_rating(worst_perm)

print_header("Best permutations")
for s, rating in best_permutations:
    print_perm_with_rating(s)

print_header("Best where digits stay on their current side")
print_perm_with_rating(best_keep_sides_perm)

print_header(f"Best with at most {MAX_N_SWAPS} swaps")
print_perm_with_rating(best_n_swaps_perm)

swaps = [f'{a} with {b}' for a, b in get_swaps(best_n_swaps_perm)]

print(f"({', '.join(swaps[:-1])} and {swaps[-1]})")

print_header(f"Best balance")
print_perm_with_rating(most_balanced_perm)