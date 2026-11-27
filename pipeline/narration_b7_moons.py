"""Batch 07 SPACE topic (happening now): What If Earth Had Two Moons? (+ teaser, submoon and Uranus-tilt Shorts).

News peg: the IAU Minor Planet Center announced on 29 Oct 2026 (MPEC K26/U95) that the small natural object 2026 QQ8,
first seen on 20 Aug 2026 by Krisztian Sarneczky, has been temporarily bound to Earth since about late April 2026 and
should stay through December. Extra happening-now Short: Uranus at opposition on 25 Nov 2026.
Scene prefix mn7_ = scenes_b7_moons.py. TTS spellings map back to captions through TTS_MAP.
"""
CARD = 1.9

def card(key, text, label="TWO MOONS", scene="mn7_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  LONG-FORM
L1 = [
    dict(key="hook", scene="mn7_hook", lines=[
        "Right now, as you watch this, Earth has two moons.",
        "One is the Moon you know. The other is a tiny rock, caught by Earth's gravity this spring, and it's looping around us as we speak.",
        "So what if that second moon wasn't tiny? What if Earth had two big moons?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="mn7_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF EARTH HAD", l2="TWO MOONS?")),
    dict(key="news", scene="mn7_news", lines=[
        "First, what actually happened. On August twentieth, Hungarian astronomer Kris-tee-ahn Shar-nets-kee spotted a faint, moving dot. At first, it wasn't even clear if it was a rock or a piece of space junk.",
        "Follow-up observations settled it. On October twenty-ninth, the International Astronomical Union's Minor Planet Center announced a natural object, most likely a tiny asteroid. Its name is twenty twenty-six Q-Q-eight.",
        "Tracing its path backwards, astronomers found it had been caught by Earth's gravity back in April. Its path isn't a neat circle. It makes messy loops around us, and never comes closer than about five hundred and sixty-eight thousand kilometers. That's about one and a half times the distance to the Moon.",
        "What's still unknown? Its exact size. Estimates range from about one to two meters across. And its exact exit date. It's expected to stay bound through December, then drift back into its own orbit around the Sun, probably early next year."]),
    dict(key="mini", scene="mn7_mini", lines=[
        "And here's the strange part. This happens all the time.",
        "Small rocks that circle the Sun on paths very like Earth's sometimes drift slowly past us, and get caught for a while. One estimate suggests Earth could have as many as six mini-moons at any given time. Most are just too small to spot.",
        "We've caught a few. Twenty twenty C-D-three looped around us for months before it left. And in twenty twenty-four, a rock called twenty twenty-four P-T-five, about ten meters long, stayed for fifty-seven days.",
        "P-T-five never completed a full loop. But its colours matched samples of Moon rock. It may be a boulder blasted off the Moon long ago, briefly coming home."]),
    card("c0", "THE RULES"),
    dict(key="rules", scene="mn7_rules", lines=[
        "So let's upgrade. Imagine Earth's second moon isn't a boulder. It's a twin of the Moon. Same size, same grey rock, same mass.",
        "We'll put it on a circular orbit at half the Moon's distance, about one hundred and ninety-two thousand kilometers away. We won't worry about how it got there. We'll just watch what happens.",
        "Here's the first surprise. A closer moon has to move faster to stay in orbit. By our rough math, using Kepler's laws, the twin circles Earth in under ten days. That's almost three times faster than the Moon.",
        "And it's close. Light from the twin would reach your eyes in about two thirds of a second. Moonlight takes about one and a quarter."]),
    card("c1", "THE FIRST NIGHT"),
    dict(key="sky", scene="mn7_sky", lines=[
        "On your first night, the twin rises in the east. And it's huge.",
        "At half the distance, it looks twice as wide as the Moon. That's four times the area. So when it's full, it should light the ground about four times as brightly as a full moon.",
        "The two moons run at different speeds, so their phases drift in and out of step. Some nights, you get a full twin and a thin crescent Moon. Other nights, both are full, and the whole landscape glows silver. Truly dark nights become rare.",
        "Like our Moon, the twin would soon be tidally locked, always showing Earth the same face. And its phases would come round every ten days or so, from new to full and back again.",
        "And when both moons are up, everything on the ground casts two shadows, each pointing a different way."]),
    card("c2", "THE FIRST TIDE"),
    dict(key="tide", scene="mn7_tide", lines=[
        "By morning, you'd notice the sea.",
        "Tides come from the difference in a moon's pull from one side of Earth to the other. And that difference fades fast with distance. It follows the cube of the distance. Halve the distance, and the tidal pull gets eight times stronger.",
        "So the twin pulls on our oceans about eight times harder than the Moon does. Add the Moon and the Sun on top, and by our rough math, the strongest tides would pull more than six times harder than today's biggest spring tides.",
        "How high would the water climb? Real tides depend on the shape of every coast and sea floor, so nobody can say exactly. But low, flat coastlines would flood and drain on a grand scale, every single day.",
        "And there'd be two tidal rhythms, one from each moon, beating against each other. On some days they'd stack up. On others, they'd partly cancel out."]),
    card("c3", "THE FIRST ECLIPSE"),
    dict(key="eclipse", scene="mn7_eclipse", lines=[
        "Halfway through our new life with two moons, a quick favour. If you're enjoying this, tap like and subscribe. It really helps the channel.",
        "Then, one afternoon, the twin slides in front of the Sun.",
        "Today, the Moon and the Sun look almost exactly the same size in our sky. That's why a total eclipse only just covers the Sun, and lets its glowing outer atmosphere, the corona, shine out around the edge.",
        "The twin looks about twice as wide as the Sun. So it covers it with room to spare. Its shadow on the ground would be far wider, but it would also hide the brightest, inner part of the corona.",
        "And because the twin laps Earth every ten days or so, eclipses would probably come far more often. Sometimes, the twin would even pass in front of the Moon itself. A moon eclipsing a moon."],
         opts=dict(cta=0)),
    card("c4", "A MILLION YEARS"),
    dict(key="spin", scene="mn7_spin", lines=[
        "Now let's fast-forward. Because tides don't just move water. They act like a brake.",
        "Earth spins faster than the Moon orbits, so it drags the tidal bulges slightly ahead. Friction slows Earth's spin, and the bulge's pull nudges the Moon outward. Today, the Moon drifts away by about three point eight centimeters a year.",
        "Close in, that braking gets much stronger. Plugging the twin into the standard tidal formula, it would brake Earth's spin about sixty-four times harder than the Moon does.",
        "By our rough math, days would stretch by about twenty-five minutes every million years. With only our Moon, that takes more than sixty million years.",
        "And the twin itself would spiral outward about forty-five times faster than the Moon. Close to two meters a year. In effect, it steals Earth's spin, and uses it to climb away."]),
    card("c5", "THE COLLISION COURSE"),
    dict(key="chaos", scene="mn7_chaos", lines=[
        "And that's where the trouble starts.",
        "Two big moons don't ignore each other. Every time the twin laps the Moon, the two pass within about two hundred thousand kilometers, and tug on each other. At that range, the Moon pulls on the twin with roughly one eightieth of the force Earth does.",
        "Each tug is small. But they repeat, again and again. And as the twin creeps outward, the gap between their orbits shrinks. Sooner or later, the tugs start to add up instead of cancelling out.",
        "In nineteen ninety-nine, planetary scientist Robin Canup and her colleagues simulated young Earths with more than one moon. Their verdict: systems like this are typically unstable. In most of their runs, it ended one of two ways. The moons crashed into each other, or the inner moon fell into Earth.",
        "We can watch a slow version of this at Mars. Its inner moon, Phobos, creeps about two meters closer to Mars every century. In thirty to fifty million years, Mars is expected to pull it apart.",
        "Exactly when our twin would meet its end depends on details we've made up. But two big moons around one planet is probably not a forever arrangement."]),
    dict(key="twist", scene="mn7_twist", lines=[
        "And here's the twist. Earth may have tried this already.",
        "In twenty eleven, planetary scientists Martin Yoot-see and Erik Asphaug proposed that, soon after the Moon formed, Earth had a second moon. About a third as wide as the Moon, and around one thirtieth of its mass.",
        "In their model, it sat at a stable point in the Moon's own orbit, sharing its path, for tens of millions of years.",
        "Then it drifted out of place, and caught up with the Moon. Not with a bang, but at a crawl. About seven thousand kilometers an hour. For two moons, that's about as gentle as a collision gets.",
        "Instead of blasting a crater, it splattered across one side of the Moon, as a layer of rock tens of kilometers thick. And that might explain why the Moon's far side is so rugged and mountainous, and so different from the side we see.",
        "When the dust settled, Asphaug said, you had one moon that might have looked a lot like ours today.",
        "It's still a hypothesis. Other scientists think tides and heat can explain the difference. But the Moon might carry the remains of its twin on the side we never see."],
         sfx=[("scratch", 0.0)]),
    dict(key="outro", scene="mn7_end", lines=[
        "So a second big moon would bring brighter nights, double shadows, giant tides and longer days. Until, one day, the two moons meet.",
        "For now, our tiny second moon is about to leave us. If you could keep a second moon forever, would you want one? Tell me in the comments."],
         hold=1.6, opts=dict(q="KEEP A SECOND MOON?")),
]
L1_CH = [("hook", "Earth has two moons right now"), ("news", "2026 QQ8: what actually happened"), ("mini", "Mini-moons happen all the time"),
         ("c0", "The rules: a twin Moon"), ("c1", "The first night: double shadows"), ("c2", "The first tide"),
         ("c3", "The first eclipse"), ("c4", "A million years: longer days"), ("c5", "The collision course"),
         ("twist", "Earth may have had two moons"), ("outro", "Would you keep it?")]

# =====================================================================  SHORTS
S1 = [  # teaser cut from the long-form
    dict(key="a1", scene="mn7_hook", lines=["Right now, Earth has two moons."], opts=dict(mode="intro", hook="EARTH HAS TWO MOONS")),
    dict(key="a2", scene="mn7_news", lines=["The second is a tiny rock called twenty twenty-six Q-Q-eight, just a meter or two across. Earth's gravity caught it in April."],
         opts=dict(mode="short", badge="2026 QQ8")),
    dict(key="a3", scene="mn7_news", lines=["It loops around us, never closer than about one and a half times the Moon's distance. It should leave early next year."],
         opts=dict(mode="loops", badge="ONLY VISITING")),
    dict(key="a4", scene="mn7_sky", lines=["But what if the second moon were a twin of ours, at half the distance?",
                                           "Like and subscribe for more what-ifs."],
         opts=dict(mode="short", cta=1, badge="TWIN MOON")),
    dict(key="a5", scene="mn7_sky", lines=["It would look twice as wide, and four times as bright. Everything would cast two shadows."],
         opts=dict(mode="shadows", badge="2 SHADOWS")),
    dict(key="a6", scene="mn7_tide", lines=["Its pull on the oceans would be eight times the Moon's."],
         opts=dict(mode="short", badge="8× TIDAL PULL")),
    dict(key="a7", scene="mn7_chaos", lines=["And sooner or later, the two moons would probably collide."],
         opts=dict(mode="short", badge="COLLISION COURSE")),
    dict(key="a8", scene="mn7_endshort", lines=["Full story on the channel."], hold=1.4, opts=dict(top="TWO MOONS?")),
]
S2 = [  # standalone: can the Moon have its own moon? (submoons)
    dict(key="m1", scene="mn7_sub", lines=["What if the Moon had a moon of its own?"], opts=dict(mode="intro", hook="A MOON FOR THE MOON?")),
    dict(key="m2", scene="mn7_sub", lines=["Of all the moons we know of in our solar system, not one has a moon of its own."],
         opts=dict(mode="none", badge="ZERO FOUND")),
    dict(key="m3", scene="mn7_sub", lines=["In twenty nineteen, astronomers Juna Coal-my-er and Sean Raymond checked if they could even exist. The problem is tides. Tugged by both the planet and the moon, most submoons can't keep a stable orbit."],
         opts=dict(mode="tides", badge="SUBMOONS")),
    dict(key="m4", scene="mn7_sub", lines=["But a few big moons, far from their planets, could keep one. Titan, Callisto, Eye-app-ih-tus, and our own Moon.",
                                           "Tap like and subscribe for more."],
         opts=dict(mode="hosts", cta=1, badge="ONLY 4 HOSTS")),
    dict(key="m5", scene="mn7_sub", lines=["On paper, our Moon could hold a submoon tens of kilometers wide, on a wide orbit."],
         opts=dict(mode="ours", badge="ON PAPER")),
    dict(key="m6", scene="mn7_sub", lines=["Up close, it's tricky. In nineteen seventy-two, Apollo sixteen left a small satellite in low lunar orbit. The Moon's lumpy gravity pulled it down in thirty-five days."],
         opts=dict(mode="lumpy", badge="DOWN IN 35 DAYS")),
    dict(key="m7", scene="mn7_endshort", lines=["So what if Earth had two moons? Full story on the channel."], hold=1.4, opts=dict(top="TWO MOONS?", look="sub")),
]
S3 = [  # standalone, happening now: Uranus at opposition 25 Nov 2026 -> what if Earth were tipped over like Uranus?
    dict(key="u1", scene="mn7_uranus", lines=["What if Earth were tipped on its side, like Uranus?"], opts=dict(mode="intro", hook="EARTH ON ITS SIDE?")),
    dict(key="u2", scene="mn7_uranus", lines=["On November twenty-fifth, Uranus reached opposition. It's as bright as it gets this year. Easy in binoculars, from Taurus, near the Pleiades."],
         opts=dict(mode="sky", badge="25 NOVEMBER 2026")),
    dict(key="u3", scene="mn7_uranus", lines=["Uranus spins tipped over by about ninety-eight degrees. NASA says a giant collision may be to blame."],
         opts=dict(mode="tilt", badge="98° TILT")),
    dict(key="u4", scene="mn7_uranus", lines=["Its year lasts eighty-four of ours. So each pole gets years of sunshine overhead, while the other half sits in a twenty-one-year winter night.",
                                              "Like and subscribe for more what-ifs."],
         opts=dict(mode="seasons", cta=1, badge="21-YEAR NIGHT")),
    dict(key="u5", scene="mn7_uranus", lines=["Tip Earth the same way, and in June, almost the whole northern half gets nonstop daylight, while the south sits in months of night."],
         opts=dict(mode="earth", badge="MIDNIGHT SUN")),
    dict(key="u6", scene="mn7_uranus", lines=["The surprise? One climate model found deep enough oceans could keep a tipped world mild, even at the poles."],
         opts=dict(mode="ocean", badge="STILL LIVABLE?")),
    dict(key="u7", scene="mn7_endshort", lines=["So what if Earth had two moons? Full story on the channel."], hold=1.4, opts=dict(top="TWO MOONS?", look="ura")),
]

VIDEOS = {"b7_moons": L1, "short_b7_moons": S1, "short_b7_moonmoon": S2, "short_b7_uranus": S3}
CHAPTERS = {"b7_moons": L1_CH}
MUSIC = {"b7_moons": "twinmoon", "short_b7_moons": "twinmoon_s", "short_b7_moonmoon": "twinmoon_s", "short_b7_uranus": "tilt_s"}
TTS_MAP = {
    "Kris-tee-ahn Shar-nets-kee": "Krisztián Sárneczky",
    "twenty twenty-six Q-Q-eight": "2026 QQ8",
    "twenty twenty-four P-T-five": "2024 PT5",
    "Twenty twenty C-D-three": "2020 CD3",
    "P-T-five": "PT5",
    "Martin Yoot-see": "Martin Jutzi",
    "Juna Coal-my-er": "Juna Kollmeier",
    "Eye-app-ih-tus": "Iapetus",
    "three point eight centimeters": "3.8 centimeters",
    "nineteen ninety-nine": "1999",
    "nineteen seventy-two": "1972",
    "Apollo sixteen": "Apollo 16",
    "October twenty-ninth": "October 29",
    "August twentieth": "August 20",
    "November twenty-fifth": "November 25",
}

META = {
    "b7_moons": dict(
        title="What If Earth Had Two Moons?",
        hook=("Right now Earth really does have a second moon: 2026 QQ8, a natural object a meter or two across that Earth's gravity caught "
              "around April 2026 (announced by the IAU Minor Planet Center on 29 October 2026). It should leave early in 2027. So what if "
              "our second moon were a full-size twin of the Moon? Double shadows, giant tides, faster eclipses, longer days, and a collision course."),
        tags=["two moons", "what if Earth had two moons", "2026 QQ8", "mini-moon", "second moon", "Moon", "tides", "eclipse", "2024 PT5",
              "far side of the Moon", "space", "astronomy", "science", "what if"],
        hashtags="#whatif #science #space", parent=None),
    "short_b7_moons": dict(
        title="Earth Just Caught a Second Moon #shorts",
        hook="Since about April 2026, a tiny natural object, 2026 QQ8, has been looping around Earth as a temporary mini-moon. So what if our second moon were as big as the first?",
        tags=["2026 QQ8", "mini-moon", "second moon", "two moons", "Moon", "space news", "what if", "shorts"], hashtags="#whatif #science #space", parent="b7_moons"),
    "short_b7_moonmoon": dict(
        title="What If the Moon Had Its Own Moon? #shorts",
        hook="No known moon has a moon of its own. A 2019 study by Juna Kollmeier and Sean Raymond found only a few big, distant moons could keep a 'submoon', and our Moon is one of them.",
        tags=["submoon", "moonmoon", "moons of moons", "Moon", "Titan", "Callisto", "Iapetus", "Kollmeier", "space", "what if", "shorts"],
        hashtags="#whatif #science #space", parent="b7_moons"),
    "short_b7_uranus": dict(
        title="What If Earth Were Tipped Over Like Uranus? #shorts",
        hook="Uranus reached opposition on 25 November 2026, its brightest of the year. It spins tipped over by about 98 degrees. Here's what that tilt would do to Earth's seasons.",
        tags=["Uranus", "Uranus opposition", "axial tilt", "seasons", "Earth on its side", "obliquity", "night sky", "space", "what if", "shorts"],
        hashtags="#whatif #science #space", parent="b7_moons"),
}
