"""Replay chosen seeds and write each one out as an mp4, sound included.

    python3 record.py --seed 98 --out-dir clips
    python3 record.py --selection selection.json --out-dir clips --jobs 2

Nothing here touches the physics: it runs the same fixed-dt loop survey.py did,
so a seed gives back exactly the match the survey measured. The video is piped
to ffmpeg a raw frame at a time -- 60s at 800x800 is about 7GB of pixels, which
is worth streaming and not worth storing. The audio is mixed separately from
the wall impacts the loop reports, then muxed on at the end; playing it through
the live mixer would only record whatever the speakers happened to do.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import wave
from functools import lru_cache
from multiprocessing import Pool

import numpy
import pygame

import balls_in_circle as sim
from runner import DT, FPS, new_balls, name_of

MIXER_CHANNELS = 8  # pygame's default; a hit with no free channel is dropped


def ffmpeg_exe():
    """A usable ffmpeg: the one on PATH, else the one imageio ships."""
    from shutil import which

    found = which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("no ffmpeg on PATH -- pip install imageio-ffmpeg, or install ffmpeg")


@lru_cache(maxsize=None)
def tone(index, rate):
    """The pre-rendered impact the live game would have reached for."""
    raw = sim.bounce_samples(index / (sim.BOUNCE_TONES - 1), rate)
    return numpy.frombuffer(raw.tobytes(), dtype=numpy.int16).astype(numpy.float32)


def mix_audio(hits, seconds, rate, path):
    """Lay every surviving impact onto one track and write it as a wav.

    Live, the mixer has eight channels and a hit that finds them all busy is
    simply not heard. Late in a run the balls are quick enough to hammer the
    wall constantly, so honouring that limit is the difference between the
    recording sounding like the game and sounding like static.
    """
    track = numpy.zeros(int(seconds * rate) + rate, dtype=numpy.float32)
    free_at = [0.0] * MIXER_CHANNELS
    dropped = 0

    for t, speed in hits:
        channel = next((c for c in range(MIXER_CHANNELS) if free_at[c] <= t), None)
        if channel is None:
            dropped += 1
            continue

        h = sim.hardness(speed)
        samples = tone(sim.bounce_index(h), rate)
        free_at[channel] = t + len(samples) / rate

        start = int(t * rate)
        track[start:start + len(samples)] += samples * sim.bounce_gain(h)

    clipped = bool(numpy.abs(track).max(initial=0.0) > 32767)
    out = numpy.clip(track, -32767, 32767).astype(numpy.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(out.tobytes())
    return {"hits": len(hits), "dropped": dropped, "clipped": clipped}


def render(seed, out_path, cap, hold, crf, threads, quiet=False):
    """Simulate seed to its finish and write the whole thing to out_path."""
    started = time.time()
    pygame.init()

    big = pygame.Surface((sim.BOX * sim.SCALE, sim.BOX * sim.SCALE))
    trail = pygame.Surface((sim.BOX, sim.BOX))
    stamp = pygame.Surface((sim.BOX, sim.BOX))
    screen = pygame.Surface((sim.WIDTH, sim.HEIGHT))
    corner = ((sim.WIDTH - sim.BOX) // 2, (sim.HEIGHT - sim.BOX) // 2)

    exe = ffmpeg_exe()
    tmp_dir = tempfile.mkdtemp(prefix=f"clip{seed}_")
    silent = os.path.join(tmp_dir, "video.mp4")
    wav = os.path.join(tmp_dir, "audio.wav")

    proc = subprocess.Popen(
        [exe, "-y", "-loglevel", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{sim.WIDTH}x{sim.HEIGHT}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
         "-pix_fmt", "yuv420p", "-threads", str(threads), silent],
        stdin=subprocess.PIPE,
    )

    balls = new_balls(seed)
    hits = []
    cap_frames = round(cap * FPS)
    frames = 0
    last = None

    while len(balls) > 1 and frames < cap_frames:
        for speed in sim.advance(balls, DT):
            hits.append((frames * DT, speed))
        sim.update_trail(trail, stamp, balls)

        screen.fill(sim.BLACK)
        screen.blit(trail, corner)
        frame = sim.render_frame(big, balls)
        frame.set_colorkey(sim.BLACK)
        screen.blit(frame, corner)

        last = pygame.image.tobytes(screen, "RGB")
        proc.stdin.write(last)
        frames += 1
        if not quiet and frames % (FPS * 5) == 0:
            print(f"\r  seed {seed}: {frames / FPS:5.1f}s rendered", end="",
                  file=sys.stderr, flush=True)

    # hold the final frame so the winner is on screen long enough to read
    held = round(hold * FPS) if last else 0
    for _ in range(held):
        proc.stdin.write(last)

    proc.stdin.close()
    proc.wait()

    total = (frames + held) / FPS
    audio = mix_audio(hits, total, sim.SAMPLE_RATE, wav)

    subprocess.run(
        [exe, "-y", "-loglevel", "error", "-i", silent, "-i", wav,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out_path],
        check=True,
    )
    for f in (silent, wav):
        os.remove(f)
    os.rmdir(tmp_dir)

    winner = name_of(balls[0]) if len(balls) == 1 else None
    if not quiet:
        print(f"\r  seed {seed}: {total:.1f}s, winner {winner}, "
              f"{audio['hits']} hits ({audio['dropped']} dropped), "
              f"{time.time() - started:.0f}s to render -> {out_path}",
              file=sys.stderr)
    return {"seed": seed, "path": out_path, "seconds": round(total, 3),
            "sim_seconds": round(frames / FPS, 3), "winner": winner, **audio}


def _one(job):
    return render(*job)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, action="append", default=[],
                    help="a seed to record; repeatable")
    ap.add_argument("--selection", help="selection.json from select.py")
    ap.add_argument("--out-dir", default="clips")
    ap.add_argument("--cap", type=float, default=90.0)
    ap.add_argument("--hold", type=float, default=1.0,
                    help="seconds to freeze on the winning frame")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--jobs", type=int, default=1,
                    help="clips to render at once; each also runs an encoder")
    ap.add_argument("--threads", type=int, default=2, help="x264 threads per clip")
    args = ap.parse_args()

    seeds = list(args.seed)
    if args.selection:
        seeds += [r["seed"] for r in json.load(open(args.selection))["clips"]]
    if not seeds:
        sys.exit("nothing to record: pass --seed or --selection")

    os.makedirs(args.out_dir, exist_ok=True)
    jobs = [
        (s, os.path.join(args.out_dir, f"seed{s:05d}.mp4"),
         args.cap, args.hold, args.crf, args.threads, args.jobs > 1)
        for s in seeds
    ]

    started = time.time()
    if args.jobs > 1:
        with Pool(args.jobs) as pool:
            done = []
            for r in pool.imap_unordered(_one, jobs):
                done.append(r)
                print(f"[{len(done)}/{len(jobs)}] seed {r['seed']}: "
                      f"{r['seconds']:.1f}s, winner {r['winner']} -> {r['path']}")
    else:
        done = [_one(j) for j in jobs]

    with open(os.path.join(args.out_dir, "clips.json"), "w") as f:
        json.dump(sorted(done, key=lambda r: r["seed"]), f, indent=2)
    print(f"\n{len(done)} clips in {args.out_dir} "
          f"({time.time() - started:.0f}s total)")


if __name__ == "__main__":
    main()
