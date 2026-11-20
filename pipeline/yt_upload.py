"""Upload a batch straight to YouTube with the YouTube Data API (free; no Metricool).

Commands
  python yt_upload.py manifest OUT_DIR   write OUT_DIR/uploads.json from OUT_DIR/meta.json
  python yt_upload.py check DIR          validate DIR/uploads.json and its files (no network)
  python yt_upload.py upload DIR         upload everything in DIR/uploads.json
  python yt_upload.py pending DIR        print "count=N", the videos in DIR/uploads.json not uploaded yet

uploads.json
  {"videos": [
    {"file": "b6_moon.mp4",             required, relative to DIR
     "title": "What If ...?",           required, at most 100 characters, no < or >
     "description": "...",             required, at most 5,000 characters, no < or >
     "tags": ["what if", "space"],      optional, 500 characters in total
     "privacy": "unlisted",             private | unlisted | public (default unlisted)
     "publish_at": null,                optional ISO 8601 UTC time; needs privacy "private"
     "thumbnail": "thumbnail_moon.png", optional; YouTube only accepts it on a phone-verified channel
     "captions": "b6_moon.srt"}         optional English .srt
  ]}

Credentials come from YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN (made once with
yt_auth.py). Results go to DIR/results.json. A video that already has an id there is skipped,
so running "upload" again only sends what is missing.
"""
import json, os, sys, time

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]
CHANNEL_ID = "UCyF8bKnMvQV_AzTCPJDxCGw"
CATEGORY = "28"                       # Science & Technology
PRIVACY = ("private", "unlisted", "public")
RETRY_STATUS = {500, 502, 503, 504}
STOP_REASONS = {"quotaExceeded", "uploadLimitExceeded", "dailyLimitExceeded", "rateLimitExceeded"}
CHUNK = 8 * 1024 * 1024
EXTRAS = {"synthetic", "placement"}   # optional fields: "altered content: No", "no paid placement"
MAX_FILE = 100 * 1024 * 1024 - 1      # GitHub's per-file limit; the queue lives in the repo


# ---------- files ----------
def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default

def save(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)

def is_short(v): return os.path.basename(v["file"]).startswith("short")

def watch_url(v, vid):
    return f"https://www.youtube.com/shorts/{vid}" if is_short(v) else f"https://www.youtube.com/watch?v={vid}"


# ---------- manifest ----------
def make_manifest(out):
    """meta.json ({name: {title, description, tags}}, long-forms first) -> uploads.json."""
    meta = load(os.path.join(out, "meta.json"))
    if not meta:
        sys.exit(f"no meta.json in {out}")
    videos = []
    for name, m in meta.items():
        v = dict(file=f"{name}.mp4", title=m["title"], description=m["description"],
                 tags=m.get("tags", []), privacy="unlisted")
        thumb = f"thumbnail_{name.split('_')[1]}.png" if not name.startswith("short") else None
        if thumb and os.path.isfile(os.path.join(out, thumb)):
            v["thumbnail"] = thumb
        if os.path.isfile(os.path.join(out, f"{name}.srt")):
            v["captions"] = f"{name}.srt"
        videos.append(v)
    videos.sort(key=is_short)          # long-forms first, original order otherwise
    save(os.path.join(out, "uploads.json"), dict(videos=videos))
    print(f"wrote {out}/uploads.json: {len(videos)} videos")


def problems(d, v):
    p = []
    for k in ("file", "title", "description"):
        if not v.get(k):
            p.append(f"missing {k}")
    for k in ("file", "thumbnail", "captions"):
        if v.get(k):
            f = os.path.join(d, v[k])
            if not os.path.isfile(f):
                p.append(f"{k} not found: {v[k]}")
            elif os.path.getsize(f) > MAX_FILE:
                p.append(f"{v[k]} is over GitHub's 100 MB file limit")
    text = v.get("title", "") + v.get("description", "")
    if "<" in text or ">" in text:
        p.append("title/description contain < or >, which YouTube rejects")
    if len(v.get("title", "")) > 100:
        p.append("title is over 100 characters")
    if len(v.get("description", "").encode("utf-8")) > 5000:
        p.append("description is over 5,000 bytes")
    if sum(len(t) + 2 for t in v.get("tags", [])) > 500:
        p.append("tags are over 500 characters in total")
    if v.get("privacy", "unlisted") not in PRIVACY:
        p.append(f"privacy must be one of {PRIVACY}")
    if v.get("publish_at") and v.get("privacy") != "private":
        p.append('publish_at needs privacy "private"')
    return p

def pending(d):
    """count=N for the GitHub workflow: queued videos with no YouTube id yet (0 when there's no queue)."""
    q = load(os.path.join(d, "uploads.json")) or {}
    done = (load(os.path.join(d, "results.json")) or {}).get("videos", {})
    print(f"count={sum(1 for v in q.get('videos', []) if not done.get(v.get('file'), {}).get('id'))}")

def check(d):
    q = load(os.path.join(d, "uploads.json"))
    if not q or not q.get("videos"):
        sys.exit(f"no videos in {d}/uploads.json")
    bad = 0
    for i, v in enumerate(q["videos"], 1):
        p = problems(d, v)
        bad += bool(p)
        print(f"{i:2}. {'FAIL' if p else 'ok  '} {v.get('file')}: {v.get('title')}")
        for x in p:
            print(f"      - {x}")
    print(f"{len(q['videos']) - bad} ok, {bad} with problems")
    return q if not bad else sys.exit(1)


