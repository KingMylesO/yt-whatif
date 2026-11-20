"""Batch 05 (HUMAN BODY): What If All the Bacteria in Your Body Vanished? (+ teaser and "You're about half bacteria" Shorts).

Scene prefix x5_ = scenes_b5_microbes.py. Music presets: "microbe" (long), "microbe_s" (Shorts).
TTS spellings are mapped back for captions via TTS_MAP (read by meta2.tts_to_text).
"""
CARD = 1.9

def card(key, text, label, scene="x5_card"):
    return dict(key=key, scene=scene, lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label))

XL = "YOUR BODY, BACTERIA-FREE"
X1 = [
    dict(key="hook", scene="x5_body", lines=[
        "Right now, about thirty-eight trillion bacteria are living in and on your body.",
        "That's more than the number of cells that are actually you. Together, they weigh about two hundred grams. Roughly the weight of an apple.",
        "So what if, in one instant, every single one of them vanished?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="x5_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF ALL YOUR BACTERIA", l2="SUDDENLY VANISHED?")),
    dict(key="rules", scene="x5_rules", lines=[
        "Here are the rules. At exactly midnight, every bacterium in and on your body disappears. Your gut, your skin, your mouth. All of them, gone.",
        "Viruses and fungi stay, just to keep things simple. And nothing else about you changes. Your own cells are completely fine.",
        "To make sure the bacteria can't sneak back in, you move into a sterile room. The air is filtered, and every meal and every glass of water is sterilized first.",
        "Labs have kept animals like this for decades. They're called germ-free animals. So we know a surprising amount about what happens next."]),
    card("c0", "THE HEADCOUNT", XL),
    dict(key="census", scene="x5_count", lines=[
        "But first, how many bacteria are we actually talking about? For decades, textbooks said they outnumbered your own cells ten to one.",
        "That ratio traces back to a quick, back-of-the-envelope estimate from nineteen seventy-two, by the microbiologist Thomas Luckey. It got repeated for more than forty years.",
        "In twenty sixteen, a team led from Israel's Weizmann Institute did a careful recount. Their answer: about thirty-eight trillion bacteria, against about thirty trillion human cells.",
        "So it's closer to one to one. And here's the strange part. About eighty-four percent of your own cells, by count, are red blood cells."],
         opts=dict(mode="census")),
    dict(key="where", scene="x5_count", lines=[
        "Almost all of those bacteria live in one place: your colon. The part packed with bacteria holds only about four hundred milliliters. A little more than a can of soda.",
        "Your skin carries around a trillion more. And your mouth, despite its reputation, holds less than one percent as many as your colon.",
        "The two totals are so close that, as the researchers pointed out, a single trip to the toilet may tip the balance back in favor of your own cells."],
         opts=dict(mode="where")),
    card("c1", "MIDNIGHT", XL),
    dict(key="vanish", scene="x5_body", lines=[
        "Midnight. The bacteria vanish. And at first, you don't feel a thing.",
        "You're about two hundred grams lighter, and almost all of that is missing from your colon.",
        "Your skin looks exactly the same. Bacteria are far too small to see. A typical one is about a micrometer across. Line up around a hundred of them, side by side, and they'd just about span the width of a human hair."],
         opts=dict(mode="vanish")),
    dict(key="genes", scene="x5_genes", lines=[
        "But you've also lost a gigantic library. A twenty-ten study catalogued about three point three million different bacterial genes in the human gut. That's more than a hundred and fifty times as many as in your own genome.",
        "Each of those genes is a tool. Tools for breaking down food, making vitamins, and building chemicals your body can't make on its own. And you just lost all of them."]),
    dict(key="odor", scene="x5_body", lines=[
        "There is one bonus. Body odor isn't really the smell of sweat itself. It's mostly made by skin bacteria, which break down molecules in sweat into pungent sulfur compounds.",
        "Some of them can be smelled at just one part per trillion. So with no bacteria, your armpits go a lot quieter."],
         opts=dict(mode="odor")),
    card("c2", "DAY ONE", XL),
    dict(key="fiber", scene="x5_gut", lines=[
        "By the next day, your gut notices. Most of the fiber you eat reaches your colon undigested, because your own body can't break it down.",
        "Normally, bacteria take over there. They ferment that fiber into short-chain fatty acids, with names like acetate, propionate and butyrate.",
        "Butyrate is the key fuel for the cells lining your colon. Most of your cells burn sugar. These ones run on food made by bacteria."],
         opts=dict(mode="normal")),
    dict(key="starve", scene="x5_gut", lines=[
        "So now, they're running on empty. In a twenty-eleven study, colon cells from germ-free mice were found in an energy-starved state. They even started digesting parts of themselves to survive.",
        "When the researchers gave those cells butyrate, the energy shortage went away.",
        "Meanwhile, the fiber you eat just passes straight through. One small upside: bacterial fermentation also makes gas. So, a lot less of that."],
         opts=dict(mode="starve")),
    card("c3", "ONE WEEK", XL),
    dict(key="vitamins", scene="x5_vitamins", lines=[
        "After a week, the missing chemistry starts to matter. Gut bacteria make vitamin K, which your blood needs to clot, and several B vitamins.",
        "In studies where volunteers ate a diet low in vitamin K, they stayed fine for weeks. But when they also took a broad-spectrum antibiotic, the level of a key clotting protein in their blood dropped.",
        "Germ-free rats in the nineteen-fifties ran into the same problem. They developed vitamin K deficiency unless it was added to their food. So in your sterile room, the menu now needs extra vitamins."]),
    dict(key="cecum", scene="x5_mouse", lines=[
        "Then comes the strangest change of all. Mice raised germ-free grow an enormous see-kum. That's a pouch at the start of the large intestine. In mice, it's where a lot of the fermenting happens.",
        "With no microbes to break things down, mucus, digestive enzymes and water pile up inside it. In some strains of germ-free mice, the see-kum can reach up to a fifth of the animal's entire body weight.",
        "Nobody knows whether a human gut would do the same. But if yours did, that pouch would weigh about fourteen kilograms. Roughly a beagle."]),
    card("c4", "ONE MONTH", XL),
    dict(key="immune", scene="x5_immune", lines=[
        "Quick favor before we go on: if you're enjoying this, tap like and subscribe. It really helps the channel.",
        "Over the following weeks, your immune system goes through a slow, quiet change. A big part of it sits along your gut, and it learns by constantly meeting your bacteria.",
        "Animals raised germ-free tend to have underdeveloped immune tissue in the gut, fewer of some kinds of immune cells, and less of a gut antibody called eye-gee-A.",
        "Your bacteria also work like bouncers. They take up the space, and eat the food, that a dangerous germ would need. Scientists call this colonization resistance."],
         opts=dict(mode="train", cta=0)),
    dict(key="cdiff", scene="x5_immune", lines=[
        "And we know what happens when the bouncers leave. Antibiotics can wipe out many gut bacteria at once. That's when a germ called see diff can take over.",
        "One C-D-C estimate counted more than four hundred and fifty thousand of these infections in the United States in a single year, linked to about twenty-nine thousand deaths.",
        "In your sterile room, there's nothing to catch. But your gut is now like a house with nobody home and the doors unlocked."],
         opts=dict(mode="cdiff")),
    dict(key="brain", scene="x5_brain", lines=[
        "Germ-free mice even behave differently. In a twenty-oh-four study in Japan, they released far more stress hormones than normal mice when they were briefly restrained.",
        "Yet in a twenty-eleven study in Sweden, germ-free mice were bolder. They explored more, and spent more time in bright, open spaces that mice usually avoid.",
        "Giving the mice bacteria early in life reversed these effects. How much of this applies to people is still an open question."]),
    card("c5", "YEARS LATER", XL),
    dict(key="history", scene="x5_history", lines=[
        "So could you live like this for years? Animals can. But it took scientists a long time to find out.",
        "In the eighteen-eighties, Louis Pasteur suspected that animals might not be able to live without bacteria at all. In the eighteen-nineties, two researchers in Berlin raised germ-free guinea pigs for the first time, for just a few days.",
        "By the nineteen-forties, labs were raising whole colonies. Bengt Gustafsson in Sweden bred germ-free rats in steam-sterilized isolators. And at the University of Notre Dame, a lab called Low-bund kept germ-free animals inside steel chambers.",
        "Today, germ-free mice are a standard research tool. With a fortified diet, they do fine. Though in some strains, that giant see-kum causes serious trouble as they age."]),
    dict(key="bubble", scene="x5_rules", lines=[
        "For humans, sterile rooms are real. But they're a medical tool, not a lifestyle. Babies born without a working immune system may need to stay in sterile isolation while they wait for a stem cell transplant.",
        "So a germ-free you could probably survive, with extra vitamins and a lot of care. But you'd be living in a bubble, with a big part of your body's machinery switched off."],
         opts=dict(mode="bubble")),
    dict(key="twist", scene="x5_out", lines=[
        "And here's the twist. The moment you open that door, the experiment is over.",
        "A Yale study found that a single person's presence can add around thirty-seven million bacteria to a room's air every hour, much of it stirred up from floor dust.",
        "A single day of meals can carry anywhere from about a million to over a billion live microbes, depending on the diet.",
        "Every breath, every handshake, every bite. You'd start picking up new bacteria right away."],
         sfx=[("scratch", 0.0)]),
    dict(key="recover", scene="x5_recover", lines=[
        "And a gut can rebuild surprisingly fast. In a twenty-eighteen study, twelve healthy men took a strong four-day mix of antibiotics. Within about six weeks, their gut communities were close to normal again.",
        "But not completely. Nine species that every one of them carried at the start were still missing in most of them six months later."]),
    dict(key="baby", scene="x5_baby", lines=[
        "And here's the best part. You've already done this once. In twenty twenty-three, a group of forty-six experts concluded that babies in the womb don't carry live bacteria. You started life essentially sterile.",
        "Then, during and after birth, you were colonized. Babies born vaginally first pick up bacteria that resemble their mother's vaginal microbes. Babies born by C-section pick up more skin bacteria first.",
        "So your thirty-eight trillion passengers aren't a fixed part of you. They're a crowd that moved in on day one, and they've been coming and going ever since."]),
    dict(key="outro", scene="x5_end", lines=[
        "So if every bacterium in your body vanished, you'd be a little lighter, a lot less smelly, and missing a huge chemistry set. And the second you stepped outside, they'd start moving back in.",
        "If you could keep just one of your bacteria's jobs, which one would it be? Tell me in the comments."],
         hold=1.6, opts=dict(q="WHICH JOB WOULD YOU KEEP?")),
]
X1_CH = [("hook", "38 trillion passengers"), ("rules", "The rules"), ("c0", "The headcount: the 10-to-1 myth"), ("c1", "Midnight: they vanish"),
         ("odor", "The bonus: no body odor"), ("c2", "Day one: starving colon cells"), ("c3", "One week: vitamins & a giant cecum"),
         ("c4", "One month: the immune system"), ("brain", "Germ-free mice behave differently"), ("c5", "Years: living germ-free"),
         ("twist", "The twist: opening the door"), ("baby", "You've done this before"), ("outro", "Which job would you keep?")]

X2 = [  # teaser
    dict(key="s1", scene="x5_body", lines=["What if every bacterium in your body vanished, right now?"], opts=dict(mode="intro", hook="ALL YOUR BACTERIA: GONE")),
    dict(key="s2", scene="x5_body", lines=["You'd lose about thirty-eight trillion cells. More than your own, by count. But they only weigh about two hundred grams."],
         opts=dict(mode="vanish", badge="38 TRILLION GONE")),
    dict(key="s3", scene="x5_gut", lines=["Within a day, the cells lining your colon would be low on fuel. They run on butyrate, made by bacteria from fiber.",
                                          "Like and subscribe for more body what-ifs."],
         opts=dict(mode="starve", cta=1)),
    dict(key="s4", scene="x5_mouse", lines=["In germ-free lab mice, a gut pouch called the see-kum balloons. In some strains, up to a fifth of their body weight."],
         opts=dict(badge="UP TO 1/5 OF BODY WEIGHT")),
    dict(key="s5", scene="x5_out", lines=["But you couldn't stay sterile. One person can add around thirty-seven million bacteria to a room's air every hour."],
         opts=dict(badge="~37 MILLION / HOUR")),
    dict(key="s6", scene="x5_endshort", lines=["So how long before they're back? Full story on the channel."], hold=1.4, opts=dict(top="ALL BACTERIA GONE?")),
]
X3 = [  # standalone: you're about half bacteria
    dict(key="h1", scene="x5_count", lines=["You are about half bacteria. Not ten to one. About half."], opts=dict(mode="census", hook="YOU'RE ~HALF BACTERIA")),
    dict(key="h2", scene="x5_count", lines=["For decades, textbooks said bacteria outnumber your cells ten to one. That came from a quick estimate in nineteen seventy-two, repeated for forty years."],
         opts=dict(mode="myth", badge="THE 10:1 MYTH")),
    dict(key="h3", scene="x5_count", lines=["In twenty sixteen, scientists recounted. About thirty-eight trillion bacteria, against thirty trillion human cells.",
                                            "Like and subscribe for more body facts."],
         opts=dict(mode="scale", badge="38 TRILLION VS 30 TRILLION", cta=1)),
    dict(key="h4", scene="x5_count", lines=["Most of your own cells are red blood cells. And most of the bacteria are packed into your colon."],
         opts=dict(mode="where", badge="84% RED BLOOD CELLS")),
    dict(key="h5", scene="x5_count", lines=["It's so close that one trip to the toilet may tip the balance back toward you."],
         opts=dict(mode="flip", badge="1.3 : 1")),
    dict(key="h6", scene="x5_endshort", lines=["So what if all those bacteria vanished? Full story on the channel."], hold=1.4, opts=dict(top="ALL BACTERIA GONE?")),
]

VIDEOS = {"b5_microbes": X1, "short_b5_microbes": X2, "short_b5_cells": X3}
CHAPTERS = {"b5_microbes": X1_CH}
MUSIC = {"b5_microbes": "microbe", "short_b5_microbes": "microbe_s", "short_b5_cells": "microbe_s"}
TTS_MAP = {
    "nineteen seventy-two": "1972", "twenty sixteen": "2016", "twenty-ten": "2010", "twenty-eleven": "2011", "twenty-oh-four": "2004",
    "twenty-eighteen": "2018", "twenty twenty-three": "2023", "nineteen-fifties": "1950s", "nineteen-forties": "1940s",
    "eighteen-eighties": "1880s", "eighteen-nineties": "1890s", "see-kum": "cecum", "eye-gee-A": "IgA", "see diff": "C. diff",
    "C-D-C": "CDC", "Low-bund": "LOBUND",
}
