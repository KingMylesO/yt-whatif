"""Batch 03 scene + narration plan (TTS-friendly wording).

Long-form: b3_rings (Earth with rings), b3_magnet (magnetic field off), b3_photo (photosynthesizing humans).
Shorts: teaser + standalone per long-form, plus short_b3_clouds (-> magnet) and short_b3_mantis (-> photo).
Scene prefixes: r_ = scenes_b3_rings.py, m_ = scenes_b3_magnet.py, p_ = scenes_b3_photo.py.
"""
CARD = 1.9

def card(key, text, label, scene):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

# =====================================================================  A. EARTH WITH RINGS
RL = "SINCE EARTH GOT RINGS"
A1 = [
    dict(key="hook", scene="r_saturn", lines=[
        "Saturn's main rings are more than two hundred and seventy thousand kilometers across. But in most places, they're only about ten meters thick.",
        "For their size, that's far thinner than a sheet of paper. And all of that ring material together weighs only about forty percent as much as Saturn's small moon Mimas.",
        "Now picture rings like that around Earth. What would your sky look like? And what would they do to the planet underneath?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="r_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF EARTH", l2="HAD RINGS?")),
    dict(key="roche", scene="r_roche", lines=[
        "First, the rules. A ring can't sit just anywhere. Get too close to a planet, and its tides pull a moon apart faster than the moon's own gravity can hold it together.",
        "That boundary is called the Rosh limit. For a rocky moon, it sits roughly three Earth radii from the center. About twelve thousand kilometers above your head.",
        "So let's say a small moon drifted inside that line, broke apart, and spread into a flat, glittering disk around the equator. Inside the limit, the pieces can never clump back together."]),
    dict(key="rock", scene="r_material", lines=[
        "Saturn's rings are about ninety-eight percent water ice, in pieces ranging from tiny grains to chunks as big as a house. That's why they shine so brightly.",
        "Ours would be different. This close to the Sun, ice slowly turns to vapor, so Earth's rings would be mostly rock and dust. Darker. Grayer. Still enormous.",
        "And the inner edge would have to stay above about a thousand kilometers. Any lower, and the debris drags through the thin upper air and burns up as meteors."]),
    card("c1d", "DAY 1", RL, "r_card"),
    dict(key="equator", scene="r_sky", lines=[
        "On day one, where you live changes everything.",
        "Stand on the equator, in a city like Quito, and you're looking at the rings edge-on. A thin, bright line rising from the horizon and running straight overhead."],
         opts=dict(lat=0)),
    dict(key="midlat", scene="r_sky", lines=[
        "Move north, to somewhere like Washington, D.C., and the rings open up into a giant arch across the southern sky.",
        "Like a rainbow that never fades, never moves, and never sets. You could find south just by looking for it, the way sailors once used the North Star to find north."], opts=dict(lat=38)),
    dict(key="arctic", scene="r_sky", lines=[
        "Go all the way up to the Arctic Circle, and they shrink to a hump on the horizon. At the poles, you wouldn't see them at all."],
         opts=dict(lat=66)),
    dict(key="night", scene="r_night", lines=[
        "And at night, they don't go dark. Sunlight still hits the parts of the rings outside Earth's shadow, so they glow. This is called ringshine.",
        "One astronomer, Caleb Sharf, worked out that if the rings reflected just ten percent of the sunlight hitting them, every square meter would shine like a hundred-and-thirty-watt light bulb.",
        "Nights get brighter. Stargazing gets a lot harder. And every night, Earth's own shadow cuts a black gap across the glowing arch."]),
    card("c1y", "1 YEAR", RL, "r_card"),
    dict(key="shadow", scene="r_shadow", lines=[
        "Over a full year, the rings start doing something sneaky. They cast shadows.",
        "Earth is tilted, so the rings are tilted too. In northern summer, their shadow falls across the Southern Hemisphere. Six months later, it swaps sides.",
        "Notice which half gets the shade: the one already having winter. Less sunlight, in the season that has the least. Winters there could get colder and harsher."]),
    dict(key="equinox", scene="r_equinox", lines=[
        "Twice a year, at the equinoxes, the Sun lines up with the ring plane itself.",
        "From the equator, the rings would seem to slice the Sun in half.",
        "On those days, the ring's shadow shrinks to a thin stripe right along the equator. Then, as the seasons turn, it slowly widens again over the other hemisphere."]),
    dict(key="tropics", scene="r_tropics", lines=[
        "Scientists at Sandia National Laboratories actually modeled an Earth with an equatorial ring. They found it would mostly shade the tropics and subtropics, bouncing a big share of tropical sunlight back to space.",
        "Their conclusion was striking: shading like that might be enough to help push Earth into an ice age."]),
    dict(key="orbit", scene="r_orbits", lines=[
        "Then there's space traffic. The International Space Station orbits about four hundred kilometers up. That's below the rings. Fine.",
        "GPS satellites orbit at about twenty thousand kilometers, and the geostationary satellites that carry TV and weather data sit near thirty-six thousand. Above the rings. Also fine.",
        "But anything orbiting along the equator in between would be flying through a shooting gallery. And radio signals from satellites near the equator would have to pass through the debris.",
        "Rockets heading for high orbits would probably launch far from the equator, and climb over the ring plane rather than punch through it."]),
    card("c1k", "1,000 YEARS", RL, "r_card"),
    dict(key="culture", scene="r_navigate", lines=[
        "Give it a thousand years, and people adapt. Unlike the Moon, the rings never move across the sky. They're a permanent landmark.",
        "The farther you are from the equator, the lower the arch sits. So a sailor could estimate their latitude just by measuring its height.",
        "Every culture would grow up under the rings. Ring calendars. Ring myths. Maybe even ring-shadow sundials.",
        "Even the night would keep time. Earth's shadow would slide along the glowing arch from dusk to dawn, like the hand of a giant clock."]),
    dict(key="astro", scene="r_astro", lines=[
        "Astronomers, though, would not be fans. From much of the planet, a stripe of the sky is permanently hidden behind a wall of glowing rock.",
        "And every telescope pointed near that stripe is fighting ringshine."]),
    card("c10m", "10 MILLION YEARS", RL, "r_card"),
    dict(key="fade", scene="r_fade", lines=[
        "But rings don't last forever. Collisions grind the particles into dust. Some slowly spiral inward and burn up, a steady drizzle of shooting stars along the equator.",
        "Our big Moon doesn't help either. Its gravity keeps tugging on the ring, and Sharf thinks that would make long-lived rings hard to keep."]),
    dict(key="rain", scene="r_saturn", lines=[
        "Even Saturn's rings are temporary. NASA says ice from the rings is raining down into the planet fast enough to fill an Olympic swimming pool every half hour.",
        "By NASA's estimate, they could be gone in less than a hundred million years.",
        "So Earth's rings would probably fade within a few tens of millions of years. Which brings us to the strangest part of this story."],
         opts=dict(mode="rain")),
    dict(key="twist", scene="r_ordovician", lines=[
        "This might have actually happened.",
        "In twenty twenty-four, geologists at Monash University in Australia studied twenty-one impact craters from a time, about four hundred and sixty-six million years ago, when Earth was being hit unusually often.",
        "Every single one of them formed within about thirty degrees of the equator of the time.",
        "That's weird. About seventy percent of the land that could have preserved those craters sat outside that band. The odds of that happening by chance? Roughly one in twenty-five million."],
         sfx=[("scratch", 0.0)]),
    dict(key="breakup", scene="r_breakup", lines=[
        "Their explanation: a large asteroid passed inside Earth's Rosh limit, was torn apart, and formed a ring.",
        "Then, over millions of years, chunks from that ring fell to the ground, mostly near the equator."]),
    dict(key="ice", scene="r_iceage", lines=[
        "Not long after, Earth cooled, and slid into the Her-nan-tee-an ice age, one of the coldest stretches of the last half a billion years.",
        "The team thinks the ring's shadow may have helped. But they're careful to say it's an idea, not a proof. Nobody knows yet how big that ring was, or how much sunlight it blocked."]),
    dict(key="moon", scene="r_moon", lines=[
        "Earth may have had a disk of debris once before, too. Most scientists think our Moon formed after a Mars-sized world slammed into the young Earth, about four and a half billion years ago.",
        "In the classic version of that story, the wreckage spread into a ring around Earth, and the ring gathered itself into the Moon. That Moon is still drifting away from us, about three point eight centimeters every year."]),
    dict(key="others", scene="r_others", lines=[
        "And rings are common out there. Jupiter, Saturn, Uranus and Neptune all have them. Even the dwarf planet Haumea and a small icy world called Chariklo have rings.",
        "Mars may get one next. Its moon Phobos is spiraling inward by about two meters every century, and could be torn apart in thirty to fifty million years."]),
    dict(key="outro", scene="r_end", lines=[
        "So the next time you look up at a plain, empty sky, remember: it might not always have been empty.",
        "If Earth got rings tomorrow, where would you want to live? Under the arch, or under the line? Tell me in the comments."],
         hold=1.6, opts=dict(q="ARCH OR LINE?")),
]
A1_CH = [("hook", "Rings thinner than paper"), ("roche", "The rules: the Roche limit"), ("c1d", "Day 1: your new sky"),
         ("night", "Ringshine"), ("c1y", "1 year: ring shadows"), ("orbit", "Satellites vs rings"), ("c1k", "1,000 years"),
         ("c10m", "10 million years: rings fade"), ("twist", "Earth may have had a ring"), ("moon", "Rings everywhere"), ("outro", "Arch or line?")]

A2 = [  # teaser
    dict(key="t1", scene="r_sky", lines=["What if Earth had rings like Saturn? From the equator, you'd see a thin, bright line running straight overhead."],
         opts=dict(lat=0, hook="EARTH WITH RINGS")),
    dict(key="t2", scene="r_sky", lines=["Farther north, they'd open into a giant arch across the sky that never moves and never sets. A permanent rainbow."], opts=dict(lat=38)),
    dict(key="t3", scene="r_night", lines=["At night, sunlight still hits them, so they'd glow. It's called ringshine."]),
    dict(key="t4", scene="r_shadow", lines=["And their shadow would fall on whichever hemisphere is having winter, making cold seasons even colder."]),
    dict(key="t5", scene="r_ordovician", lines=["Here's the wild part. About four hundred and sixty-six million years ago, Earth may actually have had a ring."],
         opts=dict(badge="466 MILLION YEARS AGO")),
    dict(key="t6", scene="r_endshort", lines=["Full story on the channel."], hold=1.6, opts=dict(top="EARTH HAD A RING?")),
]
A3 = [  # standalone: Saturn losing its rings
    dict(key="s1", scene="r_saturn", lines=["Saturn is losing its rings. Right now."], opts=dict(mode="intro", hook="SATURN IS LOSING ITS RINGS")),
    dict(key="s2", scene="r_saturn", lines=["The rings are about ninety-eight percent water ice, and bits of that ice are raining down into the planet."],
         opts=dict(mode="rain", badge="RING RAIN")),
    dict(key="s3", scene="r_saturn", lines=["NASA says it's enough to fill an Olympic swimming pool every half hour. In its final orbits, the Cassini spacecraft measured up to ten thousand kilograms a second falling in."],
         opts=dict(mode="pool")),
    dict(key="s4", scene="r_saturn", lines=["At that rate, NASA says the rings could be gone in less than a hundred million years."], opts=dict(mode="fade", badge="< 100 MILLION YEARS")),
    dict(key="s5", scene="r_saturn", lines=["They might be young, too. Cassini data suggests ten to a hundred million years old. But a twenty twenty-four study argues they could be as old as Saturn itself."],
         opts=dict(mode="age", badge="HOW OLD?")),
    dict(key="s6", scene="r_endshort", lines=["Either way, we're lucky to see them. What if Earth had rings? Full story on the channel."], hold=1.4,
         opts=dict(top="WHAT IF EARTH HAD RINGS?")),
]

# =====================================================================  B. MAGNETIC FIELD OFF
ML = "SINCE THE FIELD SWITCHED OFF"
B1 = [
    dict(key="hook", scene="m_wind", lines=[
        "Right now, a wind from the Sun is blowing past Earth at around four hundred kilometers per second. Fast enough to cross the United States in about eleven seconds.",
        "You never feel it, because of an invisible shield made in the molten heart of the planet.",
        "What if that shield switched off?"], opts=dict(mode="shield"), hold=0.2),
    dict(key="title", scene="m_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF EARTH'S MAGNETIC", l2="FIELD SWITCHED OFF?")),
    dict(key="core", scene="m_core", lines=[
        "Here's where the shield comes from. About two thousand nine hundred kilometers below your feet, there's an ocean of liquid iron and nickel, thousands of degrees hot.",
        "As it churns and swirls, it works like a giant electric generator, a dynamo. And that makes Earth's magnetic field. Down in the core, the field is about fifty times stronger than at the surface."]),
    dict(key="field", scene="m_field", lines=[
        "At the surface, the field is surprisingly weak. A fridge magnet is about twenty times stronger.",
        "But it's enormous. On the side facing the Sun, it holds the solar wind back about ten Earth radii out, more than sixty thousand kilometers away.",
        "On the night side, it's stretched into a long tail that reaches far past the Moon."]),
    dict(key="rules", scene="m_rules", lines=[
        "So here are the rules. In one instant, the dynamo stops making a field. Completely. The core stays hot. The planet keeps spinning. Only the magnetism is gone.",
        "This can't actually happen. Geophysicists think the core has enough energy to keep the dynamo running for hundreds of millions of years, possibly billions. But let's switch it off anyway."]),
    card("c1s", "SECOND 1", ML, "m_card"),
    dict(key="compass", scene="m_compass", lines=[
        "In the first second, nothing you can feel. No sound. No flash.",
        "But every compass on Earth just stopped pointing north. The needles drift, and settle wherever they happen to be.",
        "Magnetic north has wandered more than eleven hundred kilometers since eighteen thirty-one. In recent decades, it was racing toward Siberia at up to fifty-five kilometers a year. Now it simply doesn't exist.",
        "Your phone's compass gives up too. GPS keeps working, though, because it runs on satellites and clocks, not magnetism. For now."]),
    card("c3m", "3 MINUTES", ML, "m_card"),
    dict(key="wind", scene="m_wind", lines=[
        "Within minutes, the solar wind arrives. With nothing to hold it back, it slams straight into the top of the atmosphere.",
        "That sounds terrifying. But here's the first surprise: down on the ground, you're mostly fine."],
         opts=dict(mode="nofield")),
    dict(key="air", scene="m_air", lines=[
        "What really shields you from space radiation isn't the magnetic field. It's the air. Above every square centimeter of your body sits about a kilogram of atmosphere.",
        "That's roughly as much shielding as ten meters of water over your head. Today, cosmic rays give you only about a third of a millisievert a year at ground level, around a tenth of your natural background radiation.",
        "One model of a much weaker field found about thirteen percent more cosmic-ray ionization at ground level worldwide, and about a quarter more near the equator. High in the atmosphere, the jump was several times bigger."]),
    card("c1d", "DAY 1", ML, "m_card"),
    dict(key="aurora", scene="m_aurora", lines=[
        "By that night, the sky looks different. Auroras normally hug the poles, because the field funnels particles down there. Without the field, there's no funnel.",
        "Mars has no global magnetic field today, and during big solar storms its whole sky can light up with a faint, planet-wide aurora.",
        "Earth could get something similar. Dim glows over every latitude, not just the Arctic. Even today, a big storm can push auroras far south. In May twenty twenty-four, they were seen as far south as Mexico."]),
    dict(key="orbit", scene="m_orbit", lines=[
        "Up in orbit, it's a different story. The Van Allen radiation belts are held in place by the field, so they drain away. That sounds good.",
        "But now satellites are directly exposed to every blast of particles from the Sun. Astronauts lose a big part of their protection too.",
        "Even airline crews would notice. A twenty twenty-six study found that if Earth's field were as weak as it was forty-one thousand years ago, radiation on some flight routes would be significantly higher."]),
    card("c1y", "1 YEAR", ML, "m_card"),
    dict(key="storm", scene="m_storm", lines=[
        "Within a year, the Sun throws a big storm. It does that a lot.",
        "In eighteen fifty-nine, a solar storm called the Carrington Event made telegraph lines spark. Some operators kept sending messages with their batteries unplugged, running only on current from the storm.",
        "In nineteen eighty-nine, a storm knocked out power to six million people in Quebec within ninety seconds, for nine hours. And in twenty twenty-two, a minor storm dragged thirty-eight new Starlink satellites out of orbit. The twenty twenty-four storm even sent GPS-guided tractors drifting off course.",
        "All of that happened with the shield up."], sfx=[("boom", 0.0)]),
    dict(key="ozone", scene="m_ozone", lines=[
        "Without it, particles from big storms pour into the upper atmosphere, where they create chemicals that eat ozone.",
        "A twenty twenty-four study modeled an extreme solar storm hitting an Earth with no magnetic field. Severe ozone loss lasted for years instead of about one, and ultraviolet light at the surface rose by up to about a quarter.",
        "More UV means faster sunburns, and more stress for plants and plankton that live in the sunlight."]),
    dict(key="animals", scene="m_animals", lines=[
        "Meanwhile, animals that navigate by magnetism get lost. Sea turtles seem to remember the magnetic signature of the beach where they hatched, and return to it years later to nest.",
        "Salmon use it to find their way home from the open ocean. Many migrating birds, like European robins, carry a built-in magnetic compass.",
        "Most have backups: the Sun, the stars, smell. But a lot of migrations would get messy."]),
    card("c1m", "1 MILLION YEARS", ML, "m_card"),
    dict(key="mars", scene="m_mars", lines=[
        "Now the big question. Without a shield, does the solar wind strip away our air, the way it did on Mars?",
        "Mars lost its global magnetic field about four billion years ago. NASA's Maven spacecraft found the solar wind is still stripping its atmosphere, around a hundred grams every second. Over billions of years, most of the Martian air was lost to space. All that's left of its field are patches of magnetized rock in the crust, fossils of a dynamo that died."]),
    dict(key="venus", scene="m_venus", lines=[
        "But here's the surprise. Venus has no magnetic field of its own either. And its atmosphere is about ninety times heavier than ours. Instead, the solar wind's own magnetism piles up around Venus into a weak shell.",
        "Some researchers argue a magnetic field doesn't protect air as much as we assumed. A twenty eighteen study estimated that Earth, Mars and Venus all lose roughly similar amounts, around half a kilogram to two kilograms every second.",
        "At that pace, a planet as big as Earth would take far longer than a million years to lose any meaningful amount of air. So a million years in, you're still breathing."]),
    dict(key="twist", scene="m_laschamp", lines=[
        "And this isn't purely hypothetical.",
        "About forty-one thousand years ago, during an event called the La-shom excursion, Earth's field collapsed to around five percent of today's strength. The magnetic poles wandered. Neanderthals were still alive.",
        "Some scientists, studying ancient New Zealand cow-ree trees, argued the ozone layer took a beating, and linked the event to climate shifts and even extinctions.",
        "Other researchers strongly disagree. They see no clear climate signal in the ice cores. The debate is still going."],
         sfx=[("scratch", 0.0)]),
    dict(key="today", scene="m_today", lines=[
        "And the field today? It's about nine percent weaker than it was two hundred years ago.",
        "A weak spot over the South Atlantic, where satellites take extra radiation, has grown since twenty fourteen by an area nearly half the size of continental Europe.",
        "But the European Space Agency says that's still within normal ups and downs. The field is still about twice its million-year average."]),
    dict(key="outro", scene="m_end", lines=[
        "So the shield won't switch off. But it flickers, it wanders, and one day it will flip.",
        "If losing it meant auroras over your city every night, would you switch it off? Tell me in the comments."],
         hold=1.6, opts=dict(q="WORTH IT FOR AURORAS?")),
]
B1_CH = [("hook", "A wind from the Sun"), ("core", "Where the shield comes from"), ("rules", "The rules"), ("c1s", "Second 1: compasses"),
         ("c3m", "3 minutes: the solar wind hits"), ("c1d", "Day 1: auroras and satellites"), ("c1y", "1 year: storms and ozone"),
         ("animals", "Lost animals"), ("c1m", "1 million years: the air"), ("twist", "It happened 41,000 years ago"), ("today", "The field today")]

B2 = [  # teaser
    dict(key="t1", scene="m_wind", lines=["A wind from the Sun hits Earth at about four hundred kilometers per second. An invisible magnetic shield pushes it away."],
         opts=dict(mode="shield", hook="EARTH'S INVISIBLE SHIELD")),
    dict(key="t2", scene="m_compass", lines=["What if that shield switched off? Every compass on Earth would stop pointing north."]),
    dict(key="t3", scene="m_air", lines=["Surprisingly, you'd mostly be fine. The air above you is the real radiation shield."]),
    dict(key="t4", scene="m_orbit", lines=["But satellites and astronauts would be exposed to every blast from the Sun."]),
    dict(key="t5", scene="m_ozone", lines=["And big solar storms could eat into the ozone layer for years."]),
    dict(key="t6", scene="m_laschamp", lines=["Forty-one thousand years ago, the field really did drop to about five percent of today's strength."],
         opts=dict(badge="41,000 YEARS AGO")),
    dict(key="t7", scene="m_endshort", lines=["Full story on the channel."], hold=1.6, opts=dict(top="IT HAPPENED BEFORE")),
]
B3 = [  # standalone: pole flip
    dict(key="f1", scene="m_flip", lines=["Earth's magnetic poles have swapped places many times. What if it started again tomorrow?"],
         opts=dict(mode="intro", hook="THE POLES FLIP")),
    dict(key="f2", scene="m_flip", lines=["NASA counts a hundred and eighty-three flips in the last eighty-three million years. The last full one was about seven hundred and eighty thousand years ago."],
         opts=dict(mode="timeline", badge="183 FLIPS")),
    dict(key="f3", scene="m_flip", lines=["A flip isn't instant. It takes hundreds to thousands of years, and along the way the field gets much weaker, with extra poles popping up in odd places."],
         opts=dict(mode="messy")),
    dict(key="f4", scene="m_flip", lines=["Compasses get confused. Satellites take more radiation. And auroras could show up far from the poles."],
         opts=dict(mode="effects")),
    dict(key="f5", scene="m_flip", lines=["But the fossil record shows no mass extinctions caused by flips. Life has been through this many, many times."],
         opts=dict(mode="life", badge="LIFE GOES ON")),
    dict(key="f6", scene="m_endshort", lines=["What if the field switched off completely? Full story on the channel."], hold=1.4,
         opts=dict(top="NO FIELD AT ALL?")),
]
B4 = [  # standalone: no clouds for a week (-> magnet long)
    dict(key="k1", scene="m_clouds", lines=["On a typical day, about two thirds of Earth is covered by clouds. What if they all vanished for a week?"],
         opts=dict(mode="globe", hook="NO CLOUDS FOR A WEEK")),
    dict(key="k2", scene="m_clouds", lines=["First, the rain stops. A typical puffy cloud holds about five hundred tonnes of water. No clouds, no rain, anywhere."],
         opts=dict(mode="rain", badge="NO RAIN")),
    dict(key="k3", scene="m_clouds", lines=["Days get hotter. Clouds bounce sunlight back to space. Overall, they cool the planet by about twenty watts on every square meter."],
         opts=dict(mode="day", badge="HOTTER DAYS")),
    dict(key="k4", scene="m_clouds", lines=["But nights get colder. Clouds work like a blanket. Under clear, dry desert skies, the temperature can drop about twenty degrees Celsius from afternoon to night."],
         opts=dict(mode="night", badge="COLDER NIGHTS")),
    dict(key="k5", scene="m_clouds", lines=["Solar panels would love it. Farmers wouldn't. By the end of the week, you'd really miss a gray day."],
         opts=dict(mode="end")),
    dict(key="k6", scene="m_endshort", lines=["What if Earth lost its magnetic shield instead? Full story on the channel."], hold=1.4,
         opts=dict(top="NEXT: NO SHIELD")),
]

# =====================================================================  C. PHOTOSYNTHESIZING HUMANS
PL = "SOLAR-POWERED YOU"
C1 = [
    dict(key="hook", scene="p_salamander", lines=[
        "There's one animal with a backbone that's known to have algae living inside its cells. The spotted salamander.",
        "Its eggs turn green with algae living in the jelly around each embryo, and some of those algae move right into the embryo's own cells.",
        "So what if you could do something like that? What if your skin could make food from sunlight?"], hold=0.2),
    dict(key="title", scene="p_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF HUMANS COULD", l2="PHOTOSYNTHESIZE?")),
    dict(key="rules", scene="p_rules", lines=[
        "Here are the rules. Your skin is packed with chloroplasts, the tiny green solar panels that plants use. A leaf holds about half a million of them in every square millimeter.",
        "Add sunlight, water and carbon dioxide, and they make sugar for your body. You can still eat normally. The sunlight is a bonus. And to keep things simple, the rest of you stays exactly the same.",
        "Chloroplasts were once free-living bacteria, swallowed by another cell well over a billion years ago. They even still carry their own DNA, a leftover from that bacterial past. Every leaf on Earth still runs on that ancient deal."]),
    dict(key="oxygen", scene="p_oxygen", lines=[
        "That deal is also why you can breathe. About two point four billion years ago, tiny photosynthesizing microbes started filling the air with oxygen.",
        "Today, tiny drifting plankton in the ocean make roughly half of the oxygen produced on Earth. Every breath you take is, in a way, exhaust from sunlight."]),
    dict(key="green", scene="p_green", lines=[
        "So first, you'd turn green. Chlorophyll absorbs red and blue light strongly, and uses less of the green.",
        "So green is what bounces back to everyone else's eyes."]),
    card("c7", "7 A.M.", PL, "p_card"),
    dict(key="morning", scene="p_morning", lines=[
        "Seven in the morning. You step outside, sunlight hits your skin, and for the first time, your body starts making its own sugar.",
        "Most of it would come in the hours around noon. At dawn and dusk, when the light is low and weak, you'd make almost nothing. On a gray, overcast day, you'd make only a fraction of a sunny day's haul. So how much, in total? Let's do the math."]),
    card("c12", "NOON", PL, "p_card"),
    dict(key="math", scene="p_math", lines=[
        "At midday, under a clear sky, sunlight delivers about a thousand watts onto every square meter. Your skin covers about one point eight square meters, but only about half of it faces the Sun at once.",
        "Now efficiency. In theory, the best plants can store only about five or six percent of sunlight as food. Even the best real crops manage two or three percent over a season, and typical plants, more like one percent.",
        "And the Sun isn't overhead all day. Average in the mornings, the evenings, the clouds and the nights, and your green skin might collect around one or two watts. That's less than a small phone charger puts out."]),
    dict(key="tennis", scene="p_tennis", lines=[
        "Your body runs on about a hundred watts, all day, every day.",
        "Oxford plant ecologist Lindsay Turnbull estimated photosynthetic skin would cover about one percent of a person's daily energy. In food terms, that's about a cracker a day.",
        "To run on sunlight alone, she figured you'd need about a tennis court's worth of skin. That's around a hundred and fifty times more skin than you have."]),
    dict(key="leaf", scene="p_leaf", lines=[
        "So how do plants get away with it? They're built completely differently. A tree spreads its leaves out into a huge, thin solar array.",
        "And it doesn't walk around, doesn't keep its body warm, and doesn't run a brain.",
        "Even then, plants pay a price. Sugar-making needs water, and leaves lose huge amounts of it through their pores. The U.S. Geological Survey says a large oak tree can give off about a hundred and fifty thousand liters of water in a year."]),
    dict(key="brain", scene="p_brain", lines=[
        "Your brain is only about two percent of your body weight, but it uses about twenty percent of your energy.",
        "Even at high noon, your green skin would make less power than your brain alone uses."]),
    card("c1y", "1 YEAR", PL, "p_card"),
    dict(key="year", scene="p_year", lines=[
        "A year in, the small stuff adds up. Anyone working outdoors gets a free snack every sunny day. Sunny countries get more than cloudy ones. And far from the equator, winter would be lean, with the Sun low in the sky for months.",
        "Clothes become a strange trade-off. Every shirt is a cover over your solar panels. Summer fashion would get very short, and very green.",
        "But photosynthesizing well means lots of sunlight on bare skin. And sunlight carries ultraviolet light, which damages DNA. Plants deal with that every day, using protective pigments and constant repair. Your green skin would need the same tricks.",
        "It would also need carbon dioxide. Leaves are covered in tiny pores called stoh-mah-tuh that let air in. Your skin would need something similar.",
        "And green skin only makes sugar. Plants get nitrogen and minerals from the soil through their roots. You'd still need real food to build proteins, and at night, your skin would simply switch off."]),
    dict(key="lizard", scene="p_lizard", lines=[
        "To really live on sunlight, you'd have to cut your energy bill. Cold-blooded animals already do that.",
        "A resting reptile uses only about a tenth of the energy of a mammal its size, because it doesn't burn fuel to stay warm.",
        "So picture a slow, cold-blooded human, basking on a rock. Even then, sunlight-skin wouldn't come close."]),
    card("c1m", "1 MILLION YEARS", PL, "p_card"),
    dict(key="evolve", scene="p_evolve", lines=[
        "Now give evolution a million years, and imagine the people who soak up the most light do best.",
        "Bodies get flatter. Wider. Thinner. Big flaps of skin spread out like leaves. Less moving around. Less thinking.",
        "Push that far enough, and you basically turn into a plant. And plants already won that game. They don't hunt for food, because their food falls from the sky.",
        "Funny thing is, some plants went the other way. Rafflesia, which grows one of the biggest flowers on Earth, gave up photosynthesis entirely. It lives as a parasite inside a vine, and may even have lost its chloroplast genes."]),
    dict(key="twist", scene="p_coral", lines=[
        "Except some animals found a middle path.",
        "Corals are animals. The tiny algae living inside them can hand over as much as ninety percent of the food they make from sunlight. That's how corals build giant reefs in clear, nutrient-poor water. The Great Barrier Reef, built on that partnership, is the largest structure made by living things on Earth. You can see it from space.",
        "The algae also give corals their colors. Lose the algae, and the coral turns white. That's coral bleaching."], sfx=[("scratch", 0.0)]),
    dict(key="clam", scene="p_clam", lines=[
        "Giant clams farm algae in their fleshy mantle, which soaks up about ninety-five percent of the sunlight that hits it.",
        "And the green hydra, a tiny freshwater animal, keeps algae inside its cells. The algae pay it in sugar. It pays them in nitrogen.",
        "There's even a jellyfish that lives upside down. The upside-down jellyfish lies bell-first on the seafloor, arms facing up, so the algae living in those arms get as much sunlight as possible."]),
    dict(key="slug", scene="p_slug", lines=[
        "Then there's a sea slug that steals. Eh-liz-ee-uh klor-ot-ih-kuh eats algae, but keeps their chloroplasts working inside its own cells, and can go nine months or more without eating.",
        "A leaf-shaped animal, just a few centimeters long, running on stolen solar panels. Although scientists still argue about how much the sunlight really helps.",
        "Some of its relatives are even stranger. They can drop their entire body, and the head grows a whole new one, heart included, in a few weeks."]),
    dict(key="salam2", scene="p_salamander", lines=[
        "And our salamander? Inside the egg, the algae give off oxygen, and in return they get the embryo's waste to feed on. Eggs with algae hatch earlier and bigger. But once the larvae grow, most of the algae disappear.",
        "Even nature's best example uses sunlight as a head start, not a meal plan."], opts=dict(mode="hatch")),
    dict(key="outro", scene="p_end", lines=[
        "So photosynthetic skin would get you a green tint and about a cracker a day. Not a revolution. But not nothing. And it would make you, quite literally, a little bit plant.",
        "Would you take green skin for a free snack every sunny day? Tell me in the comments."],
         hold=1.6, opts=dict(q="GREEN SKIN: YES OR NO?")),
]
C1_CH = [("hook", "An animal with algae in its cells"), ("rules", "The rules"), ("green", "You turn green"), ("c7", "7 a.m."),
         ("c12", "Noon: the math"), ("leaf", "Why plants get away with it"), ("c1y", "1 year"), ("lizard", "Going cold-blooded"),
         ("c1m", "1 million years"), ("twist", "Animals that pull it off"), ("outro", "Green skin: yes or no?")]

