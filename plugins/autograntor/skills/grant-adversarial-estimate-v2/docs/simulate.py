#!/usr/bin/env python3
"""Autograntor ledger simulator -- PROTOTYPE RECONSTRUCTION.

This is NOT the Autograntor owner's original simulate.py. It was rebuilt from
the v2 skill's description of the tool and from the published Common Law
(CL-1, CL-2, CL-16, CL-17, CL-18, CL-37, CL-40, CL-55). Where those sources do
not pin a convention down, this file makes a choice and marks it "GUESS".
Swap in the original when it is available; the command line is meant to match.

Run `python3 simulate.py --help` for the ledger columns and the group list.
"""
import argparse
import csv
import io
import itertools
import json
import math
import re
import sys
from statistics import NormalDist

try:
    import numpy as np
except ImportError:  # pragma: no cover
    sys.exit("simulate.py needs numpy: pip install numpy")

VERSION = "prototype-0.3 (reconstruction, not the original)"

COLUMNS = [
    "name", "size", "kind", "weight", "p1", "p0", "ev", "sigma", "pivotal",
    "exec", "exec_mode", "group", "branch", "branch_val", "post2030", "given", "note",
]
OPTIONAL_COLUMNS = {"note", "given"}

# GUESS: the skill names only `uptake`, `values` and `exposure`. The rest of
# this list is the packager's. File by causal path, not by sign (see SKILL.md).
GROUPS = {
    "research": "Direct research or technical outputs existing (papers, tools, evals, datasets).",
    "uptake": "Outputs being used: adoption by labs, governments or the field, including the "
              "harm-branch mirror of any uptake row (e.g. 'harness is net capabilities').",
    "talent": "People entering, staying in or moving up in safety or policy work.",
    "policy": "Laws, regulations, executive actions and other government outcomes.",
    "opinion": "Opinion change in the public or in elites (PERCYs rows and their mirrors).",
    "field": "Institutions, venues, community and field infrastructure existing or surviving.",
    "continuation": "Later program years or organisational survival the grant makes possible "
                    "(CL-23, CL-31, CL-38).",
    "money": "Money charges and credits: CL-4 follow-on money, funging, freed backstops, "
             "banked runway.",
    "people": "People charges: CL-4 scarce-people cost, CL-36 bad hires and breakdown.",
    "exposure": "ONLY press, scandal, partisan-coding and incident rows.",
    "values": "ONLY rows that exist in no causal path (pure signalling or trust-norm rows).",
    "other": "Anything else; say what in the note. Avoid: it weakens the agreement test.",
}

