"""Batch 05 (EARTH): What If All the Ice on Earth Melted? + teaser, Lake Vostok and Carnian Pluvial Episode Shorts.

Scene prefix i5_ (scenes_b5_ice.py). Music: "ice" (long-form), "ice_s" (Shorts).
TTS spellings are mapped back for captions through TTS_MAP (read by meta2.tts_to_text).
"""
CARD = 1.9

def card(key, text, label, scene="i5_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

IL = "ALL THE ICE IS GONE"
L1 = [
    dict(key="hook", scene="i5_city", lines=[
        "Antarctica's ice is so thick that, in places, the ground hidden beneath it lies more than two and a half kilometers below sea level.",
        "And there's a lot of it. Melt every scrap of ice sitting on Earth's land, and the oceans rise by roughly seventy meters. That's taller than a twenty-story building.",
        "So what if it all melted? Every glacier and every ice sheet, all at once. Where would the new coastline be, and what would we find under the ice?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="i5_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF ALL THE ICE", l2="ON EARTH MELTED?")),
    dict(key="rules", scene="i5_rules", lines=[
        "Here are the rules. We flip a switch, and every bit of ice sitting on land turns to water at once. The meltwater pours into the sea. Everything else about Earth stays the same.",
        "Most of that ice is in two places. Antarctica's ice sheet covers almost fourteen million square kilometers. That's about the size of the United States and Mexico put together. On average, it's more than two kilometers thick.",
        "Greenland's ice sheet is smaller, about three times the size of Texas, but in places it's more than three kilometers thick. Between them, these two sheets of ice hold more than two thirds of all the fresh water on Earth.",
        "In the real world, melting all of this would take thousands of years. We'll get to that. But first, let's flip the switch."]),
    dict(key="budget", scene="i5_budget", lines=[
        "So how high does the water go? Antarctica alone holds enough ice to raise the oceans by about fifty-eight meters.",
        "Greenland adds about seven and a half meters more.",
        "And every other glacier on the planet, in the Alps, the Himalayas, the Andes and Alaska, adds up to only about a third of a meter. Hundreds of thousands of glaciers, and the water wouldn't even reach your knees.",
        "Add it all up, and you get roughly sixty-six meters. The U.S. Geological Survey gives a round figure of about seventy. Either way, the sea climbs higher than a twenty-story building."]),
    dict(key="seaice", scene="i5_seaice", lines=[
        "Notice what's missing from that list. The ice at the North Pole.",
        "Arctic sea ice floats. Like an ice cube in a glass of water, it already pushes aside its own weight in seawater. So when it melts, the level hardly changes.",
        "Hardly, but not zero. Meltwater is fresh, and slightly less dense than salty seawater, so it takes up a little more room. NASA estimates the effect is only about three percent of what you'd get from the same ice melting on land.",
        "So the Arctic Ocean could lose all of its ice, and the beaches would barely notice. The real danger is the ice sitting on rock."]),
    card("cday", "DAY 1", IL),
    dict(key="americas", scene="i5_map", lines=[
        "Seventy meters later, the map of the world looks very different. National Geographic mapped this exact scenario, and in the Americas, the damage is enormous.",
        "Almost all of Florida disappears, along with the Gulf Coast and the Atlantic seaboard. Miami is gone completely, and the low-lying parts of New York and Boston go under.",
        "On the West Coast, San Francisco's hills become a cluster of islands, and California's Central Valley turns into a giant bay.",
        "Further south, the Amazon basin becomes an arm of the Atlantic Ocean, and Buenos Aires is swallowed."],
         opts=dict(mode="americas")),
    dict(key="europe", scene="i5_map", lines=[
        "In Europe, London is lost. So is Venice. The Netherlands, and most of Denmark, slip under the sea.",
        "Across the Mediterranean, the water reaches Alexandria, and even Cairo, which today sits more than a hundred and fifty kilometers inland."],
         opts=dict(mode="europe")),
    dict(key="asia", scene="i5_map", lines=[
        "In Asia, nearly all of Bangladesh disappears, along with much of India's coast. In China, National Geographic estimated that land now home to around six hundred million people would flood.",
        "That includes Shanghai, a city whose center has already sunk more than three meters since the late eighteen-hundreds, and which sits behind seawalls typically just five to seven meters high.",
        "Africa, as it turns out, loses less land than most other continents, although its coastlines still shrink."],
         opts=dict(mode="asia")),
    card("cyear", "YEAR 1", IL),
    dict(key="albedo", scene="i5_albedo", lines=[
        "After the flood comes the heat. Ice is a mirror. Fresh snow can bounce back around ninety percent of the sunlight that hits it.",
        "Open ocean is the opposite. It reflects less than a tenth of the sunlight, and soaks up the rest.",
        "Swap millions of square kilometers of white for dark water and rock, and Earth absorbs far more sunshine. That warms the planet, which melts more ice, which warms it even more. Scientists call this the ice-albedo feedback.",
        "And in reality, a world warm enough to melt all of its ice would already be hot. National Geographic put that world's average temperature at around twenty-seven degrees Celsius. Today, it's about fourteen."]),
    dict(key="currents", scene="i5_currents", lines=[
        "Then there are the oceans. Around Antarctica, cold, salty water sinks to the sea floor, and drives a slow current through the deep ocean.",
        "Fresh meltwater is lighter, so it floats on top, and the sinking slows down. One study found that under high emissions, this deep circulation could slow by about forty percent by twenty fifty.",
        "Pour in an entire ice sheet's worth of fresh water, and that slow conveyor could stall. Nutrients would get stuck in the deep, and less would reach the life near the surface."]),
    dict(key="spin", scene="i5_spin", lines=[
        "Quick favour, before we go any further: if you're enjoying this, tap like and subscribe. It genuinely helps the channel.",
        "Even the length of your day changes. As meltwater flows away from the poles and spreads toward the equator, Earth's mass moves farther from its axis.",
        "It's like a figure skater spinning with her arms out. The spin slows down. Researchers estimate that melting ice and rising seas have been stretching the day by about one point three three milliseconds per century since the year two thousand.",
        "Tiny, sure. But if emissions stay high, they think this could outdo the Moon's effect on the length of our day by the end of this century."],
         opts=dict(cta=0)),
    card("c10k", "10,000 YEARS", IL),
    dict(key="rebound", scene="i5_rebound", lines=[
        "Now, fast-forward ten thousand years. Something strange is happening on land. It's rising.",
        "Ice sheets are so heavy that they press the Earth's crust down into the hot, slowly flowing rock beneath it. Take the ice away, and the land springs back. But very, very slowly.",
        "We know, because it's still happening. About ten thousand five hundred years ago, an ice sheet three kilometers thick melted off Scandinavia. Today, the coast of the Gulf of Bothnia is still rising by about eight or nine millimeters a year.",
        "In Finland's Kvar-ken archipelago, that adds about one square kilometer of new land every year. And the crust there still has about a hundred meters left to climb.",
        "On Sweden's High Coast, the highest shoreline from the end of the Ice Age now sits two hundred and eighty-six meters above today's sea."]),
    dict(key="antarctica", scene="i5_antarctica", lines=[
        "Now imagine that across all of Antarctica. With its twenty-seven million cubic kilometers of ice gone, the land underneath finally sees the sky.",
        "And it isn't one neat continent. Scientists expect East Antarctica to be a single large landmass, and West Antarctica to be a scatter of rugged, mountainous islands.",
        "That's because so much of West Antarctica's rock floor lies below sea level. Its deepest known basin, the Byrd Subglacial Basin, sits more than two and a half kilometers below the waves.",
        "Over in East Antarctica, beneath the Denman Glacier, a canyon plunges more than three and a half kilometers below sea level. It's the deepest point on land anywhere. The shore of the Dead Sea, the lowest dry land you can stand on, is only about four hundred meters down.",
        "Over thousands of years, as the rock rebounds, some of those islands would rise and join up. But for a very long time, the new Antarctica would be part land, and part sea."]),
    card("creal", "THE REAL CLOCK", IL),
    dict(key="clock", scene="i5_clock", lines=[
        "So, back to reality. How long would it actually take to melt all of this?",
        "Not a day. In twenty twenty-four, NASA measured the global sea rising about six millimeters in a single year. At that pace, reaching seventy meters would take roughly twelve thousand years.",
        "Melting speeds up as the planet warms, of course. Some scientists think melting it all would take more than five thousand years.",
        "In twenty fifteen, a team led by Ricarda Winkelmann modeled what happens if we burn all the fossil fuel we can reach. Antarctica ends up almost ice-free, and for the first thousand years, the sea rises about three meters every century.",
        "And their model suggested West Antarctica could tip into decline with far less: around six hundred to eight hundred billion extra tonnes of carbon."]),
    card("cpast", "BEEN HERE BEFORE", IL),
    dict(key="past", scene="i5_past", lines=[
        "And here's the thing. Earth has done this before.",
        "About three million years ago, in the Ply-oh-seen, carbon dioxide was last above four hundred parts per million. The planet was about three to four degrees warmer, Greenland was largely free of ice, and the seas stood fifteen to twenty meters higher. Today, carbon dioxide is above four hundred again.",
        "Go back more than thirty-four million years, and there was little or no ice at the poles at all. West Antarctica was covered in forests.",
        "Then the planet cooled, ice began to build on Antarctica, and over millions of years, the seas settled near the coastlines we know."]),
    dict(key="twist", scene="i5_finger", lines=[
        "But here's the twist. If Greenland melted, the sea right next to Greenland would actually fall.",
        "The ice sheet weighs around three thousand trillion tonnes. That much mass has its own gravity, and it tugs the nearby ocean toward it, piling water up against its coast.",
        "Melt the ice, and that pull fades. The water slumps away. And the land, freed of its weight, rises up. Models from Harvard researchers suggest sea level near Greenland's coast would drop by twenty to fifty meters.",
        "So where does the water go? Far away. More than about two thousand kilometers from Greenland, the sea rises more than the global average.",
        "Antarctica works the same way. Its melt would raise the seas most in places far to the north: across the Pacific, the Indian Ocean and the western Atlantic. Each ice sheet hits the far side of the world hardest.",
        "And this isn't just theory. Satellites measuring the sea surface since the nineteen-nineties have matched the pattern."],
         sfx=[("scratch", 0.0)]),
    dict(key="outro", scene="i5_end", lines=[
        "So if all the ice melted, the sea would rise about seventy meters, Antarctica would break into islands, your day would get a little longer, and the water would be lowest right next to the ice that melted.",
        "If the coastline moved seventy meters uphill, where would you move? Tell me in the comments."],
         hold=1.6, opts=dict(q="WHERE WOULD YOU MOVE?")),
]
L1_CH = [("hook", "Seas 70 meters higher"), ("rules", "The rules: flip the switch"), ("budget", "How high does the water go?"),
         ("seaice", "Why sea ice doesn't count"), ("cday", "Day 1: the new coastline"), ("europe", "Europe and Egypt"), ("asia", "Asia and Africa"),
         ("cyear", "Year 1: the heat"), ("currents", "The oceans stall"), ("spin", "Longer days"), ("c10k", "10,000 years: the land rises"),
         ("antarctica", "Antarctica revealed"), ("creal", "How long would it really take?"), ("cpast", "Earth has done this before"),
         ("twist", "The twist: the sea falls near Greenland"), ("outro", "Where would you move?")]

# ----------------------------------------------------------------------------- Shorts
S1 = [  # teaser cut from the long-form
    dict(key="s1", scene="i5_city", lines=["What if every bit of ice on Earth's land melted at once?"], opts=dict(mode="short", hook="ALL THE ICE: GONE")),
    dict(key="s2", scene="i5_budget", lines=["Antarctica alone would raise the oceans about fifty-eight meters. Add Greenland and every glacier, and you get roughly seventy."],
         opts=dict(badge="~70 METERS")),
    dict(key="s3", scene="i5_map", lines=["London, Venice and the Netherlands go under. So does almost all of Florida, and nearly all of Bangladesh."], opts=dict(mode="world")),
    dict(key="s4", scene="i5_antarctica", lines=["Like and subscribe for more melted maps.",
                                                 "Without its ice, West Antarctica wouldn't be land at all. It would be a chain of rocky islands."],
         opts=dict(cta=0, mode="short")),
    dict(key="s5", scene="i5_finger", lines=["And the weirdest part? Right next to Greenland, the sea would actually drop, because the ice stops pulling the water toward it."],
         opts=dict(mode="short", badge="THE SEA FALLS?!")),
    dict(key="s6", scene="i5_endshort", lines=["So how long would it really take? Full story on the channel."], hold=1.4, opts=dict(top="ALL THE ICE MELTED?")),
]
S2 = [  # standalone: Lake Vostok
    dict(key="v1", scene="i5_vostok", lines=["Almost four kilometers under Antarctica's ice, there's a lake about the size of Lake Ontario."],
         opts=dict(mode="intro", hook="A LAKE UNDER THE ICE")),
    dict(key="v2", scene="i5_vostok", lines=["It's Lake Vostok, one of six hundred and seventy-five lakes scientists have found hidden under Antarctica."],
         opts=dict(mode="lakes", badge="675 LAKES")),
    dict(key="v3", scene="i5_vostok", lines=["Heat from inside the Earth keeps them liquid, even though the air above Vostok once hit minus eighty-nine degrees."],
         opts=dict(mode="cold", badge="−89 °C")),
    dict(key="v4", scene="i5_vostok", lines=["In twenty twelve, Russian scientists drilled three thousand seven hundred and sixty-nine meters down and reached the water."],
         opts=dict(mode="drill", badge="3,769 METERS")),
    dict(key="v5", scene="i5_vostok", lines=["Hit like and subscribe for more hidden worlds.", "The lake may have been sealed off for at least fourteen million years. So, could anything live there?"],
         opts=dict(mode="sealed", cta=0)),
    dict(key="v6", scene="i5_vostok", lines=["In another buried lake, Whillans, scientists found about a hundred and thirty thousand microbes per milliliter, living without sunlight."],
         opts=dict(mode="life", badge="130,000 PER ML")),
    dict(key="v7", scene="i5_vostok", lines=["Vostok's ice has hinted at life too, but some scientists suspect contamination. The jury's still out."],
         opts=dict(mode="dna")),
    dict(key="v8", scene="i5_endshort", lines=["And what if all that ice melted? Full story on the channel."], hold=1.4, opts=dict(top="WHAT IF THE ICE MELTED?")),
]
S3 = [  # standalone: the Carnian Pluvial Episode (-> ice long-form)
    dict(key="r1", scene="i5_rain", lines=["About two hundred and thirty-four million years ago, Earth's climate turned wet, on and off, for up to two million years."],
         opts=dict(mode="intro", hook="IT RAINED FOR 2 MILLION YEARS")),
    dict(key="r2", scene="i5_rain", lines=["The likely trigger was a string of giant volcanic eruptions in what's now western North America, called Ran-jell-ee-uh. They pumped out huge amounts of carbon and heated the planet."],
         opts=dict(mode="volcano", badge="WRANGELLIA")),
    dict(key="r3", scene="i5_rain", lines=["It wasn't one endless storm. Scientists see several pulses, swinging from dry to humid and back."],
         opts=dict(mode="pulses")),
    dict(key="r4", scene="i5_rain", lines=["Like and subscribe for more deep time.", "Around a third of marine species may have died out."],
         opts=dict(mode="extinct", cta=0, badge="~1/3 OF SEA LIFE")),
    dict(key="r5", scene="i5_rain", lines=["Then, in rocks in Italy's Dolomites, the footprints change. First no dinosaur tracks, then lots. Many scientists think this wet crisis helped dinosaurs take over."],
         opts=dict(mode="dinos")),
    dict(key="r6", scene="i5_rain", lines=["Conifers, modern-style coral reefs and plankton spread too."], opts=dict(mode="modern")),
    dict(key="r7", scene="i5_endshort", lines=["Today, warming is melting Earth's ice instead. What if all of it melted? Full story on the channel."],
         hold=1.4, opts=dict(top="WHAT IF ALL THE ICE MELTED?")),
]

VIDEOS = {"b5_ice": L1, "short_b5_ice": S1, "short_b5_vostok": S2, "short_b5_rain": S3}
CHAPTERS = {"b5_ice": L1_CH}
MUSIC = {"b5_ice": "ice", "short_b5_ice": "ice_s", "short_b5_vostok": "ice_s", "short_b5_rain": "ice_s"}
TTS_MAP = {"Kvar-ken": "Kvarken", "Ply-oh-seen": "Pliocene", "Ran-jell-ee-uh": "Wrangellia",
           "late eighteen-hundreds": "late 1800s", "twenty fifty": "2050", "twenty fifteen": "2015", "twenty twelve": "2012",
           "twenty twenty-four": "2024", "nineteen-nineties": "1990s", "the year two thousand": "the year 2000",
           "U.S. Geological Survey": "U.S. Geological Survey"}
