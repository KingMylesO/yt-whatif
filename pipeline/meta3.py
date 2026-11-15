"""Batch 03: titles, tags, descriptions, and the scripts doc."""
import json, sys, re
sys.path.insert(0, "/home/claude/proj")
import narration_b3 as N, meta2
TITLES = {
 "b3_rings": "What If Earth Had Rings Like Saturn?",
 "b3_magnet": "What If Earth's Magnetic Field Switched Off?",
 "b3_photo": "What If Humans Could Photosynthesize?",
 "short_b3_rings": "What If Earth Had Rings? #shorts",
 "short_b3_saturn": "Saturn Is Losing Its Rings #shorts",
 "short_b3_magnet": "What If Earth's Shield Switched Off? #shorts",
 "short_b3_flip": "What If the Magnetic Poles Flipped Tomorrow? #shorts",
 "short_b3_clouds": "What If There Were No Clouds for a Week? #shorts",
 "short_b3_photo": "What If Your Skin Could Eat Sunlight? #shorts",
 "short_b3_slug": "This Sea Slug Runs on Stolen Sunlight #shorts",
 "short_b3_mantis": "What If You Had a Mantis Shrimp's Eyes? #shorts",
}
HOOKS = {
 "b3_rings": "Picture Saturn-style rings around Earth: a glowing arch that never sets, shadows that deepen winter, and a sky astronomers would hate. Then the twist: Earth may really have had a ring 466 million years ago.",
 "b3_magnet": "What happens if Earth's invisible magnetic shield switches off? Compasses die, satellites get hammered and the ozone layer suffers, but the real surprise is what protects you on the ground.",
 "b3_photo": "What if your skin could make food from sunlight like a leaf? We do the math (spoiler: about a cracker a day), then meet the animals that actually pull it off.",
 "short_b3_rings": "Earth with rings like Saturn: a line overhead, a permanent arch, ringshine at night, and a real ring 466 million years ago?",
 "short_b3_saturn": "Saturn's rings are raining into the planet. They may be gone in under 100 million years.",
 "short_b3_magnet": "Switch off Earth's magnetic shield and here's what changes.",
 "short_b3_flip": "Earth's magnetic poles have flipped 183 times in 83 million years. What if it started tomorrow?",
 "short_b3_clouds": "A week with zero clouds: no rain, hotter days and colder nights.",
 "short_b3_photo": "Photosynthetic skin: the math says about a cracker a day.",
 "short_b3_slug": "Elysia chlorotica keeps stolen chloroplasts alive inside its own cells.",
 "short_b3_mantis": "12 colour receptors, polarized vision, and a surprising weakness.",
}
TAGS = {
 "b3_rings": ["what if", "Earth rings", "Saturn rings", "Roche limit", "space", "science", "Ordovician ring", "planetary rings"],
 "b3_magnet": ["what if", "magnetic field", "magnetosphere", "solar wind", "space weather", "Laschamp", "science", "Earth"],
 "b3_photo": ["what if", "photosynthesis", "human body", "biology", "sea slug", "coral", "science", "green skin"],
}
for k in TITLES:
    if k.startswith("short"):
        TAGS[k] = ["shorts", "what if", "science"] + {"rings": ["Earth rings"], "saturn": ["Saturn", "ring rain"], "magnet": ["magnetic field"],
            "flip": ["pole reversal", "magnetic field"], "clouds": ["clouds", "weather"], "photo": ["photosynthesis"],
            "slug": ["sea slug", "Elysia chlorotica"], "mantis": ["mantis shrimp", "vision"]}[k.split("_")[-1]]
SHORT_PARENT = {"short_b3_rings": "b3_rings", "short_b3_saturn": "b3_rings", "short_b3_magnet": "b3_magnet", "short_b3_flip": "b3_magnet",
                "short_b3_clouds": "b3_magnet", "short_b3_photo": "b3_photo", "short_b3_slug": "b3_photo", "short_b3_mantis": "b3_photo"}

def claims():
    out, cur = {}, None
    for ln in open("/home/claude/yt-whatif/scripts/_b3_claims.md"):
        if ln.startswith("@@"): cur = ln[2:].strip(); out[cur] = []; continue
        if cur: out[cur].append(ln.rstrip("\n"))
    return {k: "\n".join(v).strip() for k, v in out.items()}

def sources(name):
    c = claims()[name]
    urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", c)
    if not urls: c = claims()[SHORT_PARENT[name]]; urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", c)
    seen, res = set(), []
    for t, u in urls:
        if u not in seen: seen.add(u); res.append(f"- {t}: {u}")
    return res

def description(name):
    tags = "#whatif #science " + ("#space" if "rings" in name or "saturn" in name else "#earth" if any(x in name for x in ("magnet", "flip", "clouds")) else "#biology")
    parts = [HOOKS[name], ""]
    if not name.startswith("short"):
        ch, _ = meta2.chapters(name); parts += ["⏱️ Chapters", ch, ""]
    else:
        parts += [f"Full story: \"{TITLES[SHORT_PARENT[name]]}\" on the channel.", ""]
    src = sources(name)
    tail = ["", "Narration uses an AI voice. Animation and music are original.", "", tags + (" #shorts" if name.startswith("short") else "")]
    while True:
        d = "\n".join(parts + ["📚 Sources"] + src + tail)
        if len(d) <= 4800 or len(src) <= 3: return d
        src = src[:-1]

def script_doc():
    C = claims(); L = ["# Scripts — Batch 03 (2026-11-15)", "",
         "Three topics: each long-form + teaser Short + standalone Short, plus two extra standalone Shorts (11 scripts).",
         "Narration text below is exactly what the voice reads (numbers mapped back to digits for readability). Fact-checked; claim → source table under each script.", ""]
    for name in N.VIDEOS:
        words = sum(len(l.split()) for sc in N.VIDEOS[name] for l in sc["lines"])
        try: dur = json.load(open(f"/home/claude/proj/build/{name}/timeline.json"))["total"]
        except Exception: dur = 0
        L += [f"## {TITLES[name]}", f"`{name}` · {words} words · {int(dur // 60)}:{int(dur % 60):02d}", ""]
        for sc in N.VIDEOS[name]:
            if sc["scene"].endswith("_card"): L += [f"**[TITLE CARD: {sc['opts']['text']}]**", ""]; continue
            if sc["scene"].endswith("_title"): L += [f"**[TITLE: {sc['opts']['l1']} {sc['opts']['l2']}]**", ""]; continue
            L += [f"*[{sc['key']} · scene {sc['scene']}]*"] + [meta2.tts_to_text(x) for x in sc["lines"]] + [""]
        L += ["**Claim → source**", "", C.get(name, ""), "", "---", ""]
    return "\n".join(L)

if __name__ == "__main__":
    open("/home/claude/yt-whatif/scripts/2026-11-15-batch-03.md", "w").write(script_doc())
    json.dump({k: dict(title=TITLES[k], description=description(k), tags=TAGS[k]) for k in TITLES}, open("/home/claude/out/b3/meta.json", "w"), indent=1, ensure_ascii=False)
    print(description("b3_rings")); print(description("short_b3_slug"))
