"""Batch 05: titles, tags, descriptions, upload sheet and the scripts doc."""
import json, sys, re, os
sys.path.insert(0, "/home/claude/proj")
import narration_b5_moon as NM, narration_b5_ice as NI, narration_b5_microbes as NX, meta2
VIDEOS = {**NM.VIDEOS, **NI.VIDEOS, **NX.VIDEOS}
REPO = "/home/claude/yt-whatif"
OUT = "/home/claude/out/b5"
TOPIC = {"moon": "moon", "drift": "moon", "pluto": "moon", "ice": "ice", "vostok": "ice", "rain": "ice", "microbes": "microbes", "cells": "microbes"}
TITLES = {
 "b5_moon": "What If the Moon Disappeared?",
 "b5_ice": "What If All the Ice on Earth Melted?",
 "b5_microbes": "What If All Your Bacteria Suddenly Vanished?",
 "short_b5_moon": "What If the Moon Vanished Tonight? #shorts",
 "short_b5_drift": "The Moon Is Slowly Leaving Us #shorts",
 "short_b5_pluto": "What If Pluto Replaced Our Moon? #shorts",
 "short_b5_ice": "What If Earth's Ice All Melted Tomorrow? #shorts",
 "short_b5_vostok": "A Lake Hidden Under 4 km of Antarctic Ice #shorts",
 "short_b5_rain": "It Rained for 2 Million Years #shorts",
 "short_b5_microbes": "All Your Bacteria Vanish Overnight #shorts",
 "short_b5_cells": "You're About Half Bacteria #shorts",
}
HOOKS = {
 "b5_moon": "The Moon vanishes at midnight. Here's what changes, from the first dark night and shrinking tides to lost animal rhythms, no more eclipses and a wobblier Earth, and why the Moon is slowly leaving anyway.",
 "b5_ice": "Melt every glacier and ice sheet on Earth and the seas rise about 70 meters. Which coasts vanish, why Antarctica turns into islands, and why the sea right next to Greenland would actually fall.",
 "b5_microbes": "About 38 trillion bacteria live in and on you, more than your own cells. At midnight they all vanish. Here's your body after one day, one week, one month and years, and why you could never stay sterile.",
 "short_b5_moon": "No Moon tonight: darker nights, weaker tides, confused corals and no more eclipses.",
 "short_b5_drift": "Lasers bounced off mirrors left by Apollo astronauts show the Moon drifting about 3.8 cm a year. That's making our days longer and will one day end total solar eclipses.",
 "short_b5_pluto": "Swap the Moon for Pluto: a smaller but brighter icy disc, tides weaker than the Sun's, and ice turning to gas.",
 "short_b5_ice": "Antarctica alone holds about 58 meters of sea level. And the strangest part: next to Greenland, the sea would drop.",
 "short_b5_vostok": "A lake about the size of Lake Ontario lies under almost 4 km of Antarctic ice, possibly sealed off for millions of years. Could anything live down there?",
 "short_b5_rain": "About 234 million years ago Earth's climate turned wet, on and off, for up to 2 million years. And dinosaurs may have taken over because of it.",
 "short_b5_microbes": "Lose all 38 trillion of your bacteria (about 200 g) and your colon cells run low on fuel. Germ-free mice grow a giant cecum. And you'd be recolonized almost immediately.",
 "short_b5_cells": "The famous \"10 bacteria for every human cell\" came from a 1972 back-of-the-envelope estimate. The 2016 recount: about 38 trillion vs 30 trillion. One trip to the toilet can tip the balance.",
}
TAGS = {
 "b5_moon": ["what if", "moon", "what if the moon disappeared", "tides", "eclipse", "earth tilt", "lunar laser ranging", "space", "science"],
 "b5_ice": ["what if", "ice melted", "sea level rise", "Antarctica", "Greenland", "glaciers", "climate", "earth science", "science"],
 "b5_microbes": ["what if", "microbiome", "gut bacteria", "human body", "germ-free mice", "bacteria", "biology", "science"],
 "short_b5_moon": ["shorts", "what if", "moon", "tides", "coral spawning", "eclipse", "space"],
 "short_b5_drift": ["shorts", "moon drifting away", "lunar laser ranging", "apollo", "length of day", "eclipse", "space"],
 "short_b5_pluto": ["shorts", "what if", "pluto", "moon", "charon", "tides", "dwarf planet", "space"],
 "short_b5_ice": ["shorts", "what if", "ice melt", "sea level", "Antarctica", "Greenland", "earth science"],
 "short_b5_vostok": ["shorts", "Lake Vostok", "Antarctica", "subglacial lakes", "extremophiles", "microbes", "science"],
 "short_b5_rain": ["shorts", "Carnian Pluvial Episode", "Triassic", "dinosaurs", "mass extinction", "volcanoes", "paleontology"],
 "short_b5_microbes": ["shorts", "what if", "microbiome", "gut bacteria", "human body", "science"],
 "short_b5_cells": ["shorts", "bacteria", "microbiome", "myth busting", "human cells", "science facts"],
}
HASH = {"moon": "#whatif #science #space", "ice": "#whatif #science #earth", "microbes": "#whatif #science #humanbody"}
SHORT_PARENT = {"short_b5_moon": "b5_moon", "short_b5_drift": "b5_moon", "short_b5_pluto": "b5_moon",
                "short_b5_ice": "b5_ice", "short_b5_vostok": "b5_ice", "short_b5_rain": "b5_ice",
                "short_b5_microbes": "b5_microbes", "short_b5_cells": "b5_microbes"}
