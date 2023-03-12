import sys
from pathlib import Path
from pprint import pprint


def run(path: Path) -> dict[str, int]:
    acc = {}
    with open(path) as f:
        content = f.read()
    for c in content:
        c_val = acc.get(c)
        if c_val is None:
            acc[c] = 1
        else:
            acc[c] = c_val + 1
    return acc

if __name__ == '__main__':
    target = sys.argv[1]
    freqs = run(Path(target))
    pprint(freqs)
    print(any([255 < ord(c) for c in freqs.keys()]))

