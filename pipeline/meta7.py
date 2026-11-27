"""Batch 07: titles, tags, descriptions (meta.json), upload sheet and the scripts doc, from each narration module's META."""
import json, sys, re, os
sys.path.insert(0, "/home/claude/proj")
import narration_b7_moons as NM, narration_b7_volcano as NV, narration_b7_crush as NC, meta2
MODS = [NM, NV, NC]
VIDEOS = {k: v for M in MODS for k, v in M.VIDEOS.items()}
META = {k: v for M in MODS for k, v in M.META.items()}
REPO = "/home/claude/yt-whatif"
OUT = "/home/claude/out/b7"
DATE = "2026-11-27"
ORDER = ["b7_moons", "b7_volcano", "short_b7_moons", "short_b7_moonmoon", "short_b7_uranus",
         "short_b7_volcano", "short_b7_iwojima", "short_b7_nodule", "short_b7_blush", "short_b7_butterflies"]
CLAIMS = ["_b7_moons_claims.md", "_b7_volcano_claims.md", "_b7_crush_claims.md"]

def claims():
    out, cur = {}, None
    for fn in CLAIMS:
        for ln in open(f"{REPO}/scripts/{fn}"):
            if ln.startswith("@@"): cur = ln[2:].strip(); out[cur] = []; continue
            if cur: out[cur].append(ln.rstrip("\n"))
    return {k: "\n".join(v).strip() for k, v in out.items()}

def sources(name):
    C = claims(); urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", C.get(name, ""))
    seen, res = set(), []
    for t, u in urls:
        if u not in seen: seen.add(u); res.append(f"- {t}: {u}")
    return res

def description(name):
    m = META[name]; parts = [m["hook"], ""]
    if not name.startswith("short"):
        ch, _ = meta2.chapters(name); parts += ["⏱️ Chapters", ch, ""]
    else:
        parts += [m.get("end_line") or f"Full story: \"{META[m['parent']]['title']}\" on the channel.", ""]
    src = sources(name)
    tail = ["", "Narration uses an AI voice. Animation and music are original.", "",
            m["hashtags"] + (" #shorts" if name.startswith("short") and "#shorts" not in m["hashtags"] else "")]
    while True:
        d = "\n".join(parts + ["📚 Sources"] + src + tail)
        if (len(d) <= 4800 and len(d.encode()) <= 4900) or len(src) <= 3: return d.replace("<", "‹").replace(">", "›")
        src = src[:-1]

def script_doc():
    C = claims(); L = [f"# Scripts — Batch 07 ({DATE})", "",
         "Two long-forms (two moons, hooked to the mini-moon 2026 QQ8; every volcano at once, hooked to the October–November 2026 Iwo Jima eruption), each with a teaser and a standalone Short, plus two happening-now Shorts (Uranus at opposition on 25 Nov 2026; 245 animals inside one deep-sea nodule) and The Crush Files #2 and #3 (Friday run). 10 scripts.",
         "Narration text below is what the voice reads (TTS spellings mapped back for readability). Fact-checked; claim → source table under each script. The like-and-subscribe line is marked ★.", ""]
    for name in ORDER:
        words = sum(len(l.split()) for sc in VIDEOS[name] for l in sc["lines"])
        try: dur = json.load(open(f"/home/claude/proj/build/{name}/timeline.json"))["total"]
        except Exception: dur = 0
        L += [f"## {META[name]['title']}", f"`{name}` · {words} words (incl. like/subscribe line) · {int(dur // 60)}:{int(dur % 60):02d}", ""]
        for sc in VIDEOS[name]:
            o = sc.get("opts", {})
            if not sc["lines"]:
                txt = " ".join(str(o[k]) for k in ("text", "l1", "l2") if k in o)
                if txt: L += [f"**[CARD: {txt}]**", ""]
                continue
            lines = [meta2.tts_to_text(x) for x in sc["lines"]]
            if "cta" in o: lines[o["cta"]] = "★ " + lines[o["cta"]]
            L += [f"*[{sc['key']} · scene {sc['scene']}]*"] + lines + [""]
        L += ["**Claim → source**", "", C.get(name, ""), "", "---", ""]
    return "\n".join(L)

def upload_sheet():
    L = [f"UPLOAD SHEET — Batch 07, {DATE}", "Privacy: Unlisted (switch to Public after processing). Category: Science & Technology. Not made for kids.",
         "Altered/synthetic content: No (animated, AI narrator disclosed in description).", ""]
    for i, n in enumerate(ORDER, 1):
        L += ["=" * 70, f"{i}. {META[n]['title']}", f"File: {n}.mp4   Type: {'Short' if n.startswith('short') else 'Long-form'}",
              f"Thumbnail: {'thumbnail_' + n.split('_')[1] + '.png' if not n.startswith('short') else '-'}   Captions: {n}.srt",
              "Tags: " + ", ".join(META[n]["tags"]), "", "Description:", description(n), ""]
    return "\n".join(L)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k in ORDER: assert len(META[k]["title"]) <= (60 if not k.startswith("short") else 100), k
    open(f"{REPO}/scripts/{DATE}-batch-07.md", "w").write(script_doc())
    json.dump({k: dict(title=META[k]["title"], description=description(k), tags=META[k]["tags"]) for k in ORDER},
              open(f"{OUT}/meta.json", "w"), indent=1, ensure_ascii=False)
    open(f"{OUT}/upload_sheet_batch07.txt", "w").write(upload_sheet())
    for k in ORDER: print(k, len(description(k).encode()), len(sources(k)), sum(len(t) for t in META[k]["tags"]))
