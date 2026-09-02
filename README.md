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

## Tuning

The constants at the top of `balls_in_circle.py` control the whole simulation:
`SPEED` and `SPEEDUP` set the pace, `RAYS_PER_BALL` and `MAX_ANCHORS` the amount
of territory, `TRAIL_ALPHA` / `TRAIL_FADE` / `TRAIL_WIDTH` the smear, and
`BOUNCE_VOLUME` through `HARD_HIT` the sound. Note the comment on `MAX_SPEED`:
collisions are tested once a frame, so raising it too far lets balls tunnel
through lines and through each other.
