"""Six coloured balls drifting inside a white circle, trailing coloured rays.

Each ball sets off in a random direction at the same speed, then bounces off the
inside of the circle and off the other balls. Ball-to-ball hits are elastic, so
speeds diverge as they trade momentum. Each ball smears a faint trail of its own
colour behind it, which fades back to black. Wall hits are audible: a glancing
touch is a barely-there tick, a square-on slam is a deeper, longer thud.

The lines are territory. Cross another ball's line and you take its anchor for
your own; bounce off the wall and you gain a fresh anchor where you struck it.
Lose your last line and you are out. Everything creeps faster as it goes. Each ray is pinned to a fixed point on the circle,
so the outer ends stay put while the inner ends travel with the balls.

Everything is drawn on a 4x surface and smoothscaled down, because pygame's
drawing is not antialiased -- the downscale is what smooths the edges. Only the
circle's bounding box is supersampled; the rest of the window is plain black.
"""

import array
import math
import random
import sys

import pygame

WIDTH, HEIGHT = 800, 800
CIRCLE_RADIUS = 260
CIRCLE_WIDTH = 3
BALL_RADIUS = 22
BALL_OUTLINE = 2  # white ring drawn outside the ball
OFFSET = 80  # how far each ball sits from the exact centre
RAYS_PER_BALL = 10
RAY_SPREAD = math.radians(48)  # total fan angle covered by one ball's rays
RAY_WIDTH = 1
MAX_ANCHORS = 50  # per ball; a ball at the cap drops its oldest to take a new one
SPEED = 200  # pixels per second, the starting speed of every ball
SPEEDUP = 0.03  # fraction of its speed each ball gains per second
MAX_SPEED = 60000  # ceiling, px/s. Collisions are tested once a frame, so a ball
# must not move more than its own width (48px, i.e. 2880px/s) between frames or
# it tunnels through lines, and half that before it tunnels through balls.
TRAIL_ALPHA = 0.28  # how bright a freshly laid trail is, against the ball colour
TRAIL_FADE = 1  # brightness subtracted from the trail every frame
TRAIL_WIDTH = 34  # thickness of the smear, in final pixels
SCALE = 4  # supersampling factor
BOUNCE_VOLUME = 0.2  # loudest a wall hit ever gets
QUIETEST = 0.09  # softest hit, as a fraction of that -- the dynamic range
SOFT_HIT = 250  # impact speed, px/s, at or below which a hit is its faintest
HARD_HIT = 960  # impact speed at or above which it is its most dramatic
BOUNCE_TONES = 11  # how many variants of the sound to pre-render
SAMPLE_RATE = 44100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLOURS = [
    (230, 25, 75),  # red
    (60, 180, 75),  # green
    (67, 99, 216),  # blue
    (245, 130, 49),  # orange
    (145, 30, 180),  # purple
    (255, 225, 25),  # yellow
]

EDGE = CIRCLE_RADIUS - CIRCLE_WIDTH / 2  # rays stop on the inner lip of the ring
GAP = BALL_RADIUS + BALL_OUTLINE  # full ball radius, white ring included
WALL = EDGE - GAP  # how far a ball's centre can get from the middle
BOX = 2 * CIRCLE_RADIUS + CIRCLE_WIDTH + 4  # supersampled region, in final pixels


def ray_end(bx, by, radius, dx, dy):
    """Where the ray leaving (bx, by) along (dx, dy) meets a circle at 0, 0."""
    b = bx * dx + by * dy
    t = -b + math.sqrt(b * b - (bx * bx + by * by) + radius * radius)
    return bx + t * dx, by + t * dy


def starting_anchors():
    """The fan of anchors each ball owns at the start.

    Anchors are fixed points on the circle, but ownership is not: they change
    hands as balls cross each other's lines.
    """
    anchors = []
    for i in range(len(COLOURS)):
        base = 2 * math.pi * i / len(COLOURS)
        bx, by = OFFSET * math.cos(base), OFFSET * math.sin(base)
        step = RAY_SPREAD / (RAYS_PER_BALL - 1)
        fan = []
        for j in range(RAYS_PER_BALL):
            a = base - RAY_SPREAD / 2 + j * step
            fan.append(ray_end(bx, by, EDGE, math.cos(a), math.sin(a)))
        anchors.append(fan)
    return anchors


