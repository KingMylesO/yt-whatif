"""Batch 04 (one-off TECH batch) scene + narration plan (TTS-friendly wording).

Long-form: b4_tubes (no transistor: a vacuum-tube world), b4_shrink (shrink inside a chip), b4_cosmic (cosmic ray flips a bit).
Shorts: teaser + standalone per long-form, plus short_b4_blackout (-> tubes) and short_b4_moore (-> shrink).
Scene prefixes: t_ = scenes_b4_tubes.py, c_ = scenes_b4_chip.py, k_ = scenes_b4_cosmic.py.
TTS spellings are mapped back for captions in meta2.tts_to_text.
"""
CARD = 1.9

def card(key, text, label, scene):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  A. NO TRANSISTOR (vacuum-tube world)
TL = "IN A WORLD WITHOUT TRANSISTORS"
A1 = [
    dict(key="hook", scene="t_phone", lines=[
        "The chip inside a recent iPhone, Apple's A seventeen Pro, holds about nineteen billion transistors.",
        "Each one is a microscopic switch, flicking on and off billions of times a second. Together, they run everything you do on that phone.",
        "Now imagine the transistor was never invented. Every one of those switches has to be a glowing glass vacuum tube. What does your world look like?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="t_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF THE TRANSISTOR", l2="WAS NEVER INVENTED?")),
    dict(key="rules", scene="t_tube", lines=[
        "First, the rules. Everything else in history stays the same. Electricity, radio, the light bulb. We just never learn to make a switch out of a solid crystal.",
        "So we're stuck with the vacuum tube. It's a glass bulb with the air pumped out. Inside, a hot filament boils electrons off a metal surface, and they fly across the vacuum to a metal plate.",
        "In between sits a fine wire mesh, called a grid. Put a small voltage on the grid, and you control a much bigger current. That's an amplifier. Or a switch. The same job a transistor does today.",
        "The first tube that could amplify like this, the Audion, was invented by Lee de Forest in nineteen-oh-six. It made long-distance phone calls and radio broadcasting possible. So in our world, the twentieth century still crackles with radio."]),
    card("c46", "1946", TL, "t_card"),
    dict(key="eniac", scene="t_eniac", lines=[
        "During World War Two, the Colossus machines at Bletchley Park in Britain used about two and a half thousand tubes each to help crack German codes.",
        "And for a while, that really is how computers were built. In nineteen forty-six, the U.S. Army's Eh-nee-ack was unveiled at the University of Pennsylvania. It had around seventeen and a half thousand vacuum tubes, and about five million hand-soldered joints.",
        "It weighed about thirty tons, and drew around a hundred and fifty kilowatts. That's like a hundred electric kettles boiling at the same time, all day.",
        "In return, it could do about five thousand additions a second. Its first programmers were six women, who learned the machine from its wiring diagrams, and programmed it by plugging cables and setting switches by hand."]),
    dict(key="burnout", scene="t_burnout", lines=[
        "There was one big problem. Tubes burn out, just like light bulbs. Early on, Eh-nee-ack lost several tubes almost every day, and was out of action about half the time.",
        "Most failures happened while the tubes were warming up or cooling down, so the trick was to switch the machine off as little as possible.",
        "Even with sturdier tubes, one still failed about every two days. Engineers became experts at hunting down the dead one."]),
    dict(key="univac", scene="t_univac", lines=[
        "Five years later, UNIVAC One went to work at the U.S. Census Bureau. It was one of the first computers sold commercially, and it still needed about five thousand tubes.",
        "Computers in this world are rare, enormous and expensive. And each one needs a room, a power line, and a team to keep it alive."]),
    card("c47", "DECEMBER 1947", TL, "t_card"),
    dict(key="bell", scene="t_bell", lines=[
        "In our real history, everything changed in December nineteen forty-seven. At Bell Labs in New Jersey, John Bardeen and Walter Brattain pressed two gold contacts onto a slab of germanium, and the crystal amplified a signal.",
        "It was the first transistor. They showed it to their bosses two days before Christmas. Bardeen, Brattain and William Shockley later shared the Nobel Prize in Physics for it.",
        "That same year, engineers at Harvard found a moth stuck inside their relay computer, and taped it into the logbook as the first actual case of a bug being found.",
        "In our what-if, that December day never comes. The germanium stays a lab curiosity. And the tube keeps its crown."]),
    card("c55", "1955", TL, "t_card"),
    dict(key="radio", scene="t_radio", lines=[
        "In the real nineteen-fifties, transistors spread fast. The first transistor radio went on sale in the U.S. in nineteen fifty-four, for forty-nine dollars and ninety-five cents. Music you could carry in your pocket.",
        "Hearing aids changed even faster. The first all-transistor hearing aid came out in nineteen fifty-three. A year later, ninety-seven percent of hearing aids used only transistors.",
        "In the tube world, none of that happens. Radios stay as big as a loaf of bread, need time to warm up, and live next to a wall socket. Hearing aids stay bulky."]),
    card("c69", "1969", TL, "t_card"),
    dict(key="apollo", scene="t_apollo", lines=[
        "Then comes the race to the Moon. The real Apollo Guidance Computer was one of the first computers built from integrated circuits: about two thousand eight hundred tiny chips, each holding two simple logic gates.",
        "No transistors means no integrated circuits. A tube computer that could do the same job would be far heavier and hungrier for power than anything you'd want to squeeze into a spacecraft.",
        "Getting to the Moon wouldn't be impossible. But it would be a lot harder, and the ground crew would have to do far more of the thinking."]),
    card("cnow", "TODAY", TL, "t_card"),
    dict(key="calc", scene="t_phonecalc", lines=[
        "Now let's jump to today, and try to rebuild just one phone chip with tubes.",
        "Eh-nee-ack's power bill works out to roughly eight and a half watts per tube. Multiply that by nineteen billion tubes, and you need around a hundred and sixty gigawatts.",
        "That's in the range of a hundred and sixty large power plants. For one phone.",
        "Size? Even a small tube is about the size of your thumb. Nineteen billion of them would fill roughly a hundred and fifty Olympic swimming pools.",
        "And at Eh-nee-ack's best failure rate, more than six of those tubes would burn out every single second."],
         opts=dict(mode="full")),
    dict(key="world", scene="t_world", lines=[
        "So in the tube world, computers stay giant and rare. Governments and big companies own a few, in air-conditioned halls. Nobody has one at home.",
        "No laptops. No smartphones. Probably no internet as we know it, and no map in your pocket.",
        "Television and radio still exist. Tubes handled those just fine. But a pocket calculator? A digital watch? A video game console? Almost certainly not.",
        "Even the night would look different. Cities would hum, and machine rooms would glow orange from thousands of hot filaments."]),
    card("cstill", "TUBES TODAY", TL, "t_card"),
    dict(key="still", scene="t_still", lines=[
        "But here's the thing. Tubes never fully died. Your microwave oven heats food with a magnetron, which is a kind of vacuum tube. Medical X-ray machines make their rays in a tube.",
        "And plenty of guitarists still swear by tube amplifiers for their warm, crunchy sound."]),
    dict(key="mig", scene="t_mig", lines=[
        "In nineteen seventy-six, a Soviet pilot flew a MiG twenty-five fighter jet to Japan. When Western analysts took it apart, they were surprised to find that much of its electronics ran on vacuum tubes.",
        "Old-fashioned? Maybe. But tubes are tough. They can keep working in radiation that would wreck delicate early transistors.",
        "And at NASA's Ames Research Center, researchers even built a nanoscale vacuum transistor, a tiny tube carved into a chip, that reached four hundred and sixty gigahertz in early tests."]),
    dict(key="twist", scene="t_patent", lines=[
        "And here's the twist. The transistor almost arrived twenty-two years early.",
        "In nineteen twenty-five, a physicist named Julius Lilly-en-feld filed a patent in Canada for a device that controlled current in a solid using an electric field. A field-effect transistor.",
        "As far as anyone knows, he never got a working version. The ultra-pure materials it needed didn't exist yet. But when Bell Labs tried to patent its own designs in the late nineteen-forties, many of the claims were rejected, partly because of his patents."],
         sfx=[("scratch", 0.0)]),
    dict(key="mos", scene="t_mos", lines=[
        "Then, in nineteen fifty-nine, Mohamed Atalla and Dawon Kong at Bell Labs built a working field-effect transistor out of silicon, with a thin layer of glass on top. The moss-fet. Much closer to Lilly-en-feld's idea than to the nineteen forty-seven device.",
        "It turned out to be the one that took over the world. By twenty eighteen, humanity had made an estimated thirteen sextillion transistors. That's a thirteen followed by twenty-one zeros, and about ninety-nine point nine percent of them were moss-fets.",
        "That makes the transistor the most manufactured thing in human history."]),
    dict(key="outro", scene="t_end", lines=[
        "So the transistor wasn't one lucky accident. The idea waited decades for materials good enough to make it work. Without it, your world would be orange, hot and humming, and computers would fill buildings instead of pockets.",
        "Which piece of tech would you miss most in a vacuum-tube world? Tell me in the comments."],
         hold=1.6, opts=dict(q="WHAT WOULD YOU MISS?")),
]
A1_CH = [("hook", "19 billion switches"), ("rules", "The rules: vacuum tubes"), ("c46", "1946: ENIAC"), ("burnout", "Tubes burn out"),
         ("c47", "December 1947: the day that never comes"), ("c55", "1955: no transistor radio"), ("c69", "1969: Apollo without chips"),
         ("cnow", "Today: a phone made of tubes"), ("cstill", "Tubes never died"), ("twist", "Patented 22 years early"), ("outro", "What would you miss?")]

A2 = [  # teaser
    dict(key="t1", scene="t_phone", lines=["What if your phone ran on vacuum tubes instead of transistors?"], opts=dict(mode="intro", hook="A PHONE MADE OF TUBES")),
    dict(key="t2", scene="t_phone", lines=["A recent phone chip holds about nineteen billion transistors. Each one is a tiny switch."], opts=dict(mode="zoom", badge="19 BILLION SWITCHES")),
    dict(key="t3", scene="t_eniac", lines=["Before transistors, those switches were glass vacuum tubes. The Eh-nee-ack computer had about seventeen and a half thousand of them, and drew a hundred and fifty kilowatts."]),
    dict(key="t4", scene="t_phonecalc", lines=["Scale that up to nineteen billion tubes, and one phone would need around a hundred and sixty gigawatts. Like a hundred and sixty big power plants."],
         opts=dict(mode="power", badge="~160 GIGAWATTS")),
    dict(key="t5", scene="t_phonecalc", lines=["It would fill about a hundred and fifty Olympic pools. And more than six tubes would burn out every second."], opts=dict(mode="pools")),
    dict(key="t6", scene="t_endshort", lines=["So what if the transistor was never invented? Full story on the channel."], hold=1.4, opts=dict(top="NO TRANSISTOR?")),
]
A3 = [  # standalone: the moth
    dict(key="m1", scene="t_moth", lines=["This moth is in a museum, because it got stuck inside a computer."], opts=dict(mode="intro", hook="THE FIRST COMPUTER BUG")),
    dict(key="m2", scene="t_moth", lines=["On September ninth, nineteen forty-seven, engineers working on the Harvard Mark Two found it trapped in relay number seventy."],
         opts=dict(mode="relay", badge="SEPTEMBER 9, 1947")),
    dict(key="m3", scene="t_moth", lines=["The Mark Two was built from relays, little switches that clicked open and shut with magnets. One moth in the wrong place, and a circuit failed."],
         opts=dict(mode="click")),
    dict(key="m4", scene="t_moth", lines=["So they taped it into the logbook, and wrote: First actual case of bug being found."], opts=dict(mode="log")),
    dict(key="m5", scene="t_moth", lines=["But the joke only works because bug was already slang. Thomas Edison was calling glitches bugs back in eighteen seventy-eight."],
         opts=dict(mode="edison", badge="EDISON, 1878")),
    dict(key="m6", scene="t_moth", lines=["Grace Hopper, who worked on the Mark Two, loved telling the story and made it famous. The logbook page is now at the Smithsonian."],
         opts=dict(mode="museum")),
    dict(key="m7", scene="t_endshort", lines=["Three months later, the transistor arrived. What if it never had? Full story on the channel."], hold=1.4, opts=dict(top="NO TRANSISTOR?")),
]
A4 = [  # standalone: every chip stops (-> tubes long)
    dict(key="b1", scene="t_blackout", lines=["What if every chip on Earth stopped working, all at once?"], opts=dict(mode="intro", hook="EVERY CHIP: OFF")),
    dict(key="b2", scene="t_blackout", lines=["Phones die instantly. So do laptops, the internet, card payments, and most TVs."], opts=dict(mode="phones")),
    dict(key="b3", scene="t_blackout", lines=["Modern cars are full of chips, so most won't start. In twenty twenty-one, just a shortage of chips cost carmakers about two hundred and ten billion dollars in sales."],
         opts=dict(mode="cars", badge="$210 BILLION")),
    dict(key="b4", scene="t_blackout", lines=["Power grids, water pumps and traffic lights lean on electronic controls too. So the lights start going out."], opts=dict(mode="grid")),
    dict(key="b5", scene="t_blackout", lines=["What still works? Wind-up clocks. Bicycles. Old cars with no electronics. And antique radios built with vacuum tubes."],
         opts=dict(mode="works", badge="STILL WORKS")),
    dict(key="b6", scene="t_mig", lines=["Tubes are so tough that a Soviet fighter jet was still flying with tube electronics in the nineteen-seventies."], opts=dict(mode="short")),
    dict(key="b7", scene="t_endshort", lines=["So what if the transistor was never invented? Full story on the channel."], hold=1.4, opts=dict(top="NO TRANSISTOR?")),
]

# =====================================================================  B. SHRINK INSIDE A CHIP
CL = "YOUR SIZE"
B1 = [
    dict(key="hook", scene="c_hair", lines=[
        "A human hair is about eighty thousand to a hundred thousand nanometers wide.",
        "The transistors in a new laptop chip are spaced just a few dozen nanometers apart. More than a thousand of them could line up across the width of that single hair.",
        "So what if you shrank down and walked inside one of those chips? What would you actually see?"], hold=0.2),
    dict(key="title", scene="c_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF YOU SHRANK", l2="INSIDE A CHIP?")),
    dict(key="rules", scene="c_rules", lines=[
        "The rules: you shrink in stages, and nothing can hurt you. You don't need air, the heat can't burn you, and somehow, you can still see.",
        "Our destination is a laptop chip, Apple's M three Max. It holds ninety-two billion transistors. That's more than ten for every person on Earth."]),
    card("c1mm", "1 MILLIMETER", CL, "c_card"),
    dict(key="package", scene="c_package", lines=[
        "At one millimeter tall, about the size of a small ant, the chip looks like a flat, dark building. That's the package, a protective shell.",
        "The real chip, called the die, is a thin slab of silicon hidden inside, wired to the outside world through thousands of tiny metal bumps.",
        "That silicon started out as quartz, and was refined until it was at least ninety-nine point nine nine nine nine nine nine nine percent pure. Nine nines. Fewer than one stray atom for every billion silicon atoms."]),
    card("c1um", "1 MICROMETER", CL, "c_card"),
    dict(key="wires", scene="c_wires", lines=[
        "Shrink a thousand times more, down to one micrometer, and you land on top of the die. It's not a smooth roof. It's a city of copper highways, stacked about fifteen levels deep.",
        "The top levels are wide, to carry power. As you climb down, the wires get thinner and more crowded. In total, a leading-edge chip can hold tens of kilometers of copper wire. Some estimates go close to a hundred kilometers.",
        "Every wire is wrapped in insulation, so signals don't leak into their neighbors. And it all fits into a few square centimeters of silicon.",
        "These highways used to be aluminum. In nineteen ninety-seven, IBM announced chips wired with copper instead. Copper carries current far more easily, and nearly every advanced chip has used it since."]),
    dict(key="clock", scene="c_clock", lines=[
        "Now watch a signal race past. A modern processor's clock ticks around four billion times a second.",
        "In one of those ticks, even light only travels about seven and a half centimeters. Signals in these wires are slower than light. So the whole city has to be planned so that data arrives exactly on time."]),
    card("c100nm", "100 NANOMETERS", CL, "c_card"),
    dict(key="fins", scene="c_fins", lines=[
        "Shrink again, until you're just a hundred nanometers tall, and you reach the ground floor. The transistors.",
        "They don't look like the flat switches in old textbook diagrams. Many are built around thin walls of silicon called fins, standing up like slices of bread in a rack. A gate drapes over the top and sides of each fin.",
        "Put a voltage on the gate, and electrons flow along the fin from one end to the other. Switch on. Take the voltage away, and the flow stops. Switch off. A one, and a zero.",
        "Intel was the first to mass-produce this kind of three-dimensional transistor, starting in twenty eleven.",
        "The newest designs go further. They slice the channel into thin stacked ribbons, and wrap the gate all the way around them."]),
    dict(key="dust", scene="c_dust", lines=[
        "And look out for dust. From down here, a speck of dust one micrometer across would be a boulder ten times your height, big enough to flatten whole rows of transistors.",
        "That's why chips are made in clean rooms. Ordinary room air can hold tens of millions of floating particles in every cubic meter. The cleanest chip-making air is filtered down to only a handful."]),
    dict(key="ruler", scene="c_ruler", lines=[
        "Here's a surprise. This is sold as a three-nanometer chip. So somewhere down here, you'd expect to find something three nanometers wide. You won't.",
        "The name is mostly marketing. Industry roadmaps put the gates of a so-called three-nanometer process about forty-eight nanometers apart, and the tightest wires about twenty-four nanometers apart.",
        "The number on the box stopped matching any real part of the transistor years ago."], sfx=[("pop", "L0+0.9")]),
    card("c1nm", "1 NANOMETER", CL, "c_card"),
    dict(key="atoms", scene="c_atoms", lines=[
        "Now shrink to a single nanometer. You're barely bigger than a few atoms. And the silicon around you isn't smooth anymore. It's a crystal, with atoms lined up in a perfect repeating pattern, about a quarter of a nanometer apart.",
        "That's so small that more than three hundred thousand silicon atoms could sit side by side across the width of one human hair.",
        "Under each gate sits a layer of insulation that's supposed to keep electrons out. By the mid two-thousands, in Intel's chips, that layer had shrunk to about one point two nanometers. Just five atoms thick."]),
    dict(key="tunnel", scene="c_tunnel", lines=[
        "And at that thickness, something strange happens. Electrons don't always stay on their side. Quantum mechanics lets some of them tunnel straight through the wall, like a ghost walking through a door.",
        "That leak wasted power and heated up the chip. The fix was a new insulator made with an element called hafnium. A thicker layer that behaves like a thin one. Intel said it cut the leak more than tenfold.",
        "Intel's cofounder Gordon Moore called it the biggest change in transistor technology since the late nineteen-sixties."]),
    card("cheat", "THE HEAT", CL, "c_card"),
    dict(key="heat", scene="c_heat", lines=[
        "Now look around. Billions of switches flipping, billions of times a second. Every flip turns a little energy into heat.",
        "In the early two-thousands, chip makers hit a wall. Air-cooled processors topped out at roughly a hundred watts. Clock speeds, which had climbed year after year, stalled at around four gigahertz, and have stayed near there ever since.",
        "Back in two thousand one, an Intel executive, Pat Gelsinger, warned that if chips kept going the way they were, they'd soon be hotter, for their size, than a nuclear reactor.",
        "So instead of making one core faster, chips got more cores. The processor in your laptop works like a team, not a single sprinter."]),
    dict(key="fab", scene="c_fab", lines=[
        "So how do you even build a city this small? With light. But not ordinary light. Extreme ultraviolet, with a wavelength of thirteen point five nanometers.",
        "To make it, a machine fires tens of thousands of droplets of molten tin every second, and blasts each one with a laser, turning it into a plasma hotter than the surface of the Sun.",
        "That light is absorbed by almost everything, even air. So it travels through a vacuum, bouncing off mirrors so smooth that, if one were blown up to the size of Germany, its biggest bump would be about a tenth of a millimeter tall."],
         opts=dict(mode="full")),
    dict(key="twist", scene="c_twist", lines=[
        "But here's the twist. You could never actually take this trip.",
        "Atoms don't shrink. At one nanometer tall, you'd be made of just a handful of atoms. No room for a brain, or eyes, or a heart.",
        "And even with eyes, you'd be blind. Visible light waves are hundreds of nanometers long, far bigger than you. Trying to see with them would be like trying to feel a grain of sand while wearing oven mitts.",
        "That's why scientists who study chips up close use electron microscopes instead. Electrons behave like waves too, and their waves can be thousands of times shorter than visible light.",
        "That's the same problem chip makers fight every day. Ordinary light is too big to draw these features, so they had to invent a shorter kind."],
         sfx=[("scratch", 0.0)]),
    dict(key="stack", scene="c_stack", lines=[
        "For more than fifty years, shrinking kept Gordon Moore's famous prediction alive: roughly twice as many transistors on a chip every two years.",
        "And now that the city can barely shrink any further, it's starting to grow upward. Chips are being stacked into towers, like the high-bandwidth memory inside A-I processors, with layers of memory piled on top of each other."]),
    dict(key="outro", scene="c_end", lines=[
        "So inside the chip in your laptop there's a city with more switches than there are people on Earth, roads only a few dozen nanometers wide, and walls just a few atoms thick.",
        "If you could shrink down for one hour, which part would you visit first? Tell me in the comments."],
         hold=1.6, opts=dict(q="WHERE WOULD YOU GO?")),
]
B1_CH = [("hook", "Thinner than a hair"), ("rules", "The rules"), ("c1mm", "1 mm: the package"), ("c1um", "1 µm: a city of copper"),
         ("clock", "4 billion ticks a second"), ("c100nm", "100 nm: the transistors"), ("ruler", "The 3 nm myth"), ("c1nm", "1 nm: atoms"),
         ("tunnel", "Quantum tunneling"), ("cheat", "The heat wall"), ("fab", "Printing with tin plasma"), ("twist", "Why you'd be blind"), ("outro", "Where would you go?")]

B2 = [  # teaser
    dict(key="s1", scene="c_hair", lines=["What if you shrank down and walked inside a computer chip?"], opts=dict(hook="SHRINK INTO A CHIP")),
    dict(key="s2", scene="c_wires", lines=["First, a city of copper. Tens of kilometers of wiring, stacked about fifteen levels deep."], opts=dict(badge="~15 LEVELS OF WIRES")),
    dict(key="s3", scene="c_fins", lines=["Then the transistors. Ninety-two billion of them in one laptop chip. More than ten for every person on Earth."], opts=dict(badge="92 BILLION")),
    dict(key="s4", scene="c_ruler", lines=["It's sold as a three-nanometer chip, but nothing in it is three nanometers wide. The gates are about forty-eight nanometers apart."],
         opts=dict(badge="MARKETING!")),
    dict(key="s5", scene="c_tunnel", lines=["And the insulating walls once got so thin, about five atoms, that electrons tunneled straight through them."]),
    dict(key="s6", scene="c_endshort", lines=["So what would you actually see down there? Full story on the channel."], hold=1.4, opts=dict(top="SHRINK INSIDE A CHIP?")),
]
B3 = [  # standalone: EUV tin plasma
    dict(key="e1", scene="c_fab", lines=["The chip in your phone was printed with light made from exploding tin."], opts=dict(mode="intro", hook="TIN + LASERS = CHIPS")),
    dict(key="e2", scene="c_fab", lines=["To draw features this small, chip makers use extreme ultraviolet light, with a wavelength of just thirteen point five nanometers."],
         opts=dict(mode="wave", badge="13.5 NANOMETERS")),
    dict(key="e3", scene="c_fab", lines=["To make it, a machine fires about fifty thousand droplets of molten tin every second, and hits each one with a laser."],
         opts=dict(mode="droplets", badge="50,000 PER SECOND")),
    dict(key="e4", scene="c_fab", lines=["The tin turns into plasma hotter than the surface of the Sun, and that plasma glows with the light."], opts=dict(mode="plasma")),
    dict(key="e5", scene="c_fab", lines=["Air absorbs that light, so it all runs in a vacuum, off mirrors so smooth that, scaled up to the size of Germany, the biggest bump would be a tenth of a millimeter."],
         opts=dict(mode="mirror")),
    dict(key="e6", scene="c_fab", lines=["Just one company, A-S-M-L, builds these machines. The newest model costs around three hundred and eighty million dollars."],
         opts=dict(mode="price", badge="~$380 MILLION")),
    dict(key="e7", scene="c_endshort", lines=["So what's inside the chips it makes? Full story on the channel."], hold=1.4, opts=dict(top="WHAT'S INSIDE?")),
]
B4 = [  # standalone: Moore's law (-> shrink long)
    dict(key="o1", scene="c_moore", lines=["In nineteen sixty-five, Gordon Moore predicted that chips would double their number of components every year."],
         opts=dict(mode="intro", hook="MOORE'S LAW FOREVER?")),
    dict(key="o2", scene="c_moore", lines=["In nineteen seventy-five, he changed it to about every two years. And for decades, the industry kept up."], opts=dict(mode="graph", badge="2X EVERY 2 YEARS")),
    dict(key="o3", scene="c_moore", lines=["So what if it never slowed down? Clock speeds would still be climbing. Instead, they stalled at around four gigahertz in the mid two-thousands."],
         opts=dict(mode="clock", badge="STUCK NEAR 4 GHZ")),
    dict(key="o4", scene="c_heat", lines=["The reason is heat. Air-cooled chips hit roughly a hundred watts. Push them much harder, and they cook themselves."]),
    dict(key="o5", scene="c_atoms", lines=["And there's a harder wall. Silicon atoms sit about a quarter of a nanometer apart. You can't build a switch smaller than an atom."]),
    dict(key="o6", scene="c_stack", lines=["So chips are starting to grow upward instead, stacking layers like a skyscraper."]),
    dict(key="o7", scene="c_endshort", lines=["What would it look like inside one? Full story on the channel."], hold=1.4, opts=dict(top="SHRINK INSIDE A CHIP?")),
]

# =====================================================================  C. COSMIC RAY FLIPS A BIT
KL = "COSMIC RAY VS COMPUTER"
C1 = [
    dict(key="hook", scene="k_vote", lines=[
        "On May eighteenth, two thousand three, in the Belgian town of Skar-bake, an electronic voting machine gave one candidate four thousand and ninety-six extra votes.",
        "It wasn't a hacker, and investigators found no software bug. The leading explanation is a particle from space that struck the machine's memory and flipped one single bit.",
        "So what happens when a cosmic ray flips a bit in your computer?"], opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="k_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF A COSMIC RAY", l2="FLIPPED A BIT?")),
    dict(key="bits", scene="k_bits", lines=[
        "First, the rules of the game. Everything your computer knows is stored as bits. Ones and zeros. A photo, a bank balance, the score in a video game. All bits.",
        "In the main memory of your computer, each bit is a tiny bucket of electric charge. Full is a one. Empty is a zero.",
        "And modern buckets are tiny. It doesn't take much to tip one over."]),
    dict(key="place", scene="k_bits", lines=[
        "Bits also have values. In a binary number, the first bit is worth one. The next is worth two, then four, eight, sixteen, doubling every time.",
        "So flipping a low bit barely changes a number. But the thirteenth bit is worth four thousand and ninety-six. Remember that number."],
         opts=dict(mode="place")),
    card("cray", "THE PARTICLE", KL, "k_card"),
    dict(key="cosmic", scene="k_shower", lines=[
        "So where does the hit come from? Cosmic rays are mostly protons and atomic nuclei, racing across the galaxy at nearly the speed of light. Many are thought to be flung out by exploding stars.",
        "When one slams into the top of our atmosphere, it shatters into a shower of other particles, spreading out as it rains toward the ground.",
        "They were discovered in nineteen twelve, when the physicist Victor Hess carried radiation detectors up in a balloon, more than five kilometers high, and found the radiation got stronger the higher he went. Not weaker. It was coming from space.",
        "The most energetic one ever recorded, in nineteen ninety-one, carried as much energy as a baseball thrown at about ninety-five kilometers an hour. All packed into a single particle smaller than an atom. Scientists nicknamed it the Oh-My-God particle.",
        "Right now, about one muon from those showers passes through every square centimeter of you, every minute. Through your body, your phone and your laptop."]),
    dict(key="neutron", scene="k_shower", lines=[
        "But for chips on the ground, the main troublemakers are neutrons from the same showers.",
        "And the higher you go, the worse it gets. At the height where airliners cruise, the neutron flux is about three hundred times stronger than at sea level.",
        "That's why the computers that fly airliners have to be designed with these hits in mind. And it's why a computer in a mountain town gets hit more often than the same one at the beach."],
         opts=dict(mode="altitude")),
    card("chit", "THE HIT", KL, "k_card"),
    dict(key="hit", scene="k_hit", lines=[
        "When a particle hits a chip just right, it leaves a thin trail of electric charge in the silicon. If that trail lands next to a memory cell, it can fill an empty bucket, or drain a full one.",
        "A zero becomes a one. Engineers call it a soft error, or a single-event upset. Nothing is broken. The memory just remembers something it was never told.",
        "Most of the time, you'd never notice. The flipped bit sits in memory nobody's using, or it gets overwritten a moment later. Sometimes a program crashes. And sometimes, a number quietly changes.",
        "And a single particle can even flip several neighboring bits at once. That's much harder to catch, because many protection schemes are built to fix just one."]),
    card("creal", "IT HAPPENED", KL, "k_card"),
    dict(key="belgium", scene="k_vote", lines=[
        "Back to Belgium. Officials noticed that the candidate's total didn't add up, so they recounted. The four thousand and ninety-six extra votes vanished.",
        "Four thousand and ninety-six is two to the twelfth power, the value of that thirteenth bit. Exactly what one flipped bit would add. After ruling out fraud and software errors, investigators concluded a single-event upset was the most likely cause."],
         opts=dict(mode="recount")),
    dict(key="voyager", scene="k_voyager", lines=[
        "Out in space, it's far worse. Over a region called the South Atlantic Anomaly, Earth's radiation belts dip close to the planet. The Hubble Space Telescope passes through it on many of its orbits, and doesn't take science observations while it's inside.",
        "In twenty ten, the Voyager Two spacecraft, more than thirteen billion kilometers from Earth, suddenly started sending home gibberish.",
        "Engineers traced it to a single bit in its data computer that had flipped from a zero to a one. They sent a command to flip it back, and Voyager went back to work.",
        "Nobody can prove what flipped it. But out there, radiation is the usual suspect."]),
    dict(key="mario", scene="k_game", lines=[
        "And in twenty thirteen, during a livestream of Super Mario sixty-four, a player's Mario suddenly shot up onto a higher floor, a jump nobody has been able to repeat in a normal game.",
        "A popular theory: a single bit in Mario's height value flipped. It's never been proven, and fans still argue about it."]),
    dict(key="alpha", scene="k_alpha", lines=[
        "The first chip culprits weren't even from space. In nineteen seventy-eight, Intel engineers Timothy May and Murray Woods found that memory chips were flipping bits on their own.",
        "The cause: tiny traces of uranium and thorium in the chips' own packaging, giving off alpha particles. Chip makers had to start using purer materials."]),
    dict(key="squat", scene="k_squat", lines=[
        "Bit flips can even send your computer to the wrong website. In twenty eleven, security researcher Artem Dinaburg registered web addresses that were exactly one bit away from famous ones.",
        "Over about seven months, they received more than fifty-two thousand requests, from computers that had flipped a bit somewhere along the way."]),
    card("crate", "HOW OFTEN?", KL, "k_card"),
    dict(key="rate", scene="k_rate", lines=[
        "So how often does this happen? In the nineteen-nineties, IBM estimated roughly one cosmic-ray error per month for every two hundred and fifty-six megabytes of memory. Other estimates came out far lower.",
        "In two thousand nine, a study of Google's servers found that more than eight percent of memory modules had at least one error a year. But the researchers argued that many came from worn or faulty chips, not from space.",
        "And in twenty twenty-six, a Mozilla engineer estimated that roughly one in ten Firefox crashes looked like bit flips, most likely from bad memory. So sometimes, when software crashes, it really isn't the software's fault."]),
    card("cfix", "THE DEFENSE", KL, "k_card"),
    dict(key="hamming", scene="k_ecc", lines=[
        "So why doesn't your computer go haywire every day? Because engineers fight back.",
        "In nineteen fifty, Richard Hamming at Bell Labs got fed up with a relay computer that kept stopping on errors over the weekend, wasting his work. So he invented error-correcting codes.",
        "The idea: store a few extra check bits alongside your data. If one bit flips, the check bits can tell you which one, and flip it back."]),
    dict(key="space", scene="k_ecc", lines=[
        "Servers use this in E-C-C memory. Spacecraft go even further. The Cassini probe's data recorders stored seven check bits for every thirty-two bits of data, and swept their memory clean of errors every nine minutes.",
        "Some systems simply run the same computer several times over and let them vote. The Space Shuttle flew with five main computers, four of them running the same software and comparing answers."],
         opts=dict(mode="vote")),
    dict(key="twist", scene="k_twist", lines=[
        "And here's the twist. Those same cosmic rays help us, too.",
        "Chip makers test their hardware by firing beams of neutrons at it, cramming years of cosmic-ray hits into a few hours.",
        "And in twenty seventeen, scientists used muons from cosmic rays like an X-ray, to look inside the Great Pyramid of Giza. They found a huge hidden empty space, at least thirty meters long, that nobody knew was there."],
         sfx=[("scratch", 0.0)]),
    dict(key="outro", scene="k_end", lines=[
        "So right now, as you watch this, particles from distant exploding stars are passing through your screen. Almost all of them miss. And when one doesn't, your computer quietly fixes it. Or it crashes, and you blame the software.",
        "Have you ever had a glitch so weird it might have been a cosmic ray? Tell me in the comments."],
         hold=1.6, opts=dict(q="COSMIC RAY OR BAD CODE?")),
]
C1_CH = [("hook", "4,096 extra votes"), ("bits", "The rules: bits"), ("cray", "Where the particles come from"), ("chit", "The hit"),
         ("creal", "It really happened"), ("alpha", "Radioactive packaging"), ("crate", "How often?"), ("cfix", "The defense"),
         ("twist", "Cosmic rays that help"), ("outro", "Cosmic ray or bad code?")]

