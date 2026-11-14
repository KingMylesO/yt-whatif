"""Batch 02 scene + narration plan (TTS-friendly wording)."""
CARD = 1.9
def card(key, text, label):
    return dict(key=key, scene="card2", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

ROT = "SINCE WOOD STOPPED ROTTING"
A1 = [
    dict(key="hook", scene="a_logfloor", lines=[
        "Every tree that falls in a forest eventually disappears. Fungi, bacteria and insects take it apart, bit by bit, until it's soil again.",
        "But what if they couldn't? What if, starting today, wood could never rot?"], hold=0.3),
    dict(key="title", scene="title2", lines=[], hold=3.2, sfx=[("rumble", 0.0)],
         opts=dict(l1="WHAT IF TREES", l2="COULD NEVER ROT?", motif="log")),
    dict(key="rules", scene="a_rules", lines=[
        "Here are the rules. Leaves still rot. Fruit still rots. Dead animals still rot. Only wood is different.",
        "Every fungus, every microbe and every termite on Earth suddenly loses the ability to break wood down.",
        "That sounds like a small change. A few extra logs on the ground. Some very confused termites."]),
    dict(key="lignin", scene="a_lignin", lines=[
        "But wood is tougher than it looks. It's made of cellulose fibers glued together with a material called lignin, one of the hardest natural substances to break down.",
        "Today, the champions at breaking down lignin are a group called white-rot fungi."]),
    dict(key="carbon", scene="a_carbon", lines=[
        "And wood matters for another reason: it's one of the biggest stores of carbon on land. Rotting is how that carbon gets back into the air.",
        "How big is that? Scientists estimate that dead wood around the world releases about eleven billion tonnes of carbon every year. That's in the same league as all the coal, oil and gas humans burn.",
        "So let's switch rot off, and see what happens."]),
    card("c1d", "DAY 1", ROT),
    dict(key="branch", scene="a_branch", lines=[
        "At first, nothing. A dead branch looks the same today as it did yesterday. That's normal. Wood rots slowly anyway.",
        "But inside the forest, a whole hidden economy just shut down."]),
    dict(key="section", scene="a_logsection", lines=[
        "Fungi that feed on dead wood start to starve. So do wood-boring beetles. Termites can still chew wood, but they rely on microbes in their gut to help digest it. Those microbes just lost the ability.",
        "Those shelf-shaped mushrooms you see growing on logs? They're the fruit of wood-eating fungi. Before long, they'd vanish from every dead tree."]),
    card("c1y", "1 YEAR", ROT),
    dict(key="pile", scene="a_pileup", lines=[
        "After a year, the first thing you'd notice is the mess. Branches, bark and fallen trees pile up on every forest floor, and none of them go anywhere.",
        "Normally, a dead tree is a buffet. Around the world, insects alone handle almost a third of the job. Now the buffet is closed."]),
    dict(key="split", scene="a_split", lines=[
        "How fast wood normally rots depends on where you are. In warm, wet tropical forests, it disappears quickly. That's where more than ninety percent of the carbon from dead wood is released.",
        "In cold northern forests, a big dead trunk can take centuries to vanish, even with rot working normally. Now it never will."]),
    dict(key="nutr", scene="a_nutrients", lines=[
        "And something quieter stops too: recycling. A tree is packed with nutrients like nitrogen and phosphorus. When it rots, those nutrients return to the soil for the next generation of plants.",
        "Without rot, they stay locked inside the dead wood. For good."]),
    card("c10y", "10 YEARS", ROT),
    dict(key="yard", scene="a_lumberyard", lines=[
        "Ten years in, forests start to look like lumber yards.",
        "Seedlings struggle to find light and space under the growing piles of logs. The soil gets poorer every year, because nothing is putting nutrients back."]),
    dict(key="barn", scene="a_barn", lines=[
        "There are some upsides. Wooden houses, fences and decks never rot. Termites stop being a homeowner's nightmare. That old barn your grandparents built? It lasts forever, as long as it doesn't burn down.",
        "Which is the catch. All that dry, dead wood is fuel. A lot of it."]),
    dict(key="fire", scene="a_fire", lines=[
        "So wildfires get bigger and hotter. And here's the strange part: fire becomes the planet's new decomposer.",
        "Burning becomes the main way left to turn wood back into carbon dioxide. Forests that used to rot quietly would now burn loudly."],
         sfx=[("fire", 0.2)]),
    card("c1ky", "1,000 YEARS", ROT),
    dict(key="bury", scene="a_swamp", lines=[
        "Over centuries, a lot of that wood never burns. It falls into swamps and rivers and gets buried under mud.",
        "And buried wood is carbon taken out of the sky. Year after year, carbon dioxide levels start to drop."]),
    dict(key="graph", scene="a_graph", lines=[
        "Less carbon dioxide means a weaker greenhouse effect. The planet slowly cools.",
        "At the same time, something unexpected happens to the air you breathe. Plants release oxygen as they grow. Rotting uses oxygen up. Take rotting away, and oxygen slowly builds up in the atmosphere."]),
    card("c1my", "1,000,000 YEARS", ROT),
    dict(key="coal", scene="a_coal", lines=[
        "Give it a million years, and that buried wood gets squeezed and heated deep underground.",
        "It turns into coal.",
        "Huge seams of it, under old swamps all over the world. The planet keeps cooling, maybe enough for ice sheets to spread from the poles. And oxygen keeps rising."]),
    dict(key="oxy", scene="a_oxygen", lines=[
        "With more oxygen, insects can grow bigger, because they don't have lungs. They breathe through tiny tubes, and richer air reaches deeper into a bigger body.",
        "Fires burn hotter and spread more easily. At high enough oxygen, even wet plants can catch fire.",
        "A colder world, rich in oxygen, full of giant insects, sitting on top of coal.",
        "Sounds made up.", "Except it isn't."], hold=0.3),
    dict(key="twist", scene="a_carbswamp", lines=[
        "Between about three hundred and sixty and three hundred million years ago, Earth went through a period called the Carboniferous. It's literally named after coal. Most of the coal that powered the Industrial Revolution formed back then.",
        "During that time, oxygen in the air may have climbed to around thirty to thirty-five percent. Today it's twenty-one.",
        "Insects got enormous. A dragonfly-like insect called Meganeura had wings about seventy centimeters across. Roughly the size of a pigeon."],
         sfx=[("scratch", 0.0)]),
    dict(key="giants", scene="a_giants", lines=[
        "Relatives of millipedes called Arthropleura grew more than two meters long. And the trees were strange too. Some of the biggest were giant relatives of today's tiny club mosses, called lycopsids, standing thirty to forty meters tall.",
        "Fires were everywhere. In some coal from that era, up to seventy percent of the material is fossil charcoal, a sign of frequent, intense fires."]),
    dict(key="ice", scene="a_icearth", lines=[
        "And carbon dioxide fell so low that ice sheets spread across the southern continents. One climate modeling study found that Earth came close to freezing over completely.",
        "So why did all that wood get buried instead of rotting?"]),
    dict(key="fungi", scene="a_fungitree", lines=[
        "For years, the favorite answer went like this. The trees came first, and the fungi came later. Trees had evolved lignin, the tough material that makes wood woody. But for millions of years, the theory goes, nothing could fully break it down.",
        "In twenty twelve, a big genetic study of thirty-one fungi suggested that the ability to digest lignin appeared around the end of the Carboniferous. Right when coal formation slowed down.",
        "One fungus changed the planet. It's a perfect story.",
        "And it might be wrong."], hold=0.3),
    dict(key="real", scene="a_bark", lines=[
        "In twenty sixteen, another team of scientists pushed back. They pointed out that many of the swamp plants that made the coal had very little lignin to begin with. Those giant lycopsids were up to eighty percent bark, a thick kind of bark that doesn't exist in any plant alive today.",
        "Fossil wood from the Carboniferous already shows signs of fungal decay. And coal kept piling up at the same rate whether the swamps were full of woody plants or not."]),
    dict(key="pangea", scene="a_pangea", lines=[
        "Their explanation is geography. At the time, the continents were crashing together into one supercontinent called Pangea. Near the equator, that created huge, sinking basins in a constantly wet climate.",
        "Dead plants fell into waterlogged swamps, where rotting slows to a crawl, and got buried before they could decay.",
        "So the trees didn't stop rotting. They got buried faster than they could rot.",
        "Scientists still argue about how much each factor mattered. But the bigger lesson isn't in doubt. When carbon gets buried, the planet cools. When it comes back out, the planet warms.",
        "That's why this old story still matters. Coal is buried carbon. Burning it returns carbon to the air that took millions of years to lock away, in just a couple of centuries."]),
    dict(key="outro", scene="a_logfloor", lines=[
        "So next time you see a mushroom on a dead log, remember: it's doing one of the most important jobs on Earth.",
        "And when we burn coal, we're releasing sunlight that swamp forests captured three hundred million years ago."],
         opts=dict(outro=True), hold=0.5),
    dict(key="end", scene="end2", lines=[
        "What do you think: would you rather live with rot, or with dragonflies the size of pigeons? Tell me in the comments."],
         hold=11.0, opts=dict(q="ROT OR GIANT BUGS?", motif="log")),
]
A1_CH = [("hook", "Wood that never rots"), ("rules", "The setup"), ("c1d", "Day 1"), ("c1y", "1 year: the mess"),
         ("c10y", "10 years: lumber-yard forests"), ("c1ky", "1,000 years: buried carbon"), ("c1my", "1 million years: coal"),
         ("twist", "The twist: the Carboniferous"), ("fungi", "The fungus theory"), ("real", "The real twist"), ("outro", "Outro")]

SL = "SINCE THE ASTEROID (30 S LATE)"
B1 = [
    dict(key="hook", scene="b_plain", lines=[
        "Sixty-six million years ago, a rock about ten kilometers wide hit Earth and ended the age of the dinosaurs.",
        "But some scientists think the real killer wasn't just the size of the rock. It was where it landed.",
        "If it had arrived thirty seconds later, you might not exist."], hold=0.3),
    dict(key="title", scene="title2", lines=[], hold=3.2, sfx=[("rumble", 0.0)],
         opts=dict(l1="WHAT IF THE ASTEROID", l2="WAS 30 SECONDS LATE?", motif="asteroid")),
    dict(key="rules", scene="b_orbit", lines=[
        "Here are the rules. Same asteroid. Same speed. Same path through space. The only difference: it shows up thirty seconds late."]),
    dict(key="scale", scene="b_everest", lines=[
        "For scale: the asteroid is about ten kilometers wide. Set it down on the ground, and it would stand taller than Mount Everest. And it was moving more than ten times faster than a rifle bullet."]),
    dict(key="earthmove", scene="b_orbit", lines=[
        "Thirty seconds sounds like nothing. But Earth is moving. It travels around the Sun at about thirty kilometers per second, and it's spinning at the same time.",
        "In thirty seconds, the whole planet moves roughly nine hundred kilometers along its orbit. So a late asteroid hits a different spot."],
         opts=dict(move=True)),
    dict(key="gulick", scene="b_gulfmap", lines=[
        "One of the geologists who led the drilling into the real crater has said that if it had struck about thirty seconds earlier or later, it would likely have landed in deep ocean.",
        "Not everyone agrees on the exact numbers. But scientists on both sides of the debate agree on one thing: the asteroid hit an unusually bad spot.",
        "To see why, let's look at what really happened."]),
    card("c66", "66 MILLION YEARS AGO", "THE REAL TIMELINE"),
    dict(key="impact", scene="b_impact", lines=[
        "The asteroid slammed into a shallow sea at the edge of what's now Mexico's Yucatán Peninsula, near a town called Cheek-shoo-loob.",
        "It released more than a billion times the energy of the atomic bombs dropped on Hiroshima and Nagasaki combined."],
         sfx=[("boom", 1.0)]),
    dict(key="crater", scene="b_crater", lines=[
        "It punched a crater about a hundred and eighty kilometers across. About twenty seconds after impact, the hole was already around thirty kilometers deep.",
        "Within minutes, the shattered rock rebounded into a ring of mountains inside the crater.",
        "Wildfires broke out on nearby land. A tsunami raced outward, then washed back into the crater, all within the first day."]),
    dict(key="rocks", scene="b_layers", lines=[
        "But the crater wasn't the worst part. The rocks it hit were.",
        "That seafloor was full of gypsum and other rock rich in sulfur, plus carbon-rich sediments. The impact blasted them into the sky."]),
    dict(key="haze", scene="b_haze", lines=[
        "The sulfur formed a haze of tiny droplets that reflected sunlight back into space. Soot added to the darkness.",
        "One study estimated the cooling at around eight to eleven degrees Celsius worldwide, and even more on land."]),
    dict(key="collapse", scene="b_collapse", lines=[
        "Sunlight dropped. Rain dropped. Plants stopped growing, on land and in the sea. And food chains collapsed from the bottom up.",
        "About three quarters of all species went extinct. Every dinosaur that couldn't fly. The flying pterosaurs. The giant marine reptiles. The ammonites."]),
    dict(key="spot", scene="b_globe13", lines=[
        "In twenty seventeen, two Japanese researchers mapped which parts of Earth's surface, back then, had enough carbon-rich rock to create that much soot.",
        "Their answer: only about thirteen percent.",
        "Hit anywhere in the other eighty-seven percent, they argue, and the mass extinction probably wouldn't have happened.",
        "Not everyone agrees with their math. Some scientists think sulfur, not soot, did most of the damage. But even the critics agree: there are only a few places on Earth where an asteroid like this could cause that much climate chaos. And Cheek-shoo-loob was one of them."]),
    dict(key="others", scene="b_othercraters", lines=[
        "Here's a hint that location matters. Big asteroids have hit Earth since then. One left a crater under Chesapeake Bay in the United States. Another left one in southern Germany.",
        "Neither caused a mass extinction. Most likely, they just didn't hit the right mix of rock.",
        "So let's run the other timeline. The asteroid is thirty seconds late, and it lands in deep ocean."]),
    card("c0", "0 SECONDS", SL),
    dict(key="ocean", scene="b_oceanimpact", lines=[
        "It's still a catastrophe. The asteroid punches through kilometers of water and into the seafloor. A giant column of steam and rock blasts into the sky. Monster tsunamis race across the ocean.",
        "If you were anywhere nearby, this is still the worst day imaginable."], sfx=[("boom", 2.0)]),
    card("c1y", "1 YEAR", SL),
    dict(key="year", scene="b_skyclear", lines=[
        "But this time, much of what goes up is water vapor and ordinary seafloor rock, not a sky full of sulfur and soot.",
        "In this scenario, the sky darkens for a while, and the planet cools, but nowhere near as much. Forests survive. Plankton survive. The food chain bends, but it doesn't break.",
        "Some species still die out. It's a terrible year. But not the end of an era."]),
    dict(key="deccan", scene="b_deccan", lines=[
        "There's one wild card. Around the same time, giant volcanic eruptions called the Deccan Traps were pouring out lava in what's now India, in pulses spread over hundreds of thousands of years.",
        "Some scientists think they stressed life too. But a twenty twenty study using climate models found that the asteroid alone was enough to wipe out every dinosaur that wasn't a bird. The volcanoes may even have helped life recover afterward.",
        "So in this timeline, the volcanoes alone might not be enough to end the dinosaurs."]),
    card("c1m", "1,000,000 YEARS", SL),
    dict(key="million", scene="b_mammals", lines=[
        "Dinosaurs keep doing what they'd done for well over a hundred million years: running the planet.",
        "Mammals keep doing what they'd done the whole time: staying small, staying hidden, and mostly coming out at night.",
        "In the real timeline, the extinction opened a door. With the big dinosaurs gone, mammals spread into every empty space. Some got huge. Some returned to the sea and became whales. Some climbed trees and became primates.",
        "In this timeline, that door stays shut."]),
    card("c66m", "66,000,000 YEARS", SL),
    dict(key="today", scene="b_today", lines=[
        "Fast forward to today. What does Earth look like?",
        "Honestly, nobody knows. Evolution doesn't follow a script. Other disasters might have happened. Dinosaurs might have changed into things we'd never recognize.",
        "But one thing seems likely: it wouldn't look like our world. And there's a real chance the branch of mammals that led to you never gets its big break.",
        "No primates. No people. Nobody around to make videos about asteroids."]),
    dict(key="twist", scene="b_birds", lines=[
        "But here's the thing. The dinosaurs didn't all die.",
        "Birds are dinosaurs. Not cousins of dinosaurs. Actual dinosaurs, from the same big family as tee rex.",
        "When the asteroid hit, a few small, beaked, feathered dinosaurs made it through. Today there are more than eleven thousand species of them. In fact, a tee rex is more closely related to a chicken than to any lizard alive today.",
        "So the asteroid didn't really end the age of dinosaurs. It made them smaller and gave them wings."],
         sfx=[("chirp", 0.2)]),
    dict(key="origin", scene="b_jupiter", lines=[
        "And the asteroid itself? A twenty twenty-four study of the metal it left behind suggests it was a carbon-rich type that formed out beyond Jupiter. It may have spent time parked in the asteroid belt before heading our way.",
        "Rocks this size are thought to hit Earth very roughly once every hundred million years, maybe even less often. The dinosaurs were around for more than a hundred and sixty million years.",
        "This one just happened to find one of the worst spots on the planet."]),
    dict(key="dart", scene="b_dart", lines=[
        "And for the first time in Earth's history, a species living here could do something about it. In twenty twenty-two, NASA crashed a spacecraft called DART into a small asteroid named Dimorphos, and changed its orbit by thirty-two minutes.",
        "Give a dangerous rock a nudge early enough, and a direct hit becomes a near miss.",
        "Thirty seconds, it turns out, is something we might one day be able to give ourselves."]),
    dict(key="outro", scene="b_plain", lines=[
        "So the next time someone says you're lucky to be alive, they have no idea.",
        "Your existence might come down to thirty seconds that never happened."], opts=dict(outro=True), hold=0.5),
    dict(key="end", scene="end2", lines=[
        "What do you think: if the dinosaurs had survived, would one of them have become smart? Tell me in the comments."],
         hold=11.0, opts=dict(q="WOULD DINOSAURS GET SMART?", motif="asteroid")),
]
B1_CH = [("hook", "The worst possible spot"), ("rules", "The setup: 30 seconds late"), ("c66", "What actually happened"),
         ("spot", "The unlucky spot"), ("c0", "0 seconds: the ocean impact"), ("c1y", "1 year"), ("c1m", "1 million years"),
         ("c66m", "Today"), ("twist", "The twist: birds"), ("dart", "Could we stop the next one?"), ("outro", "Outro")]

DRY = "SINCE GIBRALTAR CLOSED"
C1 = [
    dict(key="hook", scene="c_harbor", lines=[
        "Right now, the Mediterranean Sea is losing water. Every year, the Sun evaporates more of it than all its rivers and rain can put back.",
        "The only thing keeping it full is a gap between Spain and Morocco, about fourteen kilometers wide.",
        "So what happens if that gap closes?"], hold=0.3),
    dict(key="title", scene="title2", lines=[], hold=3.2, sfx=[("rumble", 0.0)],
         opts=dict(l1="WHAT IF THE MEDITERRANEAN", l2="DRIED UP?", motif="sea")),
    dict(key="setup", scene="c_strait", lines=[
        "The Strait of Gibraltar is the Mediterranean's lifeline. At the surface, Atlantic water pours in, all day, every day. Deeper down, saltier, heavier Mediterranean water flows out.",
        "Because so much evaporates, the Mediterranean is noticeably saltier than the Atlantic. And the strait is shallow: in places, the seafloor is only about three hundred meters down. Raise that seafloor a few hundred meters, and the door closes.",
        "The sea is so big that even with all that flow, it takes something like a century for its water to be completely replaced.",
        "That inflow is strong. During World War Two, some German submarines slipped into the Mediterranean by switching off their engines and drifting in on the current, so they were harder to detect."]),
    dict(key="rules", scene="c_wall", lines=[
        "Here are the rules. Overnight, the strait seals shut. Solid rock from Spain to Morocco. No more Atlantic water. Everything else stays the same."],
         sfx=[("grind", 0.8)]),
    card("c1d", "DAY 1", DRY),
    dict(key="day1", scene="c_budget", lines=[
        "Nothing seems to happen. The Mediterranean holds about three point seven million cubic kilometers of water. Losing a little doesn't show.",
        "But the math has already turned against it.",
        "Evaporation pulls out far more water than rivers, rain and the Black Sea put back. Today, the Atlantic covers the difference: roughly a thousand cubic kilometers of water a year. Now that's gone.",
        "The Black Sea keeps leaking in through the narrow straits at Istanbul. Rivers like the Nile and the Rhône keep flowing. But together, they can't keep up."]),
    card("c1y", "1 YEAR", DRY),
    dict(key="year", scene="c_harborwall", lines=[
        "After a year, the sea is down by around forty centimeters. Satellites that track sea level down to the millimeter would spot it right away. You'd notice it on harbor walls too. Boats sit a little lower against the docks.",
        "And the water left behind gets saltier, because evaporation takes the water but leaves the salt."], opts=dict(drop=0.4)),
    card("c10y", "10 YEARS", DRY),
    dict(key="ten", scene="c_harborwall", lines=[
        "Ten years in, the sea is down about four meters. Beaches stretch out dozens of meters. Harbors need constant digging just to stay usable. Coastal wetlands dry out.",
        "Fish and corals struggle as the water gets saltier year after year."], opts=dict(drop=4)),
    dict(key="suez", scene="c_suez", lines=[
        "Down in Egypt, something odd happens at the Suez Canal. It has no locks. As the Mediterranean drops, Red Sea water starts flowing north through it.",
        "But compared to what the sea is losing, the canal is a garden hose."]),
    card("c100y", "100 YEARS", DRY),
    dict(key="century", scene="c_map", lines=[
        "After a century, the sea has dropped about forty meters. Shallow areas, like the northern Adriatic, start turning into dry land. Venice's lagoon becomes a salt flat.",
        "Coastal cities that were built for trade by sea now find the sea has walked away from them. Islands grow. Ferry ports that ran for centuries now look out over mudflats."],
         opts=dict(stage=1)),
    card("c1ky", "1,000 YEARS", DRY),
    dict(key="thousand", scene="c_map", lines=[
        "Over thousands of years, the Mediterranean keeps falling, by hundreds of meters and eventually more. Estimates for how long it would take to mostly dry out range from about a thousand years to several thousand.",
        "Every drop that evaporates leaves its salt behind. Dry the sea out once, and the floor ends up under a layer of salt tens of meters thick.",
        "Eventually, the sea splits in two, east and west, separated by a land bridge running from Italy through Sicily toward Africa. What's left is a string of shrinking, super-salty lakes, like a chain of Dead Seas."],
         opts=dict(stage=2)),
    dict(key="basin", scene="c_basin", lines=[
        "The floor of the basin sits kilometers below sea level. Today, the lowest dry land on Earth is the shore of the Dead Sea, about four hundred and thirty meters below sea level. A dried-out Mediterranean would go kilometers deeper than that.",
        "Air gets warmer as it sinks and compresses, so down there it would be brutally hot. A salt desert, kilometers below the old shoreline."]),
    dict(key="world", scene="c_world", lines=[
        "And here's the part most people don't expect. All that evaporated water doesn't vanish. Most of it ends up in the world's other oceans. Spread across the planet, it's enough to raise global sea level by around ten meters.",
        "So drying up the Mediterranean would flood coastlines everywhere else."]),
    dict(key="twist", scene="c_saltdesert", lines=[
        "This isn't just a thought experiment. It happened.",
        "About six million years ago, the slow collision between Africa and Europe cut the Mediterranean off from the Atlantic. Scientists call what followed the Messinian Salinity Crisis."],
         sfx=[("scratch", 0.0)]),
    dict(key="drill", scene="c_drill", lines=[
        "In nineteen seventy, a drilling ship pulled up cores from deep under the Mediterranean seafloor. Inside were thick layers of salt and gypsum.",
        "And in one core, deep-sea mud that had dried to dust and been blown around by sandstorms. Sandstorms. At the bottom of the sea."]),
    dict(key="salt", scene="c_saltlayer", lines=[
        "Today we know the Mediterranean seafloor holds about a million cubic kilometers of salt, in places up to three kilometers thick.",
        "And it didn't happen just once. That's far too much salt for a single drying. The sea seems to have dried out and partly refilled again and again, as the link to the Atlantic opened and closed.",
        "Rivers like the Nile and the Rhône chased the falling sea downward and carved canyons on the scale of the Grand Canyon. They're buried under sediment now."]),
    dict(key="debate", scene="c_gauge", lines=[
        "Scientists still debate exactly how dry it got. A twenty twenty-four study suggests the sea level dropped by about two kilometers in the east and almost a kilometer in the west, and the Mediterranean lost up to seventy percent of its water.",
        "Life took a hit too. Many marine species disappeared from the Mediterranean during the crisis. When the sea came back, new ones moved in from the Atlantic."]),
    card("cflood", "5.33 MILLION YEARS AGO", "THE ATLANTIC RETURNS"),
    dict(key="flood", scene="c_flood", lines=[
        "Then, about five point three three million years ago, the Atlantic broke back in.",
        "One model of what happened next is wild. Water poured through Gibraltar at around a hundred million cubic meters per second. That's about a thousand times the flow of the Amazon River. Enough to fill Lake Geneva in about fifteen minutes.",
        "At its peak, the Mediterranean may have risen more than ten meters a day. That's a three-story building's worth of water, every single day.",
        "In that model, about ninety percent of the sea refilled in somewhere between a few months and two years."],
         sfx=[("roar", 1.0)]),
    dict(key="channel", scene="c_channel", lines=[
        "The flood carved a channel about two hundred kilometers long across the strait. Scientists spotted it while studying the seafloor for a proposed tunnel between Spain and Morocco.",
        "And it probably wasn't a giant waterfall. The water most likely rushed down a long, gentle slope. Picture the biggest rapids imaginable, kilometers wide.",
        "As the Mediterranean filled back up, that model suggests global sea level dropped by roughly ten meters.",
        "Other scientists think the refill was slower, or came in pulses. But if the fast version holds up, it would be the largest known flood in Earth's history."]),
    dict(key="again", scene="c_africa", lines=[
        "Africa is still slowly pushing north into Europe. Some geologists think the strait could close again one day, millions of years from now.",
        "Don't cancel your beach trip, though. On human timescales, the Mediterranean is safe. But on Earth's timescale, seas come and go.",
        "So the Mediterranean you swim in has done this before. And it may do it again."]),
    dict(key="outro", scene="c_dive", lines=[
        "Next time you float in the Mediterranean, remember: underneath you is a layer of salt kilometers thick, left behind by a sea that disappeared."], hold=0.6),
    dict(key="end", scene="end2", lines=[
        "What do you think: if the Mediterranean dried up, which city would you miss being a beach town? Tell me in the comments."],
         hold=11.0, opts=dict(q="WHICH BEACH WOULD YOU MISS?", motif="sea")),
]
C1_CH = [("hook", "The sea that's always draining"), ("setup", "The setup: Gibraltar"), ("c1d", "Day 1"), ("c1y", "1 year"),
         ("c10y", "10 years"), ("c100y", "100 years"), ("c1ky", "1,000 years: a salt desert"), ("twist", "The twist: it happened"),
         ("cflood", "The biggest flood on Earth?"), ("again", "Could it happen again?"), ("outro", "Outro")]

# ---------------- Shorts ----------------
A2 = [
    dict(key="s1", scene="a_logfloor", lines=["What if dead trees never rotted? Not ever."], opts=dict(hook="DEAD TREES NEVER DISAPPEAR…", frozen=True)),
    dict(key="s2", scene="a_pileup", lines=["Forests fill up with logs that never go away."]),
    dict(key="s3", scene="a_nutrients", lines=["The nutrients inside them stay locked up, so new trees starve."]),
    dict(key="s4", scene="a_swamp", lines=["Buried wood pulls carbon out of the air, and the planet slowly cools."]),
    dict(key="s5", scene="a_oxygen", lines=["Oxygen builds up. Bugs get huge. Fires get wild."]),
    dict(key="s6", scene="a_carbswamp", lines=["And here's the wild part: something like this may have happened three hundred million years ago. It's a big part of where coal comes from."]),
    dict(key="s7", scene="end_short2", lines=["But the real reason is still a fight among scientists. Full story on the channel."], hold=1.4,
         opts=dict(top="WHAT REALLY HAPPENED?", motif="log")),
]
A3 = [
    dict(key="o1", scene="a_gauge", lines=["Right now, the air you're breathing is twenty-one percent oxygen. What if it were thirty-five?"],
         opts=dict(hook="35% OXYGEN", o2=(21, 21))),
    dict(key="o2", scene="a_oxygen", lines=["First, bugs get big. Insects don't have lungs. They breathe through tiny tubes, and richer air reaches deeper into a bigger body."],
         opts=dict(badge="BUGS", bugs_only=True)),
    dict(key="o3", scene="a_fire", lines=["Second, fire. Above about twenty-five percent oxygen, scientists think dry forests would burn so often they'd struggle to grow back. Around thirty-five, even soaking-wet plants could catch fire."],
         opts=dict(badge="FIRE"), sfx=[("fire", 0.1)]),
    dict(key="o4", scene="a_carbswamp", lines=["And this isn't made up. Around three hundred million years ago, oxygen may have reached thirty to thirty-five percent. A dragonfly-like insect called Meganeura had wings about seventy centimeters wide."],
         opts=dict(badge="300 MILLION YEARS AGO")),
    dict(key="o5", scene="a_fire", lines=["Giant bugs, and a planet that's always on fire."], opts=dict(bugs=True)),
    dict(key="o6", scene="end_short2", lines=["Want to know how Earth got that much oxygen? Full story on the channel."], hold=1.4,
         opts=dict(top="WHERE DID IT COME FROM?", motif="log")),
]
B2 = [
    dict(key="t1", scene="b_plain", lines=["Sixty-six million years ago, an asteroid wiped out the dinosaurs. But it hit a really unlucky spot."],
         opts=dict(hook="30 SECONDS LATE…")),
    dict(key="t2", scene="b_layers", lines=["It slammed into a shallow sea full of sulfur-rich rock, and blasted a haze into the sky that dimmed the Sun for years."]),
    dict(key="t3", scene="b_gulfmap", lines=["One scientist who drilled into the crater said that thirty seconds earlier or later, it would likely have hit deep ocean instead."]),
    dict(key="t4", scene="b_skyclear", lines=["Less sulfur. Less soot. Maybe no mass extinction."]),
    dict(key="t5", scene="b_mammals", lines=["Dinosaurs keep ruling. And mammals like us might never get our chance."], opts=dict(short=True)),
    dict(key="t6", scene="end_short2", lines=["Full story on the channel."], hold=1.6, opts=dict(top="WHAT IF IT MISSED?", motif="asteroid")),
]
B3 = [
    dict(key="m1", scene="b_movie", lines=["In movies, flying through an asteroid belt means dodging rocks every second."], opts=dict(hook="MOVIES LIED TO YOU")),
    dict(key="m2", scene="b_emptybelt", lines=["In real life? The average distance between asteroids is around a million kilometers. That's about two and a half times the distance from Earth to the Moon."]),
    dict(key="m3", scene="b_probe", lines=["NASA's Lucy spacecraft flew through the belt on its way to Jupiter, and never had to fire its thrusters to dodge anything. Getting close to even one asteroid actually takes careful planning."]),
    dict(key="m4", scene="b_beltmass", lines=["And if you put every asteroid together, they'd weigh only about three to four percent of our Moon. About a third of that is a single dwarf planet: Ceres."]),
    dict(key="m5", scene="b_emptybelt", lines=["So the real asteroid belt isn't a minefield. It's more like a desert, with rocks scattered across unimaginable distances."], opts=dict(wide=True)),
    dict(key="m6", scene="end_short2", lines=["Want to see what happens when one actually hits Earth? Full story on the channel."], hold=1.4,
         opts=dict(top="WHEN ONE HITS…", motif="asteroid")),
]
C2 = [
    dict(key="d1", scene="c_harbor", lines=["The Mediterranean loses more water to evaporation than its rivers and rain can replace."], opts=dict(hook="THE MEDITERRANEAN VANISHED.")),
    dict(key="d2", scene="c_strait", lines=["The only thing keeping it full is the Atlantic, pouring in through a gap about fourteen kilometers wide."]),
    dict(key="d3", scene="c_map", lines=["Close that gap, and the sea starts to shrink. Over thousands of years, most of it could evaporate."], opts=dict(stage=3)),
    dict(key="d4", scene="c_world", lines=["And all that water ends up in the other oceans, raising global sea level by around ten meters."]),
    dict(key="d5", scene="c_saltdesert", lines=["This actually happened, about six million years ago. Then the Atlantic broke back in, in what may have been the biggest flood in Earth's history."]),
    dict(key="d6", scene="end_short2", lines=["Full story on the channel."], hold=1.6, opts=dict(top="THE BIGGEST FLOOD EVER?", motif="sea")),
]
C3 = [
    dict(key="g1", scene="c_amoc", lines=["There's a giant system of currents in the Atlantic. It carries warm water north, then sinks and sends cold water back south. Scientists call it the A-M-O-C."],
         opts=dict(hook="EUROPE'S HEATING, SWITCHED OFF")),
    dict(key="g2", scene="c_amoc", lines=["It helps keep northwestern Europe surprisingly mild."], opts=dict(warm=True)),
    dict(key="g3", scene="c_amocoff", lines=["What if it shut down? A twenty twenty-five study simulated it, in a world already two degrees warmer. Winter sea ice reached the coasts of Britain and Scandinavia, and cold snaps in London hit minus twenty degrees Celsius."],
         opts=dict(badge="IF IT SHUT DOWN")),
    dict(key="g4", scene="c_rainbelt", lines=["The tropical rain belts shifted, weakening monsoons that hundreds of millions of people depend on. And sea levels rose faster along the US East Coast."]),
    dict(key="g5", scene="c_amocgauge", lines=["The UN's climate panel says the current will very likely weaken this century, with medium confidence that it won't collapse before twenty-one hundred. Some newer studies think the risk is higher."],
         opts=dict(badge="COULD IT HAPPEN?")),
    dict(key="g6", scene="end_short2", lines=["Want to see what happens when a whole sea disappears? Full story on the channel."], hold=1.4,
         opts=dict(top="WHEN A SEA DISAPPEARS…", motif="sea")),
]

VIDEOS = {"b2_trees": A1, "b2_asteroid": B1, "b2_med": C1,
          "short_b2_wood": A2, "short_b2_oxygen": A3, "short_b2_30s": B2, "short_b2_belt": B3,
          "short_b2_med": C2, "short_b2_amoc": C3}
CHAPTERS = {"b2_trees": A1_CH, "b2_asteroid": B1_CH, "b2_med": C1_CH}
