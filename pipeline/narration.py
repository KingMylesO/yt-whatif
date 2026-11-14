"""Scene + narration plan for Batch 01 (TTS-friendly wording).
Each scene: key, scene (drawing fn name), lines (narration), optional:
  card  -> title-card text (no narration, fixed length)
  hold  -> extra seconds after the last line
  sfx   -> list of (sfx_name, offset_seconds)
  opts  -> dict passed to the drawing fn
"""

CARD = 1.9

LONG = [
    dict(key="hook", scene="park", lines=[
        "If the Sun vanished right now, you wouldn't notice. Not for eight minutes.",
        "And that's the last good news you'd get."], hold=0.4),
    dict(key="title", scene="title", lines=[], hold=3.4, sfx=[("rumble", 0.0)],
         opts=dict(text="WHAT IF THE SUN VANISHED?")),
    dict(key="rules", scene="solar_system", lines=[
        "Let's set the rules. We're not talking about the Sun exploding, or burning out over billions of years.",
        "We're talking about the Sun simply… gone. Deleted. One moment it's there, the next there's nothing but empty space."],
         sfx=[("pop", "L1+0.32")]),
    dict(key="impossible", scene="impossible", lines=[
        "Impossible? Completely. The laws of physics don't allow mass to just disappear."]),
    dict(key="distance", scene="distance", lines=[
        "But imagining it tells us something amazing: how much of everything around you depends on one star, a hundred and fifty million kilometers away."]),
    dict(key="clock", scene="stopwatch", lines=["So let's run the clock."], hold=0.6),
    dict(key="c0", scene="card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text="0 SECONDS")),
    dict(key="blink", scene="sun_blink", lines=[
        "The Sun disappears. And on Earth, absolutely nothing changes."], sfx=[("pop", 0.55)]),
    dict(key="beam", scene="light_beam", lines=[
        "That's because sunlight takes about eight minutes and twenty seconds to reach us.",
        "The light hitting your face right now left the Sun over eight minutes ago.",
        "So for the next eight minutes, the sky stays blue, and the light keeps coming. It's just light that's already on its way."]),
    dict(key="ghost", scene="ghost_orbit", lines=[
        "Here's the stranger part. Gravity doesn't travel instantly either. Changes in gravity move at the speed of light.",
        "So for those same eight minutes, Earth keeps curving around a Sun that isn't there anymore. Following the orbit of a ghost."]),
    dict(key="past", scene="park", lines=[
        "For eight minutes, everyone on Earth is living in the past, and no one has any idea."],
         opts=dict(timer=True), hold=0.5),
    dict(key="c820", scene="card", lines=[], hold=CARD + 0.3, sfx=[("whoosh", 0.0)],
         opts=dict(text="8 MINUTES 20 SECONDS")),
    dict(key="lightsout", scene="lights_out", lines=[
        "Then the last sunlight arrives. And after it… nothing.",
        "Half the planet goes from daytime to night in an instant. The sky goes black. Stars come out in the middle of the afternoon."],
         sfx=[("click", "L0+0.86")]),
    dict(key="moon", scene="moon_fade", lines=[
        "About a second later, the Moon disappears too.",
        "The Moon doesn't make its own light; it reflects the Sun's. With no sunlight, it's a dark rock you can't see."]),
    dict(key="planets", scene="planets", lines=[
        "The planets stay visible a little longer, because their reflected light takes longer to get here.",
        "Jupiter keeps shining for more than an hour. Saturn, for over two.",
        "One by one, the bright planets blink out of the sky."]),
    dict(key="orbit", scene="orbit_break", lines=[
        "And at that same moment, gravity catches up. Earth stops curving. It flies off in a straight line into deep space, at around thirty kilometers per second.",
        "That's fast enough to cross the entire United States in under three minutes.",
        "We're not orbiting anything anymore. We're drifting."]),
    dict(key="c1d", scene="card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text="1 DAY")),
    dict(key="city", scene="city_night", lines=[
        "At first, it doesn't feel that cold. The ground, the oceans and the air all hold onto a lot of heat.",
        "But that heat is leaking out into space, and nothing is putting it back."]),
    dict(key="plants", scene="plants", lines=[
        "Meanwhile, something quieter is already happening. Photosynthesis stops.",
        "Every plant on Earth, every tree, every blade of grass, every patch of plankton in the ocean, just lost its power source.",
        "Smaller plants will die within days to weeks. Some large trees could hang on for a surprisingly long time, living off stored energy, slowly and in the cold.",
        "But nothing can grow back."]),
    dict(key="chain", scene="food_chain", lines=[
        "And remember: almost every food chain on Earth starts with plants."], hold=0.6),
    dict(key="c1w", scene="card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text="1 WEEK")),
    dict(key="frost", scene="frost", lines=[
        "Scientists who've crunched the numbers estimate that within about a week, Earth's average surface temperature would drop below freezing.",
        "Around minus eighteen degrees Celsius. That's zero Fahrenheit."], opts=dict(temp=-18)),
    dict(key="grid", scene="grid", lines=[
        "Lakes and rivers start freezing over. Crops are gone.",
        "Power grids are under huge pressure, as billions of people try to stay warm at the same time.",
        "Solar panels are useless.",
        "Wind gets weird, because wind is driven by the Sun heating different parts of the planet unevenly. Without the Sun, the whole weather machine starts to wind down."]),
    dict(key="c1y", scene="card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text="1 YEAR")),
    dict(key="year", scene="earth_ice", lines=[
        "After a year, estimates put the average temperature at around minus seventy-three degrees Celsius. That's minus one hundred Fahrenheit.",
        "Colder than almost anywhere humans have ever recorded on Earth's surface."]),
    dict(key="ocean", scene="ocean_section", lines=[
        "But here's something you might not expect: the oceans don't freeze solid.",
        "The surface turns to ice, and that ice works like a blanket, trapping heat underneath.",
        "Combined with heat coming up from Earth's core, the deep oceans could stay liquid for a very, very long time."]),
    dict(key="survive", scene="geothermal", lines=[
        "So… could anyone survive? Surprisingly? Maybe. For a while.",
        "Earth has its own heat source: its hot interior. Places like Iceland already use geothermal energy to heat homes and make electricity.",
        "With enough preparation, people could survive in sealed habitats near geothermal sources, or powered by nuclear reactors."]),
    dict(key="bunker", scene="bunker", lines=[
        "They'd need artificial light to grow food, recycled air, and a lot of engineering.",
        "It would be the hardest survival challenge in human history. But it isn't strictly impossible."]),
    dict(key="c1m", scene="card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text="1,000,000 YEARS")),
    dict(key="deep", scene="deep_freeze", lines=[
        "Over a much longer time, Earth keeps cooling, until it eventually settles somewhere near minus two hundred and forty degrees Celsius.",
        "It never reaches absolute zero, only because the planet's core keeps leaking a tiny bit of warmth."]),
    dict(key="airsnow", scene="air_snow", lines=[
        "On the way there, it gets so cold that the air itself condenses.",
        "Oxygen and nitrogen turn to liquid, then freeze, falling as snow onto a frozen planet."]),
    dict(key="rogue", scene="rogue", lines=[
        "Earth becomes a rogue planet: a lonely world drifting between the stars, with no sun of its own.",
        "And it wouldn't be the only one. Astronomers think rogue planets could be incredibly common across the galaxy. Maybe even more common than stars."]),
    dict(key="twist", scene="vent", lines=[
        "So is that the end of life on Earth? Not quite.",
        "Deep at the bottom of the ocean, in total darkness, there are hydrothermal vents: cracks in the seafloor pouring out hot, mineral-rich water.",
        "And around them live entire ecosystems. Tube worms, crabs, shrimp, bacteria, that get their energy from chemicals, not sunlight.",
        "They've never seen the Sun. Many of them would carry on living, at least for a long time, without ever knowing it was gone."]),
    dict(key="zoom", scene="zoom_out", lines=[
        "Which means the last survivors on Earth might not be humans at all.",
        "They might be creatures that never needed the Sun in the first place."], hold=0.8),
    dict(key="outro", scene="park", lines=[
        "So next time you're outside on a sunny day, remember: the light on your face is already eight minutes old.",
        "And everything you see is running on it."], opts=dict(outro=True), hold=0.6),
    dict(key="end", scene="end_screen", lines=[
        "What do you think: would humans make it? Tell me in the comments."], hold=11.0),
]

# Chapter markers (scene key -> chapter label) for the description
CHAPTERS = [
    ("hook", "The Sun vanishes"),
    ("rules", "The setup"),
    ("c0", "0 to 8 minutes: nothing happens"),
    ("c820", "8 minutes: lights out"),
    ("c1d", "1 day: the big chill begins"),
    ("c1w", "1 week: the world freezes"),
    ("c1y", "1 year: the deep freeze"),
    ("survive", "Could anyone survive?"),
    ("c1m", "1 million years and beyond"),
    ("twist", "The twist"),
    ("outro", "Outro"),
]

SHORT_SUN = [
    dict(key="s1", scene="park", lines=["The Sun just disappeared. And you have no idea."],
         opts=dict(hook="THE SUN JUST VANISHED.")),
    dict(key="s2", scene="light_beam", lines=["Sunlight takes eight minutes to reach Earth."]),
    dict(key="s3", scene="park", lines=["So for eight minutes, the sky stays blue."], opts=dict(timer=True)),
    dict(key="s4", scene="ghost_orbit", lines=["Even gravity takes eight minutes to catch up. Earth keeps orbiting… nothing."]),
    dict(key="s5", scene="lights_out", lines=["Then: lights out."], sfx=[("click", 0.05)], opts=dict(short_switch=True)),
    dict(key="s6", scene="moon_fade", lines=["The Moon vanishes too."]),
    dict(key="s7", scene="orbit_break", lines=["Earth flies off into space."], opts=dict(quick=True)),
    dict(key="s8", scene="frost", lines=["Within a week, the whole planet is below freezing."], opts=dict(temp=-18)),
    dict(key="s9", scene="vent", lines=["But some life wouldn't even notice."]),
    dict(key="s10", scene="end_short", lines=["Want to know who survives? Full video on the channel."], hold=1.6,
         opts=dict(text="FULL VIDEO ON THE CHANNEL")),
]

SHORT_SLEEP = [
    dict(key="z1", scene="bed_awake", lines=["What if you just… stopped sleeping?"],
         opts=dict(hook="DAY 1 WITHOUT SLEEP…")),
    dict(key="z2", scene="desk_tired", lines=[
        "After twenty-four hours awake, studies show your reaction time and judgment can be as impaired as someone who's legally drunk."],
         opts=dict(badge="24 HOURS")),
    dict(key="z3", scene="microsleep", lines=[
        "By day three, your brain starts forcing microsleeps: tiny blackouts lasting a few seconds that you don't even notice.",
        "Dangerous if you're driving."], opts=dict(badge="3 DAYS")),
    dict(key="z4", scene="hallucinate", lines=[
        "After several days, people have reported hallucinations, paranoia, and trouble forming sentences."],
         opts=dict(badge="5+ DAYS")),
    dict(key="z5", scene="record_1964", lines=[
        "The famous record? In nineteen sixty-four, a high school student named Randy Gardner stayed awake for about eleven days, for a science fair.",
        "Scientists don't recommend trying it."], opts=dict(badge="11 DAYS")),
    dict(key="z6", scene="lab_rat", lines=[
        "In lab experiments, rats completely deprived of sleep died within a few weeks."]),
    dict(key="z7", scene="bed_asleep", lines=["So yeah. Go to bed."], hold=1.2),
]

VIDEOS = {"long": LONG, "short_sun": SHORT_SUN, "short_sleep": SHORT_SLEEP}