HELP_EPILOG = """
LEDGER COLUMNS (CSV, one row per consequence)
  name        Short unique label for the row.
  size        Grant size the row belongs to, e.g. 250000, $250K, 1M. Blank = every size.
  kind        event | continuous | charge
  weight      [event] utility if the outcome happens (signed; negative for a harm).
  p1          [event] probability of the outcome WITH the grant.
  p0          [event] probability of the outcome WITHOUT the grant.
              Expected value of an event row = weight x (p1 - p0)        (CL-1, CL-2)
  ev          [continuous, charge] expected utility of the row (signed).
  sigma       [continuous, charge] standard deviation of that utility (blank = 0).
  pivotal     [event, optional] share (0-1) of the row's credit that arrives in rare
              "pivotal" worlds where the grant visibly made the difference (CL-55).
              Blank or 0 = plain CL-16: weight x (1 - p0/p1) whenever the outcome occurs.
              The mean is the same either way; only the spread changes.
  exec        [event, continuous] name of the execution factor that scales this row;
              its distribution is given with --exec. Blank = no factor.
              Never applied to charge rows (CL-37, CL-40).
  exec_mode   [event rows with exec] credit | p1
              credit: p0 is the chance the same work happens anyway; the whole increment
                      (p1 - p0) is multiplied by the factor.
              p1:     p0 is a base rate from other causes; only p1 is multiplied.
              This choice changes the mean. Default: credit.
  group       One of the fixed categories below. Required.
  branch      [optional] name of a CL-11 values question this row depends on.
  branch_val  [with branch] the answer under which this row is counted.
              Rows with no branch count under every answer (CL-17).
  post2030    Share (0-1) of the row's value that comes from activity after 2030 (CL-18).
              Blank = 0.
  given       [continuous, charge; optional] name of an EVENT row. The row then counts only
              in worlds where that event happens (e.g. the cost of running a larger
              programme, paid only if the larger programme starts). `ev` stays the
              unconditional expected value, so the mean is unchanged; in the worlds where
              the event happens the row is scaled up by 1 / P(event). Give the row the same
              branch and branch_val as its event. GUESS: not described in the skill.
  note        Free text; ignored.

GROUPS
""" + "\n".join(f"  {k:<13} {v}" for k, v in GROUPS.items()) + """

ARGUMENTS THAT TAKE JSON
  --branches '{"hosting_helps": {"yes": 0.6, "no": 0.4}}'
        Weights for each values question. Weights of one question must sum to 1.
  --exec '{"team": [[0.15, 0.0], [0.60, 1.0], [0.25, 1.4]]}'
        Execution factor as [probability, multiplier] states (a collapse state is a
        multiplier of 0). Also accepted: {"team": {"lognormal": {"mean": 1.0, "sd": 0.4}}}
        or a plain number. Rows sharing a factor succeed or fail together.
  --corr '{"policy": 0.5}'
        GUESS: extra correlation between rows. The key is a group name (rows in that
        group share one common factor with that correlation) or "*" for every row.

OUTPUT
  The analytic mean is the headline. Quantiles are of realised 2030 value (CL-16) and
  are descriptive. With --branches, the headline uses the fixed weights given, and each
  "corner" (one answer per question) is also reported.
  GUESS: the "fixed-weight spread" treats a values question as a weighting, not a coin
  flip: in each simulated world the value is the weighted average over the answers.

DIFF MODE
  simulate.py --diff A.csv B.csv --size 1M --branches-a '{...}' --exec-a '{...}'
              --branches-b '{...}' --exec-b '{...}'
  Prints each ledger's headline mean under its own settings, the group-total comparison
  used by the agreement test, then row-level differences by name.
"""

TEMPLATE_ROWS = [
    ["EXAMPLE law passes", "1M", "event", "8000", "0.12", "0.10", "", "", "0.5", "team",
     "credit", "policy", "", "", "0.1", "delete these example rows"],
    ["EXAMPLE tool is used by a lab", "1M", "event", "600", "0.40", "0.10", "", "", "", "team",
     "credit", "uptake", "", "", "0", ""],
    ["EXAMPLE tool is net capabilities", "1M", "event", "-900", "0.05", "0.01", "", "", "",
     "", "", "uptake", "", "", "0", "harm mirror: same group as the row above"],
    ["EXAMPLE audience opinion shift", "1M", "continuous", "", "", "", "40", "25", "", "team",
     "", "opinion", "", "", "0", "PERCYs converted to utility"],
    ["EXAMPLE convening helps", "1M", "continuous", "", "", "", "30", "20", "", "",
     "", "values", "hosting_helps", "yes", "0", "CL-11 branch, priced both ways"],
    ["EXAMPLE convening hurts", "1M", "continuous", "", "", "", "-45", "20", "", "",
     "", "values", "hosting_helps", "no", "0", ""],
    ["EXAMPLE follow-on money charge", "1M", "charge", "", "", "", "-20", "8", "", "",
     "", "money", "", "", "0", "CL-4"],
]


def template_csv():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLUMNS)
    w.writerows(r[:-1] + [""] + r[-1:] for r in TEMPLATE_ROWS)  # blank `given` column
    return buf.getvalue()


# ---------------------------------------------------------------- parsing --