def start_balls(rng=random):
    """Every ball at its original spot, heading off in a random direction.

    The headings are the only randomness in the whole simulation, so passing a
    seeded random.Random makes a run reproducible: same seed, same match, frame
    for frame. survey.py and record.py rely on that.
    """
    balls = []
    fans = starting_anchors()
    for i in range(len(COLOURS)):
        base = 2 * math.pi * i / len(COLOURS)
        heading = rng.uniform(0, 2 * math.pi)
        balls.append(
            {
                "x": OFFSET * math.cos(base),
                "y": OFFSET * math.sin(base),
                "vx": SPEED * math.cos(heading),
                "vy": SPEED * math.sin(heading),
                "colour": COLOURS[i],
                "anchors": fans[i],
                "path": [],
            }
        )
    return balls


def collide(balls):
    """Elastic collisions between equal-mass balls, plus overlap separation.

    Momentum and energy are conserved, so individual speeds change on impact --
    SPEED is only the starting speed, not a permanent one.
    """
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            a, b = balls[i], balls[j]
            dx, dy = b["x"] - a["x"], b["y"] - a["y"]
            dist = math.hypot(dx, dy)
            if dist == 0 or dist >= 2 * GAP:
                continue

            nx, ny = dx / dist, dy / dist
            approach = (b["vx"] - a["vx"]) * nx + (b["vy"] - a["vy"]) * ny
            if approach < 0:  # ignore pairs already moving apart
                # equal masses swap the velocity component along the normal
                a["vx"] += approach * nx
                a["vy"] += approach * ny
                b["vx"] -= approach * nx
                b["vy"] -= approach * ny

            # separate them so they cannot stick together
            push = (2 * GAP - dist) / 2
            a["x"] -= nx * push
            a["y"] -= ny * push
            b["x"] += nx * push
            b["y"] += ny * push


def bounce_samples(hardness, rate, channels=1):
    """Raw 16-bit samples of one impact. hardness: 0 (light tick) to 1 (thud).

    Harder hits drop in pitch, ring longer and carry a brighter attack. That is
    what separates a thud from a tick far more than volume alone does. Kept
    apart from the mixer so an offline recording can build the same sound
    without opening an audio device.
    """
    freq = 620 - 300 * hardness  # deeper the harder it lands
    decay = 95 - 55 * hardness  # and it rings on rather than clipping short
    bright = 0.25 + 0.5 * hardness  # attack transient, strongest on a slam
    length = int(rate * (0.06 + 0.10 * hardness))

    samples = array.array("h")
    phase = 0.0
    for i in range(length):
        t = i / rate
        # sweep the pitch down as it decays; that sag is the 'thud'
        phase += 2 * math.pi * (freq * (1 - 0.18 * hardness * t / 0.12)) / rate
        v = math.sin(phase) * math.exp(-t * decay)
        v += bright * math.sin(2.9 * phase) * math.exp(-t * decay * 3)
        v *= min(1.0, t / 0.002)  # tiny fade-in, or the start of it clicks
        level = int(max(-1.0, min(1.0, v * 0.6)) * 32767)
        for _ in range(abs(channels)):
            samples.append(level)

    return samples


def bounce_tone(hardness, rate, channels):
    """The same impact, handed to the mixer as a playable Sound."""
    return pygame.mixer.Sound(buffer=bounce_samples(hardness, rate, channels).tobytes())


def make_bounce_sounds():
    """A bank of impact sounds, light to heavy. None if there is no audio.

    The buffers match however the mixer actually opened -- feeding a mono buffer
    to a stereo mixer plays it at double speed, an octave sharp.
    """
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        except pygame.error:
            return None

    rate, _, channels = pygame.mixer.get_init()
    return [
        bounce_tone(i / (BOUNCE_TONES - 1), rate, channels)
        for i in range(BOUNCE_TONES)
    ]


