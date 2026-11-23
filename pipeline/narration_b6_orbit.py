"""Batch 06 BODY topic: What If You Lived in Space for 10 Years? (+ teaser, 'taller' and ozone Shorts).

Scene prefix or6_ = scenes_b6_orbit.py. TTS spellings are mapped back for captions via TTS_MAP (read by meta2).
Happening now: Shenzhou-23 (launched 24 May 2026), one crew member to stay ~1 year (CMSA, 23 May 2026);
Shenzhou-24 rolled out 17 Nov 2026, not launched as of 23 Nov 2026. NASA/NOAA 2026 ozone hole report (4 Nov 2026).
"""
CARD = 1.9

def card(key, text, label="LIFE IN ORBIT", met=0):
    return dict(key=key, scene="or6_card", lines=[], hold=CARD, sfx=[("whoosh", 0.0)], opts=dict(text=text, label=label, met=met))

# =====================================================================  LONG-FORM
L1 = [
    dict(key="hook", scene="or6_hook", lines=[
        "In May, three astronauts flew up to China's Tyen-gong space station, for what was meant to be a six-month stay.",
        "But China's space agency says one of them won't come home with the others. That astronaut will stay for about a whole year. China's first.",
        "So what if you stayed up there, not for one year, but for ten?"],
         opts=dict(mode="intro"), hold=0.2),
    dict(key="title", scene="or6_title", lines=[], hold=3.2, sfx=[("rumble", 0.0)], opts=dict(l1="WHAT IF YOU LIVED", l2="IN SPACE FOR 10 YEARS?")),
    dict(key="news", scene="or6_news", lines=[
        "First, what's actually happening. Shen-joe twenty-three launched on the twenty-fourth of May, twenty twenty-six, with commander Joo Yahng-joo, pilot Jahng Jir-ywen, and payload specialist Lie Kah-ying, the first person from Hong Kong to fly to space.",
        "The day before launch, the China Manned Space Agency said one of the three would stay in orbit for about a year, to study what long spaceflight does to the human body.",
        "Which astronaut? That hasn't been announced. The agency says the choice depends on how the mission goes.",
        "Meanwhile, the next ship, Shen-joe twenty-four, was rolled out to its launch pad on the seventeenth of November. It's expected to carry the first foreign astronaut to visit Tyen-gong, from Pakistan, for about a week. As this video was made, it hadn't launched yet."]),
    dict(key="rules", scene="or6_rules", lines=[
        "Now, the rules of our what-if. You move into a station in low orbit, like Tyen-gong or the International Space Station. You get food, air, water, and a gym.",
        "You never come down. Not for ten whole years.",
        "And a station like this races around the Earth about every ninety minutes. That's sixteen sunrises and sixteen sunsets every day. By our rough math, ten years is about fifty-eight thousand sunrises.",
        "Every single day, you cover about the distance to the Moon and back. And your body has to deal with all of it."]),
    card("c1", "DAY 1", met=0.2),
    dict(key="fluid", scene="or6_fluid", lines=[
        "The engines cut off, and you float. Within hours, your body notices that something is very wrong.",
        "On Earth, gravity pulls your blood and other fluids down toward your feet. Up here, nothing does. So about two liters of fluid shift upward, out of your legs and into your chest and head.",
        "Your face puffs up. Your legs get skinny. Astronauts have a name for it: puffy face, bird legs. Many say their head feels full, like it's stuffed."]),
    dict(key="sick", scene="or6_sick", lines=[
        "There's also a good chance you feel sick. Roughly sixty to eighty percent of space travelers get space motion sickness.",
        "Your inner ear still expects gravity to tell it which way is down. Your eyes say you're floating. Your brain can't make the two agree.",
        "A typical bout lasts two or three days. Then your brain adapts, and down becomes wherever your feet happen to be."]),
    card("c2", "WEEK 1", met=7),
    dict(key="muscle", scene="or6_muscle", lines=[
        "By the end of the first week, your muscles have noticed too.",
        "On Earth, your calves, thighs, back and neck fight gravity every second you stand. Scientists call them antigravity muscles. Up here, they have nothing to fight.",
        "The Canadian Space Agency says astronauts can lose up to twenty percent of their muscle mass on flights lasting just five to eleven days.",
        "That's why astronauts on the space station exercise about two and a half hours a day. In our what-if, so do you. Every day, for ten years."]),
    card("c3", "MONTH 1", met=30),
    dict(key="bone", scene="or6_bone", lines=[
        "One month in, a quieter loss is adding up. Your bones.",
        "Bone is alive. It's constantly rebuilt to match the loads you put on it. Take the load away, and your body starts taking bone apart.",
        "NASA says that on missions of four to six months, weight-bearing bones like the spine and hips lose one to one and a half percent of their density every month.",
        "That's fast enough, NASA warns, to put astronauts at risk of fractures and premature osteoporosis, the bone-thinning disease that normally comes with old age."]),
    dict(key="spine", scene="or6_spine", lines=[
        "But you also get a strange bonus. You grow.",
        "Without gravity squashing your spine, the soft discs between your vertebrae relax and spread out. NASA scientists say astronauts can grow up to three percent taller.",
        "For someone one point eight meters tall, that's about five centimeters.",
        "It isn't all good news. In one study of six astronauts on the space station, more than half reported back pain, and the muscles that support the lower spine shrank by about a fifth."]),
    card("c4", "MONTH 6", met=182),
    dict(key="eyes", scene="or6_eyes", lines=[
        "Six months in, the doctors watching you pay close attention to your eyes.",
        "That fluid pushed toward your head never fully drains away. About seventy percent of astronauts on long missions develop signs of something called SANS. Spaceflight associated neuro-ocular syndrome.",
        "The nerve at the back of the eye can swell. The back of the eyeball can flatten. Some astronauts come home needing new glasses.",
        "So far, no astronaut has lost their sight permanently. But nobody fully understands what causes it, and longer missions could make it worse."]),
    dict(key="rad", scene="or6_rad", lines=[
        "Quick pause. If this is blowing your mind a little, a like and a subscribe really helps the channel.",
        "Now the danger you can't feel at all. Radiation.",
        "Down here, the atmosphere and Earth's magnetic field shield you. On the ground, people typically get about two to three millisieverts a year.",
        "In low orbit, you're still partly inside that magnetic shield, but the station's walls can't stop everything. Space station crews typically pick up about point two to point five millisieverts every single day.",
        "By our rough math, that's a month or two of ground-level radiation, every day. NASA says one millisievert is about ten chest X-rays. So that's like a few chest X-rays, every day, for as long as you stay."],
         opts=dict(cta=0)),
    card("c5", "ONE YEAR", met=365),
    dict(key="twins", scene="or6_twins", lines=[
        "One year. This is where the real data gets thin. Very few people have ever done it.",
        "From twenty fifteen to twenty sixteen, NASA astronaut Scott Kelly spent three hundred and forty days on the space station, while his identical twin brother Mark stayed on Earth. Ten research teams compared them.",
        "The strangest result? Scott's telomeres, the protective caps on the ends of his chromosomes, got longer in space. Within about two days of landing, they shortened again, and some ended up a bit shorter than before.",
        "His gene activity changed too. About ninety-one percent of those changes went back to normal within six months. But his thinking speed and accuracy dropped after landing, and were still lower six months later.",
        "And remember, it's a study of two people. The researchers themselves warn that you can't draw firm rules from it."]),
    dict(key="records", scene="or6_records", lines=[
        "The record for the longest single stay belongs to Russian doctor and cosmonaut Valeri Polyakov. Four hundred and thirty-seven days aboard the Mir station, from January nineteen ninety-four to March nineteen ninety-five.",
        "His mission was meant to test whether a human body could survive a trip as long as a journey to Mars. After landing, cosmonauts were usually carried from the capsule. He chose to walk.",
        "The record for the most total time in space belongs to Oleg Kononenko. In June twenty twenty-four, he became the first person to pass one thousand days. He finished with one thousand one hundred and eleven, over five flights.",
        "Now put our what-if on the same chart. Ten years is about three thousand six hundred and fifty days. More than three times anyone has ever spent up there, even added together."]),
    card("c6", "TEN YEARS", met=3652),
    dict(key="ten", scene="or6_ten", lines=[
        "So, ten years. Nobody has done it, so from here on we're extrapolating. Treat this as rough math, not a forecast.",
        "Start with radiation. NASA's limit for an astronaut's entire career is six hundred millisieverts.",
        "At point two to point five millisieverts a day, you'd reach that limit somewhere between about three and eight years in. After ten years, you'd have roughly seven hundred and thirty to eighteen hundred. Up to three times the career limit.",
        "Then bone. Nobody knows if bone keeps disappearing at the same pace, because nobody has stayed long enough to find out. NASA itself says more research is needed on longer missions.",
        "And your eyes, your arteries and your immune system are all on the list of things that changed in the twin study. For ten years, the honest answer is: we don't know."]),
    dict(key="mars", scene="or6_mars", lines=[
        "And that's exactly why space agencies care. Because a trip to Mars is the real long haul.",
        "In one NASA reference plan, the flight out takes about one hundred and eighty days, then you stay about five hundred days on the surface, and fly another one hundred and eighty days home. Nearly two and a half years.",
        "On its way to Mars, NASA's Curiosity rover carried a radiation detector. It measured about one point eight millisieverts a day in deep space. By that measure, just the flights there and back would add up to about six hundred and sixty millisieverts. Already past the career limit, before anyone sets foot on Mars.",
        "That's what a year on Tyen-gong is really for. Every month someone spends up there teaches us how to keep a body working far from home."]),
    dict(key="twist", scene="or6_twist", lines=[
        "And here's the twist. The ten years in orbit might not be the hardest part. Coming home is.",
        "Remember those extra five centimeters? You lose them. Within a few months back on Earth, astronauts shrink back to their normal height.",
        "A lot of the other changes fade too. In the twin study, Scott Kelly's gut bacteria went back to how they were before the flight, and most of his gene changes went back to normal.",
        "But not everything. In a study of seventeen astronauts, the weight-bearing bones of most of them had only partly recovered a year after landing. The lasting loss was about the same as a decade of normal aging.",
        "And in that study of six astronauts, the risk of a slipped disc was about four times higher in the months after they got home. Your spine stretched out in space, and gravity squeezes it back."],
         sfx=[("scratch", 0.0)]),
    dict(key="outro", scene="or6_end", lines=[
        "So ten years in space would stretch you, puff you up, thin your bones and soak you in radiation. Much of it would heal. Not all of it.",
        "And right now, somebody up there is starting the year that helps us find out how far a body can go. Would you sign up for the ten-year trip? Tell me in the comments."],
         hold=1.6, opts=dict(q="WOULD YOU GO?")),
]
L1_CH = [("hook", "One astronaut stays a year"), ("news", "What's happening on Tiangong"), ("rules", "The rules"),
         ("c1", "Day 1: puffy face, bird legs"), ("sick", "Space motion sickness"), ("c2", "Week 1: muscles"),
         ("c3", "Month 1: bones"), ("spine", "You grow taller"), ("c4", "Month 6: your eyes"), ("rad", "Radiation"),
         ("c5", "One year: the twin study"), ("records", "The records"), ("c6", "Ten years: the rough math"),
         ("mars", "Why Mars needs this"), ("twist", "Coming home is the hard part"), ("outro", "Would you go?")]