def parse_money(text):
    """'250000', '$250K', '1M', '1.5m', '$3,000,000' -> dollars (float)."""
    t = str(text).strip().replace("$", "").replace(",", "").replace(" ", "").lower()
    m = re.fullmatch(r"([0-9]*\.?[0-9]+)([kmb]?)", t)
    if not m:
        raise ValueError(f"cannot read grant size {text!r}")
    return float(m.group(1)) * {"": 1, "k": 1e3, "m": 1e6, "b": 1e9}[m.group(2)]


def fmt_money(d):
    if d >= 1e6:
        return f"${d / 1e6:g}M"
    if d >= 1e3:
        return f"${d / 1e3:g}K"
    return f"${d:g}"


def num(row, key, default=None, lo=None, hi=None):
    raw = (row.get(key) or "").strip()
    if raw == "":
        if default is None:
            raise ValueError(f"row {row.get('name')!r}: column '{key}' is required here")
        return default
    try:
        v = float(raw.rstrip("%")) / (100 if raw.endswith("%") else 1)
    except ValueError:
        raise ValueError(f"row {row.get('name')!r}: '{key}' is not a number: {raw!r}")
    if (lo is not None and v < lo) or (hi is not None and v > hi):
        raise ValueError(f"row {row.get('name')!r}: '{key}'={v} is outside [{lo}, {hi}]")
    return v


def load_ledger(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])
                   and c not in OPTIONAL_COLUMNS]
        if missing:
            raise ValueError(f"{path}: missing columns {missing}. See --template.")
        rows = []
        for raw in reader:
            if not any((v or "").strip() for v in raw.values()):
                continue
            r = {k: (v or "").strip() for k, v in raw.items() if k}
            name = r["name"]
            if not name:
                raise ValueError(f"{path}: a row has no name")
            kind = r["kind"].lower()
            if kind not in ("event", "continuous", "charge"):
                raise ValueError(f"row {name!r}: kind must be event, continuous or charge")
            group = r["group"].lower()
            if group not in GROUPS:
                raise ValueError(
                    f"row {name!r}: group {r['group']!r} is not one of {', '.join(GROUPS)}")
            row = {
                "name": name,
                "size": parse_money(r["size"]) if r["size"] else None,
                "kind": kind,
                "group": group,
                "exec": r["exec"],
                "exec_mode": (r["exec_mode"] or "credit").lower(),
                "branch": r["branch"],
                "branch_val": r["branch_val"],
                "post2030": num(r, "post2030", 0.0, 0.0, 1.0),
                "given": r.get("given", ""),
            }
            if row["given"] and kind == "event":
                raise ValueError(f"row {name!r}: 'given' is for continuous and charge rows")
            if bool(row["branch"]) != bool(row["branch_val"]):
                raise ValueError(f"row {name!r}: give both branch and branch_val, or neither")
            if kind == "event":
                row["weight"] = num(r, "weight")
                row["p1"] = num(r, "p1", lo=0.0, hi=1.0)
                row["p0"] = num(r, "p0", lo=0.0, hi=1.0)
                row["pivotal"] = num(r, "pivotal", 0.0, 0.0, 1.0)
                if row["exec_mode"] not in ("credit", "p1"):
                    raise ValueError(f"row {name!r}: exec_mode must be credit or p1")
            else:
                row["ev"] = num(r, "ev")
                row["sigma"] = num(r, "sigma", 0.0, 0.0)
                if kind == "charge" and row["exec"]:
                    print(f"note: row {name!r} is a charge; its exec factor is ignored "
                          "(CL-37, CL-40)", file=sys.stderr)
                    row["exec"] = ""
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def parse_json_arg(text, label):
    if not text:
        return {}
    try:
        v = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"{label}: not valid JSON ({e})")
    if not isinstance(v, dict):
        raise ValueError(f"{label}: expected a JSON object")
    return v


