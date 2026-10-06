# Vocab App: The Plan

Status: design only, nothing built yet. This is the blueprint we build from.

## 0. The short version

The app is built around one idea: **knowing a word is not one fact, it is a ladder.**
First you recognise it when you read it. Then you can pull it out of your head when
you need it. Then you can use it correctly in your own sentences. Most vocab apps stop
at the first rung (flashcards and multiple choice), which is why people "learn"
hundreds of words and use none of them.

This app walks every word up all three rungs, schedules each rung with a modern memory
model (FSRS), grades you on what you actually do rather than what you say you know, and
feeds you words you will actually meet again, especially words you capture from your
own reading.

It is one web app (a PWA) that installs on your phone and your PC, works offline, and
syncs through a tiny free server. Hosting is free. The only optional cost is AI feedback
on sentences you write (well under $5/month, with a hard cap), and the app works fully
without it.

---

## 1. What actually makes vocabulary stick, and the feature each one becomes

| Principle | What it means | Feature in the app |
|---|---|---|
| Retrieval practice | Pulling a word out of memory strengthens it far more than re-reading it | Nearly every screen makes you answer, not just look |
| Spacing | Reviews spread over growing gaps beat cramming | FSRS scheduler |
| Recognition is not production | Knowing a word when you see it is much easier than producing it | Two memory tracks per word; production unlocks later |
| Varied contexts | A word met in many different sentences is understood, not memorised as one card | Every review uses a different sentence; your own sentences get reused |
| Generation and self-reference | Making your own sentence, especially about your own life, encodes deeply | Writing tasks with personal prompts |
| Pretesting | Guessing a meaning before being told helps it stick, even when the guess is wrong | New words start with "guess from context" |
| Morphology | Knowing roots lets you decode words you have never studied | Roots on every word; a roots module |
| Interference | Learning near-synonyms or look-alikes together makes them blur | Scheduler keeps confusables apart, then drills them on purpose |
| Relevance and re-encounter | Words you meet in real life matter more and get free extra exposure | Captured words jump the queue; reading companion |
| Honest feedback | Self-graded flashcards let you fool yourself | Objective typed checks; ratings come from performance |

---

## 2. What it means to "know" a word: the stages

Each word (strictly, each word *sense*, see section 11) moves through these stages.
The stage decides which exercises you get.

| Stage | Meaning | How you get there |
|---|---|---|
| Queued | In your pool, not started | Placement test, word bank, or captured |
| Learning | Met today, going through short in-session steps | Introduced in a session |
| Recognise | You know it when you read it | Passed the in-session steps |
| Recall | You can produce it from a meaning or context | Recognition stability reaches 4 days |
| Use | You have used it correctly in your own sentence | Production stability reaches 10 days, then a writing task passed |
| Owned | You will very likely still produce it 2 months from now | Production stability reaches 60 days, plus at least one accepted sentence of your own |

"Stability" is FSRS's estimate of how many days until your chance of recalling the
word falls to 90%. So "Owned" literally means: the model predicts at least a 90% chance
you can still *produce* this word 60 days from now.

Stages can go **down**. If you start failing production, an Owned word drops back to
Recall. The numbers you see are honest.

Side states: **Known** (you proved you already knew it, see 3.5), **Suspended** (parked
for now), **Ignored**.

---

## 3. Where words come from

### 3.1 Placement test (first launch, about 6 minutes)

Goal: find your **frontier**, the band of words you half-know or have seen but cannot
use. Words far past it are rare (you would hardly ever meet them); words below it you
already have.

1. **Yes/No checklist.** About 100 items: 80 real words sampled from 16 frequency bands
   (roughly the 2,000th to the 60,000th most common word), plus 20 convincing fake
   words ("plimsious", "devorant"). "Do you know what this means?" Quick taps.
2. **Verification.** 15 of your "yes" words get a quick meaning check.
3. **Scoring.** For each band: the share you know, corrected for fake words you claimed
   (your over-claiming rate) and for failed verifications. Summed across bands, that
   gives a vocabulary size estimate with a range.
4. **Result.** Your estimated size, and your frontier: the bands where you know about
   30-80%. Your starting pool is drawn from those bands.

