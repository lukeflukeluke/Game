# Clip originals

The twenty recorded runs, full quality (H.264 CRF 18, 800x800, 60fps, AAC audio).
Each is one seed of `balls_in_circle.py`: the run played out to a single surviving
ball, plus exactly 2.00s of that winner alone in the circle.

This branch holds nothing but the videos. The code that made them, and the seeds
they came from, are on `claude/simulation-recording-strategy-ppfd2g`:

    python3 record.py --selection selection.json --out-dir clips --jobs 4

reproduces these files exactly, since a seed names one match frame for frame.

| file | length | won at | winner |
| --- | --- | --- | --- |
| seed00414.mp4 | 62.23s | 60.23s | yellow |
| seed00227.mp4 | 62.30s | 60.30s | green |
| seed00929.mp4 | 62.37s | 60.37s | red |
| seed00472.mp4 | 62.60s | 60.60s | green |
| seed00034.mp4 | 62.85s | 60.85s | blue |
| seed00101.mp4 | 62.88s | 60.88s | green |
| seed00536.mp4 | 63.13s | 61.13s | green |
| seed00466.mp4 | 63.40s | 61.40s | purple |
| seed00636.mp4 | 63.68s | 61.68s | yellow |
| seed00361.mp4 | 64.17s | 62.17s | orange |
| seed00966.mp4 | 64.63s | 62.63s | red |
| seed00808.mp4 | 65.78s | 63.78s | orange |
| seed00487.mp4 | 65.83s | 63.83s | red |
| seed00441.mp4 | 66.02s | 64.02s | orange |
| seed00874.mp4 | 66.10s | 64.10s | orange |
| seed00828.mp4 | 66.28s | 64.28s | yellow |
| seed00814.mp4 | 66.72s | 64.72s | yellow |
| seed00286.mp4 | 68.77s | 66.77s | blue |
| seed00972.mp4 | 69.82s | 67.82s | blue |
| seed00064.mp4 | 69.90s | 67.90s | blue |

Exactly one purple win, by design: `seed00466.mp4`.