# ---------- YouTube ----------
def youtube():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    env = {k: os.environ.get(k, "").strip() for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")}
    missing = [k for k, val in env.items() if not val]
    if missing:
        raise RuntimeError("missing secrets: " + ", ".join(missing))
    creds = Credentials(None, refresh_token=env["YT_REFRESH_TOKEN"], client_id=env["YT_CLIENT_ID"],
                        client_secret=env["YT_CLIENT_SECRET"], token_uri="https://oauth2.googleapis.com/token",
                        scopes=SCOPES)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)

def reason(e):
    try:
        return json.loads(e.content)["error"]["errors"][0]["reason"]
    except Exception:
        return ""

def body_for(v, extras):
    status = dict(privacyStatus=v.get("privacy", "unlisted"), selfDeclaredMadeForKids=False,
                  embeddable=True, license="youtube")
    if v.get("publish_at"):
        status["publishAt"] = v["publish_at"]
    if "synthetic" in extras:
        status["containsSyntheticMedia"] = False      # animated, non-realistic: "altered content" = No
    body = dict(snippet=dict(title=v["title"], description=v["description"], tags=v.get("tags", []),
                             categoryId=CATEGORY, defaultLanguage="en", defaultAudioLanguage="en"),
                status=status)
    parts = ["snippet", "status"]
    if "placement" in extras:
        body["paidProductPlacementDetails"] = dict(hasPaidProductPlacement=False)
        parts.append("paidProductPlacementDetails")
    return ",".join(parts), body

def send_video(yt, path, v):
    """Resumable upload with retries. Optional fields YouTube rejects as unknown are dropped once."""
    import http.client
    import httplib2
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    extras = EXTRAS                    # shared, so a field YouTube rejects is dropped for the whole batch
    while True:
        part, body = body_for(v, extras)
        req = yt.videos().insert(part=part, body=body, notifySubscribers=False,
                                 media_body=MediaFileUpload(path, mimetype="video/mp4", chunksize=CHUNK, resumable=True))
        resp, tries, shown = None, 0, -1
        try:
            while resp is None:
                try:
                    st, resp = req.next_chunk()
                    if st and int(st.progress() * 10) != shown:
                        shown = int(st.progress() * 10); print(f"    {shown * 10}%", flush=True)
                except HttpError as e:
                    if e.resp.status not in RETRY_STATUS or tries >= 8:
                        raise
                    tries += 1; time.sleep(min(60, 2 ** tries))
                except (OSError, httplib2.HttpLib2Error, http.client.HTTPException):
                    if tries >= 8:
                        raise
                    tries += 1; time.sleep(min(60, 2 ** tries))
            return resp["id"]
        except HttpError as e:
            text = str(e.content)
            dropped = {x for x, key in (("synthetic", "containsSyntheticMedia"), ("placement", "paidProductPlacement"))
                       if x in extras and e.resp.status == 400 and key in text}
            if not dropped:
                raise
            print(f"    YouTube rejected {sorted(dropped)}; retrying without", flush=True)
            extras -= dropped

def upload(d):
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    q = check(d)
    rpath = os.path.join(d, "results.json")
    res = load(rpath, {}) or {}
    res.setdefault("videos", {})
    try:
        yt = youtube()
        me = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
        cid = me[0]["id"] if me else "?"
        res["channel"] = cid
        if cid != CHANNEL_ID:
            raise RuntimeError(f"signed in to channel {cid}, expected {CHANNEL_ID}; nothing uploaded")
    except Exception as e:
        res["error"] = f"auth: {e}"; save(rpath, res); print(res["error"]); sys.exit(2)
    res.pop("error", None)
    failed = 0
    for v in q["videos"]:
        r = res["videos"].setdefault(v["file"], {})
        if r.get("id"):
            print(f"skip {v['file']}: already uploaded ({r['url']})"); continue
        print(f"upload {v['file']}: {v['title']}", flush=True)
        try:
            vid = send_video(yt, os.path.join(d, v["file"]), v)
        except HttpError as e:
            r["error"] = f"{e.resp.status} {reason(e) or str(e)[:300]}"; failed += 1; save(rpath, res)
            print(f"    FAILED: {r['error']}")
            if reason(e) in STOP_REASONS:
                print("    YouTube limit reached; stopping"); break
            continue
        except Exception as e:
            r["error"] = str(e)[:300]; failed += 1; save(rpath, res); print(f"    FAILED: {r['error']}"); continue
        r.update(id=vid, url=watch_url(v, vid), title=v["title"], privacy=v.get("privacy", "unlisted"))
        r.pop("error", None)
        save(rpath, res)
        print(f"    done: {r['url']}", flush=True)
        if v.get("thumbnail"):
            try:
                p = os.path.join(d, v["thumbnail"])
                yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(
                    p, mimetype="image/png" if p.lower().endswith(".png") else "image/jpeg")).execute()
                r["thumbnail"] = "ok"
            except HttpError as e:
                r["thumbnail"] = f"failed: {e.resp.status} {reason(e)}"
            print(f"    thumbnail {r['thumbnail']}")
        if v.get("captions"):
            try:
                yt.captions().insert(part="snippet", body=dict(snippet=dict(
                    videoId=vid, language="en", name="English", isDraft=False)),
                    media_body=MediaFileUpload(os.path.join(d, v["captions"]),
                                               mimetype="application/octet-stream")).execute()
                r["captions"] = "ok"
            except HttpError as e:
                r["captions"] = f"failed: {e.resp.status} {reason(e)}"
            print(f"    captions {r['captions']}")
        save(rpath, res)
    done = sum(1 for v in q["videos"] if res["videos"].get(v["file"], {}).get("id"))
    res["summary"] = f"{done} of {len(q['videos'])} uploaded"
    save(rpath, res)
    print(res["summary"])
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    cmds = {"manifest": make_manifest, "check": check, "upload": upload, "pending": pending}
    if len(sys.argv) != 3 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]](sys.argv[2])
