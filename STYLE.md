# What If Channel: Style Guide

This is the rulebook for every script, title and thumbnail on the channel, and every Claude session follows it. The run-by-run process is in CLAUDE.md.

## 1. Channel concept
- **Niche:** science what-ifs about space, planet Earth and the human body.
- **Promise to the viewer:** "A wild hypothetical, answered with real science, told like a story."
- **Audience:** curious 13–35 year olds who watch Kurzgesagt, Veritasium and What If–style channels but want faster pacing.
- **Format:** faceless. Narration (the Kokoro "Heart" AI voice) over code-drawn animation with original music.
- **Channel:** Myles AI stories.

## 2. Output cadence (owner's decision, 2026-11-20; four runs a week before that)
- **When:** two runs a week, on Monday and Friday at 01:43 Africa/Lagos.
- **What each run makes:**
  - 15 new ideas, at least 5 of them about something important that is really happening right now (CLAUDE.md step 2).
  - 10 or more videos: 2 long-form plus 8 Shorts.
  - Each long-form gets a teaser Short and a standalone Short, and the run adds 4 extra standalone Shorts. At least one long-form and two of the extra Shorts are about something happening now.
- **Release:** uploaded **unlisted** with the channel's own uploader (CLAUDE.md step 12) right after each run. The owner switches them to public in Studio once YouTube has finished processing them.
- **Long-form:** 8–12 minutes, 1,300–1,900 words. Batches 03–04 measured about 0.38 s per word at this voice's pace, so **write at least 1,300 words** to clear 8:00, the minimum for mid-roll ads. Add real "wait, really?" facts rather than padding.
- **Shorts:** 30–55 seconds, 90–140 words, ending by pointing to the long video.
- **Like and subscribe:** every video, long-form and Short, asks for it once around the middle (owner, 2026-11-18). See sections 4–5.

## 3. Voice and tone
- Second person ("you"), present tense, with the viewer inside the scenario.
- A calm, confident narrator with dry humor. Never shouty, never clickbait-panicky.
- Short sentences, one idea per sentence.
- A "wait, really?" moment (a surprising, true fact) every 30–45 seconds.
- No filler openers. The hook is the first line.
- Explain any number with a comparison.

## 4. Long-form structure
1. **Hook** (0:00–0:15): one shocking, true statement plus the question.
2. **Setup** (0:15–1:00): the rules of the hypothetical.
3. **Timeline:** escalating time jumps (e.g. 8 minutes → 1 day → 1 year → 1 million years), each with a title card.
4. **Like and subscribe** (about the halfway mark, 45–55% of the runtime, at a chapter boundary; never in the hook, the twist or the outro): one short, natural line in the narrator's calm voice, worded differently in every video, e.g. "Quick favour: if you're enjoying this, hit like and subscribe. It really helps the channel." It doesn't count toward the word minimum.
5. **Twist** (last ~90 s): a counterintuitive outcome, or "this actually almost happened".
6. **Outro** (last ~15 s): a callback to the hook plus a question for the comments.

## 5. Shorts structure
1. **Hook** (0–2 s): the on-screen text matches the narration.
2. **Payoff** (2–40 s): 3–5 fast beats, each a new fact.
3. **Mid-Short like and subscribe** (around the halfway mark, between two beats): eight words or fewer, e.g. "Like and subscribe for more what-ifs." Then keep going; the Short still ends with "Full story on the channel."
4. **Loop or redirect** (last 5 s): end on "Full story on the channel."

Vertical 9:16 with burned-in captions, and a visual change every 1–2 seconds.

