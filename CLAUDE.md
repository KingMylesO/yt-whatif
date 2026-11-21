# What If channel: batch runbook

This repo makes and uploads videos for the YouTube channel **Myles AI stories** (science what-ifs: space, Earth, the human body). Read this file, then `STYLE.md` and `topics.md`, before doing anything.

> **Owner update, 2026-11-20. This overrides the scheduled task's own prompt.** That prompt still says four runs a week, 25 ideas, at least 11 videos (3 long-form + 8 Shorts) and uploads through Metricool. The owner cut the volume to fit the Claude plan's usage limits. Follow this runbook instead: **15 ideas, 10 videos (2 long-form + 8 Shorts)**, at least one long-form about something important happening right now (steps 2–3), and the channel's own uploader (step 12).

## Standing instructions from the owner (Myles)
- A scheduled task runs this **every Monday and Friday** at 01:43 Africa/Lagos (owner, 2026-11-20; it ran four times a week before).
- Each run: **15 new ideas**, then **at least 10 finished videos: 2 long-form + 8 Shorts** (owner, 2026-11-20). One full run should fit inside one 5-hour usage window, so don't over-build: reuse helpers from earlier scene modules where they fit.
- Upload **unlisted** right after the run with the channel's **own free uploader** (GitHub Actions + YouTube Data API, step 12); Metricool is only the fallback. The owner switches them to **public** in YouTube Studio once YouTube has finished processing them. No script review step, so nobody is there to answer questions. Make sensible decisions and record them in the report.
- Every video, long-form and Short, says like and subscribe around the middle (owner, 2026-11-18). See STYLE.md sections 4-5.
- Quality beats quantity, except that the minimum of 10 still stands. If a video fails QA and can't be fixed, replace it with another idea; don't publish it broken.

## Workspace facts
- Cloud workspace: 2 CPU cores, no GPU. Network allowlist: GitHub (including raw.githubusercontent.com) and pip only. huggingface.co is blocked. WebSearch and WebFetch work for research.
- Paths are hardcoded: code in `/home/claude/proj`, renders in `/home/claude/proj/build/<name>/`, maps in `/home/claude/data`, voice model in `/home/claude/tts`, finished files in `/home/claude/out/<batch>/`.
- Background processes die a few minutes after a turn ends. **Never end your turn while rendering.** Wait in the foreground (`sleep 500` chunks, under 10 minutes per call) until the render finishes.

## The run, step by step
0. **Setup (≈5 min):** `bash pipeline/setup.sh`. It installs packages, downloads the Kokoro voice and the Natural Earth maps, and renders a self-test Short. It must print `SETUP OK`.
1. **Batch number:** the next N after the last batch in `topics.md`. Use names `bN_<slug>` for long-form videos and `short_bN_<slug>` for Shorts. A name starting with `short` renders 1080×1920; anything else renders 1920×1080.
2. **15 ideas:** research fresh what-ifs, mixing space, Earth and body. Never repeat anything in `topics.md`. For each idea give a one-line hook, why it works, and 2–3 real sources. Save them to `ideas/YYYY-MM-DD.md`.
   - **Something important happening (owner, 2026-11-20):** at least 5 of the 15 hang off something big that is really happening: a discovery, launch, mission, record, natural event or tech breakthrough from roughly the last 2–3 weeks, or one coming up soon. Find them with WebSearch for the current dates, and name what happened and when in the hook ("Last week, astronomers found…" → "What if…?").
   - Date the event and cite a primary source (space agency, journal, university, official body). Say plainly what is confirmed and what is still unknown.
   - Events with real victims (disasters, wars, outbreaks): explain the science calmly, never sensationalise, and skip any idea that would trade on people's suffering.