ORDER = ["b5_moon", "b5_ice", "b5_microbes", "short_b5_moon", "short_b5_drift", "short_b5_pluto",
         "short_b5_ice", "short_b5_vostok", "short_b5_rain", "short_b5_microbes", "short_b5_cells"]
CLAIMS = {"moon": "_b5_moon_claims.md", "ice": "_b5_ice_claims.md", "microbes": "_b5_microbes_claims.md"}

def topic(name): return TOPIC[name.split("_")[-1]]

def claims():
    out, cur = {}, None
    for fn in CLAIMS.values():
        for ln in open(f"{REPO}/scripts/{fn}"):
            if ln.startswith("@@"): cur = ln[2:].strip(); out[cur] = []; continue
            if cur: out[cur].append(ln.rstrip("\n"))
    return {k: "\n".join(v).strip() for k, v in out.items()}

def sources(name):
    C = claims(); urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", C.get(name, ""))
    if len(urls) < 2 and name in SHORT_PARENT:
        urls += re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", C[SHORT_PARENT[name]])[:6]
    seen, res = set(), []
    for t, u in urls:
        if u not in seen: seen.add(u); res.append(f"- {t}: {u}")
    return res

def description(name):
    parts = [HOOKS[name], ""]
    if not name.startswith("short"):
        ch, _ = meta2.chapters(name); parts += ["⏱️ Chapters", ch, ""]
    else:
        parts += [f"Full story: \"{TITLES[SHORT_PARENT[name]]}\" on the channel.", ""]
    src = sources(name)
    tail = ["", "Narration uses an AI voice. Animation and music are original.", "",
            HASH[topic(name)] + (" #shorts" if name.startswith("short") else "")]
    while True:
        d = "\n".join(parts + ["📚 Sources"] + src + tail)
        if (len(d) <= 4800 and len(d.encode()) <= 4900) or len(src) <= 3: return d
        src = src[:-1]

def script_doc():
    C = claims(); L = ["# Scripts — Batch 05 (2026-11-20)", "",
         "Three topics (Moon disappears, all ice melts, all your bacteria vanish): each long-form + teaser Short + standalone Short, plus two extra standalone Shorts (Pluto as our Moon → Moon long-form; the 2-million-year rain → ice long-form). 11 scripts.",
         "Narration text below is what the voice reads (TTS spellings mapped back for readability). Fact-checked; claim → source table under each script. The like-and-subscribe line is marked ★.", ""]
    for name in ORDER:
        words = sum(len(l.split()) for sc in VIDEOS[name] for l in sc["lines"])
        try: dur = json.load(open(f"/home/claude/proj/build/{name}/timeline.json"))["total"]
        except Exception: dur = 0
        L += [f"## {TITLES[name]}", f"`{name}` · {words} words (incl. like/subscribe line) · {int(dur // 60)}:{int(dur % 60):02d}", ""]
        for sc in VIDEOS[name]:
            o = sc.get("opts", {})
            if sc["scene"].endswith("_card"): L += [f"**[TITLE CARD: {o.get('text', '')}]**", ""]; continue
            if sc["scene"].endswith("_title"): L += [f"**[TITLE: {o.get('l1', '')} {o.get('l2', '')}]**", ""]; continue
            lines = [meta2.tts_to_text(x) for x in sc["lines"]]
            if "cta" in o: lines[o["cta"]] = "★ " + lines[o["cta"]]
            L += [f"*[{sc['key']} · scene {sc['scene']}]*"] + lines + [""]
        L += ["**Claim → source**", "", C.get(name, ""), "", "---", ""]
    return "\n".join(L)

def upload_sheet():
    L = ["UPLOAD SHEET — Batch 05, 2026-11-20", "Privacy: Unlisted (switch to Public after processing). Category: Science & Technology. Not made for kids.",
         "Altered/synthetic content: No (animated, AI narrator disclosed in description).", ""]
    for i, n in enumerate(ORDER, 1):
        L += ["=" * 70, f"{i}. {TITLES[n]}", f"File: {n}.mp4   Type: {'Short' if n.startswith('short') else 'Long-form'}",
              f"Thumbnail: {'thumbnail_' + n.split('_')[1] + '.png' if not n.startswith('short') else '-'}   Captions: {n}.srt",
              "Tags: " + ", ".join(TAGS[n]), "", "Description:", description(n), ""]
    return "\n".join(L)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k in ORDER: assert len(TITLES[k]) <= (60 if not k.startswith("short") else 100), k
    open(f"{REPO}/scripts/2026-11-20-batch-05.md", "w").write(script_doc())
    json.dump({k: dict(title=TITLES[k], description=description(k), tags=TAGS[k]) for k in ORDER}, open(f"{OUT}/meta.json", "w"), indent=1, ensure_ascii=False)
    open(f"{OUT}/upload_sheet_batch05.txt", "w").write(upload_sheet())
    for k in ORDER: print(k, len(description(k)), len(sources(k)))
    print(description("b5_moon")); print(); print(description("short_b5_pluto"))