# =====================================================================  SHORTS
S1 = [  # teaser
    dict(key="a1", scene="or6_hook", lines=["What if you lived in space for ten years?"], opts=dict(mode="intro", hook="10 YEARS IN SPACE")),
    dict(key="a2", scene="or6_fluid", lines=["Day one. About two liters of fluid rush up toward your head. Astronauts call it puffy face, bird legs."],
         opts=dict(badge="2 LITERS HEADWARD")),
    dict(key="a3", scene="or6_bone", lines=["Month one. Your spine and hips lose one to one and a half percent of their bone density, every month."],
         opts=dict(badge="−1.5% BONE A MONTH")),
    dict(key="a4", scene="or6_spine", lines=["Like and subscribe for more what-ifs.",
                                           "Meanwhile, your spine stretches. You can grow up to three percent taller."],
         opts=dict(cta=0, badge="UP TO 3% TALLER")),
    dict(key="a5", scene="or6_ten", lines=["And each day in orbit brings a month or two of ground-level radiation. Ten years would blow past NASA's career limit."],
         opts=dict(mode="short", badge="PAST THE LIMIT")),
    dict(key="a6", scene="or6_endshort", lines=["One astronaut on China's space station is about to stay a whole year. Full story on the channel."],
         hold=1.4, opts=dict(top="10 YEARS UP?")),
]
S2 = [  # standalone: astronauts come home taller
    dict(key="t1", scene="or6_spine", lines=["Astronauts come home taller."], opts=dict(mode="intro", hook="ASTRONAUTS GROW")),
    dict(key="t2", scene="or6_spine", lines=["In orbit, nothing squashes your spine. The soft discs between your vertebrae relax and spread out."],
         opts=dict(mode="discs")),
    dict(key="t3", scene="or6_spine", lines=["NASA scientists say you can grow up to three percent. For someone one point eight meters tall, that's about five centimeters."],
         opts=dict(mode="ruler", badge="UP TO 5 CM")),
    dict(key="t4", scene="or6_spine", lines=["Like and subscribe for more body what-ifs.",
                                             "But there's a price. In one study, more than half the crew had back pain, and their lower back muscles shrank by about a fifth."],
         opts=dict(mode="pain", cta=0, badge="−19% BACK MUSCLE")),
    dict(key="t5", scene="or6_twist", lines=["Back on Earth, gravity squeezes you down again within a few months. And the risk of a slipped disc was about four times higher."],
         opts=dict(mode="short", badge="4× DISC RISK")),
    dict(key="t6", scene="or6_endshort", lines=["So what would ten years in space do to you? Full story on the channel."], hold=1.4, opts=dict(top="10 YEARS UP?")),
]
S3 = [  # standalone, happening now: the 2026 ozone hole -> what if the ozone layer disappeared
    dict(key="z1", scene="or6_oz", lines=["This year's ozone hole was the biggest in a decade."], opts=dict(mode="intro", hook="BIGGEST IN A DECADE")),
    dict(key="z2", scene="or6_oz", lines=["On November fourth, NASA and NOAA reported it averaged about twenty-five million square kilometers. About the size of North America."],
         opts=dict(mode="size", badge="25 MILLION KM²")),
    dict(key="z3", scene="or6_oz", lines=["The cause was an unusually strong polar vortex. And the good news? The layer is still healing."],
         opts=dict(mode="vortex", badge="STILL HEALING")),
    dict(key="z4", scene="or6_oz", lines=["So what if the ozone layer disappeared?",
                                          "Like and subscribe for more Earth what-ifs.",
                                          "Squeeze all that ozone down to sea level, and it's only about three millimeters thick."],
         opts=dict(mode="thin", cta=1, badge="ONLY ~3 MM")),
    dict(key="z5", scene="or6_oz", lines=["That thin shield soaks up all of the Sun's UV-C, and most of its UV-B. In a NASA simulation of a world that never banned ozone-killing chemicals, you could get sunburned in about five minutes."],
         opts=dict(mode="uv", badge="SUNBURN IN 5 MIN")),
    dict(key="z6", scene="or6_ozend", lines=["What does space radiation do to your body? Full story on the channel."], hold=1.4, opts=dict(top="SPACE RADIATION?")),
]

