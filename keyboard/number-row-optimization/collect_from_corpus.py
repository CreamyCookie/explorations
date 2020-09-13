from pathlib import Path
from collections import Counter


counter = Counter()

for f in Path("/tmp/gutenberg-dammit-files/").rglob("*.txt"):
    try:
        for c in f.read_text():
            counter[c] += 1
    except:  # file can't be read or decoded
        print(f"error for {f}")

print(counter)