3. **Pick 10 videos:**
   - 2 long-form topics, each with 2 Shorts: a teaser cut from it and a standalone mini what-if on the same theme. **At least one long-form comes from the "happening now" ideas.**
   - 4 more standalone Shorts from the idea list, each pointing to the closest long-form. At least 2 of them come from the "happening now" ideas.
   - **The Crush Files, Friday runs only (owner, 2026-11-20):** check the day with `TZ=Africa/Lagos date +%A`. On a Friday run, the other 2 extra Shorts are crush-science Shorts starring Kai in the 3D-world/2D-character style (STYLE.md section 11). Take topics from the Crush Files backlog in `topics.md` (or research new ones), never repeat one, and point them to the closest long-form or to "more Crush Files on the channel". On a Monday run, those 2 Shorts are ordinary standalone what-if Shorts instead.
4. **Scripts:** follow `STYLE.md`. Long-form is **≥1,300 words** (batches 03–04 measured ≈0.38 s per word with this voice; 8:00 is the mid-roll minimum). Shorts are 90–140 words. **Every script includes the like-and-subscribe line** near the middle (STYLE.md sections 4–5); it doesn't count toward the word minimum. Fact-check every claim with WebSearch and put a claim → source table under each script. Save to `scripts/YYYY-MM-DD-batch-NN.md`.
5. **Narration plan:** write `/home/claude/proj/narration_bN.py`, copying the structure of `narration2.py`:
   - `VIDEOS` dict: each name maps to a list of scenes, and each scene has `key`, `scene`, `lines`, `opts`, `sfx` and `hold`.
   - `CHAPTERS` for the long-form videos.
   - `MUSIC`: name → preset from `audio.PRESETS`. Add new presets for new moods.
   - **Like and subscribe:** put the line in the scene nearest the midpoint (a chapter boundary for long-form, between two beats for Shorts) and add `"cta": <index of that line in the scene's lines>` to that scene's `opts`. The renderer (`cta.py`, called from `render.Drawer.frame`) then shows the animated subscribe button from 0.1 s before the line until 0.6 s after it. It sits at 0.82H on long-form and 0.75H on Shorts (below the captions), so pick a scene whose band there is free of key visuals.
   - Spell for text-to-speech: numbers and years as words, phonetic spellings for hard names (e.g. "Cheek-shoo-loob"). `meta2.tts_to_text` maps them back for captions, so add new mappings there.
   - Then run `python3 voice.py <names...>`.
6. **Scenes:** write `/home/claude/proj/scenes_bN_<topic>.py`. Every module needs a `SCENES` dict, and render.py loads any `scenes_*.py` automatically.
   - **Crush Files scenes** import `kit3d` and `mc` (both libraries, not scene modules) and build every shot as: `kit3d.render(...)` the set (cache static cameras with `kit3d.CACHE`), then `mc.kai(...)` / `mc.crush(...)` at `kit3d.anchor(...)`. Animate with the camera (slow dolly or orbit), Kai's pose/expression changes on the narration beats, and 3D props (`heart`, `question_mark`, phones, brains built from spheres). Reuse sets across videos but vary camera, props and time of day so videos don't look identical.
   - **Libraries:** build from `core.py` (drawing and text), `common2.py` (props, `beats`, `phase`, `Layer`, chips, generic `title2`, `card2`, `end2`, `end_short2`) and `geo.py` (real-coastline `draw_map`, textured `globe`, `globe_xy` for pins, `map_rect`).
   - **Shorts layout:** keep content between 0.20H and 0.58H. Captions are burned in at 0.635H, the badge sits at 0.14H, and the hook text at 0.2H.
   - **Variety:** give each long-form its own visual motif and palette. Avoid near-identical videos; YouTube demonetizes "inauthentic", mass-produced content.
