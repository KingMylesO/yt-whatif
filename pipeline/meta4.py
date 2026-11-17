"""Batch 04 (tech): titles, tags, descriptions, upload sheet and the scripts doc."""
import json, sys, re
sys.path.insert(0, "/home/claude/proj")
import narration_b4 as N, meta2
REPO = "/home/claude/yt-whatif"
OUT = "/home/claude/out/b4"
TITLES = {
 "b4_tubes": "What If the Transistor Was Never Invented?",
 "b4_shrink": "What If You Shrank Down Inside a Computer Chip?",
 "b4_cosmic": "What If a Cosmic Ray Flipped a Bit in Your Computer?",
 "short_b4_tubes": "What If Your Phone Ran on Vacuum Tubes? #shorts",
 "short_b4_moth": "The First Computer Bug Was a Real Moth #shorts",
 "short_b4_blackout": "What If Every Chip on Earth Stopped at Once? #shorts",
 "short_b4_shrink": "What If You Shrank Inside a Computer Chip? #shorts",
 "short_b4_euv": "Your Chips Are Printed With Exploding Tin #shorts",
 "short_b4_moore": "What If Moore's Law Never Slowed Down? #shorts",
 "short_b4_cosmic": "What If a Cosmic Ray Hit Your Computer? #shorts",
 "short_b4_vote": "The Election Glitch That Added 4,096 Votes #shorts",
}
HOOKS = {
 "b4_tubes": "Your phone's chip holds about 19 billion transistors. Rebuild it with vacuum tubes and you'd need around 160 gigawatts and 150 Olympic pools of glass. So what would a world without the transistor look like? And why was it almost invented 22 years early?",
 "b4_shrink": "Shrink down and walk inside a laptop chip: a package like a building, a city of copper highways 15 levels deep, transistor fins like slices of bread, and walls only five atoms thick. Plus the reason a \"3 nm\" chip has nothing 3 nm wide.",
 "b4_cosmic": "In 2003 a Belgian voting machine gave a candidate exactly 4,096 extra votes, and the leading explanation is a single bit flipped by a particle from space. Here's how cosmic rays flip bits, what has really happened, and how your computer fights back.",
 "short_b4_tubes": "A phone chip rebuilt with vacuum tubes would need about 160 gigawatts.",
 "short_b4_moth": "September 9, 1947: a moth in relay #70 of the Harvard Mark II. But \"bug\" is older than the moth.",
 "short_b4_blackout": "Every chip on Earth switches off at once. What stops, and what still works?",
 "short_b4_shrink": "Copper highways, 92 billion transistors, and walls so thin electrons tunnel through.",
 "short_b4_euv": "Chips are printed with 13.5 nm light from laser-blasted tin droplets.",
 "short_b4_moore": "Clock speeds stalled near 4 GHz. Here's why Moore's law hit heat and atoms.",
 "short_b4_cosmic": "Particles from space pass through your phone every minute. Sometimes one flips a bit.",
 "short_b4_vote": "4,096 is 2 to the 12th power. That number is the clue that points to a single flipped bit.",
}
BASE = ["what if", "technology", "science", "computer hardware"]
TAGS = {
 "b4_tubes": BASE + ["transistor", "vacuum tube", "ENIAC", "Bell Labs", "history of computing", "MOSFET", "semiconductors"],
 "b4_shrink": BASE + ["microchip", "transistor", "semiconductor", "3nm", "EUV lithography", "quantum tunneling", "CPU"],
 "b4_cosmic": BASE + ["cosmic rays", "bit flip", "soft error", "single event upset", "ECC memory", "Voyager 2", "computer memory"],
}
for k in TITLES:
    if k.startswith("short"):
        TAGS[k] = ["shorts"] + BASE + {"tubes": ["vacuum tube", "transistor"], "moth": ["computer bug", "Harvard Mark II", "Grace Hopper"],
            "blackout": ["microchips", "chip shortage"], "shrink": ["microchip", "transistor"], "euv": ["EUV lithography", "semiconductors"],
            "moore": ["Moore's law", "CPU"], "cosmic": ["cosmic rays", "bit flip"], "vote": ["bit flip", "cosmic rays", "election"]}[k.split("_")[-1]]
SHORT_PARENT = {"short_b4_tubes": "b4_tubes", "short_b4_moth": "b4_tubes", "short_b4_blackout": "b4_tubes",
                "short_b4_shrink": "b4_shrink", "short_b4_euv": "b4_shrink", "short_b4_moore": "b4_shrink",
                "short_b4_cosmic": "b4_cosmic", "short_b4_vote": "b4_cosmic"}
ORDER = ["b4_tubes", "b4_shrink", "b4_cosmic", "short_b4_tubes", "short_b4_moth", "short_b4_blackout",
         "short_b4_shrink", "short_b4_euv", "short_b4_moore", "short_b4_cosmic", "short_b4_vote"]

def claims():
    out, cur = {}, None
    for ln in open(f"{REPO}/scripts/_b4_claims.md"):
        if ln.startswith("@@"): cur = ln[2:].strip(); out[cur] = []; continue
        if cur: out[cur].append(ln.rstrip("\n"))
    return {k: "\n".join(v).strip() for k, v in out.items()}

def sources(name):
    c = claims()[name]
    urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", c)
    if not urls: c = claims()[SHORT_PARENT[name]]; urls = re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", c)[:6]
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
            "#whatif #technology #science" + (" #shorts" if name.startswith("short") else "")]
    while True:
        d = "\n".join(parts + ["📚 Sources"] + src + tail)
        if len(d) <= 4800 or len(src) <= 3: return d
        src = src[:-1]

def script_doc():
    C = claims(); L = ["# Scripts — Batch 04 (2026-11-17, one-off tech batch)", "",
         "Three topics: each long-form + teaser Short + standalone Short, plus two extra standalone Shorts (11 scripts).",
         "Narration text below is what the voice reads (TTS spellings mapped back for readability). Fact-checked; claim → source table under each script.", ""]
    for name in ORDER:
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

def upload_sheet():
    L = ["UPLOAD SHEET — Batch 04 (tech), 2026-11-17", "Privacy: Unlisted (switch to Public after processing). Category: Science & Technology. Not made for kids.",
         "Altered/synthetic content: No (animated, AI narrator disclosed in description).", ""]
    for i, n in enumerate(ORDER, 1):
        L += ["=" * 70, f"{i}. {TITLES[n]}", f"File: {n}.mp4   Type: {'Short' if n.startswith('short') else 'Long-form'}",
              f"Thumbnail: {'thumbnail_' + n.split('_')[1] + '.png' if not n.startswith('short') else '-'}   Captions: {n}.srt",
              "Tags: " + ", ".join(TAGS[n]), "", "Description:", description(n), ""]
    return "\n".join(L)

if __name__ == "__main__":
    import os; os.makedirs(OUT, exist_ok=True)
    open(f"{REPO}/scripts/2026-11-17-batch-04.md", "w").write(script_doc())
    json.dump({k: dict(title=TITLES[k], description=description(k), tags=TAGS[k]) for k in ORDER}, open(f"{OUT}/meta.json", "w"), indent=1, ensure_ascii=False)
    open(f"{OUT}/upload_sheet_batch04.txt", "w").write(upload_sheet())
    for k in ORDER: assert len(TITLES[k]) <= 60 if not k.startswith("short") else len(TITLES[k]) <= 100, k
    print(description("b4_tubes")); print(); print(description("short_b4_vote"))
