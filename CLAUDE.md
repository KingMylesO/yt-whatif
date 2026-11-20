# What If channel: batch runbook

This repo makes and uploads videos for the YouTube channel **Myles AI stories** (science what-ifs: space, Earth, the human body). Read this file, then `STYLE.md` and `topics.md`, before doing anything.

## Standing instructions from the owner (Myles)
- A scheduled task runs this **every Wednesday, Friday, Saturday and Sunday** at 01:43 Africa/Lagos.
- Each run: **25 new ideas**, then **at least 11 finished videos: 3 long-form + 8 Shorts**.
- Upload **unlisted** right after the run with the channel's **own free uploader** (GitHub Actions + YouTube Data API, step 12); Metricool is only the fallback. The owner switches them to **public** in YouTube Studio once YouTube has finished processing them. No script review step, so nobody is there to answer questions. Make sensible decisions and record them in the report.
- Every video, long-form and Short, says like and subscribe around the middle (owner, 2026-11-18). See STYLE.md sections 4-5.
- Quality beats quantity, except that the minimum of 11 still stands. If a video fails QA and can't be fixed, replace it with another idea; don't publish it broken.

## Workspace facts
- Cloud workspace: 2 CPU cores, no GPU. Network allowlist: GitHub (including raw.githubusercontent.com) and pip only. huggingface.co is blocked. WebSearch and WebFetch work for research.
- Paths are hardcoded: code in `/home/claude/proj`, renders in `/home/claude/proj/build/<name>/`, maps in `/home/claude/data`, voice model in `/home/claude/tts`, finished files in `/home/claude/out/<batch>/`.
- Background processes die a few minutes after a turn ends. **Never end your turn while rendering.** Wait in the foreground (`sleep 500` chunks, under 10 minutes per call) until the render finishes.

## The run, step by step
0. **Setup (≈5 min):** `bash pipeline/setup.sh`. It installs packages, downloads the Kokoro voice and the Natural Earth maps, and renders a self-test Short. It must print `SETUP OK`.
1. **Batch number:** the next N after the last batch in `topics.md`. Use names `bN_<slug>` for long-form videos and `short_bN_<slug>` for Shorts. A name starting with `short` renders 1080×1920; anything else renders 1920×1080.
2. **25 ideas:** research fresh what-ifs, mixing space, Earth and body. Never repeat anything in `topics.md`. For each idea give a one-line hook, why it works, and 2–3 real sources. Save them to `ideas/YYYY-MM-DD.md`.
3. **Pick 11 videos:**
   - 3 long-form topics, each with 2 Shorts: a teaser cut from it and a standalone mini what-if on the same theme.
   - 2 more standalone Shorts from the idea list, each pointing to the closest long-form.
4. **Scripts:** follow `STYLE.md`. Long-form is **≥1,300 words** (batches 03–04 measured ≈0.38 s per word with this voice; 8:00 is the mid-roll minimum). Shorts are 90–140 words. **Every script includes the like-and-subscribe line** near the middle (STYLE.md sections 4–5); it doesn't count toward the word minimum. Fact-check every claim with WebSearch and put a claim → source table under each script. Save to `scripts/YYYY-MM-DD-batch-NN.md`.
5. **Narration plan:** write `/home/claude/proj/narration_bN.py`, copying the structure of `narration2.py`:
   - `VIDEOS` dict: each name maps to a list of scenes, and each scene has `key`, `scene`, `lines`, `opts`, `sfx` and `hold`.
   - `CHAPTERS` for the long-form videos.
   - `MUSIC`: name → preset from `audio.PRESETS`. Add new presets for new moods.
   - **Like and subscribe:** put the line in the scene nearest the midpoint (a chapter boundary for long-form, between two beats for Shorts) and add `"cta": <index of that line in the scene's lines>` to that scene's `opts`. The renderer (`cta.py`, called from `render.Drawer.frame`) then shows the animated subscribe button from 0.1 s before the line until 0.6 s after it. It sits at 0.82H on long-form and 0.75H on Shorts (below the captions), so pick a scene whose band there is free of key visuals.
   - Spell for text-to-speech: numbers and years as words, phonetic spellings for hard names (e.g. "Cheek-shoo-loob"). `meta2.tts_to_text` maps them back for captions, so add new mappings there.
   - Then run `python3 voice.py <names...>`.
6. **Scenes:** write `/home/claude/proj/scenes_bN_<topic>.py`. Every module needs a `SCENES` dict, and render.py loads any `scenes_*.py` automatically.
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
    2. **Push the queue:** `git fetch origin main && git checkout -B upload origin/main`, copy `uploads.json` and every file it names into `queue/`, and commit and push one file per commit (`git push -f origin upload` for the first, plain pushes after). Push `queue/uploads.json` **last**, with `[upload]` in its commit message: that push starts the workflow, which uploads each video, then its thumbnail and captions. Go back to `main` afterwards.
    3. **Wait for the result:** every minute run `git fetch -q origin upload && git show origin/upload:queue/results.json` until it has a `summary` or an `error` (allow up to 90 minutes; never end the turn while waiting). Each video gets an `id` and `url`, plus `thumbnail` and `captions` set to "ok" or the reason they failed (custom thumbnails need a phone-verified channel). Once everything is up, the workflow removes the media from the branch.
    4. **Retry:** if some videos failed but a `summary` exists, push an empty commit to `upload` with `[upload]` in the message (`git commit --allow-empty -m "retry [upload]"`). The uploader skips videos that already have an id. Retry once.
    5. **Fallback:** if `results.json` shows `"error": "auth: ..."` (secrets missing or revoked), or nothing appears within 90 minutes, upload whatever isn't up through Metricool (step 12b) and say so in the report.

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
       - Upload all 11 straight away: the first one ~3 minutes after scheduling, then 30 seconds apart. Metricool rounds to whole minutes, so that works out at about 2 per minute.
       - Put the 3 long-form videos first, then the Shorts.
    5. **Clean up:** force-push an empty commit to `media` so the links stop working.
    6. **Verify** with `getScheduledPosts`: wait until all 11 show `PUBLISHED` (uploaded as unlisted) and note each `publicUrl`.
13. **Record:**
    - Append the batch to `topics.md` (titles plus scheduled dates).
    - Commit `pipeline/narration_bN.py`, `pipeline/scenes_bN_*.py`, the ideas, the scripts and `reports/YYYY-MM-DD.md` to `main`, then push.
    - If the Projects tool is available, write the report to the "YT" project as `claude/batch-NN-production.md`.
14. **Finish:** send one short summary covering:
    - the 11 titles with their YouTube links (unlisted);
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
- Custom thumbnails fail until the channel is phone-verified; the uploader records the failure and carries on.
