"""Shared plumbing for running the simulation off-screen and reproducibly.

The game itself steps on whatever dt the clock hands it, which is fine to play
but useless to record: two runs of the same seed would drift apart. Everything
here steps on a fixed dt instead, so a seed names one exact match. survey.py
watches thousands of those matches with nothing drawn; record.py replays the
handful worth keeping and draws every frame.
"""

import os

# both have to be set before pygame is imported, or it looks for real devices
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import random  # noqa: E402

import balls_in_circle as sim  # noqa: E402

FPS = 60
DT = 1.0 / FPS

COLOUR_NAMES = dict(
    zip(sim.COLOURS, ["red", "green", "blue", "orange", "purple", "yellow"])
)
NAME_COLOURS = {name: colour for colour, name in COLOUR_NAMES.items()}


def new_balls(seed):
    """The opening position for one seed."""
    balls = sim.start_balls(random.Random(seed))
    for b in balls:
        b["path"] = [(b["x"], b["y"])]
    return balls


def name_of(ball):
    return COLOUR_NAMES[ball["colour"]]


def simulate(seed, cap_seconds):
    """Play one seed out with nothing drawn.

    Stops when a single ball is left, when the last balls go out together, or
    when cap_seconds is reached -- most runs never settle, and waiting on them
    is the whole cost of a survey.
    """
    balls = new_balls(seed)
    alive = {name_of(b) for b in balls}
    knockouts = []
    cap_frames = round(cap_seconds * FPS)
    frames = 0

    while len(balls) > 1 and frames < cap_frames:
        sim.advance(balls, DT)
        frames += 1
        left = {name_of(b) for b in balls}
        for gone in sorted(alive - left):
            knockouts.append({"t": round(frames * DT, 4), "colour": gone})
        alive = left

    if len(balls) == 1:
        outcome, winner = "won", name_of(balls[0])
    elif not balls:
        outcome, winner = "wiped_out", None
    else:
        outcome, winner = "unfinished", None

    return {
        "seed": seed,
        "frames": frames,
        "seconds": round(frames * DT, 4),
        "outcome": outcome,
        "winner": winner,
        "survivors": sorted(alive),
        "knockouts": knockouts,
    }
