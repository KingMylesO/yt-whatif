"""Tiny Short used by setup.sh to prove the voice -> render -> mix chain works in a fresh workspace."""
VIDEOS = {"short_selftest": [
    dict(key="s1", scene="a_gauge", lines=["Self test. If you can hear this, the pipeline works.", "Like and subscribe for more what-ifs."],
         opts=dict(hook="SELF TEST", o2=(21, 21), cta=1)),
]}