VIDEOS = {"b6_orbit": L1, "short_b6_orbit": S1, "short_b6_taller": S2, "short_b6_ozone": S3}
CHAPTERS = {"b6_orbit": L1_CH}
MUSIC = {"b6_orbit": "orbit", "short_b6_orbit": "orbit_s", "short_b6_taller": "orbit_s", "short_b6_ozone": "sky2_s"}
TTS_MAP = {
    "Shen-joe twenty-three": "Shenzhou-23",
    "Shen-joe twenty-four": "Shenzhou-24",
    "Shen-joe": "Shenzhou",
    "Tyen-gong": "Tiangong",
    "Joo Yahng-joo": "Zhu Yangzhu",
    "Jahng Jir-ywen": "Zhang Zhiyuan",
    "Lie Kah-ying": "Lai Ka-ying",
    "twenty fifteen": "2015",
    "twenty sixteen": "2016",
    "nineteen ninety-four": "1994",
    "nineteen ninety-five": "1995",
    "point two to point five millisieverts": "0.2 to 0.5 millisieverts",
    "one point eight millisieverts": "1.8 millisieverts",
    "one point eight meters": "1.8 meters",
}
META = {
    "b6_orbit": dict(
        title="What If You Lived in Space for 10 Years?",
        hook="On 23 May 2026, China's space agency said one Shenzhou-23 astronaut, launched to the Tiangong station on 24 May, will stay in orbit for about a year, China's first year-long mission. So what would ten years up there do to your body? Day by day, from puffy faces and growing spines to bone loss, eye changes and radiation, with the real data from the NASA Twins Study and the records of Polyakov and Kononenko.",
        tags=["what if", "space", "astronaut", "human body", "Tiangong", "Shenzhou-23", "year in space", "NASA twins study",
              "bone loss", "space radiation", "microgravity", "science", "space station"],
        hashtags="#whatif #science #space", parent=None),
    "short_b6_orbit": dict(
        title="What If You Lived in Space for 10 Years? #shorts",
        hook="One Shenzhou-23 astronaut (launched 24 May 2026) is set to stay on China's Tiangong station for about a year. What would ten years do to your body?",
        tags=["what if", "space", "astronaut", "human body", "Tiangong", "shorts"],
        hashtags="#whatif #science #space", parent="b6_orbit"),
    "short_b6_taller": dict(
        title="Why Astronauts Come Home Taller #shorts",
        hook="In microgravity your spine stretches and astronauts can grow up to 3% taller, but it comes with back pain and doesn't last.",
        tags=["astronaut", "taller in space", "spine", "microgravity", "human body", "shorts"],
        hashtags="#whatif #science #space", parent="b6_orbit"),
    "short_b6_ozone": dict(
        title="What If the Ozone Layer Disappeared? #shorts",
        hook="On 4 November 2026, NASA and NOAA reported that the 2026 Antarctic ozone hole averaged about 25 million km², the largest in a decade. So what if the ozone layer vanished altogether?",
        tags=["ozone layer", "ozone hole", "2026", "NASA", "NOAA", "Montreal Protocol", "UV", "what if", "shorts"],
        hashtags="#whatif #science #earth", parent="b6_orbit"),
}
