"""Batch 06 HAPPENING-NOW Shorts: ESA's Hera at Dimorphos, and supernova SN 2026ahvu.

Scene prefix nw6_ (scenes_b6_now.py). Both Shorts point to the space long-form b6_mercury.
TTS spellings are mapped back for captions through TTS_MAP (read by meta2.tts_to_text).
"""

# =====================================================================  HERA AT DIMORPHOS
S1 = [
    dict(key="h1", scene="nw6_hera", lines=["We crashed a spacecraft into an asteroid. Now we're checking the damage."],
         opts=dict(mode="intro", hook="WE HIT AN ASTEROID")),
    dict(key="h2", scene="nw6_hera", lines=["In twenty twenty-two, NASA's DART probe hit Dye-mor-fuss, a little asteroid moon, on purpose."],
         opts=dict(mode="dart", badge="SEPTEMBER 2022"), sfx=[("whoosh", "L0+0.55")]),
    dict(key="h3", scene="nw6_hera", lines=["It worked. Its orbit around its bigger partner got about thirty-two minutes shorter."],
         opts=dict(mode="orbit", badge="ORBIT: −32 MINUTES")),
    dict(key="h4", scene="nw6_hera", lines=["This month, Europe's Hera spacecraft arrived at the crime scene."],
         opts=dict(mode="arrive", badge="NOVEMBER 2026")),
    dict(key="h5", scene="nw6_hera", lines=["Gravity here is two hundred thousand times weaker than Earth's. Hera creeps along at twelve centimeters a second."],
         opts=dict(mode="gravity", badge="12 CM PER SECOND")),
    dict(key="h6", scene="nw6_hera", lines=["Like and subscribe for more space news.",
                                            "Hera will weigh Dye-mor-fuss, and see if DART left a crater, or reshaped the whole asteroid."],
         opts=dict(mode="job", cta=0)),
    dict(key="h7", scene="nw6_hera", lines=["Two shoebox-sized cube sats will fly closer. One carries radar to see inside."],
         opts=dict(mode="cubesat", badge="RADAR INSIDE AN ASTEROID")),
    dict(key="h8", scene="nw6_hera", lines=["Still unknown: what the crash site looks like. First close-ups are due November twenty-fifth."],
         opts=dict(mode="unknown", badge="STILL UNKNOWN")),
    dict(key="h9", scene="nw6_hera", lines=["It's practice for the day a real asteroid heads our way."],
         opts=dict(mode="playbook", badge="PLANETARY DEFENSE")),
    dict(key="h10", scene="nw6_endshort", lines=["Now, what if you lived on Mercury? Full story on the channel."],
         hold=1.0, opts=dict(top="LIVE ON MERCURY?")),
]

# =====================================================================  SUPERNOVA SN 2026ahvu
S2 = [
    dict(key="s1", scene="nw6_sn", lines=["A star just exploded, and you can see it with a backyard telescope."],
         opts=dict(mode="intro", hook="A STAR JUST EXPLODED")),
    dict(key="s2", scene="nw6_sn", lines=["On November second, the ATLAS sky survey spotted it in the galaxy N-G-C fourteen thirty-three."],
         opts=dict(mode="find", badge="FOUND: 2 NOVEMBER 2026")),
    dict(key="s3", scene="nw6_sn", lines=["It's a Type one A supernova: a dead star, a white dwarf, blowing itself apart."],
         opts=dict(mode="wd", badge="TYPE Ia SUPERNOVA"), sfx=[("rumble", "L0+0.6")]),
    dict(key="s4", scene="nw6_sn", lines=["Around now it should be near its peak, visible from the southern sky."],
         opts=dict(mode="peak", badge="PEAK: 18–23 NOVEMBER")),
    dict(key="s5", scene="nw6_sn", lines=["These blasts peak at similar brightness, so astronomers use them to measure the expanding universe."],
         opts=dict(mode="candle", badge="STANDARD CANDLES")),
    dict(key="s6", scene="nw6_sn", lines=["Like and subscribe for more sky news.",
                                          "So what if one went off near Earth? NASA says it would need to be within about fifty light-years to damage our ozone layer."],
         opts=dict(mode="near", cta=0)),
    dict(key="s7", scene="nw6_sn", lines=["The closest known candidate for this kind of blast is about a hundred and fifty light-years away."],
         opts=dict(mode="nearest", badge="≈150 LIGHT-YEARS AWAY")),
    dict(key="s8", scene="nw6_sn", lines=["Still unknown: this one's distance. Estimates range from thirty to sixty million light-years."],
         opts=dict(mode="unknown", badge="STILL UNKNOWN")),
    dict(key="s9", scene="nw6_endshort", lines=["Closer to home: what if you lived on Mercury? Full story on the channel."],
         hold=1.4, opts=dict(top="LIVE ON MERCURY?", look="n")),
]

VIDEOS = {"short_b6_dimorphos": S1, "short_b6_supernova": S2}
CHAPTERS = {}
MUSIC = {"short_b6_dimorphos": "deep_s", "short_b6_supernova": "deep_s"}
TTS_MAP = {
    "Dye-mor-fuss": "Dimorphos",
    "Did-ih-mos": "Didymos",
    "cube sats": "CubeSats",
    "N-G-C fourteen thirty-three": "NGC 1433",
    "Type one A": "Type Ia",
    "six point one kilometers per second": "6.1 kilometers per second",
    "November twenty-fifth": "November 25",
    "November second": "November 2",
}
META = {
    "short_b6_dimorphos": dict(
        title="We Hit an Asteroid. Now We're Checking the Damage #shorts",
        hook=("In November 2026, ESA's Hera spacecraft arrived at the asteroid pair Didymos and Dimorphos, the target NASA's DART probe hit "
              "on purpose on 26 September 2022. Here's what Hera is measuring, and what we still don't know."),
        tags=["Hera", "ESA", "DART", "Dimorphos", "Didymos", "asteroid", "planetary defense", "asteroid deflection", "space news", "what if", "science", "shorts"],
        hashtags="#whatif #science #space", parent="b6_mercury"),
    "short_b6_supernova": dict(
        title="A Star Just Exploded. What If One Went Off Near Us? #shorts",
        hook=("On 2 November 2026, the ATLAS survey discovered SN 2026ahvu, a Type Ia supernova in the galaxy NGC 1433, expected to peak "
              "around 18–23 November. So how close would a supernova have to be to hurt Earth?"),
        tags=["supernova", "SN 2026ahvu", "NGC 1433", "Type Ia supernova", "white dwarf", "ATLAS", "astronomy", "space news", "what if", "science", "shorts"],
        hashtags="#whatif #science #space", parent="b6_mercury"),
}
