"""Batch 07 EARTH topic (happening now): What If Every Volcano Erupted at Once? (+ teaser, Iwo Jima and nodule Shorts).

News peg: an underwater eruption off Iwo Jima (Iō Tō, Japan), reported by the Japan Meteorological Agency on 27 Oct 2026,
added ~50 ha of new land (Japan Coast Guard, 16 Nov; NASA Earth Observatory, 24 Nov 2026).
Extra Short: Diaz-Recio Lorenzo et al. 2026 (Scientific Reports), animals living inside deep-sea polymetallic nodules.
Scene prefix vo7_ = scenes_b7_volcano.py. TTS spellings map back to captions through TTS_MAP.
"""
CARD = 1.9

def card(key, text, label="EVERY VOLCANO AT ONCE", scene="vo7_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  LONG-FORM
L1 = [
    dict(key="hook", scene="vo7_hook", lines=[
        "On October twenty-seventh, twenty twenty-six, an eruption broke through the sea, just off a small Japanese island called Iwo Jima.",
        "Within three weeks, the island had grown. About fifty hectares of brand-new land. That's roughly ninety football fields.",
        "One volcano did that. So what if every volcano on Earth erupted at once?"],
         sfx=[("rumble", "L0+0.5")], hold=0.2),
    dict(key="title", scene="vo7_title", lines=[], hold=3.2, sfx=[("boom", 0.0)], opts=dict(l1="WHAT IF EVERY VOLCANO", l2="ERUPTED AT ONCE?")),
    dict(key="news", scene="vo7_news", lines=[
        "First, what actually happened. Iwo Jima sits about twelve hundred kilometers south of Tokyo, and the whole island is the top of an active volcano.",
        "In late October, seismic sensors picked up a sharp jump in activity. On October twenty-seventh, Japan's Meteorological Agency reported the first photos of an eruption, just off the island's southeast coast.",
        "NASA's Landsat nine satellite had photographed that coast the day before. When the clouds finally cleared on November eleventh, it saw new land, still hot enough to glow in infrared, and a long streak of floating pumice.",
        "On November sixteenth, Japan's Coast Guard confirmed it. The new land is joined to the island's southeast beach. NASA estimates it makes Iwo Jima about one point seven percent bigger.",
        "What's still unknown is how long it will last. Land made mostly of ash is loose, and waves chew it up. After an eruption here in twenty twenty-three, the new land was gone within weeks.",
        "NASA's Daniel Slayback expects this one to wash away within a few months too. But, he adds, we'll have to wait and see."]),
    card("c0", "THE RULES"),
    dict(key="rules", scene="vo7_rules", lines=[
        "Now, the what-if. The U-S Geological Survey counts about thirteen hundred and fifty potentially active volcanoes on Earth. And that's not counting the long chains of volcanoes along ridges on the ocean floor.",
        "In a typical year, only about forty to fifty of them erupt. Less than one in ten.",
        "So here are our rules. At the same moment, all thirteen hundred and fifty wake up. Each one erupts in its own style. Some ooze rivers of lava. Some explode.",
        "And for now, we'll ignore whether this is even possible. We'll come back to that at the end."]),
    card("c1", "MINUTE ONE"),
    dict(key="ring", scene="vo7_ring", lines=[
        "In the first minute, seen from space, the planet lights up. But not evenly.",
        "The glow traces lines. That's because most volcanoes sit where the giant plates of Earth's crust meet. About sixty percent of active volcanoes are on plate boundaries.",
        "The brightest line of all wraps around the Pacific Ocean. It's the Ring of Fire. It runs for about forty thousand kilometers, and it's made up of more than four hundred and fifty volcanoes.",
        "Iwo Jima is one of them. So are Mount Fuji, Mount Saint Helens, and the long chain of volcanoes down the Andes.",
        "Out in the Atlantic, Iceland glows too. In Africa, a line of volcanoes runs down the East African Rift. And Hawaii lights up in the middle of the Pacific.",
        "Meanwhile, under the sea, where most of Earth's volcanoes are hidden, the long volcanic ridges on the seafloor join in."]),
    card("c2", "DAY ONE"),
    dict(key="ash", scene="vo7_ash", lines=[
        "By the end of the first day, the biggest problem for most of the world isn't lava. It's ash.",
        "Volcanic ash isn't soft, like the ash in a fireplace. It's tiny bits of rock, minerals and volcanic glass. It's hard, it's abrasive, and it doesn't dissolve in water.",
        "And aircraft hate it. In nineteen eighty-two, a British Airways jumbo jet flew into an ash cloud from Gah-loong-goong, a volcano in Indonesia. All four engines stopped.",
        "The jet dropped about seven and a half kilometers. Then, in clearer air, the crew got the engines going again, and landed safely in Jakarta.",
        "Today, pilots stay away from ash completely. In April twenty ten, one Icelandic volcano spread ash across the skies of Europe. Over a hundred thousand flights were cancelled in a single week, and about seven million travelers were stuck.",
        "That was one volcano. With ash drifting downwind of hundreds of volcanoes at once, you can expect most of the world's air traffic to stop."]),
    card("c3", "THE FIRST MONTH"),
    dict(key="sulfur", scene="vo7_sulfur", lines=[
        "Ash falls out of the sky within days to weeks. The bigger, longer problem is invisible. It's sulfur.",
        "Big explosive eruptions fire sulfur dioxide gas high into the stratosphere, above the weather. There, it turns into a haze of tiny droplets that reflect sunlight back into space.",
        "In nineteen ninety-one, Mount Pinatubo in the Philippines blasted columns of ash and gas up to about forty kilometers high, along with around seventeen million tonnes of sulfur dioxide.",
        "That haze spread around the Earth in about three weeks. Within a year, it covered the whole globe.",
        "And the height record is even more recent. In January twenty twenty-two, the underwater Hunga Tonga volcano sent its plume about fifty-eight kilometers up, into the mesosphere. The highest plume in the satellite record.",
        "Now picture hundreds of plumes like that, all at once, all feeding the same haze."]),
    card("c4", "ONE YEAR LATER"),
    dict(key="winter", scene="vo7_winter", lines=[
        "Before we get to the coldest part, a quick favour. If you're enjoying this, hit like and subscribe. It really helps the channel.",
        "One year in, the sky is pale and milky. Sunsets glow red. And the planet is cooling.",
        "We know this works, because it has happened before, with just one volcano. After Pinatubo, the haze cooled the Northern Hemisphere by up to about half a degree Celsius.",
        "In eighteen fifteen, Mount Tambora in Indonesia produced the largest volcanic eruption ever recorded.",
        "The next year, eighteen sixteen, became known as the year without a summer. Snow fell in New England in July. Crops failed across much of North America, Western Europe and parts of Asia.",
        "Now add every volcano on Earth at once. Nobody can put an exact number on how cold it would get. But scientists who have looked at this scenario describe darker skies, a sharp drop in temperature, and plants struggling for light. A volcanic winter, worse than any in recorded history.",
        "The good news is that the haze doesn't last forever. After Pinatubo, the cooling faded after about three years, as the droplets slowly fell out of the stratosphere."],
         opts=dict(cta=0)),
    card("c5", "TEN YEARS LATER"),
    dict(key="co2", scene="vo7_co2", lines=[
        "So a few years later, the sky clears. But volcanoes don't only breathe out sulfur. They also breathe out carbon dioxide. So, do we swap a freezer for an oven?",
        "Here's a surprise. You may have heard that volcanoes release more carbon dioxide than humans do. They don't. Not even close.",
        "All the world's volcanoes, on land and under the sea, add up to roughly a third of a billion tonnes a year. Humans emit around forty billion tonnes.",
        "That means we emit more than sixty times as much as every volcano on Earth combined.",
        "Even Pinatubo, at the height of its eruption, only matched humanity's carbon dioxide output for about nine hours.",
        "So a single burst, even a huge one, isn't the real carbon danger. The danger comes when eruptions keep going for a very, very long time. Hold that thought."]),
    card("c6", "THE GIANTS"),
    dict(key="super", scene="vo7_super", lines=[
        "Of course, volcanoes aren't all the same size. A few are supervolcanoes, able to blast out more than a thousand cubic kilometers of material in one go.",
        "By our rough math, that's enough to bury all of London under more than half a kilometer of rock.",
        "The most recent super-eruption on Earth happened about twenty-seven thousand years ago, at Toe-po in New Zealand.",
        "Yellowstone is the famous one. The U-S Geological Survey puts the yearly chance of another giant eruption there at about one in seven hundred and thirty thousand. And it says there's no evidence that one is coming."]),
    dict(key="twist", scene="vo7_twist", lines=[
        "But here's the twist. Something like this did happen once. Just not all at once.",
        "About two hundred and fifty-two million years ago, in what's now Siberia, the ground cracked open, and kept erupting.",
        "The Siberian Traps released enough lava and magma to cover an area the size of the United States, a kilometer deep.",
        "But it took its time. The big eruptions began about three hundred thousand years before the great extinction. And a third of the magma came in the five hundred thousand years after it.",
        "Scientists think its gases, including enormous amounts of carbon dioxide, helped drive the end-Permian extinction. By one estimate, more than ninety-six percent of ocean species and about seventy percent of land species disappeared.",
        "So the worst volcanic event in Earth's history wasn't thirteen hundred volcanoes erupting in a single day. It was one region erupting, on and off, for hundreds of thousands of years."],
         sfx=[("scratch", 0.0)]),
    dict(key="why", scene="vo7_why", lines=[
        "So could every volcano really erupt at once? Scientists say no.",
        "Each volcano is fed by its own local supply of magma, deep underground. There's no switch that connects them. Science Focus magazine compared it to every bubble in a fizzy drink reaching the surface at exactly the same moment.",
        "On a normal day, a few dozen volcanoes are erupting somewhere on Earth. In March twenty twenty-two, the Smithsonian's Global Volcanism Program counted forty-eight.",
        "And that's how volcanoes really shape our planet. Slowly. Eruption by eruption. Island by island."]),
    dict(key="outro", scene="vo7_end", lines=[
        "Which brings us back to Iwo Jima. One eruption, three weeks, and about ninety football fields of brand-new land.",
        "Volcanoes can chill the planet, ground every plane, and end an era. But they also build new ground, right in front of us.",
        "So what do you think? Will Iwo Jima's new beach still be there a year from now? Tell me in the comments."],
         hold=1.6, opts=dict(q="STILL THERE IN 2027?")),
]
L1_CH = [("hook", "A volcano just made new land"), ("news", "What happened at Iwo Jima"), ("c0", "The rules"),
         ("c1", "Minute one: the Ring of Fire lights up"), ("c2", "Day one: the ash"), ("c3", "The first month: sulfur"),
         ("c4", "One year: a volcanic winter"), ("c5", "Ten years: the carbon dioxide myth"), ("c6", "The supervolcanoes"),
         ("twist", "It almost happened: the Siberian Traps"), ("why", "Could it really happen?"), ("outro", "Will the new land survive?")]

# =====================================================================  SHORTS
S1 = [  # teaser cut from the long-form
    dict(key="a1", scene="vo7_rules", lines=["What if every volcano on Earth erupted at the same time?"],
         opts=dict(seq=["all"], hook="EVERY VOLCANO AT ONCE?"), sfx=[("rumble", "L0+0.3")]),
    dict(key="a2", scene="vo7_rules", lines=["There are about thirteen hundred and fifty potentially active volcanoes. In a normal year, only forty to fifty erupt."],
         opts=dict(seq=["dots", "year"], badge="≈1,350 VOLCANOES")),
    dict(key="a3", scene="vo7_ash", lines=["Day one, the skies close. In twenty ten, one Icelandic volcano cancelled over a hundred thousand flights.",
                                           "Like and subscribe for more what-ifs."],
         opts=dict(seq=["ash", "europe"], cta=1, badge="100,000+ FLIGHTS")),
    dict(key="a4", scene="vo7_sulfur", lines=["Then the sulfur haze. In nineteen ninety-one, Pinatubo alone cooled the Northern Hemisphere by about half a degree."],
         opts=dict(seq=["pinatubo", "spread"], badge="PINATUBO, 1991")),
    dict(key="a5", scene="vo7_winter", lines=["In eighteen fifteen, Tambora caused a year without a summer. Snow fell in New England in July."],
         opts=dict(seq=["tambora", "snow"], badge="1816: NO SUMMER")),
    dict(key="a6", scene="vo7_winter", lines=["Now imagine all of them at once."], opts=dict(seq=["plunge"], badge="ALL AT ONCE")),
    dict(key="a7", scene="vo7_endshort", lines=["So could it really happen? Full story on the channel."], hold=1.4, opts=dict(top="EVERY VOLCANO AT ONCE?")),
]
S2 = [  # standalone, happening now: Iwo Jima's new land
    dict(key="i1", scene="vo7_iwo", lines=["An island just grew by about a hundred and twenty-five acres."],
         opts=dict(seq=["grow"], hook="THIS ISLAND JUST GREW"), sfx=[("rumble", "L0+0.2")]),
    dict(key="i2", scene="vo7_iwo", lines=["On October twenty-seventh, Japan's weather agency reported an underwater eruption, just off Iwo Jima."],
         opts=dict(seq=["map", "quake"], badge="27 OCTOBER 2026")),
    dict(key="i3", scene="vo7_iwo", lines=["NASA's Landsat nine caught the before and after. October twenty-sixth, then November eleventh."],
         opts=dict(seq=["before", "after"], badge="NASA LANDSAT 9")),
    dict(key="i4", scene="vo7_iwo", lines=["Ash and rock piled up along the southeast beach. On November sixteenth, Japan's Coast Guard confirmed the new land.",
                                           "Like and subscribe for more Earth news."],
         opts=dict(seq=["newland"], cta=1, badge="≈50 HECTARES")),
    dict(key="i5", scene="vo7_iwo", lines=["That's about ninety football fields."], opts=dict(seq=["fields"], badge="≈90 FOOTBALL FIELDS")),
    dict(key="i6", scene="vo7_iwo", lines=["Still unknown: how long it lasts. In twenty twenty-three, waves washed new land here away within weeks."],
         opts=dict(seq=["erode"], badge="STILL UNKNOWN")),
    dict(key="i7", scene="vo7_iwo", lines=["NASA's Daniel Slayback expects this land to wash away within months too. But, he says, we'll have to wait and see."],
         opts=dict(seq=["wait"], badge="WAIT AND SEE")),
    dict(key="i8", scene="vo7_endshort", lines=["Now, what if every volcano erupted at once? Full story on the channel."], hold=1.4,
         opts=dict(top="EVERY VOLCANO AT ONCE?")),
]
S3 = [  # standalone, happening now: animals living inside deep-sea nodules
    dict(key="n1", scene="vo7_nod", lines=["This rock has two hundred and forty-five animals living inside it."],
         opts=dict(seq=["intro"], hook="245 ANIMALS INSIDE A ROCK")),
    dict(key="n2", scene="vo7_nod", lines=["It's a metal nodule from the deep Pacific seafloor. These rocks grow just a few millimeters every million years."],
         opts=dict(seq=["deep", "grow"], badge="4–6 KM DEEP")),
    dict(key="n3", scene="vo7_nod", lines=["This month, scientists reported cracking open two hundred and forty-four nodules. Inside, four thousand one hundred and thirty-nine animals."],
         opts=dict(seq=["crack", "count"], badge="NOVEMBER 2026")),
    dict(key="n4", scene="vo7_nod", lines=["The average nodule held about seventeen. Two hundred and forty-five was the record.",
                                           "Like and subscribe for more ocean science."],
         opts=dict(seq=["record"], cta=1, badge="AVERAGE: 17")),
    dict(key="n5", scene="vo7_nod", lines=["Tiny roundworms and crustaceans, under a millimeter long, live in the cracks. And they differ from the animals in the mud around them."],
         opts=dict(seq=["zoom", "mud"], badge="UNDER 1 MM")),
    dict(key="n6", scene="vo7_nod", lines=["The catch: nodules hold nickel, cobalt and copper, and miners want them. Co-author Sah-bee-nuh Gollner warns mining may mean an irreversible loss of unique life."],
         opts=dict(seq=["mining", "warn"], badge="THE MINING QUESTION")),
    dict(key="n7", scene="vo7_endshort", lines=["Now, what if every volcano erupted at once? Full story on the channel."], hold=1.4,
         opts=dict(top="EVERY VOLCANO AT ONCE?", look="nod")),
]

VIDEOS = {"b7_volcano": L1, "short_b7_volcano": S1, "short_b7_iwojima": S2, "short_b7_nodule": S3}
CHAPTERS = {"b7_volcano": L1_CH}
MUSIC = {"b7_volcano": "volcano", "short_b7_volcano": "volcano_s", "short_b7_iwojima": "volcano_s", "short_b7_nodule": "abyss_s"}
TTS_MAP = {
    "Gah-loong-goong": "Galunggung",
    "Toe-po": "Taupō",
    "Sah-bee-nuh Gollner": "Sabine Gollner",
    "U-S Geological Survey": "US Geological Survey",
    "Landsat nine": "Landsat 9",
    "October twenty-seventh": "October 27",
    "October twenty-sixth": "October 26",
    "November eleventh": "November 11",
    "November sixteenth": "November 16",
    "twenty twenty-three": "2023",
    "nineteen eighty-two": "1982",
    "nineteen ninety-one": "1991",
    "eighteen fifteen": "1815",
    "eighteen sixteen": "1816",
    "one point seven percent": "1.7 percent",
    "thirteen hundred and fifty": "1,350",
    "twelve hundred kilometers": "1,200 kilometers",
    "two hundred and fifty-two million": "252 million",
    "two hundred and forty-five": "245",
    "two hundred and forty-four": "244",
    "four thousand one hundred and thirty-nine": "4,139",
    "seven hundred and thirty thousand": "730,000",
    "twenty-seven thousand": "27,000",
    "a hundred and twenty-five acres": "125 acres",
    "more than four hundred and fifty": "more than 450",
    "forty thousand kilometers": "40,000 kilometers",
    "ninety-six percent": "96 percent",
    "seventy percent": "70 percent",
    "sixty percent": "60 percent",
}

META = {
    "b7_volcano": dict(
        title="What If Every Volcano Erupted at Once?",
        hook=("On 27 October 2026, an underwater eruption off Iwo Jima (Iō Tō, Japan) began building new land: about 50 hectares, "
              "confirmed by Japan's Coast Guard on 16 November and seen by NASA's Landsat 9. One volcano did that. So what if all of Earth's "
              "~1,350 potentially active volcanoes erupted at once? Ash, a sulfur haze, a volcanic winter, the carbon dioxide myth, "
              "supervolcanoes, and the one time something like this really happened."),
        tags=["what if", "volcano", "volcanoes", "every volcano erupted at once", "Iwo Jima", "new island", "Ring of Fire", "volcanic winter",
              "Pinatubo", "Tambora", "year without a summer", "supervolcano", "Yellowstone", "Siberian Traps", "Earth science", "science"],
        hashtags="#whatif #science #earth", parent=None),
    "short_b7_volcano": dict(
        title="What If Every Volcano Erupted at the Same Time? #shorts",
        hook="About 1,350 potentially active volcanoes, all erupting at once: ash, a sulfur haze and a year without a summer.",
        tags=["volcano", "what if", "volcanic winter", "Pinatubo", "Tambora", "Earth science", "shorts"],
        hashtags="#whatif #science #earth", parent="b7_volcano"),
    "short_b7_iwojima": dict(
        title="This Island Just Grew 125 Acres #shorts",
        hook=("On 27 October 2026, Japan's Meteorological Agency reported an underwater eruption off Iwo Jima. By 16 November, Japan's Coast "
              "Guard confirmed about 50 hectares (125 acres) of new land on the island's southeast beach. Will it last?"),
        tags=["Iwo Jima", "Iō Tō", "new island", "volcano", "underwater eruption", "Landsat 9", "NASA Earth Observatory", "Earth news", "shorts"],
        hashtags="#science #earth #volcano", parent="b7_volcano"),
    "short_b7_nodule": dict(
        title="This Rock Has 245 Animals Living Inside It #shorts",
        hook=("A November 2026 study in Scientific Reports dissected 244 deep-sea polymetallic nodules from the Pacific's Clarion-Clipperton Zone "
              "and found 4,139 tiny animals: about 17 per nodule on average, and 245 in the most crowded one."),
        tags=["deep sea", "polymetallic nodules", "meiofauna", "Clarion-Clipperton Zone", "deep-sea mining", "ocean", "marine biology", "science news", "shorts"],
        hashtags="#science #ocean #deepsea", parent="b7_volcano"),
}
