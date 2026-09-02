# Balls in a Circle

Six coloured balls drift inside a white circle, each trailing a fan of coloured
rays pinned to fixed anchor points on the rim.

## Rules

- Every ball starts at the same speed in a random direction.
- Wall bounces are reflections; ball-to-ball hits are elastic, so speeds diverge
  as the balls trade momentum.
- The rays are territory. Cross another ball's line and you take its anchor;
  bounce off the wall and you gain a fresh anchor where you struck it.
- Lose your last line and you are out.
- Everything creeps faster as the run goes on.

Wall hits are audible: a glancing touch is a faint tick, a square-on slam is a
deeper, longer thud. The impact sounds are synthesised at startup, so there are
no audio assets to ship.

Rendering is done on a 4x surface and smoothscaled down, since pygame's drawing
is not antialiased. Only the circle's bounding box is supersampled; the rest of
the window stays plain black.

## Running

```
pip install -r requirements.txt
python balls_in_circle.py
```

Press Escape or close the window to quit.

## Recording a batch

Rendering a run costs minutes; simulating one costs under a second. So the
pipeline simulates first and only draws the runs that turned out to be worth
drawing.

```
pip install -r requirements-recording.txt

python3 survey.py --runs 1000 --cap 90 --out runs.jsonl
python3 select.py --runs runs.jsonl --count 20 --low 60 --high 70 --limit purple=1
python3 record.py --selection selection.json --out-dir clips --jobs 2
```

- `survey.py` plays seeds out with nothing drawn, four at a time, and writes
  one line per run: how long it lasted, who won, when each ball went out. Runs
  that have not settled by `--cap` are abandoned there; most never settle.
- `select.py` filters that down to a window of lengths and fills per-colour
  quotas -- `--limit purple=1` means at most one purple win, and the other
  nineteen are shared round-robin between the remaining colours so the set is
  not all one colour. Nothing has been encoded yet, so changing your mind here
  is free.
- `record.py` replays the chosen seeds and pipes raw frames to ffmpeg, mixing
  the audio separately from the wall impacts the physics reports.

The three share `runner.py`, which pins the step to a fixed 1/60s and seeds the
one random choice in the game -- the six opening headings. That is what makes a
seed name a match: the survey's measurement and the recording of it are the
same run, frame for frame. The live game still steps on real elapsed time, so
playing a seed by hand will not reproduce its clip.

Clip length is the run's length plus `--hold`, the freeze on the winning frame.

## Tuning

The constants at the top of `balls_in_circle.py` control the whole simulation:
`SPEED` and `SPEEDUP` set the pace, `RAYS_PER_BALL` and `MAX_ANCHORS` the amount
of territory, `TRAIL_ALPHA` / `TRAIL_FADE` / `TRAIL_WIDTH` the smear, and
`BOUNCE_VOLUME` through `HARD_HIT` the sound. Note the comment on `MAX_SPEED`:
collisions are tested once a frame, so raising it too far lets balls tunnel
through lines and through each other.
