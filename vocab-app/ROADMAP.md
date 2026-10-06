# Vocab App: Build Roadmap

The order we build in, what Claude does in each session, and what you do between
sessions. The design itself is in [PLAN.md](PLAN.md).

---

## How we work

**Every Claude Code session starts fresh, with no memory of earlier chats.** The repo
is the memory. Each session starts by reading these files:

| File | What it holds |
|---|---|
| `PLAN.md` | What we are building and why |
| `ROADMAP.md` (this file) | Build order, plus a checkbox for each finished session |
| `LOG.md` | One short entry per session: what was done, what's next, anything you need to do (created in S1) |
| `CLAUDE.md` | Rules for working in the repo: commands, conventions, writing style (created in S1) |

**There are two lanes of work:**

- **Build sessions (S1, S2, ...)** write the app's code. They run **in order, one at a
  time**, because each one builds on the last and they edit the same files.
- **Content sessions (C1, C2, ...)** write word entries for the word bank. They only
  add files under `content/`, so they can run **any time after S3, even at the same
  time as a build session.**
- **Feedback sessions (F1, F2, ...)** fix and tune things based on what you noticed
  using the app.

**Every session ends the same way:**
1. Tests pass.
2. The ROADMAP checkbox is ticked and a LOG entry is written.
3. The work is pushed and a pull request is opened. Cloudflare posts a **preview link**
   on it.
4. You open the preview link on your iPhone and check it.
5. You say "merge" in the session, or tap Merge on GitHub. The live app updates.

### Prompts to start a session (copy and paste)

| To do | Start a new session in the `vocab` repo with |
|---|---|
| The next build step | `Vocab app: do the next unchecked build session in ROADMAP.md.` |
| More word entries | `Vocab app: content session. Write the next batch of entries following content/GUIDE.md.` |
| Fix things you noticed | `Vocab app: feedback session. Here's what I noticed: ...` |
| Something is broken on the live app | `Vocab app: fix this first: ...` |

### Rules of thumb

- One session = one roadmap item. Smaller steps are easier to test on the phone.
- Test the preview on your iPhone before merging.
- Never run two **build** sessions at the same time. A content session alongside a
  build session is fine.
- If you hit usage limits, just push the schedule back. The order matters, the dates
  don't.

---

## Day 0: your setup (about 20 minutes, once)

1. **Make a new GitHub repository called `vocab`** (private is fine). Tick "Add a README"
   so it has a `main` branch. The app gets its own repo: this `Game` repo has no `main`
   branch and holds unrelated projects.
2. **Give Claude access to it.** When you start a session, pick `vocab` as the
   repository. If it isn't listed, allow the Claude GitHub app on that repo.
3. **Make a free Cloudflare account** at dash.cloudflare.com. Nothing else yet: S1
   gives you click-by-click steps to connect it.

---

## Suggested calendar

About 4 weeks to the full app, and you use it daily from **day 4**. If you go faster or
slower, follow the order, not the dates.

| Day | Start these sessions | Your part (besides testing previews) |
|---|---|---|
| 0 | none | Repo + Cloudflare account (20 min) |
| 1 | S1 | Connect Cloudflare; add the app to your home screen |
| 2 | S2 and S3 (two sessions, same day is fine) | Read the simulation table; confirm your daily time |
| 3 | S4, and C1 alongside it | Try the demo session on your iPhone |
| 4 | S5 | Take the placement test; **first real session. Daily use starts.** |
| 5-6 | F1 | Tell me everything that felt off |
| 7 | S6 | Cloudflare database steps (10 min); install on your PC |
| 8 | S7, and C2 alongside it | Build the iOS Shortcut (5 min) |
| 9 | S8 | Allow notifications |
| 10-11 | C3, F2 | Feedback |
| 12 | S9 | |
| 13 | S10 | Tell me your subjects |
| 14 | S11 | Make an Anthropic API key (10 min) |
| 15-16 | C4, C5, F3 | Feedback |
| 17-21 | S12, S13, S14 | |
| Week 6-8 | S15 | Nothing; needs about 1,000 of your reviews first |

---

## Week 1: first usable app on your iPhone (Phases 0 and 1)

### [ ] S1: Foundations
Claude builds:
- The `vocab` repo layout: moves `PLAN.md` and `ROADMAP.md` over and creates `CLAUDE.md`
  and `LOG.md`.
- The app skeleton: TypeScript, Svelte, Vite. It is installable (a PWA) and works
  offline, with iPhone home-screen settings (icon, status bar, safe areas).
- Testing tools: Vitest for unit tests, Playwright for full runs on an iPhone-sized
  screen. One `npm test` runs everything.