The test is **repeated monthly** with fresh words (never reused, never words you have
studied). That gives a growth chart measuring your real vocabulary, not app activity.

### 3.2 The word bank

A pre-built set of rich word entries (section 11) aimed at the frontier of an educated
adult. Start with about 1,500-3,000 entries and grow. Candidates come from frequency
ranks of roughly 8,000-40,000, filtered to remove proper nouns, slurs, obsolete words,
ultra-niche jargon, and see-through derivatives (if you know "happy" you do not need
"unhappiness" as a card).

### 3.3 Capture: words from your real life (the most valuable source)

When you hit an unfamiliar word while reading, you capture it, together with the
sentence it appeared in, in two taps on phone or PC (section 13.5). It lands in an
**Inbox**:

- If it is in the bank, it links to that entry and your sentence is added as an example.
- If not, the app builds an entry from open dictionary data (Wiktionary) and asks which
  sense matches your sentence (AI can pick it for you if turned on).
- You triage it: **Learn**, **Already know**, or **Ignore**.

Captured words **jump the queue** and get introduced within a day or two. Your original
sentence becomes their first example and, later, one of their fill-in-the-blank tests.

### 3.6 Academic focus

The goal is the vocabulary of strong academic reading and writing. Basic academic lists
(like the Academic Word List) are aimed at people learning English and are too easy for
a native speaker; the placement test will put you above most of them anyway. The bank
targets the tier above:

- **Academic-ness score** for every candidate: how much more often it appears in
  academic writing than in general text. It feeds the priority score in 3.4.
- **Word families that do the most work in essays**, tagged so they get extra weight:
  - stance and argument verbs: posit, contend, concede, refute, corroborate, undermine
  - analysis words: salient, tenuous, pervasive, nuanced, contingent, ostensible
  - connectors and structure: notwithstanding, conversely, albeit, hence, insofar as
  - hedging: arguably, plausibly, tentatively