def step_ball(b, dt):
    """Move one ball for dt, reflecting off the wall at the exact contact point.

    Records the corner it turned through, so the trail bends on the wall instead
    of jumping to it.
    """
    path = b["path"]
    impacts = []
    left = dt

    for _ in range(4):  # more than one bounce per frame is possible, barely
        speed_sq = b["vx"] ** 2 + b["vy"] ** 2
        if speed_sq == 0:
            break
        # solve |p + v t| = WALL for the time of impact
        along = b["x"] * b["vx"] + b["y"] * b["vy"]
        outside = b["x"] ** 2 + b["y"] ** 2 - WALL**2
        disc = along**2 - speed_sq * outside
        if disc <= 0:
            break
        hit = (-along + math.sqrt(disc)) / speed_sq
        if hit > left:
            break

        b["x"] += b["vx"] * hit
        b["y"] += b["vy"] * hit
        path.append((b["x"], b["y"]))
        left -= hit

        nx, ny = b["x"] / WALL, b["y"] / WALL
        dot = b["vx"] * nx + b["vy"] * ny
        b["vx"] -= 2 * dot * nx
        b["vy"] -= 2 * dot * ny
        # speed straight into the wall, plus where on the wall it landed
        impacts.append((abs(dot), nx, ny))

    b["x"] += b["vx"] * left
    b["y"] += b["vy"] * left
    path.append((b["x"], b["y"]))
    return impacts


def distance_to_line(px, py, ax, ay, bx, by):
    """Shortest distance from a point to the segment ab."""
    dx, dy = bx - ax, by - ay
    span = dx * dx + dy * dy
    if span == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / span))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def steal_lines(balls):
    """Any ball sitting on someone else's line takes that anchor for itself."""
    for taker in balls:
        for owner in balls:
            if owner is taker:
                continue

            kept = []
            for ax, ay in owner["anchors"]:
                # measure against the line as drawn, which starts clear of the
                # owner's own ball rather than at its centre
                dx, dy = ax - owner["x"], ay - owner["y"]
                length = math.hypot(dx, dy)
                if length == 0:
                    kept.append((ax, ay))
                    continue
                sx = owner["x"] + GAP * dx / length
                sy = owner["y"] + GAP * dy / length

                if distance_to_line(taker["x"], taker["y"], sx, sy, ax, ay) < GAP:
                    taker["anchors"].append((ax, ay))
                else:
                    kept.append((ax, ay))
            owner["anchors"] = kept


def speed_up(balls, dt):
    """Nudge every ball a little faster, without letting it outrun the physics."""
    scale = (1 + SPEEDUP) ** dt
    for b in balls:
        speed = math.hypot(b["vx"], b["vy"])
        if speed == 0:
            continue
        wanted = min(MAX_SPEED, speed * scale)
        b["vx"] *= wanted / speed
        b["vy"] *= wanted / speed


def step_world(balls, dt):
    """One slice of simulation. Returns the wall impacts inside that slice."""
    impacts = []
    for b in balls:
        for speed, nx, ny in step_ball(b, dt):
            impacts.append(speed)
            # a bounce earns a new anchor, right where the ball struck
            b["anchors"].append((nx * EDGE, ny * EDGE))

    collide(balls)

    # a shove out of an overlap can put a ball through the wall; pull it back
    for b in balls:
        dist = math.hypot(b["x"], b["y"])
        if dist > WALL:
            b["x"], b["y"] = b["x"] / dist * WALL, b["y"] / dist * WALL
        if (b["x"], b["y"]) != b["path"][-1]:
            b["path"].append((b["x"], b["y"]))

    steal_lines(balls)

    # nothing in the rules ever destroys a line, so without this the count only
    # climbs and the frame rate goes with it
    for b in balls:
        if len(b["anchors"]) > MAX_ANCHORS:
            del b["anchors"][:-MAX_ANCHORS]

    # a ball with no lines left is out; edit in place so main keeps its list
    balls[:] = [b for b in balls if b["anchors"]]

    return impacts


def advance(balls, dt):
    """Move every ball, reflecting off the circle and off the other balls.

    Contacts are tested once per slice, so a ball that would cross more than
    half its own width in one go is moved in several slices instead. Without
    that it sails straight through other balls and through lines.

    Returns the impact speed of each wall hit that happened this frame.
    """
    speed_up(balls, dt)

    for b in balls:
        b["path"] = [(b["x"], b["y"])]

    fastest = max((math.hypot(b["vx"], b["vy"]) for b in balls), default=0.0)
    slices = max(1, math.ceil(fastest * dt / (GAP / 2)))

    impacts = []
    for _ in range(slices):
        impacts += step_world(balls, dt / slices)

    return impacts


