"""Batch 05 SPACE topic: What If the Moon Disappeared? (+ teaser, drift and Pluto Shorts).

Scene prefix m5_ = scenes_b5_moon.py. TTS spellings are mapped back for captions via TTS_MAP (read by meta2).
"""
CARD = 1.9

def card(key, text, label="WITHOUT THE MOON", scene="m5_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  LONG-FORM
L1 = [
    dict(key="hook", scene="m5_hook", lines=[
        "For about four and a half billion years, the same grey rock has circled the Earth.",
        "It pulls the oceans up and down. It sets the clock for animals all over the planet. It even helps steady the tilt of the whole world.",
        "So what if, tonight, the Moon just disappeared?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="m5_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF THE MOON", l2="DISAPPEARED?")),
    dict(key="rules", scene="m5_rules", lines=[
        "First, the rules. At midnight, the Moon vanishes. No explosion, and no rocks raining down on us. It's simply gone, and so is its gravity.",
        "Everything else stays the same. Earth keeps circling the Sun, and the Sun keeps shining.",
        "And here's what we're losing. The Moon is about three thousand four hundred and seventy-five kilometers wide, roughly a quarter the width of Earth.",
        "It sits about three hundred and eighty-four thousand kilometers away. Its light takes about one and a quarter seconds to reach your eyes."]),
    card("c0", "MIDNIGHT"),
    dict(key="night", scene="m5_night", lines=[
        "If it happens near a new moon, you might not notice at all. On those nights, the Moon is up during the day, lost in the Sun's glare.",
        "But on a full moon night, it's instant. Moonlight is just sunlight bouncing off that grey rock. Switch it off, and the landscape goes dark. Your moon shadow disappears, and far more stars come out.",
        "Here's a surprise. The Moon isn't actually very bright. It reflects only about twelve percent of the sunlight that hits it. It's a dark, dusty grey. It only looks brilliant because the sky behind it is black."]),
    dict(key="wobble", scene="m5_wobble", lines=[
        "Something else changes that nobody could feel. Earth and the Moon don't simply orbit one another. They both circle a shared balance point, about four thousand six hundred and seventy kilometers from Earth's center.",
        "That's inside the Earth, but well off-center. So every month, our whole planet wobbles around it.",
        "At midnight, the wobble stops. Earth carries on around the Sun, alone."]),
    card("c6", "6 HOURS LATER"),
    dict(key="tides", scene="m5_tides", lines=[
        "By morning, sailors and surfers notice. The tide doesn't come in the way it should.",
        "The Moon's gravity pulls hardest on the side of Earth facing it, and weakest on the far side. That stretches the oceans into two bulges, and as Earth spins through them, most coasts get two high tides a day.",
        "The Sun raises tides too. But its pull on the oceans is less than half as strong as the Moon's. About forty-six percent.",
        "So now the Sun is in charge. Tides don't disappear, but they shrink to less than half of what they were. By our rough math, about a third the height of today's biggest spring tides.",
        "And those spring and neap tides are gone. That monthly rhythm came from the Sun and Moon lining up, then pulling against each other. With one partner gone, the tides lose their monthly beat."]),
    dict(key="fundy", scene="m5_fundy", lines=[
        "In Canada's Bay of Fundy, the sea can rise up to sixteen meters between low and high tide. That's about as tall as a five-story building.",
        "Without the Moon, those famous tides would be a shadow of themselves. Tidal power stations, which run on the rising and falling sea, would lose much of their energy.",
        "And the strip of shore that floods and drains every day, home to crabs, mussels and seaweed, would shrink."]),
    card("c30", "ONE MONTH LATER"),
    dict(key="reef", scene="m5_reef", lines=[
        "Over the next few weeks, the strangest effects show up in nature. Because a huge number of living things keep time by the Moon.",
        "On the Great Barrier Reef, many corals release their eggs and sperm all at once, in the nights after a full moon. It looks like an underwater snowstorm.",
        "In two thousand seven, researchers found a light-sensing gene in corals that responds to the faint blue light of the full moon. Corals have no eyes, but they can sense the Moon.",
        "Without moonlight, scientists think that cue is gone. And when spawning drifts out of sync, fewer eggs get fertilized."]),
    dict(key="crabs", scene="m5_crabs", lines=[
        "On Christmas Island in the Indian Ocean, millions of red crabs march down to the sea every year.",
        "The females release their eggs before dawn, as the high tide turns, timed to the Moon's last quarter. Take away the Moon, and they lose their calendar."]),
    dict(key="beetle", scene="m5_beetle", lines=[
        "In South Africa, one kind of dung beetle keeps its ball rolling in a straight line at night by reading the pattern of polarized moonlight across the sky. In two thousand three, it became the first animal known to navigate this way.",
        "And in the Arctic, during the long polar night, tiny animals called zooplankton swim up and down to the rhythm of the Moon instead of the Sun. Around each full moon, they sink, about fifty meters down, probably to hide from predators that hunt by moonlight.",
        "Without the Moon, some of these creatures lose a compass, a clock or a hiding cue. Many would likely adapt. Some might not."]),
    card("c1y", "ONE YEAR LATER"),
    dict(key="eclipse", scene="m5_eclipse", lines=[
        "Quick favour before we go on. If you're enjoying this, tap like and subscribe. It really helps the channel.",
        "A year in, you'd notice what's missing from the calendar. No more eclipses. Not solar, and not lunar.",
        "Total solar eclipses are a cosmic coincidence. The Sun is about four hundred times wider than the Moon, but also about four hundred times farther away. So from Earth, they look almost exactly the same size.",
        "And those few minutes of darkness have changed science. During an eclipse in eighteen sixty-eight, astronomers studying the Sun's glowing edge spotted a yellow line in its light that matched no known element. It was helium. Found on the Sun, years before anyone found it on Earth.",
        "In nineteen nineteen, Arthur Eddington's team used a total eclipse to photograph stars right next to the Sun, and showed that the Sun's gravity bends their light, as Einstein had predicted."],
         opts=dict(cta=0)),
    dict(key="sky", scene="m5_sky", lines=[
        "Astronomers do get one upside. Dark skies, every night of the month, with no full moon washing out faint galaxies.",
        "And the month itself loses its meaning. It began as the time from one new moon to the next, about twenty-nine and a half days. Calendars still built on the Moon's phases, like the Islamic calendar, would have nothing left to count."]),
    card("cmy", "MILLIONS OF YEARS LATER"),
    dict(key="tilt", scene="m5_tilt", lines=[
        "Now jump far ahead. The biggest question about a moonless Earth is its tilt.",
        "Earth's axis leans about twenty-three degrees, and that tilt gives you seasons. Today it only rocks gently, by a little more than a degree either way, over about forty thousand years.",
        "In nineteen ninety-three, French astronomer Jacques Laskar and his colleagues ran the numbers without the Moon. Their answer was alarming. Over long spans of time, the tilt could wander chaotically, anywhere from zero to more than eighty-five degrees.",
        "Mars shows what that might look like. It has no big moon, and its tilt is thought to swing chaotically, from below ten degrees to above sixty. Tip a planet far enough, and its poles can face the Sun for months at a time."]),
    dict(key="debate", scene="m5_tilt", lines=[
        "But wait. In two thousand eleven, a team including Jason Barnes and Jack Lissauer ran longer, more detailed simulations of a moonless Earth.",
        "They found that over hundreds of millions of years, the tilt might wander by only about ten to twenty degrees. That's a much bigger swing than today, but nowhere near the chaos people feared.",
        "So the Moon helps keep our seasons steady. But a moonless Earth might not have been as wild as we thought."],
         opts=dict(mode="debate")),
    dict(key="day", scene="m5_day", lines=[
        "One thing would change for certain. The Moon's tides act like a brake on Earth's spin. Every century, they add a tiny bit of length to the day. Records of ancient eclipses suggest about one point eight milliseconds per century.",
        "That sounds like nothing. But it adds up. A fossil shell from seventy million years ago, from the age of the dinosaurs, recorded days only about twenty-three and a half hours long. Its year had three hundred and seventy-two days.",
        "Without the Moon, the Sun's weaker tides would still brake our spin, but far more gently. Your days would stay close to twenty-four hours for much, much longer."]),
    dict(key="twist", scene="m5_drift", lines=[
        "And here's the twist. The Moon is already leaving.",
        "Apollo astronauts left mirrors on the Moon's surface. Observatories still fire lasers at them, and time the echo, which takes about two and a half seconds to come back.",
        "The answer: the Moon is drifting away by about three point eight centimeters a year. Roughly as fast as your fingernails grow. It's that same tidal brake. As Earth's spin slows, the Moon is nudged into a wider orbit.",
        "So it will slowly shrink in our sky. NASA lunar scientist Richard Vondrak estimated that Earth's last total solar eclipse will happen about six hundred million years from now."],
         sfx=[("scratch", 0.0)]),
    dict(key="origin", scene="m5_origin", lines=[
        "But it won't escape. In about five billion years, the Sun is expected to swell into a red giant, and scientists expect that to wreck the Earth and Moon long before the Moon could get away.",
        "And it all began just as violently. Scientists think the Moon formed about four and a half billion years ago, when a Mars-sized world, nicknamed Thee-uh, smashed into the young Earth. One simulation suggests the Moon could have taken shape in just a few hours."]),
    dict(key="outro", scene="m5_end", lines=[
        "So the Moon isn't just a light in the sky. It's a tide maker, a clock for corals and crabs, an eclipse machine, and a brake on our spin. And it's leaving us, one fingernail at a time.",
        "If it vanished tonight, what would you miss most? The tides, the eclipses, or the moonlight? Tell me in the comments."],
         hold=1.6, opts=dict(q="WHAT WOULD YOU MISS?")),
]
L1_CH = [("hook", "Four and a half billion years"), ("rules", "The rules"), ("c0", "Midnight: the lights go out"), ("wobble", "Earth stops wobbling"),
         ("c6", "6 hours later: the tides shrink"), ("fundy", "The Bay of Fundy"), ("c30", "One month later: lost rhythms"), ("crabs", "Crabs, beetles and plankton"),
         ("c1y", "One year later: no more eclipses"), ("sky", "Darker skies"), ("cmy", "Millions of years: the tilt"), ("debate", "A wild planet? Maybe not"),
         ("day", "The brake on our spin"), ("twist", "The Moon is already leaving"), ("origin", "Born in a collision"), ("outro", "What would you miss?")]

# =====================================================================  SHORTS
S1 = [  # teaser
    dict(key="a1", scene="m5_hook", lines=["What if the Moon vanished tonight?"], opts=dict(mode="intro", hook="NO MOON TONIGHT")),
    dict(key="a2", scene="m5_night", lines=["The full moon goes dark. Moonlight is just sunlight bouncing off grey rock that reflects only about twelve percent of it."],
         opts=dict(badge="ONLY 12% REFLECTED")),
    dict(key="a3", scene="m5_tides", lines=["By morning, the tides shrink. The Sun's pull on the oceans is less than half the Moon's."],
         opts=dict(mode="short", badge="SUN: 46% OF THE MOON")),
    dict(key="a4", scene="m5_reef", lines=["Like and subscribe for more what-ifs.",
                                           "Corals on the Great Barrier Reef time their spawning by moonlight. They'd lose their cue."],
         opts=dict(mode="short", cta=0)),
    dict(key="a5", scene="m5_eclipse", lines=["No more eclipses, ever. And over millions of years, Earth's tilt could wander much more than it does today."],
         opts=dict(mode="short", badge="NO MORE ECLIPSES")),
    dict(key="a6", scene="m5_endshort", lines=["So how much do we really need the Moon? Full story on the channel."], hold=1.4, opts=dict(top="NO MOON?")),
]
S2 = [  # standalone: the Moon is drifting away
    dict(key="d1", scene="m5_drift", lines=["The Moon is running away from us."], opts=dict(mode="intro", hook="THE MOON IS LEAVING")),
    dict(key="d2", scene="m5_drift", lines=["Apollo astronauts left mirrors on the Moon. Observatories still fire lasers at them, and time the echo. About two and a half seconds, there and back."],
         opts=dict(mode="laser", badge="≈2.5 SECONDS")),
    dict(key="d3", scene="m5_drift", lines=["The result: the Moon drifts about three point eight centimeters farther away every year. About as fast as your fingernails grow."],
         opts=dict(mode="nail", badge="3.8 CM A YEAR")),
    dict(key="d4", scene="m5_day", lines=["Like and subscribe for more space what-ifs.",
                                          "The cause is tides. They brake Earth's spin, and nudge the Moon outward."],
         opts=dict(mode="brake", cta=0)),
    dict(key="d5", scene="m5_day", lines=["So our days get longer. Seventy million years ago, a day lasted only about twenty-three and a half hours."],
         opts=dict(mode="shell", badge="23.5-HOUR DAYS")),
    dict(key="d6", scene="m5_drift", lines=["And in about six hundred million years, the Moon may look too small to cover the Sun. No more total solar eclipses."],
         opts=dict(mode="eclipse", badge="LAST TOTAL ECLIPSE")),
    dict(key="d7", scene="m5_endshort", lines=["But what if the Moon vanished tonight? Full story on the channel."], hold=1.4, opts=dict(top="NO MOON?")),
]
S3 = [  # standalone: Pluto replaces the Moon (-> moon long)
    dict(key="p1", scene="m5_pluto", lines=["What if Pluto replaced our Moon?"], opts=dict(mode="intro", hook="PLUTO AS OUR MOON")),
    dict(key="p2", scene="m5_pluto", lines=["Pluto is about two thousand three hundred and seventy-seven kilometers wide. About two-thirds the width of our Moon, so it would look smaller in the sky."],
         opts=dict(mode="size", badge="2/3 AS WIDE")),
    dict(key="p3", scene="m5_pluto", lines=["But it's coated in bright ices, and reflects roughly six times more light. By our rough math, a full Pluto could outshine the full Moon."],
         opts=dict(mode="bright", badge="≈6× MORE REFLECTIVE")),
    dict(key="p4", scene="m5_pluto", lines=["Pluto has only about a sixth of the Moon's mass. So its tides would be weaker than the Sun's."],
         opts=dict(mode="tides", badge="1/6 OF THE MASS")),
    dict(key="p5", scene="m5_pluto", lines=["Like and subscribe for more what-ifs.",
                                            "And sunlight here is about fifteen hundred times stronger than out at Pluto. Its nitrogen ice would start turning to gas."],
         opts=dict(mode="melt", cta=0, badge="~1,500× MORE SUNLIGHT")),
    dict(key="p6", scene="m5_pluto", lines=["Its big moon Charon is half Pluto's size, and they circle each other every six point four days. This close to Earth, the pair might not stay together."],
         opts=dict(mode="charon")),
    dict(key="p7", scene="m5_endshort", lines=["So what if we had no Moon at all? Full story on the channel."], hold=1.4, opts=dict(top="NO MOON AT ALL?")),
]

VIDEOS = {"b5_moon": L1, "short_b5_moon": S1, "short_b5_drift": S2, "short_b5_pluto": S3}
CHAPTERS = {"b5_moon": L1_CH}
MUSIC = {"b5_moon": "moon", "short_b5_moon": "moon_s", "short_b5_drift": "moon_s", "short_b5_pluto": "moon_s"}
TTS_MAP = {
    "Thee-uh": "Theia",
    "eighteen sixty-eight": "1868",
    "nineteen nineteen": "1919",
    "nineteen ninety-three": "1993",
    "two thousand seven": "2007",
    "two thousand three": "2003",
    "two thousand eleven": "2011",
    "three point eight centimeters": "3.8 centimeters",
    "one point eight milliseconds": "1.8 milliseconds",
    "six point four days": "6.4 days",
}
