#!/usr/bin/env python3
"""Hand-checkable tests for the prototype simulate.py.

Run:  python3 tests/test_simulate.py
Every expected number below can be verified with a pocket calculator.
"""
import csv
import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, "..", "plugins", "autograntor", "skills",
                   "grant-adversarial-estimate-v2", "docs", "simulate.py")
spec = importlib.util.spec_from_file_location("simulate", SIM)
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)

TMP = tempfile.mkdtemp()


def ledger(name, rows):
    path = os.path.join(TMP, name)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=sim.COLUMNS)
        w.writeheader()
        for r in rows:
            base = {c: "" for c in sim.COLUMNS}
            base.update(size="1M", group="policy", post2030="0")
            base.update(r)
            w.writerow(base)
    return path


def model(path, branches=None, execs=None, corr=None, size=1e6):
    return sim.Model(sim.load_ledger(path), size, branches or {}, execs or {}, corr or {})


def close(a, b, tol=1e-6):
    assert abs(a - b) <= tol, f"{a} != {b} (tol {tol})"


def test_event_mean_is_weight_times_probability_shift():
    # CL-2's example: a law at 10% -> 12% gets 2% of the weight.
    m = model(ledger("a.csv", [dict(name="law", kind="event", weight=8000, p1=0.12, p0=0.10)]))
    close(m.analytic()["mean"], 160.0)


def test_three_row_ledger_adds_up():
    # 5000 x 0.02 + 300 x 0.40 - 200 x 0.04 = 100 + 120 - 8 = 212
    m = model(ledger("b.csv", [
        dict(name="law", kind="event", weight=5000, p1=0.12, p0=0.10),
        dict(name="paper", kind="event", weight=300, p1=0.60, p0=0.20, group="research"),
        dict(name="press", kind="event", weight=-200, p1=0.05, p0=0.01, group="exposure"),
    ]))
    a = m.analytic()
    close(a["mean"], 212.0)
    close(a["groups"]["policy"], 100.0)
    close(a["groups"]["research"], 120.0)
    close(a["groups"]["exposure"], -8.0)


def test_simulated_mean_matches_analytic_mean():
    m = model(ledger("c.csv", [
        dict(name="law", kind="event", weight=5000, p1=0.12, p0=0.10),
        dict(name="paper", kind="event", weight=300, p1=0.60, p0=0.20, group="research"),
        dict(name="charge", kind="charge", ev=-20, sigma=5, group="money"),
    ]))
    fixed, _ = m.simulate(400000, 1)
    close(fixed.mean(), m.analytic()["mean"], tol=4.0)


def test_cl16_credit_when_outcome_occurs():
    # p1 = 0.5, p0 = 0.25, weight 100: credit is 100 x (1 - 0.25/0.5) = 50 in the half of
    # worlds where it happens, 0 otherwise. Mean 25, median 0 or 50, never above 50.
    m = model(ledger("d.csv", [dict(name="x", kind="event", weight=100, p1=0.5, p0=0.25)]))
    fixed, _ = m.simulate(100000, 2)
    close(m.analytic()["mean"], 25.0)
    assert set(round(v, 6) for v in set(fixed.tolist())) == {0.0, 50.0}
    close(fixed.mean(), 25.0, tol=0.5)


def test_pivotal_changes_spread_not_mean():
    plain = model(ledger("e1.csv", [dict(name="x", kind="event", weight=100, p1=0.5, p0=0.25)]))
    piv = model(ledger("e2.csv", [dict(name="x", kind="event", weight=100, p1=0.5, p0=0.25,
                                       pivotal=1)]))
    close(plain.analytic()["mean"], piv.analytic()["mean"])
    fp, _ = piv.simulate(100000, 3)
    # fully pivotal: full weight 100 in the 25% of worlds where the grant made the difference
    assert set(round(v, 6) for v in set(fp.tolist())) == {0.0, 100.0}
    close(fp.mean(), 25.0, tol=0.6)
    close((fp > 0).mean(), 0.25, tol=0.01)


def test_grant_that_lowers_a_probability():
    # A harm (weight -1000) made less likely, 10% -> 4%: value = -1000 x (0.04 - 0.10) = +60.
    m = model(ledger("f.csv", [dict(name="harm averted", kind="event", weight=-1000,
                                    p1=0.04, p0=0.10, group="exposure")]))
    close(m.analytic()["mean"], 60.0)
    fixed, _ = m.simulate(400000, 4)
    close(fixed.mean(), 60.0, tol=1.5)


def test_exec_modes_give_different_means():
    execs = {"team": [[0.2, 0.0], [0.8, 1.0]]}  # mean multiplier 0.8, 20% collapse
    credit = model(ledger("g1.csv", [dict(name="x", kind="event", weight=1000, p1=0.30, p0=0.10,
                                          exec="team", exec_mode="credit")]), execs=execs)
    p1mode = model(ledger("g2.csv", [dict(name="x", kind="event", weight=1000, p1=0.30, p0=0.10,
                                          exec="team", exec_mode="p1")]), execs=execs)
    # credit: 1000 x 0.20 x 0.8 = 160
    close(credit.analytic()["mean"], 160.0)
    # p1: with-grant probability is 0.30 in 80% of worlds and 0 in 20%: 0.24. 1000 x (0.24-0.10)
    close(p1mode.analytic()["mean"], 140.0)
    f1, _ = credit.simulate(400000, 5)
    f2, _ = p1mode.simulate(400000, 5)
    close(f1.mean(), 160.0, tol=3.0)
    close(f2.mean(), 140.0, tol=3.0)