- **Every entry carries a register label** (formal / neutral / informal) and
  **essay-ready phrases** ("posit that...", "a salient feature of...", "the evidence
  corroborates...").
- **Writing prompts are set in essays** ("Use *corroborate* in a sentence from a history
  essay"), using your subjects if you add them in settings.
- **"Make it academic"** exercise (U3, section 5): rewrite a casual sentence in essay
  register using the target word.
- The reading companion (section 9) is aimed at textbooks, articles and papers.

### 3.4 Choosing today's new words

Each queued word gets a priority score:

- **plus, big:** you captured it (more if recent)
- **plus:** frontier fit (bands where you know about half score highest)
- **plus:** usefulness (common in edited writing such as news and books, not only in
  speech or in one specialist field)
- **plus:** root bonus (shares a root with a word you learned recently; roots reinforce
  each other)
- **minus, big:** interference (near-synonym, look-alike, or known confusable of
  anything introduced in the last 7 days)
- **minus:** same part of speech or topic as words already picked today (variety)

### 3.5 "I already know this"

Any new word has an "I know this" button. Tapping it gives you an immediate typed
check (fill in the blank). Pass: it is marked Known and gets one surprise check in about
60 days. Fail: it is learned normally. This stops over-claiming from hollowing out
your learning.

---

## 4. Meeting a new word

The introduction takes about 45-60 seconds and is always active, never just reading.

**Step 1: Guess first.** You see the word in a rich sentence where the context strongly
suggests the meaning. "What do you think *laconic* means?" Pick one of 4, or tap
"No idea". It does not count against you; the guess primes your memory.

**Step 2: The word page.** Layered so the essentials take about 30 seconds.

- Always shown: the word, pronunciation (IPA plus a play button), part of speech; a
  plain-English definition written as a full sentence ("If someone is laconic, they use
  very few words."); two examples from different settings; and the **"vs" box**, which
  says how it differs from its nearest neighbours ("terse: short and a bit rude.
  taciturn: rarely talks at all. laconic: says little, often to dry effect.").
- Tap to expand: roots and origin ("Laconia, home of the Spartans, famous for one-line
  replies"), word family (laconically), common partners ("a laconic reply / wit /
  style"), more examples, your notes or mnemonic, where you captured it.

**Step 3: Immediate check.** Meaning-in-context multiple choice, with a *new* sentence.

**Step 4: A few minutes later in the session** (after about 5 other items). Fill in the
blank with the first letter shown: "Asked about the defeat, the coach was l_____:
'We lost.'"

**Step 5: End of session.** One more recognition check, with yet another sentence.

Miss any step and it comes back a few items later with a different sentence. From
tomorrow, FSRS takes over.

---

## 5. The exercises

Two scheduled tracks per word: **Recognition** (word to meaning) and **Production**
(meaning or context to word). Plus **Usage** tasks that fire at milestones.

### Recognition

| ID | Exercise | Tests | Graded by |
|---|---|---|---|
| R1 | **Meaning in context.** Sentence with the word highlighted; pick its meaning from 4 | Core meaning | App |
| R2 | **Spot the misuse.** Two sentences; which uses the word correctly? ("The laconic lecture ran three hours" vs "Her laconic texts, just 'k' and 'fine', drove him mad") | Nuance, partners, tone | App |
| R3 | **Quick recall.** See the word in a sentence, say the meaning in your head, reveal, rate yourself Missed / Fuzzy / Got it | Free recall; fast, good on phone | You (limited, see 6.2) |
| R4 | **Closest meaning.** Which everyday word is nearest in meaning? | Linking to words you already know | App |

### Production

| ID | Exercise | Tests | Graded by |
|---|---|---|---|
| P1 | **Typed fill-in-the-blank.** Sentence with a gap; type the word | Recall in context | App |
| P2 | **Definition to word.** Just the meaning; type the word | Pure recall, the hardest | App |
| P3 | **Which word fits?** A context; choose from 4 of *your own* learning words | Telling your words apart | App |
| P4 | **Contrast drill.** For a pair you mix up (6.6): several sentences, pick which of the two fits each | Untangling confusables | App |

### Usage

| ID | Exercise | When | Graded by |
|---|---|---|---|
| U1 | **Write your own sentence**, from a personal prompt ("Describe someone you know using *laconic*") | On reaching Use; again if production lapses later | AI (optional) or self-check |
| U2 | **Use it today.** Two words a day to use in real conversation, texts or writing; next day: "Did you?" | From the Use stage on | You, logged |
| U3 | **Make it academic.** A casual sentence ("The results kind of back up what she said") to rewrite in essay register with the target word ("The results corroborate her claim") | Use stage; alternates with U1 | AI (optional) or self-check against a model answer |

### Rules that apply to all exercises

- **Good distractors.** Wrong options in R1 are definitions of words with the same part
  of speech, similar difficulty and nearby meaning, never obvious junk you can rule out
  instantly.
- **Typed answers.** Case doesn't matter. Right word in the wrong form ("obfuscate" when
  the sentence needs "obfuscated") counts as correct and shows the right form. A
  one-letter slip on a word of 5+ letters counts as Hard and shows the spelling.
  Autocorrect and predictive text are turned off on answer boxes so the phone keyboard
  can't type the answer for you.
- **Hint ladder (P1, P2).** First letter, then number of letters, then a short
  definition, then reveal. Each hint lowers the rating.
- **"I don't know" button everywhere.** Better than guessing, because lucky guesses on
  multiple choice create false confidence. After a miss you retype the correct answer
  once before moving on.
- **Variety.** A word never repeats the same sentence within 3 reviews, never gets the
  same exercise type twice in a row, and exercise types you recently failed come up more.

### Which exercise a review uses

- Recognition with stability under 7 days: R1 or R4. After that: R2 and R3 (R3 at most
  1 in 5 recognition reviews).
- Production, first one or two reviews: P3, or P1 with the first letter shown. Stability
  under 21 days: P1. After that: P1 and P2 mixed, and P1 prefers your own sentences once
  you have written some.

---

## 6. The scheduler

### 6.1 FSRS

We use FSRS (Free Spaced Repetition Scheduler): open source, the current best-performing
scheduler, and the one Anki now uses. For each item it tracks *stability*, *difficulty*
and *retrievability* (your current chance of recall). Each review is rated Again, Hard,
Good or Easy, and the next review lands when your recall chance is predicted to hit
your target retention (default 90%). There is a maintained TypeScript implementation
(ts-fsrs).

Every word has two FSRS items: recognition and production.

### 6.2 Ratings come from what you do, not what you claim

| What happened | Rating |
|---|---|
| Wrong, or "I don't know" | Again |
| Right, but with a hint, a near-miss spelling, or slow (over 2x your usual time for that exercise type) | Hard |
| Right | Good |
| Right, no hint, fast (under 0.6x your usual time), on a typed exercise | Easy |

Multiple choice can never earn Easy, since a quarter of right answers could be guesses.
R3's self-ratings (Missed / Fuzzy / Got it) map to Again / Hard / Good, never Easy.
"Your usual time" is your rolling median for that exercise type, so it adapts to you
and to phone versus PC typing speed.

### 6.3 Unlocking and the sibling rule

- Production unlocks once recognition stability reaches 4 days.
- If both tracks of a word are due on the same day, only production is shown, and
  passing it also counts as a recognition pass (producing a word proves you recognise
  it). A word never appears twice in one session for review.

### 6.4 Daily load

- The day rolls over at 4am local time, so late-night study counts for the same day.
- You set a daily time budget (default 15 minutes) and a new-word target (default 5).
- The app predicts session length from your own average seconds per exercise type.
- New words shrink automatically when reviews are heavy: if today's reviews exceed 1.3x
  your 14-day average, new words are halved; above 2x, zero.
- **Catch-up mode** after missed days: no new words; the backlog is ordered most at-risk
  first (lowest recall chance) and spread over several days within your budget, instead
  of a 300-review wall.
- Rough expectation: 5 new words a day settles at about 50-70 reviews a day, around
  15 minutes. Before building the interface, we run a simulation of the scheduler to
  tune these defaults.

### 6.5 Leeches: words that will not stick

A track with 5 or more lapses becomes a leech. Next time it is due, instead of a normal
review, you get "This one keeps slipping": the word page again, then a prompt to write
your own mnemonic or a vivid personal sentence (both much stronger than ready-made
ones), a contrast drill if it is a confusion problem, and a restart of its learning
steps. At 8 or more lapses the app suggests parking it for a month. Dropping a few
stubborn words is fine.

### 6.6 Confusion tracking

Every wrong answer records *what you chose instead*. If you pick or type word B when the
answer is A twice, A and B become a **confusion pair** with their own P4 contrast-drill
item, scheduled like everything else. Classic confusables tagged in the bank
(affect/effect, imply/infer, venal/venial, ambiguous/ambivalent) are introduced at least
7 days apart, then drilled deliberately once both are stable.

### 6.7 Your daily time, tailored

You choose how many minutes a day (5 to 45), optionally different on weekdays and
weekends. The app builds each day's session to fit what you chose. Starting defaults
below are provisional; the scheduler simulation (build session S2) sets the real
numbers, and after that the app adjusts to your own measured pace.

| Daily time | New words/day | Also included |
|---|---|---|
| 5 min | 1 | Writing task every 3rd day |
| 10 min | 3 | Writing task every other day |
| 15 min (default) | 5 | 1 writing task a day |
| 20 min | 7 | 1 writing task + contrast drills |
| 30 min | 10 | 2 writing tasks + a suggested reading-companion text |

How it holds you to it:
- **The session fits the time.** When your time is nearly up, it stops adding new words
  and only finishes what is due.
- **Fortnightly check-in.** If you keep running over, skipping days or finishing early,
  it suggests a better time and shows what the change would mean.
- **Changes ease in.** Reviews lag behind new words by weeks, so cutting your time
  doesn't cut today's reviews. The app lowers new words first and the load follows over
  1-2 weeks.
- **"Busy week ahead" mode** (exams, deadlines): pauses new words for a few days ahead
  of time, so the busy week itself is light.

---

## 7. A daily session (15 minutes)

```
Start:  "Today: 41 reviews, 5 new words, 1 writing task (about 15 min)"
  1. Reviews: about 10 items, most at-risk first, recognition and production mixed
  2. New word 1: guess, word page, immediate check
  3. Reviews: about 5 items
  4. New word 2 (new word 1's fill-in-the-blank step turns up in here)
  5. ...and so on until all new words are in, reviews spread between them
  6. Writing task (U1) for a word that just reached Use
  7. Wrap-up: a final recognition check on today's new words
End:    accuracy, words that moved up a stage, "Use today: laconic, mitigate"
```

**2-minute mode** for the phone: 6-8 due reviews, no new words. Uses dead time (queues,
the bus) and keeps the main session shorter.

A session can be paused on one device and resumed on the other: reviews are synced
events, so the queue simply recomputes.

---

## 8. One word's life (illustrative; FSRS sets the real gaps)

| Day | What happens |
|---|---|
| 0 | Reading an article you hit "His laconic reply...". Share, Vocab. It lands in the Inbox with that sentence. |
| 1 | Introduced first, because captured words jump the queue. You guess "lazy" (wrong, doesn't matter), see the word page, pass R1, later the "l_____" blank, and the end-of-session check. |
| 2 | R1 with a new sentence: pass |
| 5 | R2 spot-the-misuse: pass. Recognition stability is now over 4 days, so production unlocks. |
| 6 | P3 "which word fits" among your own words: pass |
| 10 | P1, no hint: you type "lacoinc". Hard, spelling shown. |
| 14 | P1: pass |
| 25 | Production stability over 10 days, so U1: "Describe someone you know using *laconic*." You write "My grandad is laconic; he answers most questions with a nod." Accepted. Stage: Use. Sentence saved. |
| 26 | "Use today: laconic." Next day you log that you used it in a text. |
| 50 | P2, definition to word: pass |
| 110 | P1 using *your own* sentence: "My grandad is ____; he answers most questions with a nod." Pass. Production stability over 60 days: **Owned**. |
| Later | A review every few months. A few seconds a year to keep it. |

Total: about 12 reviews and 4-5 minutes of your time, spread over roughly 4 months.

---

## 9. Beyond the daily session

- **Reading companion** (PC first, phone too). Paste an article, or share text from
  your phone. The app highlights words you are learning (tapping logs "seen in the wild",
  shown on the word page) and frontier words from the bank you don't know yet (tap to
  capture with the sentence). Offline, no AI. Turns any reading into practice and
  capture.
- **Sentence journal.** All your accepted sentences, searchable. They are reused as
  future fill-in-the-blank tests, the most memorable contexts possible because they are
  about your life.
- **Roots module** (later phase). About 150 high-yield roots and affixes (bene, mal,
  chron, loqu, spec, -phile, -cracy...). Each is a small item with its own recognition
  track, plus "decode it" exercises: an unseen word made of roots you know; guess what
  it means. This builds the skill of working out new words on your own, which grows
  your vocabulary beyond what you study.

---

## 10. Progress you can trust

- **Headline number: Words Owned.** Not XP, not streaks.
- **Stage funnel:** how many words sit at each stage.
- **Vocabulary size estimate** from the monthly retest, charted over time. The real
  "is this working" number.
- **Retention** on mature reviews, per track. Target about 90%. Much lower means too many
  new words; much higher means you could go faster.
- **Production gap:** words you recognise but cannot yet produce.
- **Forecast:** reviews due over the next 7 and 30 days.
- **Self-grading calibration:** for R3, how often your "Got it" is followed by a pass on
  the next objective check. If you are generous with yourself it tells you, and leans
  on objective exercises more.
- **Consistency:** a weekly streak (weeks with 5+ study days) instead of a daily streak
  that punishes one missed day.
- **Used-in-the-wild log.**

After about 1,000 reviews, we re-fit the FSRS parameters to *your* review history with
the FSRS optimiser, so intervals match how your memory actually behaves.

---

## 11. Content: what a word entry holds and where it comes from

### 11.1 The unit is a sense, not a word

"Temper" (a mood) and "temper" (to moderate) are separate things to learn. Each entry
is one sense. A word with two useful senses becomes two entries, introduced weeks apart.

### 11.2 What each entry contains

- Headword, part of speech, IPA, audio (device text-to-speech: free and offline)
- Plain definition as a full sentence ("If someone is laconic, they..."), 20 words max
- Register label (formal / neutral / informal) and essay-ready phrases (see 3.6)
- Nuance note: 2-3 sentences on tone, formality, when to use it
- 6 example sentences across settings: conversation, news, fiction, formal writing
- 3 fill-in-the-blank sentences where the context clearly points to the word (a blank
  you can't infer is unfair)
- 2 misuse sentences (plausible but wrong) with why they are wrong
- Common word partners, word family, antonyms
- Near-synonyms, each with its "vs" distinction
- Look-alike confusables
- Roots and affixes with meanings, 3 sibling words, a short origin story
- Frequency band, topic tags, usefulness score

### 11.3 Sources (all open)

| Need | Source | Licence |
|---|---|---|
| Definitions, IPA, origins, word forms, senses | Wiktionary, via the kaikki.org machine-readable extracts | CC BY-SA |
| Sense structure, synonyms, related words | Open English WordNet | CC BY 4.0 |
| Word frequency | wordfreq data | CC BY-SA |
| Real example sentences | Tatoeba; Project Gutenberg books | CC BY / public domain |
| Pronunciation audio | Device text-to-speech | n/a |

We do not scrape copyrighted dictionaries (Merriam-Webster, Etymonline, Vocabulary.com).

### 11.4 Building the bank

Open data gives the raw facts. The teaching content (plain definitions, "vs" boxes,
blank and misuse sentences, distractors) is written by an LLM from that data and then
checked. Two routes:

- **$0:** Claude writes entries during our build sessions in batches of about 50; you
  skim and flag. Good for the first 300-500 entries (beyond that it eats a lot of your
  Claude usage).
- **One-time paid batch run** for the rest (section 12).

Every entry passes automatic checks: the blank's answer isn't given away in the
sentence, the definition doesn't use the word itself, all fields present, sentence
lengths sane. Every card in the app has a **"Something's wrong"** button that adds it to
a fix list we work through.

---

## 12. AI: where it helps, what it costs, and running without it

The core app needs **no AI while you use it**. All teaching content is pre-built.

Optional AI features:

1. **Grading your written sentences (U1).** Is the meaning right? Grammar OK? Natural
   word partners? Plus a one-line tip and an improved version.
   - Without AI: a self-check list ("right meaning? right part of speech? would a good
     writer say it this way?") and 3 model sentences to compare against.
   - Free middle option: a "Copy for review" button that copies your week's sentences
     with a ready-made prompt, to paste into your normal Claude chat.
2. **Enriching captured words** that aren't in the bank: picking the sense from your
   sentence and writing the plain definition, "vs" box and blanks. Without AI you get
   Wiktionary definitions plus your own sentence.

### Rough costs (Anthropic API, per million tokens, input / output)

Three tiers of model: top ($4 / $20), middle ($2 / $10), small and fast ($1 / $5).

| | Top tier | Middle tier | Small tier |
|---|---|---|---|
| Grading, about 5 sentences/day (realistic) | ~$1.30/month | ~$0.65/month | ~$0.20/month |
| Grading, about 20 sentences/day (heavy) | ~$5/month | ~$2.60/month | ~$0.70/month |
| One-time bank of 2,000 entries (Batch API, 50% off) | ~$20-30 | ~$10-15 | ~$5-7 |

Assumptions: about 400 input + 150 output tokens per grade, about 1,300 input + 900
output tokens per bank entry, plus some thinking tokens on the top and middle tiers.
The grading prompt is too short to benefit from prompt caching. Bank content is seen
hundreds of times and is permanent, so that is where model quality matters most;
grading is a simpler judgement. The choice of model is yours.

The server enforces a hard monthly spend cap you set (say $3) and a daily call limit.
The API key lives only on the server as a secret, never in the app's code.

---

## 13. Phone and PC

### 13.1 Decision: one Progressive Web App (PWA)

One codebase: a website that installs and behaves like an app.

| Option | Verdict |
|---|---|
| **PWA** | Free, one codebase, installs to the phone home screen and on PC (Chrome/Edge "Install app"), works offline, updates instantly. **Chosen.** |
| Native iOS/Android apps | iOS needs a $99/year developer account, or re-installing every 7 days. Two codebases. No. |
| Desktop app (Electron/Tauri) | The PWA already installs on PC. Not needed. |

PWA downsides, and answers:
- No home-screen widgets: accepted.
- On iPhone, the share sheet can't send to a PWA: solved with an iOS Shortcut (13.5).
- iOS can clear a web app's storage: the sync server holds the real copy.
- If we ever need native-only features, the same app can be wrapped with Capacitor.

### 13.2 Architecture: local-first, with a tiny sync server

```
   Phone (installed PWA)                 PC (installed PWA)
  +-------------------------+          +-------------------------+
  | UI: session, word pages |          | UI                      |
  | Engine: FSRS, session   |          | Engine                  |
  |   builder, grading      |          |                         |
  | IndexedDB: event log +  |          | IndexedDB               |
  |   derived state         |          |                         |
  | Cached word bank        |          | Cached word bank        |
  +-----------+-------------+          +------------+------------+
              |   send new events / fetch events since cursor
              +-------------------+-------------------+
                                  |
                     +------------v-------------+
                     | Cloudflare Worker        |
                     |   /sync  /inbox  /ai/*   |
                     | D1 database (SQLite):    |
                     |   events, inbox          |
                     | Secret: AI API key       |
                     +--------------------------+

     App files + word bank: Cloudflare Pages (static, free)
```

- **All the logic runs on the device.** The app works fully offline; the server only
  stores and relays.
- Hosting: Cloudflare Pages for the app and word-bank files; a Cloudflare Worker with a
  D1 database for sync. The free tier is far beyond what one person uses, and it doesn't
  pause when idle (Supabase's free tier does, which would be annoying).
- **Login:** it's a single-user app. A long random sync key, entered once per device and
  sent with every request. Simple, and enough for a personal app.

### 13.3 Sync design: an event log

Everything you do is an event added to a log: word_added, review, sentence_written,
use_logged, settings_changed, and so on. Each has a unique id, a timestamp and a device id.

- Device to server: "here are my new events". Server to device: "here is everything
  after your cursor".
- Your state (each word's stage, FSRS numbers, what is due) is **computed by replaying
  the log**. FSRS state is a pure function of review history, so if you review on the
  phone offline on a train and on the PC at home, merging is just "combine both lists
  and sort by time". No conflicts, nothing lost.
- Editable text (mnemonics, notes): last edit wins.
- Periodic snapshots keep replay fast as the log grows.
- Syncs when the app opens, after every session, and every few minutes while open.

### 13.4 Backups

- The server backs up the log weekly (a scheduled Worker job writing to Cloudflare R2,
  also free at this size).
- A "Download everything" button gives JSON plus a CSV of your words. Your data is never
  trapped.

### 13.5 Capturing words on each device

Every capture route writes to the server Inbox, so a word captured anywhere shows up
everywhere.

- **Android:** the installed PWA appears in the system share sheet (Web Share Target).
  Select text in any app, Share, Vocab.
- **iPhone:** an iOS Shortcut in the share sheet ("Add to Vocab") that sends the selected
  text straight to the Inbox. (Opening a link would land in Safari, which on iOS keeps
  separate storage from the installed app, hence going via the server.)
- **PC:** a bookmarklet. Select a word on any web page, click "+Vocab", and a small popup
  grabs the word, the sentence around it, and the page title and URL. Optionally later,
  a tiny browser extension with a right-click "Add to Vocab".
- **Everywhere:** a quick-add box inside the app.

### 13.6 Same app, different layouts

| | Phone | PC |
|---|---|---|
| Best for | Daily reviews, 2-minute mode, capturing | Writing tasks, reading companion, browsing your words |
| Input | Big buttons in thumb reach; answer boxes with autocorrect and predictions off | Keyboard-first: 1-4 to answer, Enter to submit, Space to reveal, H for a hint, ? for "don't know" |
| Layout | One card at a time | Word page with a side panel (roots, related words, your sentences) |
| Reminders | One daily push notification (Android; iPhone on iOS 16.4+ once added to the home screen) | Optional |

### 13.7 Tech stack (proposal)

- TypeScript throughout.
- Svelte + Vite for the interface (small and quick on phones).
- vite-plugin-pwa for offline support and installing.
- Dexie on top of IndexedDB for on-device storage.
- ts-fsrs for scheduling.
- Cloudflare Worker + D1 for sync, R2 for backups.
- Vitest for unit tests (scheduler, grading, log replay); Playwright for end-to-end tests,
  including a phone-sized screen.
- Python scripts for building the word bank (good tooling for Wiktionary and WordNet
  data).

---

## 14. Data model (conceptual)

**Static: the word bank**
- Entry: id, headword, sense, part of speech, IPA, definition, nuance, examples,
  blank sentences, misuse sentences, word partners, family, synonyms with "vs" notes,
  confusables, roots, origin, band, tags, usefulness
- Root: id, form, meaning, example words

**Yours: the event log (the only source of truth)**
- Event: id, time, device, type, payload
- Review payload: entry, track, exercise type, which sentence was shown, your answer,
  correct or not, hints used, response time, rating, and what you chose instead (for
  confusion tracking)

**Derived: rebuilt from events and cached**
- Your word: entry, stage, source, captured sentences, mnemonic, your sentences,
  recognition FSRS state, production FSRS state, lapses, leech flag, confusion pairs,
  times seen in the wild
- Stats totals, today's queue

---

## 15. Build roadmap

Every phase ends with something you use daily.

| Phase | What gets built | Done when |
|---|---|---|
| 0. Content foundations | Word-list selection, entry format, quality checks, first ~150 entries, Wiktionary import for captured words, scheduler simulation to set defaults | 150 entries pass checks; simulation confirms 5 new/day is about 15 min |
| 1. Core loop (on-device) | Placement test, new-word introduction, R1 R3 P1 P3, two-track FSRS with stages, daily session with load balancing, basic stats, export | You do a real daily session in the phone browser and on PC for 2 weeks |
| 2. One app, two devices | Installable PWA + offline, sync server, Inbox and capture (share target, iOS Shortcut, bookmarklet) | Review on the phone, see it on the PC; capture works from both |
| 3. Depth | R2 R4 P2 P4, confusion tracking, leeches, writing tasks with self-check, optional AI grading, use-it challenges, your sentences as blanks, bank to ~1,500 | Words start reaching Owned |
| 4. Growth | Reading companion, roots module, monthly retest and growth chart, personal FSRS tuning, bank to 3,000+ | Vocabulary estimate trending up |

The session-by-session build order is in [ROADMAP.md](ROADMAP.md).

---

## 16. Risks

| Risk | Answer |
|---|---|
| Reviews pile up and you quit | Time budget, auto-throttled new words, catch-up mode, 2-minute mode |
| Bad content (wrong definition, unfair blank) | Automatic checks, "Something's wrong" button, fix list |
| Fake progress (guessing, generous self-grading) | Typed checks, "I don't know", multiple choice never Easy, calibration stat, monthly vocab test |
| Data loss or iOS clearing storage | Server copy, weekly backups, export |
| Scope creep | Phases; Phase 1 on its own is already useful |

---

## 17. Decisions

| Question | Decision | What it changes |
|---|---|---|
| Phone | iPhone | Capture through an iOS Shortcut (13.5); reminders need the app added to the home screen (iOS 16.4+); everything is tested on iPhone Safari and as a home-screen app first |
| Language | English is the first language; goal is a richer, more precise vocabulary | Frontier and word bank as planned |
| Focus | Academic | Section 3.6: academic weighting, register labels, essay-ready phrases, essay writing prompts, U3 "Make it academic" |
| Daily time | Your choice, and the app tailors itself to it | Section 6.7. Default 15 minutes |
| AI | Word bank: written by Claude in content sessions ($0). Sentence feedback: free self-check and "Copy for review" first; AI grading switched on in build session S11 using the top-tier model with a $3/month cap (realistic use about $1-2/month). Cheaper tiers are an option. | Section 12; build session S11 |
| Kindle | No | Kindle import removed |

Still open (not blocking): your subjects and level (school, university), to make the
writing prompts and example sentences more relevant. It can also be a setting in the app.
