"""Batch 07 (Friday run, 2026-11-27): The Crush Files #2 and #3, both Shorts (1080x1920).

Scene prefix cr7_ = scenes_b7_crush.py. Kai and the Crush come from mc.py, the sets from kit3d.py.
  #2 short_b7_blush       - why you blush around your crush (school hallway at golden hour, slow dolly)
  #3 short_b7_butterflies - why your crush gives you butterflies (park bench at dusk, slow orbit)
Neither has a long-form parent: both end on "More Crush Files on the channel." META["end_line"] carries
that pointer for the description; META["parent"] names the sibling Crush Short so meta6-style code works.
"""

# =====================================================================  #2 BLUSH (hallway, golden hour)
BLUSH = [
    dict(key="b1", scene="cr7_hall", lines=["You see your crush, and your face goes red. Here's why."],
         opts=dict(mode="hook", hook="YOUR FACE GOES RED"), sfx=[("pop", "L0+0.3")]),
    dict(key="b2", scene="cr7_hall", lines=[
        "Your fight-or-flight system switches on. Nerves and adrenaline tell the blood vessels in your face to widen."],
         opts=dict(mode="alarm", badge="FIGHT-OR-FLIGHT: ON"), sfx=[("whoosh", 0.0)]),
    dict(key="b3", scene="cr7_hall", lines=[
        "Your cheeks are packed with tiny blood vessels, close to the surface. So the extra blood shows, and your face feels warm."],
         opts=dict(mode="vessels", badge="CLOSE TO THE SURFACE"), sfx=[("whoosh", 0.0)]),
    dict(key="b4", scene="cr7_hall", lines=[
        "And you can't fake a blush, or switch it off. It's automatic.",
        "Like and subscribe for more Crush Files."],
         opts=dict(mode="auto", cta=1, badge="100% AUTOMATIC"), sfx=[("click", "L0+0.5")]),
    dict(key="b5", scene="cr7_hall", lines=[
        "Charles Darwin called blushing the most peculiar and the most human of all expressions."],
         opts=dict(mode="darwin", badge="CHARLES DARWIN, 1872"), sfx=[("whoosh", 0.0)]),
    dict(key="b6", scene="cr7_hall", lines=[
        "And it may even help. In one Dutch study led by Corine Dike, people rated faces after a mistake. Blushing faces were mostly rated more favorably."],
         opts=dict(mode="study", badge="ONE STUDY: IT MAY HELP"), sfx=[("pop", "L0+0.55")]),
    dict(key="b7", scene="cr7_hall", lines=["So that red face? It's just your body being honest. More Crush Files on the channel."], hold=1.3,
         opts=dict(mode="end"), sfx=[("pop", "L0+0.6")]),
]

# =====================================================================  #3 BUTTERFLIES (park, dusk)
FLY = [
    dict(key="f1", scene="cr7_park", lines=["Your crush walks in, and your stomach flips. Here's what's really going on."],
         opts=dict(mode="hook", hook="YOUR STOMACH FLIPS"), sfx=[("pop", "L0+0.2")]),
    dict(key="f2", scene="cr7_park", lines=[
        "Your brain flags this moment as a very big deal, and flips on fight-or-flight. Adrenaline floods your body."],
         opts=dict(mode="alarm", badge="ADRENALINE RUSH"), sfx=[("whoosh", 0.0)]),
    dict(key="f3", scene="cr7_park", lines=[
        "Your heart speeds up. Blood rushes to your muscles, and away from your gut. Digestion slows right down."],
         opts=dict(mode="blood", badge="BLOOD → MUSCLES, NOT GUT"), sfx=[("whoosh", 0.0)]),
    dict(key="f4", scene="cr7_park", lines=[
        "Here's the twist. Your gut has its own nervous system, with two hundred to six hundred million nerve cells. Some scientists call it the second brain."],
         opts=dict(mode="gut", badge="THE SECOND BRAIN"), sfx=[("pop", "L0+0.45")]),
    dict(key="f5", scene="cr7_park", lines=[
        "Like and subscribe for more Crush Files.",
        "And the vagus nerve, your gut-brain hotline, mostly carries messages up. Eight or nine of every ten fibers report to your brain."],
         opts=dict(mode="hotline", cta=0, badge="THE GUT–BRAIN HOTLINE"), sfx=[("whoosh", 0.0)]),
    dict(key="f6", scene="cr7_park", lines=[
        "So when blood leaves your gut, its nerves notice. Scientists think that's the flutter you feel."],
         opts=dict(mode="flutter", badge="THAT'S THE FLUTTER"), sfx=[("whoosh", 0.0)]),
    dict(key="f7", scene="cr7_park", lines=["No real butterflies. Just your whole body saying: this matters. More Crush Files on the channel."], hold=1.3,
         opts=dict(mode="end"), sfx=[("pop", "L0+0.55")]),
]

VIDEOS = {"short_b7_blush": BLUSH, "short_b7_butterflies": FLY}
CHAPTERS = {}
MUSIC = {"short_b7_blush": "crush_blush_s", "short_b7_butterflies": "crush_dusk_s"}
TTS_MAP = {
    "Corine Dike": "Corine Dijk",
    "two hundred to six hundred million": "200 to 600 million",
}
META = {
    "short_b7_blush": dict(
        title="Why You Blush Around Your Crush #shorts",
        hook=("You see your crush and your face goes red. Here's the science: your fight-or-flight system widens the blood vessels "
              "in your face, your cheeks are packed with vessels close to the surface, and one study suggests a blush may even help."),
        tags=["shorts", "crush", "the crush files", "blushing", "why do we blush", "fight or flight", "adrenaline",
              "Charles Darwin", "body science", "psychology", "science", "what if"],
        hashtags="#shorts #crush #science", parent="short_b7_butterflies",
        end_line="The Crush Files: real science of crushes, every Friday. More Crush Files on the channel."),
    "short_b7_butterflies": dict(
        title="Why Your Crush Gives You Butterflies #shorts",
        hook=("Your crush walks in and your stomach flips. Here's the science: adrenaline sends blood away from your gut, your gut has "
              "its own nervous system of 200 to 600 million nerve cells, and the vagus nerve mostly carries messages up to your brain."),
        tags=["shorts", "crush", "the crush files", "butterflies in stomach", "gut brain axis", "second brain",
              "enteric nervous system", "vagus nerve", "adrenaline", "body science", "science", "what if"],
        hashtags="#shorts #crush #science", parent="short_b7_blush",
        end_line="The Crush Files: real science of crushes, every Friday. More Crush Files on the channel."),
}
