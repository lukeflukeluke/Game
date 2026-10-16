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

# Backseat Brawl

`backseat-brawl/index.html` is a two-player party game for one phone, made for
long car journeys. Hold the phone sideways between you: the left half of the
screen is Orange, the right half is Blue. Every game is played by tapping or
holding your own half, so it still works on a bumpy road.

Eight micro-games are dealt in random order, and the first player to 5 points
wins (tap the pill on the title screen to switch to 3 or 7):

- **Green Light**: tap on green; jumping the light (including prank ambers) hands over the point.
- **Pump It**: pump your balloon. Both balloons burst at the same secret size, and the biggest one left wins.
- **Armrest War**: mash to shove the other elbow off the armrest.
- **Park It**: brake (with momentum) as close to the wall as you dare.
- **Pass the Bomb**: tap the number on the bomb to throw it back. Each throw needs one more tap.
- **Cow Spotter**: tap only for a cow. Bulls and buffalo are not cows.
- **Pothole Hop**: same road for both of you; jump cones and potholes, and the last car still driving wins.
- **Tunnel Vision**: both hold, then let go at exactly N seconds after the clock disappears.

Open the file in Safari (no install, no build). It needs a connection only for
the fonts; once loaded it plays offline. On a computer, `A` and `L` act as the
two players' thumbs.
