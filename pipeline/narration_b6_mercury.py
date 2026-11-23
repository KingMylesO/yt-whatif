"""Batch 06 SPACE topic (happening now): What If You Lived on Mercury? (+ teaser, Mercury-day and Voyager Shorts).

News peg: ESA/JAXA BepiColombo was captured into orbit around Mercury on 21 Nov 2026 (ESA flight dynamics confirmed
it early on 22 Nov). Scene prefix me6_ = scenes_b6_mercury.py. TTS spellings map back to captions through TTS_MAP.
"""
CARD = 1.9

def card(key, text, label="LIVING ON MERCURY", scene="me6_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  LONG-FORM
L1 = [
    dict(key="hook", scene="me6_hook", lines=[
        "On November twenty-first, twenty twenty-six, after more than eight years in space, a European and Japanese spacecraft fired its engine, and let Mercury catch it.",
        "It's called Beppy Colombo. And it's only the second mission ever to orbit the planet closest to the Sun.",
        "So what if you'd been on board? What if you landed on Mercury, and tried to live there?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="me6_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF YOU LIVED", l2="ON MERCURY?")),
    dict(key="news", scene="me6_news", lines=[
        "First, what actually happened. The big engine burn began on the evening of November twenty-first, European time. Just after midnight, E-S-A's flight dynamics team confirmed it. Beppy Colombo had been captured into orbit.",
        "It's really two spacecraft stacked together. E-S-A's Mercury Planetary Orbiter, and Japan's Mee-oh, built to study the planet's magnetic field. They're due to split apart on December ninth and tenth.",
        "Science is set to begin in April twenty twenty-seven. Until then, each orbiter still has to be steered into its final orbit, so what they'll discover is still unknown.",
        "Only one spacecraft has orbited Mercury before. NASA's Messenger circled it from twenty eleven to twenty fifteen, then ended its mission by crashing into the surface."]),
    card("c0", "GETTING THERE"),
    dict(key="trip", scene="me6_trip", lines=[
        "Here's a surprise. Mercury is hard to reach. Not because it's far away, but because the Sun is in the way.",
        "Fall toward the Sun and you speed up, like a car rolling downhill. To be captured by little Mercury, you have to shed a huge amount of that speed.",
        "According to some estimates, it takes less energy to reach Pluto than to reach Mercury.",
        "So Beppy Colombo braked the clever way, with nine flybys. One of Earth, two of Venus, and six of Mercury itself. Each one stole a little speed.",
        "The mission is named after Italian scientist Joo-zeppy Colombo, nicknamed Beppy. In nineteen seventy, he worked out how NASA's Mariner ten could loop back and fly past Mercury a second time."]),
    card("c1", "TOUCHDOWN"),
    dict(key="land", scene="me6_land", lines=[
        "Now the rules. You ride down in a lander, with a heat-proof suit and a small base. We'll ignore the cost. Your only job is to stay alive.",
        "You touch down at dawn, right on the line between night and day. And the first thing you notice is how light you feel. Mercury's gravity is only about thirty-eight percent of Earth's. A ten kilogram backpack feels like less than four.",
        "Then you look up. The sky is black, even in daylight. Mercury has no real atmosphere. Just a thin haze of atoms called an exosphere, knocked off the ground by the solar wind and tiny meteorites.",
        "And the Sun is enormous. It can look more than three times wider than it does from Earth, and its light can be as much as seven times brighter."]),
    card("c2", "THE FIRST HOUR"),
    dict(key="heat", scene="me6_heat", lines=[
        "In your first hour, the sunlight starts to bite. In full daylight, Mercury's ground can reach about four hundred and thirty degrees Celsius. That's hot enough to melt lead.",
        "But step into the shadow of a boulder, and it's a different world. With no air to carry heat around, shade stays cold. On the night side, the ground drops to about minus one hundred and eighty degrees.",
        "That's a swing of about six hundred degrees between day and night.",
        "Luckily, you won't have to face it all at once. Because on Mercury, the Sun barely moves."]),
    card("c3", "THE FIRST SUNRISE"),
    dict(key="dawn", scene="me6_dawn", lines=[
        "Mercury spins very slowly. One turn takes about fifty-nine Earth days. Meanwhile, it races around the Sun in just eighty-eight.",
        "Put those together, and something strange happens. From one sunrise to the next takes about one hundred and seventy-six Earth days.",
        "So the line between night and day creeps across the ground. By our rough math, at the equator it moves at about three and a half kilometers an hour on average. That's slower than a brisk walk.",
        "Which means, in theory, you could live on the move. Keep pace with that line, and you'd stay at dawn forever, never facing the full heat of noon or the deepest cold of night.",
        "In Kim Stanley Robinson's novel twenty-three twelve, a whole city called Terminator does exactly that, crawling around Mercury on rails, just ahead of the rising Sun."]),
    card("c4", "ONE MERCURY YEAR"),
    dict(key="year", scene="me6_year", lines=[
        "Stay put instead, and after eighty-eight Earth days, Mercury has gone once around the Sun. Your first year is over.",
        "But your first day isn't. Mercury spins three times for every two trips around the Sun. So one full day, sunrise to sunrise, lasts two whole Mercury years.",
        "Astronomers only worked this out in nineteen sixty-five, using radar. Before that, many thought one side of Mercury always faced the Sun.",
        "And Mercury has a party trick. Its orbit is stretched, so near its closest pass to the Sun, it moves so fast that its orbit briefly outruns its spin.",
        "From some places on the surface, the Sun rises, stops, sinks back below the horizon, then rises again. A double sunrise. And at two spots on the equator, the noon Sun hangs almost still overhead for weeks."]),
    card("c5", "NIGHTFALL"),
    dict(key="night", scene="me6_night", lines=[
        "Before the Sun goes down, a quick favour. If you're enjoying this, tap like and subscribe. It really helps the channel.",
        "Around eighty-eight Earth days after your sunrise, the Sun finally sets. And the night lasts just as long. Roughly three Earth months of darkness.",
        "With no atmosphere to hold the heat, the ground bleeds its warmth into space, down toward minus one hundred and eighty degrees Celsius.",
        "Your base now needs heaters, not coolers. On Mercury, whether you freeze or fry depends almost entirely on where the Sun is."],
         opts=dict(cta=0)),
    card("c6", "ONE MERCURY DAY"),
    dict(key="poles", scene="me6_poles", lines=[
        "After one full Mercury day, you'd probably want a better address. And the best one might be at the poles.",
        "Mercury's axis is tilted only about two degrees. So near the poles, the Sun always skims the horizon, and the floors of some deep craters never see sunlight at all.",
        "In twenty twelve, NASA's Messenger confirmed what radar had hinted at. Those dark craters hold water ice. On the planet closest to the Sun.",
        "One estimate put it at a hundred billion to a trillion tonnes. Enough, said lead scientist David Lawrence, to bury an area the size of Washington, D.C. under more than three kilometers of ice.",
        "Much of it is hidden under a dark layer that scientists think is made of organic compounds, probably delivered by comets and asteroids.",
        "For a settler, that ice could mean water to drink, oxygen to breathe and fuel to make. Right next to the endless power of the Sun."]),
    card("c7", "UNDER YOUR FEET"),
    dict(key="shrink", scene="me6_shrink", lines=[
        "Now look down. Because the ground beneath you is shrinking.",
        "Mercury is mostly metal. Its iron core reaches out to about eighty-five percent of the planet's radius. Picture a peach that is almost all stone. That's why it's the second densest planet in the solar system, after Earth.",
        "As that core slowly cooled over billions of years, the whole planet contracted. In twenty fourteen, scientists using Messenger's maps estimated its radius has shrunk by as much as seven kilometers.",
        "The crust buckled into giant cliffs called lobate scarps. Some run for hundreds of kilometers, and rise up to about three kilometers high."]),
    dict(key="field", scene="me6_field", lines=[
        "That core still makes a magnetic field, but at the surface it's only about one percent as strong as Earth's. A weak shield against the solar wind.",
        "It even twists into what NASA calls magnetic tornadoes, that funnel hot particles from the Sun down to the surface. Your base would need serious radiation shielding."]),
    card("c8", "ONE CENTURY"),
    dict(key="einstein", scene="me6_einstein", lines=[
        "Stay a century, and you'd be living on the planet that helped prove Einstein right.",
        "Mercury's stretched orbit slowly swings around the Sun. In eighteen fifty-nine, astronomer Urbain Luh Vair-ee-ay found that it swings a little too fast for Newton's laws.",
        "The gap was tiny. Forty-three arcseconds per century. By our rough math, that's about the width of a coin seen from a hundred meters away.",
        "Einstein's new theory of gravity, general relativity, predicted exactly that extra swing. Mercury's orbit became one of its first big wins."]),
    dict(key="twist", scene="me6_twist", lines=[
        "And here's the twist. Mercury is one of the hardest planets to reach. Yet on average, it's the closest planet to Earth.",
        "Venus comes nearest at its closest point. But it also spends long stretches on the far side of the Sun. Mercury never strays far from the Sun, so it never gets that far from us.",
        "In twenty nineteen, three engineers ran the numbers in the magazine Physics Today. On average, Mercury is the closest planet to Earth. And to every other planet in the solar system, too. By their math, Mercury averages about one point zero four times the Earth-Sun distance from us. Venus, about one point one four.",
        "So our nearest neighbour, on average, took more than eight years to reach. And starting next spring, Beppy Colombo will study how this strange little planet formed, and how it changed."],
         sfx=[("scratch", 0.0)]),
    dict(key="outro", scene="me6_end", lines=[
        "So life on Mercury means a black sky, a Sun three times wider, a day that lasts two years, and ice hiding next to the hottest sunlight of any planet.",
        "If you moved there, where would you live? In the frozen craters at the poles, or chasing the sunrise forever? Tell me in the comments."],
         hold=1.6, opts=dict(q="POLES OR SUNRISE?")),
]
L1_CH = [("hook", "BepiColombo reaches Mercury"), ("news", "What actually happened"), ("c0", "Getting there: harder than Pluto?"),
         ("c1", "Touchdown: black sky, giant Sun"), ("c2", "The first hour: 430 °C"), ("c3", "The first sunrise"),
         ("c4", "One Mercury year: the double sunrise"), ("c5", "Nightfall"), ("c6", "Ice at the poles"),
         ("c7", "A shrinking planet"), ("field", "Magnetic tornadoes"), ("c8", "The planet that proved Einstein right"),
         ("twist", "Our closest neighbour?"), ("outro", "Where would you live?")]

# =====================================================================  SHORTS
S1 = [  # teaser cut from the long-form
    dict(key="a1", scene="me6_hook", lines=["On November twenty-first, a spacecraft went into orbit around Mercury. What if you went too?"],
         opts=dict(mode="intro", hook="WE JUST REACHED MERCURY")),
    dict(key="a2", scene="me6_land", lines=["You'd feel light. Mercury's gravity is just thirty-eight percent of Earth's. And the sky stays black, even at noon."],
         opts=dict(mode="sky", badge="38% GRAVITY")),
    dict(key="a3", scene="me6_land", lines=["The Sun looks more than three times wider than at home."],
         opts=dict(mode="sun", badge="3× WIDER SUN")),
    dict(key="a4", scene="me6_heat", lines=["By day, the ground hits about four hundred and thirty degrees Celsius. Hot enough to melt lead.",
                                            "Like and subscribe for more space what-ifs."],
         opts=dict(mode="short", cta=1, badge="430 °C")),
    dict(key="a5", scene="me6_night", lines=["And sunrise to sunrise takes about one hundred and seventy-six Earth days. Nights drop to minus one eighty."],
         opts=dict(mode="short", badge="−180 °C NIGHTS")),
    dict(key="a6", scene="me6_poles", lines=["Yet in dark craters at the poles, there's water ice. Next to the Sun."],
         opts=dict(mode="short", badge="ICE AT THE POLES")),
    dict(key="a7", scene="me6_endshort", lines=["So could you survive there? Full story on the channel."], hold=1.4, opts=dict(top="LIVE ON MERCURY?")),
]
S2 = [  # standalone: one Mercury day lasts two Mercury years
    dict(key="d1", scene="me6_mday", lines=["On Mercury, one day lasts two years."], opts=dict(mode="intro", hook="1 DAY = 2 YEARS")),
    dict(key="d2", scene="me6_mday", lines=["Mercury races around the Sun in just eighty-eight Earth days. That's one Mercury year."],
         opts=dict(mode="year", badge="1 YEAR = 88 DAYS")),
    dict(key="d3", scene="me6_mday", lines=["But it spins slowly. Once every fifty-nine days. Three spins for every two laps of the Sun."],
         opts=dict(mode="spin", badge="3 SPINS : 2 ORBITS")),
    dict(key="d4", scene="me6_mday", lines=["Put them together, and sunrise to sunrise takes about one hundred and seventy-six Earth days. Two whole Mercury years.",
                                            "Tap like and subscribe for more."],
         opts=dict(mode="day", cta=1, badge="1 DAY = 176 DAYS")),
    dict(key="d5", scene="me6_mday", lines=["Near its closest pass, Mercury's orbit outruns its spin. In some places, the Sun rises, sets, then rises again."],
         opts=dict(mode="double", badge="DOUBLE SUNRISE")),
    dict(key="d6", scene="me6_mday", lines=["And with nights lasting months, the ground swings from about four hundred and thirty degrees to minus one eighty."],
         opts=dict(mode="temp", badge="430 °C → −180 °C")),
    dict(key="d7", scene="me6_endshort", lines=["So could you live there? Full story on the channel."], hold=1.4, opts=dict(top="LIVE ON MERCURY?", look="mday")),
]
S3 = [  # standalone, happening now: Voyager 1 is one light-day away (-> closest space long-form: Mercury)
    dict(key="v1", scene="me6_voy", lines=["What if you texted Voyager 1 right now?"], opts=dict(mode="intro", hook="TEXT VOYAGER 1?")),
    dict(key="v2", scene="me6_voy", lines=["On November eighteenth, twenty twenty-six, it became the first spacecraft ever to reach one light-day from Earth. About twenty-six billion kilometers away."],
         opts=dict(mode="far", badge="1 LIGHT-DAY AWAY")),
    dict(key="v3", scene="me6_voy", lines=["Your message flies at the speed of light, and still takes a full day to arrive. The reply takes another day."],
         opts=dict(mode="text", badge="24 H EACH WAY")),
    dict(key="v4", scene="me6_voy", lines=["It launched in nineteen seventy-seven, and it's still flying at about seventeen kilometers every second.",
                                           "Like and subscribe for more space what-ifs."],
         opts=dict(mode="speed", cta=1, badge="LAUNCHED 1977")),
    dict(key="v5", scene="me6_voy", lines=["Its nuclear power drops about four watts a year, so most instruments are off. Two are still on."],
         opts=dict(mode="power", badge="−4 WATTS A YEAR")),
    dict(key="v6", scene="me6_voy", lines=["And right now, the team is living this. Since November fourteenth, Voyager has sent a signal, but no data. Every test takes two days to answer."],
         opts=dict(mode="glitch", badge="DATA PAUSED")),
    dict(key="v7", scene="me6_endshort", lines=["Closer to home, we just reached Mercury. Full story on the channel."], hold=1.4,
         opts=dict(top="ONE LIGHT-DAY", look="voy")),
]

VIDEOS = {"b6_mercury": L1, "short_b6_mercury": S1, "short_b6_mday": S2, "short_b6_voyager": S3}
CHAPTERS = {"b6_mercury": L1_CH}
MUSIC = {"b6_mercury": "mercury", "short_b6_mercury": "mercury_s", "short_b6_mday": "mercury_s", "short_b6_voyager": "deep_s"}
TTS_MAP = {
    "Beppy Colombo": "BepiColombo",
    "Joo-zeppy Colombo, nicknamed Beppy": "Giuseppe Colombo, nicknamed Bepi",
    "Mee-oh": "Mio",
    "E-S-A": "ESA",
    "Urbain Luh Vair-ee-ay": "Urbain Le Verrier",
    "Mariner ten": "Mariner 10",
    "twenty-three twelve": "2312",
    "one point zero four times": "1.04 times",
    "one point one four": "1.14",
    "twenty twenty-seven": "2027",
    "twenty fifteen": "2015",
    "twenty nineteen": "2019",
    "nineteen sixty-five": "1965",
    "nineteen seventy-seven": "1977",
}

META = {
    "b6_mercury": dict(
        title="What If You Lived on Mercury?",
        hook="On 21 November 2026, ESA and JAXA's BepiColombo went into orbit around Mercury after more than eight years in space, only the second mission ever to do it. So what if you went with it and tried to live there? A day that lasts two years, a double sunrise, 430 °C afternoons and ice hiding at the poles.",
        tags=["Mercury", "BepiColombo", "what if", "living on Mercury", "ESA", "JAXA", "MESSENGER", "Mercury day", "double sunrise",
              "space", "planets", "solar system", "science", "astronomy"],
        hashtags="#whatif #science #space", parent=None),
    "short_b6_mercury": dict(
        title="We Just Reached Mercury. Could You Live There? #shorts",
        hook="On 21 November 2026, BepiColombo went into orbit around Mercury. Here's what living there would be like.",
        tags=["Mercury", "BepiColombo", "what if", "space", "shorts"], hashtags="#whatif #science #space", parent="b6_mercury"),
    "short_b6_mday": dict(
        title="On Mercury, One Day Lasts Two Years #shorts",
        hook="Mercury's year is 88 Earth days, but sunrise to sunrise takes about 176. Here's why, and why some places get a double sunrise.",
        tags=["Mercury", "Mercury day", "double sunrise", "spin-orbit resonance", "space", "shorts"], hashtags="#whatif #science #space", parent="b6_mercury"),
    "short_b6_voyager": dict(
        title="What If You Texted Voyager 1 Right Now? #shorts",
        hook="On 18 November 2026, NASA's Voyager 1 became the first spacecraft one light-day from Earth. A message now takes a full day each way.",
        tags=["Voyager 1", "NASA", "light-day", "interstellar space", "space", "shorts"], hashtags="#whatif #science #space", parent="b6_mercury"),
}