7. **Preview and fix:** run `python3 render.py preview <name>` and **look at every sheet** (scenes with a `cta` get an extra mid-button frame). Fix overlaps, empty frames, unreadable text and wrong geography before rendering.
8. **Render:** `python3 build_batch.py /home/claude/out/bN name=file.mp4 ...`. A long-form takes about 10–13 minutes, a Short about 1–3.
9. **QA each file:**
   - Duration: long-form ≥ 8:00.
   - Loudness ≈ −14 LUFS: `ffmpeg -nostats -i f.mp4 -af ebur128 -f null -`.
   - Look at a contact sheet: `ffmpeg -i f.mp4 -vf fps=1/20,scale=384:-1,tile=5x5 -frames:v 1 sheet.jpg`.
   - Like and subscribe: from `build/<name>/timeline.json`, check the `cta` line starts at 40–60% of the video's runtime, then grab a frame during it (`ffmpeg -ss <line start + 1.5> -i f.mp4 -frames:v 1 cta.jpg`) and confirm the subscribe button is visible and clear of the captions.
10. **Thumbnails** (long-form only, 1280×720): one big subject, at most 3 words, Inter Display 900, accent `#FFC93C`. See `thumb2.py`.
11. **Metadata:**
    - Captions and chapters: `python3 meta2.py OUT name=file.srt ...`.
    - Descriptions follow STYLE.md section 9 and always include "Narration uses an AI voice. Animation and music are original."
12. **Upload with the channel's own uploader** (free; unlisted; long-forms first). This workspace can't reach Google's APIs, so the upload itself runs on GitHub Actions (`.github/workflows/youtube-upload.yml` runs `pipeline/yt_upload.py`), using the repo secrets `YT_CLIENT_ID`, `YT_CLIENT_SECRET` and `YT_REFRESH_TOKEN`.
    1. **Queue:** `python3 pipeline/yt_upload.py manifest /home/claude/out/bN` writes `uploads.json` from `meta.json` (it picks up `<name>.mp4`, `thumbnail_<topic>.png` for long-forms and `<name>.srt`). Then `python3 pipeline/yt_upload.py check /home/claude/out/bN` must report every video ok. Every file must be under 100 MB (GitHub's limit); re-encode a long-form with a higher CRF if it isn't.
    2. **Carry over leftovers first:** `git fetch origin upload` and compare `origin/upload:queue/uploads.json` with `queue/results.json`. Any video there without an `id` (its files are still on the branch) goes into this batch's queue too, right after this batch's long-forms. Then you can reset the branch.
       **Push the queue:** `git fetch origin main && git checkout -B upload origin/main`, copy `uploads.json` and every file it names into `queue/`, and commit and push one file per commit (`git push -f origin upload` for the first, plain pushes after). Push `queue/uploads.json` **last**, with `[upload]` in its commit message: that push starts the workflow, which uploads each video, then its thumbnail and captions. Go back to `main` afterwards.
    3. **Wait for the result:** every minute run `git fetch -q origin upload && git show origin/upload:queue/results.json` until it has a `summary` or an `error` (allow up to 90 minutes; never end the turn while waiting). Each video gets an `id` and `url`, plus `thumbnail` and `captions` set to "ok" or the reason they failed (custom thumbnails need a phone-verified channel). Once everything is up, the workflow removes the media from the branch.
    4. **Daily limit:** `uploadLimitExceeded` is YouTube's own cap on uploads per channel per 24 hours (about 10 while the channel isn't phone-verified). The uploader stops there, and the workflow retries what's left every hour on its own, so don't use Metricool for those (it hits the same cap). List them in the report as "queued, uploads automatically within a day".
    5. **Other failures:** if some videos failed for another reason but a `summary` exists, push an empty commit to `upload` with `[upload]` in the message (`git commit --allow-empty -m "retry [upload]"`) once. The uploader skips videos that already have an id.
    6. **Fallback:** if `results.json` shows `"error": "auth: ..."` (secrets missing or revoked), or nothing appears within 90 minutes, upload whatever isn't up through Metricool (step 12b) and say so in the report.