## 6. Accuracy rules (non-negotiable)
- Every factual claim needs a reputable source: NASA, ESA, peer-reviewed papers, university press releases or major science outlets. List the sources in the description.
- Separate fact from speculation ("scientists think…", "one estimate suggests…").
- Never present a made-up number as fact. If unsure, cut it.
- If newer research disputes a popular claim, say so. The debate can be the twist.
- Attribute claims that come from one person to that person.
- Put a claim → source table under every script.
- **No health or medical advice.** Body topics are explainers, never "you should do X".
- **"Happening now" topics:** give the date of the event, cite the primary source (agency, journal, university or official body) as well as any news coverage, and say plainly what's confirmed and what's still unknown. Early news gets corrected, so prefer the primary source's own wording. Treat events with real victims with care: explain the science, never sensationalise.

## 7. Titles
Keep titles under 60 characters. Formulas:
- `What If [Impossible Thing] Happened?`
- `What If You [Did Extreme Thing] for [Time]?`
- `What Happens If [Thing] Disappeared?`
- `What If Earth Had [Unusual Feature]?`

Write 5 options and pick the one with the clearest single image.

## 8. Thumbnails
- One big subject with one strong contrast.
- At most 3 words of text, which don't repeat the title.
- High saturation and readable at phone size.
- Brand: Inter Display Black, accent yellow #FFC93C, dark navy outline.

## 9. Description template
```
[1–2 sentence hook summary]

⏱️ Chapters
0:00 [Hook]
...

📚 Sources
- [Source]

Narration uses an AI voice. Animation and music are original.

#whatif #science #space
```

## 10. YouTube policy guardrails
- **Avoid "inauthentic" (mass-produced or repetitious) content.**
  - Every topic is distinct.
  - Every long-form has its own hand-built visual motif and palette.
  - Vary scene designs and structures between videos.
  - Never upload near-identical videos.
- **AI disclosure:** the Studio AI question covers realistic content only, so our animated videos with a generic AI narrator answer **No** (`isAiGeneratedContent: false`). The description always says the narration uses an AI voice.
- **Audience:** always "not made for kids".
- **No real people:** no likenesses or voices of real people, no copyrighted characters or brands, and only original music and art.

## 11. The Crush Files (owner's series, 2026-11-20)
- **What:** every **Friday** run (not Monday), 2 of the 10 videos are *The Crush Files*: real science of crushes and attraction (what your brain and body do around a crush), told in second person like everything else. By default both are Shorts, taking 2 of the run's 4 extra standalone Shorts.
- **Look: 3D world, 2D character.** Backgrounds and objects are low-poly 3D sets (`pipeline/kit3d.py`: `bedroom()`, `hallway()`, or new sets built from `box`, `cylinder`, `sphere`, `heart`, `question_mark`). Characters are flat 2D with thick navy outlines (`pipeline/mc.py`), planted on the 3D floor with `kit3d.anchor()`.
- **Kai** is the main character: 19, curious, royal-blue hoodie with the yellow "?" patch, coral headphones around his neck. Use `mc.kai(...)` with its poses (idle, wave, phone, think, shrug, point, cheeks, fist) and expressions (neutral, happy, blush, nervous, shocked, lovestruck, sad, curious, talk). Never redraw him differently: the character sheet is `reports/kai_assets/kai_character_sheet.png`.
- **The Crush** is always the faceless glowing silhouette from `mc.crush(...)`, so every viewer can picture their own. Never give it a face, a name, a gender or an age.
- **Keep it PG and kind.** No sexual content, nothing about bodies being attractive or not, no body-shaming, no pickup tactics or "how to make them like you" advice, no relationship or mental-health advice. It's an explainer about feelings everyone has. Studies about attraction are often small: say "one study found", name the researchers, and don't overstate.
- **Shorts framing:** fill the frame with the 3D set, and keep Kai's head below 0.20H and feet above 0.58H (captions burn in at 0.635H). The camera in `kai_art.style_short` does this; static cameras can cache the set with `kit3d.CACHE`.
- **Titles:** e.g. "What Your Brain Does When Your Crush Texts Back", "Why You Blush Around Your Crush". Badge chip: "THE CRUSH FILES". Topic ideas are in the Crush Files backlog in `topics.md`.