def draw_scene(big, balls):
    """Draw the oversized frame for the balls' current positions."""
    big.fill(BLACK)
    c = BOX * SCALE / 2  # centre of the supersampled surface

    def pt(x, y):
        return round(c + x * SCALE), round(c + y * SCALE)

    pygame.draw.circle(
        big, WHITE, (round(c), round(c)), CIRCLE_RADIUS * SCALE, CIRCLE_WIDTH * SCALE
    )

    for ball in balls:
        colour = ball["colour"]
        bx, by = ball["x"], ball["y"]

        # rays run from the ball out to the anchors it currently owns
        for ax, ay in ball["anchors"]:
            dx, dy = ax - bx, ay - by
            length = math.hypot(dx, dy)
            if length <= GAP:
                continue  # ball has drifted over its own anchor
            dx, dy = dx / length, dy / length
            start = pt(bx + GAP * dx, by + GAP * dy)
            pygame.draw.line(big, colour, start, pt(ax, ay), RAY_WIDTH * SCALE)

        # white ring first, then the colour on top of it
        pygame.draw.circle(big, WHITE, pt(bx, by), GAP * SCALE)
        pygame.draw.circle(big, colour, pt(bx, by), BALL_RADIUS * SCALE)


def update_trail(trail, stamp, balls):
    """Fade the trail a notch, then smear each ball's path onto it."""
    trail.fill((TRAIL_FADE,) * 3, special_flags=pygame.BLEND_RGB_SUB)

    stamp.fill(BLACK)
    half = BOX / 2
    for ball in balls:
        faint = tuple(round(v * TRAIL_ALPHA) for v in ball["colour"])
        pts = [(round(half + x), round(half + y)) for x, y in ball["path"]]
        for a, b in zip(pts, pts[1:]):
            pygame.draw.line(stamp, faint, a, b, TRAIL_WIDTH)
        # round off every joint, otherwise a bounce leaves a notch on the corner
        for pt in pts:
            pygame.draw.circle(stamp, faint, pt, TRAIL_WIDTH // 2)

    # keep whichever is brighter, so crossing trails do not punch holes
    trail.blit(stamp, (0, 0), special_flags=pygame.BLEND_RGB_MAX)


def render_frame(big, balls):
    """One finished, antialiased frame at window size."""
    draw_scene(big, balls)
    return pygame.transform.smoothscale(big, (BOX, BOX))


def hardness(speed):
    """Where an impact speed sits between the faintest and the most dramatic."""
    return min(1.0, max(0.0, (speed - SOFT_HIT) / (HARD_HIT - SOFT_HIT)))


def bounce_gain(h):
    """How loud a hit of hardness h plays.

    Curved, so soft hits drop away sharply instead of fading evenly.
    """
    return BOUNCE_VOLUME * (QUIETEST + (1 - QUIETEST) * h**1.7)


def bounce_index(h):
    """Which of the pre-rendered tones a hit of hardness h uses."""
    return min(BOUNCE_TONES - 1, int(h * BOUNCE_TONES))


def play_bounces(sounds, impacts):
    """One hit per wall contact, its weight chosen by how hard it landed."""
    for speed in impacts:
        h = hardness(speed)
        channel = sounds[bounce_index(h)].play()
        if channel:
            channel.set_volume(bounce_gain(h))


def main():
    pygame.mixer.pre_init(SAMPLE_RATE, -16, 1, 512)  # small buffer, low latency
    pygame.init()
    bounces = make_bounce_sounds()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Balls in a Circle")

    big = pygame.Surface((BOX * SCALE, BOX * SCALE))
    trail = pygame.Surface((BOX, BOX))
    stamp = pygame.Surface((BOX, BOX))
    corner = ((WIDTH - BOX) // 2, (HEIGHT - BOX) // 2)
    clock = pygame.time.Clock()
    balls = start_balls()
    for b in balls:
        b["path"] = [(b["x"], b["y"])]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        dt = clock.tick(60) / 1000
        impacts = advance(balls, dt)
        update_trail(trail, stamp, balls)
        if bounces:
            play_bounces(bounces, impacts)

        # trail underneath, then the scene with its black treated as clear
        screen.fill(BLACK)
        screen.blit(trail, corner)
        frame = render_frame(big, balls)
        frame.set_colorkey(BLACK)
        screen.blit(frame, corner)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