12b. **Metricool fallback** (MCP tools `mcp__Metricool_Social_Media_Management__*`). The free plan only publishes about 20 posts a month, then fails with "You have reached your Metricool account limit." If the first post fails with that error, stop creating posts and send the owner the files plus `upload_sheet_batchNN.txt` to upload by hand.
    1. `getBrandSettings`. Use the brand whose `networksData.youtubeData` is `UCyF8bKnMvQV_AzTCPJDxCGw`; brand 8106210 had it on 2026-11-14. Timezone: Africa/Lagos.
    2. **Host the files:**
       - Clone this repo with push access (`add_repo` KingMylesO/yt-whatif, access "push").
       - Push the MP4s and thumbnails to an orphan branch **`media`**, one commit and push per file, force-push allowed. GitHub releases and branch deletion are blocked for these sessions.
       - The URL is `https://raw.githubusercontent.com/KingMylesO/yt-whatif/media/<file>`.
    3. **Schedule each video** with `createScheduledPost`:
       - `providers` [{"network":"youtube"}], `autoPublish` true.
       - `text` = the description.
       - `youtubeData` = {title, type "video" or "short", privacy **"unlisted"**, tags, category "SCIENCE_TECHNOLOGY", madeForKids false, isAiGeneratedContent false}.
       - Metricool copies the media to its own storage the moment the post is created.
       - For long-form videos, include `videoThumbnailUrl`. If you get `VIDEO_THUMBNAIL_NOT_APPLICABLE` (channel not verified yet), retry without it.
    4. **When to post:**
       - Upload all 10 straight away: the first one ~3 minutes after scheduling, then 30 seconds apart. Metricool rounds to whole minutes, so that works out at about 2 per minute.
       - Put the 2 long-form videos first, then the Shorts.
    5. **Clean up:** force-push an empty commit to `media` so the links stop working.
    6. **Verify** with `getScheduledPosts`: wait until all 10 show `PUBLISHED` (uploaded as unlisted) and note each `publicUrl`.
13. **Record:**
    - Append the batch to `topics.md` (titles plus scheduled dates).
    - Commit `pipeline/narration_bN.py`, `pipeline/scenes_bN_*.py`, the ideas, the scripts and `reports/YYYY-MM-DD.md` to `main`, then push.
    - If the Projects tool is available, write the report to the "YT" project as `claude/batch-NN-production.md`.
14. **Finish:** send one short summary covering:
    - the 10 titles with their YouTube links (unlisted);
    - a reminder to the owner to switch them to **Public** in YouTube Studio once processing finishes (Content → select them → Edit → Visibility → Public);
    - anything skipped or replaced, and any decisions you made.

## Known gotchas
- `skia.FontStyle.Black` doesn't exist. Use `skia.FontStyle(900, kNormal_Width, kUpright_Slant)` (already done in `core.font`).
- `geo.globe` rounds R down to a multiple of 4. Use `geo.globe_xy` for pins so they line up.
- `land_path` is cached by rect, so keep map rects constant and animate with canvas transforms instead.
- A map with a salt rim or shrinking sea must clip land drawing to the map rect (see `scenes_med.med_map`).
- `phase()` keeps the outgoing panel opaque until the next one has faded in, so draw panels in time order.
- The browser pane can't open file pickers, so uploads never go through YouTube Studio.
- Since 2026-11-02, YouTube no longer locks uploads from unverified API projects to private (Data API revision history), so the channel's own uploader can post unlisted or public. The default quota is 100 uploads a day per project.
- The uploader also posts captions (`captions.insert`). Metricool can't, so after a Metricool fallback keep the .srt files in `reports/bN_assets/` and mention them in the report.
- The channel was phone-verified on 2026-11-20, so custom thumbnails now work (the batch 04–05 long-forms got theirs that day). If a thumbnail fails, the uploader records it and carries on.
- To add a thumbnail or captions to a video that's already on YouTube, queue an entry with `video_id` (plus `title` as a guard) instead of `file`; see the top of `pipeline/yt_upload.py`.