def exec_states(spec, label):
    """Normalise an execution-factor spec to (probabilities, multipliers)."""
    if isinstance(spec, (int, float)):
        return np.array([1.0]), np.array([float(spec)])
    if isinstance(spec, dict) and "lognormal" in spec:
        mean = float(spec["lognormal"]["mean"])
        sd = float(spec["lognormal"]["sd"])
        if mean <= 0 or sd < 0:
            raise ValueError(f"--exec {label}: lognormal needs mean > 0 and sd >= 0")
        s2 = math.log(1 + (sd / mean) ** 2)
        mu = math.log(mean) - s2 / 2
        n = 401  # equal-probability points; their average reproduces the mean closely
        nd = NormalDist()
        q = np.array([nd.inv_cdf((i + 0.5) / n) for i in range(n)])
        mult = np.exp(mu + math.sqrt(s2) * q)
        mult *= mean / mult.mean()
        return np.full(n, 1.0 / n), mult
    if isinstance(spec, list) and spec and all(isinstance(s, list) and len(s) == 2 for s in spec):
        p = np.array([float(s[0]) for s in spec])
        m = np.array([float(s[1]) for s in spec])
        if (p < 0).any() or abs(p.sum() - 1) > 1e-6:
            raise ValueError(f"--exec {label}: state probabilities must sum to 1")
        if (m < 0).any():
            raise ValueError(f"--exec {label}: multipliers must be >= 0")
        return p, m
    raise ValueError(f"--exec {label}: use [[prob, multiplier], ...], a number, or "
                     '{"lognormal": {"mean": m, "sd": s}}')


# ------------------------------------------------------------- the model --