def test_exec_factor_never_touches_charges():
    execs = {"team": [[0.5, 0.0], [0.5, 1.0]]}
    m = model(ledger("h.csv", [
        dict(name="program", kind="continuous", ev=100, sigma=0, exec="team", group="research"),
        dict(name="cost", kind="charge", ev=-30, sigma=0, exec="team", group="money"),
    ]), execs=execs)
    close(m.analytic()["mean"], 100 * 0.5 - 30)
    fixed, _ = m.simulate(1000, 6)
    assert set(round(v, 6) for v in set(fixed.tolist())) == {-30.0, 70.0}


def test_branches_mix_and_corners():
    m = model(ledger("i.csv", [
        dict(name="base", kind="continuous", ev=100, sigma=0, group="research"),
        dict(name="helps", kind="continuous", ev=30, sigma=0, group="values",
             branch="q", branch_val="yes"),
        dict(name="hurts", kind="continuous", ev=-45, sigma=0, group="values",
             branch="q", branch_val="no"),
    ]), branches={"q": {"yes": 0.6, "no": 0.4}})
    a = m.analytic()
    close(a["mean"], 100 + 0.6 * 30 - 0.4 * 45)  # 100
    corners = {ans["q"]: mean for ans, _, mean in a["corners"]}
    close(corners["yes"], 130.0)
    close(corners["no"], 55.0)


def test_post2030_share():
    m = model(ledger("j.csv", [
        dict(name="now", kind="continuous", ev=75, sigma=0, post2030=0),
        dict(name="later", kind="continuous", ev=25, sigma=0, post2030=1),
    ]))
    a = m.analytic()
    close(a["post2030"] / a["mean"], 0.25)


def test_lognormal_exec_keeps_its_mean():
    m = model(ledger("k.csv", [dict(name="x", kind="continuous", ev=100, sigma=0, exec="t")]),
              execs={"t": {"lognormal": {"mean": 1.0, "sd": 0.5}}})
    close(m.analytic()["mean"], 100.0, tol=1e-6)


def test_correlation_widens_spread_not_mean():
    rows = [dict(name=f"r{i}", kind="continuous", ev=10, sigma=10) for i in range(10)]
    ind = model(ledger("l1.csv", rows))
    cor = model(ledger("l2.csv", rows), corr={"policy": 0.8})
    fi, _ = ind.simulate(100000, 7)
    fc, _ = cor.simulate(100000, 7)
    close(fi.mean(), 100.0, tol=1.0)
    close(fc.mean(), 100.0, tol=1.0)
    # independent sd = sqrt(10) x 10 = 31.6; with rho 0.8, sd = 10 x sqrt(10 + 90 x 0.8) = 90.6
    close(fi.std(), 31.6, tol=1.0)
    close(fc.std(), 90.6, tol=2.0)


def test_diff_agreement_test():
    a = ledger("m1.csv", [
        dict(name="a1", kind="continuous", ev=100, sigma=0, group="policy"),
        dict(name="a2", kind="continuous", ev=20, sigma=0, group="talent"),
    ])
    b_close = ledger("m2.csv", [
        dict(name="b1", kind="continuous", ev=110, sigma=0, group="policy"),
        dict(name="b2", kind="continuous", ev=25, sigma=0, group="talent"),
    ])
    b_far = ledger("m3.csv", [
        dict(name="b1", kind="continuous", ev=30, sigma=0, group="policy"),
        dict(name="b2", kind="continuous", ev=100, sigma=0, group="talent"),
    ])
    none = {"branches": {}, "exec": {}}
    assert "AGREEMENT TEST: AGREE" in sim.diff(a, b_close, 1e6, none, none)
    out = sim.diff(a, b_far, 1e6, none, none)
    assert "AGREEMENT TEST: DIVERGE" in out
    assert "same: NO" in out


def test_given_makes_a_cost_conditional_without_changing_the_mean():
    # A programme starts with probability 0.10 (vs 0 without the grant), worth 200 if it does.
    # Its running cost has an unconditional expected value of -8, i.e. -80 if it starts.
    rows = [dict(name="starts", kind="event", weight=200, p1=0.10, p0=0.0, group="field"),
            dict(name="cost", kind="charge", ev=-8, sigma=0, group="people")]
    plain = model(ledger("n1.csv", rows))
    rows[1]["given"] = "starts"
    cond = model(ledger("n2.csv", rows))
    close(plain.analytic()["mean"], 12.0)
    close(cond.analytic()["mean"], 12.0)
    fp, _ = plain.simulate(200000, 8)
    fc, _ = cond.simulate(200000, 8)
    # unconditional: -8 in the 90% of worlds where nothing happens
    close((fp < 0).mean(), 0.90, tol=0.01)
    # conditional: exactly 0 when nothing happens, 200 - 80 = 120 when it starts
    assert set(round(v, 6) for v in set(fc.tolist())) == {0.0, 120.0}
    close(fc.mean(), 12.0, tol=0.6)


def test_template_runs_and_unknown_group_is_rejected():
    path = os.path.join(TMP, "t.csv")
    with open(path, "w") as fh:
        fh.write(sim.template_csv())
    assert sim.main([path, "--branches", '{"hosting_helps":{"yes":0.5,"no":0.5}}',
                     "--exec", '{"team": 1}', "--n", "2000"]) == 0
    bad = ledger("bad.csv", [dict(name="x", kind="continuous", ev=1, group="misc")])
    try:
        sim.load_ledger(bad)
    except ValueError as e:
        assert "group" in str(e)
    else:
        raise AssertionError("unknown group was accepted")


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"ok    {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {name}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