C2 = [  # teaser
    dict(key="k1", scene="k_shower", lines=["Right now, particles from space are passing through your phone."], opts=dict(hook="SPACE VS YOUR PHONE")),
    dict(key="k2", scene="k_shower", lines=["About one muon passes through every square centimeter, every minute."], opts=dict(badge="1 PER CM² PER MINUTE")),
    dict(key="k3", scene="k_hit", lines=["When a particle hits a memory chip just right, it can flip a single bit. A zero becomes a one."]),
    dict(key="k4", scene="k_voyager", lines=["In twenty ten, a flipped bit made Voyager Two send home gibberish, until engineers flipped it back."]),
    dict(key="k5", scene="k_vote", lines=["And in Belgium in two thousand three, a single flipped bit is the leading explanation for one candidate getting four thousand and ninety-six extra votes."],
         opts=dict(mode="recount", badge="+4,096 VOTES")),
    dict(key="k6", scene="k_endshort", lines=["So why doesn't your computer crash every day? Full story on the channel."], hold=1.4, opts=dict(top="COSMIC RAY VS COMPUTER")),
]
C3 = [  # standalone: the 4,096 votes
    dict(key="v1", scene="k_vote", lines=["In two thousand three, a voting machine in Belgium gave one candidate four thousand and ninety-six extra votes."],
         opts=dict(mode="intro", hook="+4,096 VOTES")),
    dict(key="v2", scene="k_vote", lines=["The total didn't add up, so officials recounted. The extra votes vanished."], opts=dict(mode="recount")),
    dict(key="v3", scene="k_vote", lines=["Investigators ruled out fraud and software bugs. The leading explanation: one bit in the machine's memory had flipped."],
         opts=dict(mode="bit", badge="ONE BIT")),
    dict(key="v4", scene="k_bits", lines=["Here's the giveaway. In binary, each bit is worth double the one before. One, two, four, eight. The thirteenth bit is worth exactly four thousand and ninety-six."],
         opts=dict(mode="place", badge="2¹² = 4,096")),
    dict(key="v5", scene="k_hit", lines=["What flips a bit? Very often, a particle from a cosmic-ray shower, crashing into the chip."]),
    dict(key="v6", scene="k_endshort", lines=["What else can a cosmic ray do to your computer? Full story on the channel."], hold=1.4, opts=dict(top="WHAT ELSE CAN IT DO?")),
]

VIDEOS = {"b4_tubes": A1, "b4_shrink": B1, "b4_cosmic": C1,
          "short_b4_tubes": A2, "short_b4_moth": A3, "short_b4_blackout": A4,
          "short_b4_shrink": B2, "short_b4_euv": B3, "short_b4_moore": B4,
          "short_b4_cosmic": C2, "short_b4_vote": C3}
CHAPTERS = {"b4_tubes": A1_CH, "b4_shrink": B1_CH, "b4_cosmic": C1_CH}
MUSIC = {"b4_tubes": "tubes", "b4_shrink": "chip", "b4_cosmic": "cosmic",
         "short_b4_tubes": "tubes_s", "short_b4_moth": "tubes_s", "short_b4_blackout": "tubes_s",
         "short_b4_shrink": "chip_s", "short_b4_euv": "chip_s", "short_b4_moore": "chip_s",
         "short_b4_cosmic": "cosmic_s", "short_b4_vote": "cosmic_s"}