class Model:
    def __init__(self, rows, size, branches, execs, corr):
        self.size = size
        self.rows = [r for r in rows if r["size"] is None or abs(r["size"] - size) < 0.5]
        if not self.rows:
            raise ValueError(f"no rows for size {fmt_money(size)}")
        names = [r["name"] for r in self.rows]
        dup = sorted({n for n in names if names.count(n) > 1})
        if dup:
            raise ValueError(f"duplicate row names at size {fmt_money(size)}: {dup}")

        used = sorted({r["branch"] for r in self.rows if r["branch"]})
        self.branches = {}
        for b in used:
            if b not in branches:
                raise ValueError(f"rows use branch {b!r} but --branches does not define it")
            w = {str(k): float(v) for k, v in branches[b].items()}
            if any(v < 0 for v in w.values()) or abs(sum(w.values()) - 1) > 1e-6:
                raise ValueError(f"--branches {b}: weights must be >= 0 and sum to 1")
            vals = {r["branch_val"] for r in self.rows if r["branch"] == b}
            unknown = vals - set(w)
            if unknown:
                raise ValueError(f"branch {b!r}: rows use answers {sorted(unknown)} "
                                 f"not in --branches ({sorted(w)})")
            self.branches[b] = w
        self.corners = []
        for combo in itertools.product(*[list(self.branches[b].items()) for b in self.branches]):
            answers = {b: a for b, (a, _) in zip(self.branches, combo)}
            prob = math.prod(p for _, p in combo)
            self.corners.append((answers, prob))
        if len(self.corners) > 64:
            raise ValueError("more than 64 branch corners; reduce the number of values questions")

        self.execs = {}
        for g in sorted({r["exec"] for r in self.rows if r["exec"]}):
            if g not in execs:
                raise ValueError(f"rows use exec factor {g!r} but --exec does not define it")
            self.execs[g] = exec_states(execs[g], g)

        by_name = {r["name"]: r for r in self.rows}
        for r in self.rows:
            if r["given"]:
                ev_row = by_name.get(r["given"])
                if ev_row is None or ev_row["kind"] != "event":
                    raise ValueError(f"row {r['name']!r}: given={r['given']!r} must name an "
                                     "event row at the same grant size")
                if (ev_row["branch"], ev_row["branch_val"]) != (r["branch"], r["branch_val"]):
                    raise ValueError(f"row {r['name']!r}: must have the same branch and "
                                     f"branch_val as its event row {r['given']!r}")
        self.corr = {}
        for k, v in corr.items():
            v = float(v)
            if not 0 <= v < 1:
                raise ValueError(f"--corr {k}: correlation must be in [0, 1)")
            if k != "*" and k not in GROUPS:
                raise ValueError(f"--corr key {k!r} must be a group name or '*'")
            self.corr[k] = v

    # -- analytic expectations -------------------------------------------
    def _p1_eff(self, r, f):
        """With-grant probability after the execution factor f (scalar or array)."""
        if not r["exec"]:
            return np.asarray(r["p1"], dtype=float) + 0 * np.asarray(f, dtype=float)
        if r["exec_mode"] == "credit":
            return np.clip(r["p0"] + f * (r["p1"] - r["p0"]), 0.0, 1.0)
        return np.clip(f * r["p1"], 0.0, 1.0)

    def row_mean(self, r):
        if r["exec"]:
            p, m = self.execs[r["exec"]]
        else:
            p, m = np.array([1.0]), np.array([1.0])
        if r["kind"] == "event":
            return float((p * r["weight"] * (self._p1_eff(r, m) - r["p0"])).sum())
        if r["kind"] == "continuous":
            return float((p * m).sum() * r["ev"])
        return float(r["ev"])

    @staticmethod
    def active(r, answers):
        return not r["branch"] or answers.get(r["branch"]) == r["branch_val"]

    def row_weight(self, r):
        """Probability weight of the worlds in which the row counts."""
        return sum(p for a, p in self.corners if self.active(r, a))

    def analytic(self):
        means = [self.row_mean(r) for r in self.rows]
        mix = [m * self.row_weight(r) for m, r in zip(means, self.rows)]
        total = sum(mix)
        groups = {}
        for r, v in zip(self.rows, mix):
            groups[r["group"]] = groups.get(r["group"], 0.0) + v
        post = sum(v * r["post2030"] for r, v in zip(self.rows, mix))
        corners = [(a, p, sum(m for m, r in zip(means, self.rows) if self.active(r, a)))
                   for a, p in self.corners]
        return {"mean": total, "row_means": means, "row_mix": mix, "groups": groups,
                "post2030": post, "corners": corners}

    # -- simulation -------------------------------------------------------
    def simulate(self, n, seed):
        rng = np.random.default_rng(seed)
        k = len(self.rows)
        z = rng.standard_normal((n, k))
        commons = {key: rng.standard_normal(n) for key in self.corr}
        for j, r in enumerate(self.rows):
            key = r["group"] if r["group"] in self.corr else ("*" if "*" in self.corr else None)
            if key is not None:
                rho = self.corr[key]
                z[:, j] = math.sqrt(rho) * commons[key] + math.sqrt(1 - rho) * z[:, j]
        u = _phi(z)
        factors = {}
        for g, (p, m) in self.execs.items():
            factors[g] = m[rng.choice(len(p), size=n, p=p)]

        vals = np.zeros((n, k))
        happened = {}
        for j, r in enumerate(self.rows):
            f = factors[r["exec"]] if r["exec"] else np.ones(n)
            if r["kind"] == "event":
                w, p0, s = r["weight"], r["p0"], r["pivotal"]
                p1 = self._p1_eff(r, f)
                up = p1 >= p0
                # grant raises the probability: credit when the outcome occurs
                occurs = u[:, j] < p1
                piv = u[:, j] < (p1 - p0)
                with np.errstate(divide="ignore", invalid="ignore"):
                    diffuse = np.where(p1 > 0, 1 - p0 / np.where(p1 > 0, p1, 1), 0.0)
                v_up = w * (s * piv + (1 - s) * diffuse * occurs)
                # grant lowers the probability: credit when the outcome is averted
                averted = u[:, j] < (1 - p1)
                piv_d = u[:, j] < (p0 - p1)
                with np.errstate(divide="ignore", invalid="ignore"):
                    diffuse_d = np.where(p1 < 1, 1 - (1 - p0) / np.where(p1 < 1, 1 - p1, 1), 0.0)
                v_dn = -w * (s * piv_d + (1 - s) * diffuse_d * averted)
                vals[:, j] = np.where(up, v_up, v_dn)
                happened[r["name"]] = occurs
            elif r["kind"] == "continuous":
                vals[:, j] = f * (r["ev"] + r["sigma"] * z[:, j])
            else:
                vals[:, j] = r["ev"] + r["sigma"] * z[:, j]

        for j, r in enumerate(self.rows):
            if r["given"]:
                ev_row = next(x for x in self.rows if x["name"] == r["given"])
                if ev_row["exec"]:
                    pe, me = self.execs[ev_row["exec"]]
                else:
                    pe, me = np.array([1.0]), np.array([1.0])
                p_event = float((pe * self._p1_eff(ev_row, me)).sum())
                if p_event > 0:
                    vals[:, j] = np.where(happened[r["given"]], vals[:, j] / p_event, 0.0)

        corner_totals = []
        for answers, prob in self.corners:
            mask = np.array([self.active(r, answers) for r in self.rows])
            corner_totals.append(vals[:, mask].sum(axis=1))
        fixed = sum(p * t for (_, p), t in zip(self.corners, corner_totals))
        return fixed, corner_totals