- A startup script for cloud sessions, so every future session installs everything and
  can run the tests.
- The core data layer:
  - every action is saved as an event in a log on the device (IndexedDB)
  - a replay engine rebuilds your progress from that log
  - tests prove that two devices with shuffled events end up with identical results
- A placeholder home screen.

You:
- Connect the repo to Cloudflare Pages (click-by-click steps, about 10 min). The live
  app follows `main`, and every pull request gets a preview link.
- On your iPhone: open the live link in Safari, then Share, then **Add to Home Screen**.
  Then open it in airplane mode to check it works offline.

Done when: the app icon on your home screen opens, even offline.

### [ ] S2: The scheduler and time tailoring
Claude builds:
- FSRS (the ts-fsrs library) with two tracks per word (recognising and producing).
- The stage machine, from Queued to Owned, including dropping back down.
- Ratings worked out from what you did.
- The unlock and sibling rules, and the 4am day boundary.
- The daily planner: given your minutes, it builds today's queue (most at-risk reviews
  first, new words, writing tasks, drills). It also handles throttling, catch-up mode
  and "busy week ahead" mode.
- A **simulation** of a virtual learner over 180 days at 5, 10, 15, 20 and 30 minutes a
  day. It produces a table of new words a day, reviews a day, real minutes, and words
  Owned by day 180. That table sets the defaults in PLAN 6.7.
- Thorough unit tests.

You: read the simulation table (2 min) and confirm your daily time.

Done when: the simulation results are committed and the tests pass.

### [ ] S3: Word bank pipeline
Can run on the same day as S2, in a second session (it touches different files).

Claude builds:
- Python scripts that download and process the open data: Wiktionary (kaikki.org),
  Open English WordNet and wordfreq.
- The academic-ness score (PLAN 3.6).
- A ranked candidate list of about 4,000 word senses in the academic frontier.
- The entry format (a JSON schema) and a validator that runs every automatic check from
  PLAN 11.4.
- `content/GUIDE.md`: exact instructions for content sessions, so every batch has
  consistent style and quality.
- The placement test pool: 1,000+ real words across frequency bands and 250 fake words.
- A compact dictionary file, so captured words that aren't in the bank can still get an
  entry later (S7).
- About 20 sample entries for S4 to test with.

Done when: the validator runs, and the candidate list and guide are committed.

### [ ] C1: Content batch 1 (150 entries)
Claude writes 150 entries following `content/GUIDE.md`. They are spread across your
frontier, with mixed parts of speech and topics and academic weighting, and all pass
the validator. The pull request includes a readable preview of the entries.

You: skim about 15 random entries and flag anything that reads wrong.

### [ ] S4: Learning screens
Claude builds:
- The session runner: queue, progress bar, pause and resume.
- New-word introduction: guess first, then the word page, the immediate check and the
  in-session steps.
- Exercises R1, R3, P1 and P3, plus:
  - the "I don't know" button
  - the hint ladder
  - typed-answer checking (word forms, near-miss spellings)
  - retyping the answer after a miss
- Pronunciation using the phone's own text-to-speech.
- iPhone polish:
  - buttons within thumb reach
  - the keyboard never covers the answer box
  - autocorrect and predictive text off
  - safe areas
- Keyboard shortcuts on PC.
- An end-to-end test of a full session on an iPhone-sized screen.

You: run the demo session on the preview link. Note anything awkward: text size,
buttons, speed, wording.

Done when: a complete session works on your iPhone.

### [ ] S5: Onboarding, home screen and stats (Phase 1 complete)
Needs C1 merged, so there are real words to learn.

Claude builds:
- The placement test: yes/no with fake words, then verification and scoring, then a
  results screen.
- Onboarding: placement test, then choosing your daily time, then your first session.
- The Today screen ("about 15 min: 38 reviews, 5 new, 1 writing"), a Start button and
  2-minute mode.
- Stats v1: Words Owned, the stage funnel, retention, the review forecast and the weekly
  streak.
- Settings:
  - minutes per day, with optional weekday and weekend times
  - target retention
  - export and import of a backup file
- A hidden "time travel" setting, so weeks of scheduling can be tested in minutes.

You: merge it, take the placement test and do your first real session. **From here on,
do one session every day.** Until sync arrives in S6 your data lives only on the phone,
so tap Export once a week as a backup.

Done when: you have done day 1 for real.

### [ ] F1: Feedback and fixes
You bring everything you noticed in 2-3 days of real use. Claude fixes, tunes and
polishes.

---

