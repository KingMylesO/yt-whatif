"""The Crush Files #1 (one-off, owner's request 2026-11-20): What your brain does when your crush texts back.

Scene prefix cf1_ = scenes_cf01.py. Kai and the Crush come from mc.py, the set from kit3d.py.
"""
CF1 = [
    dict(key="hook", scene="cf1_room", lines=["Your crush just texted back. Here's what your brain just did."],
         opts=dict(mode="hook", hook="YOUR CRUSH TEXTED BACK"), sfx=[("pop", "L0+0.05")]),
    dict(key="maybe", scene="cf1_room", lines=[
        "Before you even open it, there's suspense. And your brain's reward chemical, dopamine, loves suspense.",
        "In one monkey study, dopamine cells stayed most active when a treat was fifty-fifty."],
         opts=dict(mode="maybe", badge="DOPAMINE LOVES SUSPENSE"), sfx=[("whoosh", 0.0)]),
    dict(key="reward", scene="cf1_room", lines=[
        "Then you see their name. When scientists scanned people who were intensely in love, a photo of their person lit up the brain's dopamine-rich reward areas."],
         opts=dict(mode="reward", badge="REWARD SYSTEM: ON"), sfx=[("whoosh", 0.0), ("pop", "L0+0.3")]),
    dict(key="flutter", scene="cf1_room", lines=[
        "Like and subscribe for more Crush Files.",
        "Now adrenaline kicks in. Your heart speeds up, and blood is pulled away from your stomach. Hello, butterflies."],
         opts=dict(mode="flutter", cta=0, badge="HEART RATE UP"), sfx=[("whoosh", 0.0)]),
    dict(key="reread", scene="cf1_room", lines=[
        "And rereading it ten times? One small study found people newly in love had serotonin changes a lot like people with O C D."],
         opts=dict(mode="reread", badge="SEROTONIN SHIFTS"), sfx=[("whoosh", 0.0)]),
    dict(key="end", scene="cf1_room", lines=["Your whole brain just reacted. More Crush Files on the channel."], hold=1.4,
         opts=dict(mode="end"), sfx=[("pop", "L0+0.5")]),
]

VIDEOS = {"short_cf01_text": CF1}
CHAPTERS = {}
MUSIC = {"short_cf01_text": "crush_s"}
TTS_MAP = {"O C D": "OCD"}