def _phi(z):
    """Standard normal CDF (Abramowitz-Stegun 7.1.26; error < 1.5e-7)."""
    x = np.abs(z) / math.sqrt(2)
    t = 1 / (1 + 0.3275911 * x)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741
              + t * (-1.453152027 + t * 1.061405429))))
    erf = 1 - poly * np.exp(-x * x)
    return 0.5 * (1 + np.sign(z) * erf)


def summarise(x):
    return {"mean": float(x.mean()), "p10": float(np.percentile(x, 10)),
            "median": float(np.percentile(x, 50)), "p90": float(np.percentile(x, 90)),
            "pneg": float((x < 0).mean())}


# ---------------------------------------------------------------- output --

def f1(v):
    return f"{v:,.1f}"


def report(path, model, n, seed, args_echo):
    a = model.analytic()
    fixed, corner_totals = model.simulate(n, seed)
    s = summarise(fixed)
    size = model.size
    out = []
    out.append(f"=== {path} | grant size {fmt_money(size)} | {len(model.rows)} rows ===")
    out.append(f"simulate.py {VERSION}")
    out.append(f"arguments: {args_echo}")
    out.append("")
    out.append(f"MEAN (analytic, headline)   {f1(a['mean'])}")
    out.append(f"per $1M                     {f1(a['mean'] / (size / 1e6))}")
    out.append(f"median                      {f1(s['median'])}")
    out.append(f"P10 / P90                   {f1(s['p10'])} / {f1(s['p90'])}")
    out.append(f"P(negative)                 {s['pneg'] * 100:.1f}%")
    share = a["post2030"] / a["mean"] * 100 if abs(a["mean"]) > 1e-9 else float("nan")
    out.append(f"post-2030 share of mean     {share:.1f}%   (CL-18; activity after 2030)")
    out.append(f"simulated mean (check)      {f1(s['mean'])}   "
               f"({n:,} worlds, seed {seed}; should be close to the analytic mean)")
    out.append("")
    out.append("GROUP TOTALS (analytic mean, branch-weighted)")
    for g, v in sorted(a["groups"].items(), key=lambda kv: -abs(kv[1])):
        out.append(f"  {g:<13} {f1(v):>12}")
    if model.branches:
        out.append("")
        out.append("VALUES BRANCHES (CL-11): headline uses these fixed weights")
        for b, w in model.branches.items():
            out.append(f"  {b}: " + ", ".join(f"{k}={v:g}" for k, v in w.items()))
        out.append("CORNERS (each answer taken as certain)")
        out.append(f"  {'answers':<40} {'weight':>7} {'mean':>10} {'P10':>10} {'median':>10} "
                   f"{'P90':>10} {'P(neg)':>7}")
        for (answers, prob, mean), tot in zip(a["corners"], corner_totals):
            cs = summarise(tot)
            label = ", ".join(f"{k}={v}" for k, v in answers.items())
            out.append(f"  {label:<40} {prob:>7.3f} {f1(mean):>10} {f1(cs['p10']):>10} "
                       f"{f1(cs['median']):>10} {f1(cs['p90']):>10} {cs['pneg'] * 100:>6.1f}%")
    if model.execs:
        out.append("")
        out.append("EXECUTION FACTORS (program rows only; never charges)")
        for g, (p, m) in model.execs.items():
            out.append(f"  {g}: mean multiplier {float((p * m).sum()):.3f}, "
                       f"P(multiplier = 0) {float(p[m == 0].sum()) * 100:.1f}%")
    out.append("")
    out.append("ROWS (analytic mean; '~' marks rows that count only under one branch answer)")
    order = sorted(range(len(model.rows)), key=lambda i: -abs(a["row_mix"][i]))
    for i in order:
        r = model.rows[i]
        tag = f"~{r['branch']}={r['branch_val']}" if r["branch"] else ""
        out.append(f"  {f1(a['row_mix'][i]):>10}  {r['group']:<13} {r['name']} {tag}")
    return "\n".join(out), a


