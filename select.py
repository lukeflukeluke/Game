"""Pick the clips worth recording out of a survey.

    python3 select.py --runs runs.jsonl --count 20 --low 60 --high 70 \
        --limit purple=1 --out selection.json

The brief was twenty runs that come in a little over a minute, exactly one of
them won by purple. That is a filter (finished, inside the window) plus a quota
(one purple, the rest shared out), and both are decided here on numbers the
survey already measured -- no video has been encoded at this point.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict


def load(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def parse_limits(pairs):
    """--limit purple=1 --limit red=0 -> {'purple': 1, 'red': 0}."""
    limits = {}
    for pair in pairs:
        name, _, value = pair.partition("=")
        if not value.isdigit():
            sys.exit(f"bad --limit {pair!r}, expected colour=number")
        limits[name] = int(value)
    return limits


def pick(runs, count, low, high, limits, target):
    """Choose count runs inside the window, honouring the per-colour quotas.

    Quotas are filled first, since a colour capped at one is the scarce thing.
    The rest goes round-robin over the colours that are still open, so twenty
    clips are not eighteen blue ones. Within a colour the run closest to target
    wins, which is what 'slightly over' means in practice.
    """
    pool = defaultdict(list)
    for r in runs:
        if r["winner"] and low <= r["seconds"] <= high:
            pool[r["winner"]].append(r)
    for colour in pool:
        pool[colour].sort(key=lambda r: (abs(r["seconds"] - target), r["seed"]))

    chosen, shortfalls = [], []
    for colour, quota in sorted(limits.items()):
        take = pool.get(colour, [])[:quota]
        if len(take) < quota:
            shortfalls.append(f"wanted {quota} {colour}, found {len(take)}")
        chosen += take
        pool[colour] = []  # a quota is a cap as well as a target

    open_colours = sorted(c for c in pool if c not in limits and pool[c])
    while len(chosen) < count and open_colours:
        # widest spread first: whichever open colour is least represented
        taken = Counter(r["winner"] for r in chosen)
        open_colours.sort(key=lambda c: (taken[c], -len(pool[c]), c))
        colour = open_colours[0]
        chosen.append(pool[colour].pop(0))
        open_colours = [c for c in open_colours if pool[c]]

    if len(chosen) < count:
        shortfalls.append(f"wanted {count} clips, found {len(chosen)}")
    return sorted(chosen, key=lambda r: r["seconds"]), shortfalls


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", default="runs.jsonl")
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--low", type=float, default=60.0)
    ap.add_argument("--high", type=float, default=70.0)
    ap.add_argument("--target", type=float, default=None,
                    help="length to sit closest to; defaults to --low")
    ap.add_argument("--limit", action="append", default=["purple=1"],
                    metavar="COLOUR=N", help="cap a colour's wins; repeatable")
    ap.add_argument("--out", default="selection.json")
    args = ap.parse_args()

    runs = load(args.runs)
    limits = parse_limits(args.limit)
    target = args.low if args.target is None else args.target
    chosen, shortfalls = pick(runs, args.count, args.low, args.high, limits, target)

    print(f"{len(runs)} runs surveyed, {len(chosen)} selected\n")
    print(f"{'seed':>6}  {'length':>7}  winner")
    for r in chosen:
        print(f"{r['seed']:>6}  {r['seconds']:6.2f}s  {r['winner']}")
    print("\n" + ", ".join(f"{c} {n}" for c, n in
                           Counter(r["winner"] for r in chosen).most_common()))

    for line in shortfalls:
        print(f"\nshort: {line} -- survey more seeds or widen --low/--high",
              file=sys.stderr)

    with open(args.out, "w") as f:
        json.dump({
            "source": args.runs,
            "window": [args.low, args.high],
            "target": target,
            "limits": limits,
            "clips": chosen,
        }, f, indent=2)
    print(f"\nwritten to {args.out}")
    if shortfalls:
        sys.exit(1)


if __name__ == "__main__":
    main()