C2 = [  # teaser
    dict(key="t1", scene="p_green", lines=["What if your skin could make food from sunlight, like a leaf?"], opts=dict(hook="SOLAR-POWERED SKIN")),
    dict(key="t2", scene="p_green", lines=["First, you'd turn green. Chlorophyll uses less of the green light, so green is what bounces back."], opts=dict(full=True)),
    dict(key="t3", scene="p_math", lines=["At noon, sunlight brings about a thousand watts to every square meter. But plants only store around one percent of it."]),
    dict(key="t4", scene="p_tennis", lines=["For you, that's about one percent of your daily energy. Roughly a cracker a day. To live on sunlight alone, you'd need about a tennis court of skin."]),
    dict(key="t5", scene="p_brain", lines=["Your brain alone burns about twenty percent of your energy."]),
    dict(key="t6", scene="p_endshort", lines=["So how do some animals pull it off? Full story on the channel."], hold=1.4, opts=dict(top="HOW DO CORALS DO IT?")),
]
C3 = [  # standalone: sea slug
    dict(key="g1", scene="p_slug", lines=["This sea slug looks like a leaf. And in a way, it acts like one."], opts=dict(hook="THIS SLUG EATS SUNLIGHT")),
    dict(key="g2", scene="p_slug", lines=["Eh-liz-ee-uh klor-ot-ih-kuh eats a green alga, but doesn't fully digest it. It keeps the alga's chloroplasts working inside its own cells."],
         opts=dict(mode="steal", badge="STOLEN SOLAR PANELS")),
    dict(key="g3", scene="p_slug", lines=["Those stolen solar panels keep working for months. The slug can go nine months or more without eating."],
         opts=dict(mode="months", badge="9+ MONTHS")),
    dict(key="g4", scene="p_slug", lines=["Scientists once thought it had stolen algae genes too. Later sequencing found no evidence of that. How the chloroplasts keep running is still a mystery."],
         opts=dict(mode="dna", badge="STILL A MYSTERY")),
    dict(key="g5", scene="p_slug", lines=["And some of its relatives can drop their own body and regrow a whole new one from the head."],
         opts=dict(mode="regrow", badge="WAIT, WHAT?")),
    dict(key="g6", scene="p_endshort", lines=["So could you eat sunlight like a sea slug? Full story on the channel."], hold=1.4, opts=dict(top="COULD YOU DO IT?")),
]
C4 = [  # standalone: mantis shrimp eyes (-> photo long)
    dict(key="e1", scene="p_mantis", lines=["You see color with three types of receptors. A mantis shrimp has twelve."], opts=dict(mode="cones", hook="12 COLOR RECEPTORS")),
    dict(key="e2", scene="p_mantis", lines=["It sees ultraviolet. And it was the first animal ever shown to see circularly polarized light."],
         opts=dict(mode="uv", badge="UV + POLARIZED LIGHT")),
    dict(key="e3", scene="p_mantis", lines=["Each eye sits on its own stalk, moves on its own, and can judge depth by itself."], opts=dict(mode="eyes")),
    dict(key="e4", scene="p_mantis", lines=["So you'd see colors no human ever has? Not quite. In tests, they were worse than us at telling similar colors apart. We can spot differences of a few nanometers. They often failed below about twenty-five."],
         opts=dict(mode="test", badge="PLOT TWIST")),
    dict(key="e5", scene="p_mantis", lines=["Scientists think they recognize colors instantly instead of comparing them. Speed over detail. Handy, when your punch moves at over twenty meters per second."],
         opts=dict(mode="punch")),
    dict(key="e6", scene="p_endshort", lines=["What if your skin could eat sunlight? Full story on the channel."], hold=1.4, opts=dict(top="NEXT: SOLAR-POWERED YOU")),
]

VIDEOS = {"b3_rings": A1, "b3_magnet": B1, "b3_photo": C1,
          "short_b3_rings": A2, "short_b3_saturn": A3,
          "short_b3_magnet": B2, "short_b3_flip": B3, "short_b3_clouds": B4,
          "short_b3_photo": C2, "short_b3_slug": C3, "short_b3_mantis": C4}
CHAPTERS = {"b3_rings": A1_CH, "b3_magnet": B1_CH, "b3_photo": C1_CH}
MUSIC = {"b3_rings": "rings", "b3_magnet": "magnet", "b3_photo": "photo",
         "short_b3_rings": "rings_s", "short_b3_saturn": "rings_s",
         "short_b3_magnet": "magnet_s", "short_b3_flip": "magnet_s", "short_b3_clouds": "sky_s",
         "short_b3_photo": "photo_s", "short_b3_slug": "photo_s", "short_b3_mantis": "reef_s"}