def diff(path_a, path_b, size, set_a, set_b):
    rows_a, rows_b = load_ledger(path_a), load_ledger(path_b)
    ma = Model(rows_a, size, set_a["branches"], set_a["exec"], {})
    mb = Model(rows_b, size, set_b["branches"], set_b["exec"], {})
    aa, ab = ma.analytic(), mb.analytic()
    A, B = aa["mean"], ab["mean"]
    big = max(abs(A), abs(B))
    out = [f"=== DIFF at {fmt_money(size)} ===", f"simulate.py {VERSION}",
           f"A = {path_a}", f"B = {path_b}", "",
           f"HEADLINE MEAN   A {f1(A)}   B {f1(B)}   (each under its own weights and factor)"]
    gap = abs(A - B) / big * 100 if big > 0 else 0.0
    near_zero = abs(A) <= 50 and abs(B) <= 50
    means_ok = near_zero or gap <= 30
    out.append(f"  gap {gap:.1f}% of the larger mean; both within 50 of zero: "
               f"{'yes' if near_zero else 'no'}  ->  means agree: {'YES' if means_ok else 'NO'}")

    def top(g):
        return max(g.items(), key=lambda kv: abs(kv[1]))[0] if g else "-"

    ta, tb = top(aa["groups"]), top(ab["groups"])
    top_ok = ta == tb
    out.append(f"LARGEST GROUP   A {ta}   B {tb}  ->  same: {'YES' if top_ok else 'NO'}")
    out.append("")
    out.append(f"GROUP TOTALS    {'group':<13} {'A':>10} {'B':>10} {'A-B':>10}  flag")
    flagged = 0
    for g in sorted(set(aa["groups"]) | set(ab["groups"]),
                    key=lambda g: -abs(aa["groups"].get(g, 0) - ab["groups"].get(g, 0))):
        va, vb = aa["groups"].get(g, 0.0), ab["groups"].get(g, 0.0)
        over = big > 0 and abs(va - vb) > 0.30 * big
        flagged += over
        out.append(f"                {g:<13} {f1(va):>10} {f1(vb):>10} {f1(va - vb):>10}  "
                   f"{'> 30% of larger mean' if over else ''}")
    out.append(f"groups differing by more than 30% of the larger mean: {flagged}")
    agree = means_ok and top_ok and flagged == 0
    out.append("")
    out.append(f"AGREEMENT TEST: {'AGREE' if agree else 'DIVERGE'}")
    if not agree:
        why = []
        if not means_ok:
            why.append("headline means differ by more than 30%")
        if not top_ok:
            why.append("the largest group differs")
        if flagged:
            why.append(f"{flagged} group total(s) differ by more than 30% of the larger mean")
        out.append("  because: " + "; ".join(why))
    out.append("")
    out.append("ROW-LEVEL DIFFERENCES BY NAME (independent estimators rarely share names)")
    da = {r["name"]: v for r, v in zip(ma.rows, aa["row_mix"])}
    db = {r["name"]: v for r, v in zip(mb.rows, ab["row_mix"])}
    shared = sorted(set(da) & set(db), key=lambda k: -abs(da[k] - db[k]))
    for k in shared:
        out.append(f"  both    {f1(da[k]):>10} {f1(db[k]):>10} {f1(da[k] - db[k]):>10}  {k}")
    for k in sorted(set(da) - set(db), key=lambda k: -abs(da[k])):
        out.append(f"  A only  {f1(da[k]):>10} {'':>10} {'':>10}  {k}")
    for k in sorted(set(db) - set(da), key=lambda k: -abs(db[k])):
        out.append(f"  B only  {'':>10} {f1(db[k]):>10} {'':>10}  {k}")
    return "\n".join(out)


