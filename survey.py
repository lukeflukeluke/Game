"""Play a batch of seeds out with nothing drawn, and write down how each ended.

    python3 survey.py --runs 200 --out runs.jsonl

Rendering a minute of this costs minutes; simulating it costs under a second,
so the cheap thing goes first and the expensive thing only ever sees the runs
worth keeping. Every result is one JSON object on one line, keyed by the seed
that produced it -- record.py replays a seed to get that exact match back.
"""

import argparse
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool

from runner import simulate


def survey(seeds, cap, jobs):
    """Run every seed, newest results first out of whichever worker finishes."""
    started = time.time()
    results = []
    with Pool(jobs) as pool:
        for done, result in enumerate(
            pool.imap_unordered(_one, [(s, cap) for s in seeds], chunksize=1), 1
        ):
            results.append(result)
            elapsed = time.time() - started
            left = elapsed / done * (len(seeds) - done)
            print(
                f"\r{done}/{len(seeds)} runs  {elapsed:5.0f}s elapsed"
                f"  {left:5.0f}s left ",
                end="",
                file=sys.stderr,
                flush=True,
            )
    print(file=sys.stderr)
    return sorted(results, key=lambda r: r["seed"])


def _one(args):
    return simulate(*args)


def summarise(results, low, high):
    """What the batch looked like, and how much of it is worth recording."""
    finished = [r for r in results if r["winner"]]
    keepable = [r for r in finished if low <= r["seconds"] <= high]
    print(f"\n{len(results)} runs simulated")
    print(f"  {len(finished):4d} produced a winner")
    print(f"  {len(results) - len(finished):4d} were still going at the cap")
    if finished:
        lengths = sorted(r["seconds"] for r in finished)
        mid = lengths[len(lengths) // 2]
        print(f"  winning runs ran {lengths[0]:.0f}-{lengths[-1]:.0f}s,"
              f" median {mid:.0f}s")
        tally = Counter(r["winner"] for r in finished).most_common()
        print("  winners: " + ", ".join(f"{name} {n}" for name, n in tally))
    print(f"\n{len(keepable)} in the {low:g}-{high:g}s window:")
    for name, n in Counter(r["winner"] for r in keepable).most_common():
        print(f"  {name:7s} {n}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", type=int, default=200, help="how many seeds to try")
    ap.add_argument("--start-seed", type=int, default=0)
    ap.add_argument("--cap", type=float, default=90.0,
                    help="seconds of simulation before a run is abandoned")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default="runs.jsonl")
    ap.add_argument("--low", type=float, default=60.0,
                    help="window the summary reports on")
    ap.add_argument("--high", type=float, default=70.0)
    args = ap.parse_args()

    seeds = range(args.start_seed, args.start_seed + args.runs)
    results = survey(seeds, args.cap, args.jobs)
    with open(args.out, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    summarise(results, args.low, args.high)
    print(f"\nwritten to {args.out}")


if __name__ == "__main__":
    main()