## Week 2: iPhone and PC as one app (Phase 2)

### [ ] S6: Sync
Claude builds:
- The sync server: a Cloudflare Worker with a D1 database (tables for events and the
  Inbox).
- Sync-key login, with endpoints to send and fetch events.
- The sync engine in the app: it syncs when the app opens, after each session, and every
  few minutes while open.
- Tests for merging two devices' events without conflicts.
- A sync status indicator, and instructions for installing the app on your PC.

You:
- Follow the steps to create the database and connect the Worker in the Cloudflare
  dashboard (about 10 min).
- Make a sync key on your iPhone and enter it on your PC.
- Install the app on your PC (the "Install" icon in Chrome or Edge).

Done when: a review done on your iPhone shows up on your PC within a minute.

### [ ] S7: Capture
Claude builds:
- The Inbox screen, with sorting into Learn / Know it / Ignore, and a sense picker.
- Entries for words that aren't in the bank, built from the compact dictionary.
- Captured words jump the queue.
- An **iOS Shortcut, "Add to Vocab"**: step-by-step instructions to build it in the
  Shortcuts app (a Shortcut has to be made on the phone itself).
- A **PC bookmarklet** that grabs the selected word and the sentence around it.
- A quick-add box in the app.

You: build the Shortcut (about 5 min), add the bookmarklet on your PC, and capture 3
real words.

Done when: a word shared from Safari on your iPhone appears in the Inbox on both
devices.

### [ ] S8: Reminders and backups
Claude builds:
- Push reminders for the home-screen app (iOS 16.4+). They arrive at your chosen time,
  and only if today's session isn't done.
- An automatic weekly backup of your event log to Cloudflare R2.
- A prompt when a new version of the app is available, plus offline polish.

You: allow notifications and pick a reminder time.

Done when: a reminder arrives on your phone.

### [ ] C2, [ ] C3: Content batches 2 and 3 (150 each, about 450 total)
### [ ] F2: Feedback and fixes

---

## Week 3: Depth (Phase 3)

### [ ] S9: More exercises and smarter corrections
Claude builds:
- Exercises R2 (spot the misuse), R4 (closest meaning), P2 (definition to word) and P4
  (contrast drill).
- Confusion tracking, which creates contrast drills automatically.
- The leech flow for words that won't stick.
- The variety rules, and choosing the exercise type from stability.

### [ ] S10: Writing and using words (academic)
Claude builds:
- U1 writing tasks with essay prompts based on your subjects.
- U3 "Make it academic".
- The free sentence check: a self-check list and model sentences.
- The sentence journal.
- Your own sentences reused as fill-in-the-blank tests.
- The "Copy for review" button.
- U2 "Use it today", with a check-in the next day.

You: tell Claude your subjects, or set them in the app.

### [ ] S11: AI sentence feedback
Claude builds:
- A grading endpoint on the Worker that gives structured feedback (meaning, grammar,
  natural phrasing, a tip and an improved version).
- A monthly spend cap ($3) and a daily limit.
- AI-written entries for captured words.
- An on/off switch in settings.

You: make an Anthropic API account (separate from your Claude subscription), add a
small prepaid credit, create an API key, and paste it into Cloudflare as a secret
(step-by-step instructions provided).

Done when: you get AI feedback on a sentence you wrote.

### [ ] C4, [ ] C5: Content batches 4 and 5 (about 750 total)
### [ ] F3: Feedback and fixes

---

## Week 4 onwards: Growth (Phase 4)

### [ ] S12: Reading companion
Paste text, or send it from your iPhone with a second Shortcut ("Read in Vocab"). The
app highlights words you are learning and frontier words you don't know yet; tap one to
capture it with its sentence. Includes "seen in the wild" logging and handling of word
forms (studies, studied, studying).

### [ ] S13: Roots
About 150 roots and affixes as content, each with its own recognition track; "decode
it" exercises; roots on word pages; and a root explorer.

### [ ] S14: Progress you can trust
The monthly vocabulary retest and growth chart, the production gap, the self-grading
calibration stat, and the fortnightly time check-in (PLAN 6.7).

### [ ] S15: Personal FSRS tuning (around week 6-8)
Once you have about 1,000 reviews: fit the FSRS parameters to your own history. After
that it re-fits automatically every month.

---

## Ongoing, after the build

- **Content:** keep running content sessions until the bank has about 1,500 entries
  (about 10 batches), then only as needed. The app warns you when fewer than about 60
  days' worth of new words are left in your queue, so you know when to run one.
- **Weekly feedback session:** bring what you noticed, plus the cards you flagged with
  "Something's wrong".