# ------------------------------------------------------------------ main --

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Simulate an Autograntor ledger (prototype reconstruction).",
        epilog=HELP_EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ledger", nargs="?", help="ledger CSV")
    ap.add_argument("--size", help="score only this grant size (default: every size in the ledger)")
    ap.add_argument("--branches", default="", help="JSON: weights for values questions")
    ap.add_argument("--corr", default="", help="JSON: correlation by group")
    ap.add_argument("--exec", dest="exec_", default="", help="JSON: execution factors")
    ap.add_argument("--n", type=int, default=20000, help="simulated worlds (default 20000)")
    ap.add_argument("--seed", type=int, default=0, help="random seed (default 0)")
    ap.add_argument("--template", action="store_true", help="print a ledger template and exit")
    ap.add_argument("--diff", nargs=2, metavar=("A.csv", "B.csv"), help="compare two ledgers")
    ap.add_argument("--branches-a", default="")
    ap.add_argument("--exec-a", default="")
    ap.add_argument("--branches-b", default="")
    ap.add_argument("--exec-b", default="")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args(argv)

    try:
        if args.template:
            sys.stdout.write(template_csv())
            return 0
        if args.diff:
            if not args.size:
                raise ValueError("--diff needs --size")
            if not (args.branches_a or args.exec_a or args.branches_b or args.exec_b):
                print("warning: no --branches-a/--exec-a/--branches-b/--exec-b given; "
                      "the diff will fail or mislead if the ledgers use them", file=sys.stderr)
            print(diff(args.diff[0], args.diff[1], parse_money(args.size),
                       {"branches": parse_json_arg(args.branches_a, "--branches-a"),
                        "exec": parse_json_arg(args.exec_a, "--exec-a")},
                       {"branches": parse_json_arg(args.branches_b, "--branches-b"),
                        "exec": parse_json_arg(args.exec_b, "--exec-b")}))
            return 0
        if not args.ledger:
            ap.error("give a ledger CSV, or --template, or --diff A.csv B.csv")
        rows = load_ledger(args.ledger)
        branches = parse_json_arg(args.branches, "--branches")
        execs = parse_json_arg(args.exec_, "--exec")
        corr = parse_json_arg(args.corr, "--corr")
        if args.size:
            sizes = [parse_money(args.size)]
        else:
            sizes = sorted({r["size"] for r in rows if r["size"] is not None})
            if not sizes:
                raise ValueError("no row has a size; fill the size column or pass --size")
        echo = (f"--branches '{args.branches or '{}'}' --corr '{args.corr or '{}'}' "
                f"--exec '{args.exec_ or '{}'}' --n {args.n} --seed {args.seed}")
        summary = []
        for size in sizes:
            text, a = report(args.ledger, Model(rows, size, branches, execs, corr),
                             args.n, args.seed, echo)
            print(text)
            print()
            summary.append((size, a["mean"]))
        if len(summary) > 1:
            print("SUMMARY BY SIZE")
            for size, mean in summary:
                print(f"  {fmt_money(size):>8}  mean {f1(mean):>10}  "
                      f"per $1M {f1(mean / (size / 1e6)):>10}")
        return 0
    except (ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
