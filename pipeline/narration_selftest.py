"""Tiny Short used by setup.sh to prove the voice -> render -> mix chain works in a fresh workspace."""
VIDEOS = {"short_selftest": [
    dict(key="s1", scene="a_gauge", lines=["Self test. If you can hear this, the pipeline works."], opts=dict(hook="SELF TEST", o2=(21, 21))),
]}
