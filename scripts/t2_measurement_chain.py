"""
T2: Measurement-chain simulation for the photonic-coupler test of the
terminal-indivisibility theorem (paper 1, Sec. 10a).

Physical system: passive PT coupler, Klauck-2019 class (Nat. Photonics 13,
883): two fs-laser-written waveguides in fused silica, coupling kappa
[1/cm], one guide with engineered bending loss gamma [1/cm, amplitude
convention: broken phase iff gamma > 2*kappa]. Subtracting the mean loss,
the device realizes the paper's dimer with
    sin(theta) -> a = gamma/2   (loss-splitting rate, 1/cm)
    s          -> kappa          (coupling, 1/cm)
    t          -> z              (propagation length, cm)
Closed forms (Theorem thm:terminal, all rates in 1/cm):
    ktil    = sqrt(a^2 - kappa^2)                     (broken)
    t_c     = arcsinh(ktil/(kappa*sqrt(2)))/ktil      (divisibility onset)
    floor   = -(a + ktil)                             (generator floor)
    period  = pi/sqrt(kappa^2 - a^2)                  (unbroken windows)

Measurement chain simulated:
  ladder of chip lengths z_i; per length, launch into each guide, record
  two output intensities relative to a straight reference guide.
  Noise sources: (1) fabrication disorder on kappa and a per sample,
  (2) per-launch transmission-calibration error (facet coupling),
  (3) photon shot noise (Poisson, N photons per launch),
  (4) additive dark/crosstalk floor.
Estimators:
  t_c    : first sign change of det(Gamma_hat) (per-column-scale invariant),
  floor  : L_12 from central-difference generator at the largest lengths,
  model fit: least-squares fit of the closed forms with calibration
             nuisances (the estimator a real experiment would use).
Dissociation observable (same data): late-window conditional TV backflow
  (predicted 0 in broken phase) vs indivisibility depth (predicted < 0).

Controls (inline):
  C1 zero-noise recovery of t_c/floor/period vs analytic closed forms,
  C2 Hermitian device (gamma=0): recurrent (not terminal) det crossings,
  C3 uncoupled device (kappa=0): generator off-diagonals = 0 within noise,
  C4 column-scale invariance: t_c estimate unchanged under random
     per-column rescaling of every measured matrix.

ASCII output only. numpy + scipy only. Runtime ~1-2 min.
"""

import zlib

import numpy as np
from scipy.optimize import least_squares

rng_global = np.random.default_rng(20260711)


# ----------------------------------------------------------------------
# closed forms and exact propagator
# ----------------------------------------------------------------------

def contraction(z, a, kappa):
    """C(z) = exp(-i H_loss z) for the loss-frame dimer, exact 2x2.
    H_loss = -i a 1 + i a sz + kappa sx   (site 1 = low-loss guide)."""
    A = np.array([[1j * a, kappa], [kappa, -1j * a]])  # i a sz + k sx
    # A^2 = (kappa^2 - a^2) 1 = -ktil^2
    disc = kappa ** 2 - a ** 2
    if abs(disc) < 1e-15:
        c, s = 1.0, z
    elif disc < 0:
        kt = np.sqrt(-disc)
        c, s = np.cosh(kt * z), np.sinh(kt * z) / kt
    else:
        kk = np.sqrt(disc)
        c, s = np.cos(kk * z), np.sin(kk * z) / kk
    expA = c * np.eye(2) - 1j * s * A          # exp(-i A z)
    return np.exp(-a * z) * expA


def gamma_red(z, a, kappa):
    C = contraction(z, a, kappa)
    return np.abs(C) ** 2


def pqr(z, a, kappa):
    kt2 = a ** 2 - kappa ** 2
    if kt2 > 0:
        kt = np.sqrt(kt2)
        c, s = np.cosh(kt * z), np.sinh(kt * z) / kt
    elif kt2 < 0:
        kk = np.sqrt(-kt2)
        c, s = np.cos(kk * z), np.sin(kk * z) / kk
    else:
        c, s = 1.0, z
    return c + a * s, c - a * s, kappa * s


def analytic_tc(a, kappa):
    kt2 = a ** 2 - kappa ** 2
    if kt2 > 0:
        kt = np.sqrt(kt2)
        return np.arcsinh(kt / (kappa * np.sqrt(2))) / kt
    if kt2 < 0:
        kk = np.sqrt(-kt2)
        return np.arcsin(min(1.0, kk / (kappa * np.sqrt(2)))) / kk
    return 1.0 / (kappa * np.sqrt(2))


def analytic_floor(a, kappa):
    return -(a + np.sqrt(a ** 2 - kappa ** 2))


# ----------------------------------------------------------------------
# measurement model
# ----------------------------------------------------------------------

def measure_ladder(zs, a, kappa, noise, rng):
    """Return list of measured 2x2 transfer matrices Gamma_hat(z).
    noise = dict(dis, cal, nphot, dark); any may be 0/None."""
    out = []
    for z in zs:
        a_i = a * (1 + noise['dis'] * rng.standard_normal())
        k_i = kappa * (1 + noise['dis'] * rng.standard_normal())
        G = gamma_red(z, a_i, k_i)
        Gh = np.empty((2, 2))
        for col in range(2):                       # one launch per column
            cal = 1 + noise['cal'] * rng.standard_normal()
            p = G[:, col] * cal + noise['dark']
            p = np.clip(p, 1e-12, None)
            if noise['nphot']:
                counts = rng.poisson(p * noise['nphot'])
                Gh[:, col] = counts / noise['nphot']
            else:
                Gh[:, col] = p
        out.append(Gh)
    return out


NOISE0 = dict(dis=0.0, cal=0.0, nphot=None, dark=0.0)


# ----------------------------------------------------------------------
# estimators
# ----------------------------------------------------------------------

def det_norm(M):
    """det of the column-sum-normalized matrix: exactly invariant under
    per-column rescaling (calibration errors), sign = sign(det)."""
    c = M.sum(axis=0)
    c = np.where(np.abs(c) < 1e-12, 1e-12, c)
    return np.linalg.det(M / c[None, :])


def est_tc(zs, mats):
    """First sign change of the normalized det; local quadratic root."""
    d = np.array([det_norm(M) for M in mats])
    for i in range(len(zs) - 1):
        if d[i] > 0 and d[i + 1] < 0:
            j0 = max(0, i - 1)
            pts_z = np.array(zs[j0:i + 2])
            pts_d = d[j0:i + 2]
            if len(pts_z) == 3:
                a2, a1, a0 = np.polyfit(pts_z, pts_d, 2)
                rts = np.roots([a2, a1, a0])
                rts = rts[np.isreal(rts)].real
                rts = rts[(rts >= zs[i]) & (rts <= zs[i + 1])]
                if len(rts):
                    return rts[0]
            f = d[i] / (d[i] - d[i + 1])
            return zs[i] + f * (zs[i + 1] - zs[i])
    return np.nan


def det_signs(zs, mats):
    return np.sign([det_norm(M) for M in mats])


def est_floor(zs, mats, ntail=3):
    """L_12 by central difference over the last ntail interior points."""
    vals = []
    for i in range(len(zs) - ntail - 1, len(zs) - 1):
        if i < 1:
            continue
        dz = zs[i + 1] - zs[i - 1]
        Ld = (mats[i + 1] - mats[i - 1]) / dz
        try:
            L = Ld @ np.linalg.inv(mats[i])
        except np.linalg.LinAlgError:
            continue
        vals.append(L[0, 1])
    return np.median(vals) if vals else np.nan


def est_model_fit(zs, mats, a0, k0):
    """Least-squares fit of the closed form with per-launch calibration
    nuisances (one scale per column per length is unidentifiable; the
    experiment constrains calibration to be unbiased, so we fit a single
    global scale per column stream plus (a, kappa))."""
    def resid(p):
        a, k, c1, c2 = p
        r = []
        for z, M in zip(zs, mats):
            G = gamma_red(z, a, k)
            G = G * np.array([c1, c2])[None, :]
            r.extend((M - G).ravel())
        return np.array(r)
    try:
        sol = least_squares(resid, x0=[a0 * 1.05, k0 * 0.95, 1.0, 1.0],
                            method='lm', max_nfev=2000)
        a, k = sol.x[0], sol.x[1]
        return analytic_tc(a, k), analytic_floor(a, k) if a > k else np.nan
    except Exception:
        return np.nan, np.nan


def backflow_late(zs, mats, zmin):
    """Conditional (survival-normalized) TV distance between the two
    launch columns; return max increase (backflow) for z >= zmin."""
    tv = []
    for z, M in zip(zs, mats):
        c1 = M[:, 0] / max(M[:, 0].sum(), 1e-12)
        c2 = M[:, 1] / max(M[:, 1].sum(), 1e-12)
        tv.append(0.5 * np.abs(c1 - c2).sum())
    tv = np.array(tv)
    sel = np.array(zs) >= zmin
    t = tv[sel]
    inc = np.diff(t)
    return max(0.0, inc.max()) if len(inc) else 0.0


def est_period(zs, mats):
    """Unbroken phase: window period from 1st and 3rd normalized-det
    zero crossing (their separation is exactly pi/sqrt(k^2-a^2))."""
    d = np.array([det_norm(M) for M in mats])
    cross = []
    for i in range(len(zs) - 1):
        if d[i] * d[i + 1] < 0:
            f = d[i] / (d[i] - d[i + 1])
            cross.append(zs[i] + f * (zs[i + 1] - zs[i]))
    if len(cross) >= 3:
        return cross[2] - cross[0]
    return np.nan


# ----------------------------------------------------------------------
# devices and ladders
# ----------------------------------------------------------------------

# Non-dimensionalize with r = gamma/(2 kappa): kappa*t_c and floor/kappa are pure
# functions of r alone. The ORIGINAL D2 (kappa=0.15, gamma=0.90) had r=3.00,
# IDENTICAL to D1 -- both give kappa*t_c = 0.5104 -- so D2 re-tested only the
# trivial 1/kappa scaling and not the closed form's r-dependence, while its label
# claimed "deep". Re-spec'd 2026-07-15 to r=4 by LOWERING kappa with gamma pinned
# at its maximum; raising gamma to reach depth instead would need 1.2 [1/cm] =
# 10.4 dB/cm, outside the 2.6-7.8 dB/cm range the device table REQUIRES
# (that range is derived here from the table via 2*gamma*10/ln(10); it is not
# a figure quoted from Eichelkraut2014, which reports only "almost arbitrary"
# tunable radiation loss).
#
# r=4 is a measured optimum, not a guess. Sweeping r at fixed gamma=0.90 (block
# [C6] of main(), which reproduces this table) shows the det-crossing estimator -- the paper's
# PRIMARY calibration-immune observable -- degrading faster than the lever grows:
#     r=3.0  det +/-0.141  bias +0.023   |  r=4.5  det +/-0.388  bias +0.187
#     r=4.0  det +/-0.266  bias +0.114   |  r=5.0  det +/-0.589  bias +0.379
#     r=6.0  det +/-0.963  bias +0.385, and DEAD on 7/400 realizations
# At r>=5 the dark floor swamps the (weakening) surviving diagonal and the
# determinant stops cleanly crossing zero. r=4 buys a 12.4% lever in kappa*t_c
# (0.5104 -> 0.4473, ~3 sigma on the model fit) while keeping det alive on all
# 400 trials, 7.82 dB/cm, and t_c=3.98 cm inside 6 cm chips (D2's stated purpose).
# Its +0.114 bias is the known dark-floor bias the paper already prescribes
# subtracting.
DEVICES = {
    'D1 broken moderate': dict(kappa=0.10, gamma=0.60),
    'D2 broken deep':     dict(kappa=0.1125, gamma=0.90),
    'D3 unbroken':        dict(kappa=0.50, gamma=0.30),
}
ZS = np.arange(0.5, 10.01, 0.5)          # 20 chip lengths, cm

NTRIALS = 400


def run_mc(dev, noise, ntrials=NTRIALS, seed=1):
    a, k = dev['gamma'] / 2, dev['kappa']
    rng = np.random.default_rng(seed)
    tcs, floors, fits_tc, fits_fl, bfs, pers = [], [], [], [], [], []
    for _ in range(ntrials):
        mats = measure_ladder(ZS, a, k, noise, rng)
        tcs.append(est_tc(ZS, mats))
        floors.append(est_floor(ZS, mats))
        ftc, ffl = est_model_fit(ZS, mats, a, k)
        fits_tc.append(ftc)
        fits_fl.append(ffl)
        bfs.append(backflow_late(ZS, mats, zmin=5.0))
        pers.append(est_period(ZS, mats))
    def stat(x):
        x = np.array(x, dtype=float)
        x = x[np.isfinite(x)]
        if len(x) == 0:
            return (np.nan, np.nan, np.nan, 0)
        return (np.median(x), np.percentile(x, 16), np.percentile(x, 84),
                len(x))
    return dict(tc=stat(tcs), floor=stat(floors), ftc=stat(fits_tc),
                ffl=stat(fits_fl), bf=stat(bfs), per=stat(pers))


def fmt(s, ref=None):
    m, lo, hi, n = s
    base = "%7.3f [%7.3f,%7.3f] (n=%d)" % (m, lo, hi, n)
    if ref is not None and np.isfinite(m):
        base += "  ref %7.3f" % ref
    return base


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------

def main():
    print("=" * 72)
    print("T2 measurement-chain simulation -- Klauck-class passive PT coupler")
    print("=" * 72)

    # ---------------- C1: zero-noise recovery --------------------------
    print("\n[C1] zero-noise recovery vs closed forms")
    for name, dev in DEVICES.items():
        a, k = dev['gamma'] / 2, dev['kappa']
        mats = measure_ladder(ZS, a, k, NOISE0, rng_global)
        tc_hat = est_tc(ZS, mats)
        tc_ref = analytic_tc(a, k)
        line = "  %-18s t_c_hat=%6.3f  t_c=%6.3f  |err|=%.4f" % (
            name, tc_hat, tc_ref, abs(tc_hat - tc_ref))
        if a > k:
            fl_hat = est_floor(ZS, mats)
            fl_ref = analytic_floor(a, k)
            line += "   floor_hat=%7.4f floor=%7.4f" % (fl_hat, fl_ref)
        print(line)

    # C2: Hermitian control -- recurrent crossings
    matsH = measure_ladder(ZS, 0.0, 0.26, NOISE0, rng_global)
    sgn = det_signs(ZS, matsH)
    ncross = int(np.sum(np.abs(np.diff(sgn)) > 0))
    print("[C2] Hermitian control (kappa=0.26, gamma=0): det sign changes "
          "over ladder = %d (recurrent, not terminal)  first at z=%.2f "
          "(pi/(4k)=%.2f)" % (ncross, est_tc(ZS, matsH), np.pi / (4 * 0.26)))

    # C3: uncoupled null -- with and without dark floor
    noise_nodark = dict(dis=0.02, cal=0.03, nphot=10 ** 5, dark=0.0)
    noise_dark = dict(dis=0.02, cal=0.03, nphot=10 ** 5, dark=1e-4)
    fl_nd = est_floor(ZS, measure_ladder(ZS, 0.30, 0.0, noise_nodark,
                                         rng_global))
    fl_dk = est_floor(ZS, measure_ladder(ZS, 0.30, 0.0, noise_dark,
                                         rng_global))
    print("[C3] uncoupled null (kappa=0): |L_12| = %.4f without dark "
          "floor (clean), %.4f with dark=1e-4 -- dark counts leak into "
          "the generator once survival ~ dark level; subtract darks or "
          "cap the ladder where survival >> dark." % (abs(fl_nd),
                                                      abs(fl_dk)))

    # C4: column-scale invariance of t_c (normalized-det estimator)
    a, k = 0.30, 0.10
    mats = measure_ladder(ZS, a, k, NOISE0, rng_global)
    tc1 = est_tc(ZS, mats)
    matsS = [M * rng_global.uniform(0.5, 1.5, size=(1, 2)) for M in mats]
    tc2 = est_tc(ZS, matsS)
    print("[C4] column-rescaling invariance: t_c %-.6f -> %-.6f "
          "(diff %.1e)" % (tc1, tc2, abs(tc1 - tc2)))

    # C5: D2 onset AND floor recoverable within 6 cm chips (its stated
    # purpose; the global ladder above runs to 10 cm, so cap it here).
    ZS6 = np.arange(0.5, 6.01, 0.5)
    d2 = DEVICES['D2 broken deep']
    a2, k2 = d2['gamma'] / 2, d2['kappa']
    rng6 = np.random.default_rng(11)
    fits6 = []
    for _ in range(NTRIALS):
        m6 = measure_ladder(ZS6, a2, k2,
                            dict(dis=0.02, cal=0.03, nphot=10 ** 4, dark=1e-4),
                            rng6)
        _, ffl = est_model_fit(ZS6, m6, a2, k2)
        fits6.append(ffl)
    s6 = np.array([x for x in fits6 if np.isfinite(x)])
    med6, lo6, hi6 = (np.median(s6), np.percentile(s6, 16),
                      np.percentile(s6, 84))
    sig6 = abs(med6) / max((hi6 - lo6) / 2, 1e-12)
    print("[C5] D2 on a 6 cm-capped ladder (0.5-6.0 cm, 1e4 photons, "
          "n=%d/%d): floor %.4f [%.4f,%.4f] -> %.1f sigma below zero "
          "(floor=%.4f); t_c=%.2f cm and the floor fit both fall inside "
          "6 cm chips" % (
              len(s6), NTRIALS, med6, lo6, hi6, sig6,
              analytic_floor(a2, k2), analytic_tc(a2, k2)))

    # ---------------- error budget --------------------------------------
    budgets = [
        ('disorder 2% only', dict(dis=0.02, cal=0.0, nphot=None, dark=0.0)),
        ('calib 3% only',    dict(dis=0.0, cal=0.03, nphot=None, dark=0.0)),
        ('shot 1e4 only',    dict(dis=0.0, cal=0.0, nphot=10 ** 4, dark=0.0)),
        ('shot 1e6 only',    dict(dis=0.0, cal=0.0, nphot=10 ** 6, dark=0.0)),
        ('dark 1e-4 only',   dict(dis=0.0, cal=0.0, nphot=None, dark=1e-4)),
        ('all (1e4)',        dict(dis=0.02, cal=0.03, nphot=10 ** 4,
                                  dark=1e-4)),
        ('all (1e6)',        dict(dis=0.02, cal=0.03, nphot=10 ** 6,
                                  dark=1e-4)),
    ]

    for name, dev in DEVICES.items():
        a, k = dev['gamma'] / 2, dev['kappa']
        broken = a > k
        print("\n" + "-" * 72)
        print("%s  (kappa=%.2f /cm, gamma=%.2f /cm; %s)" % (
            name, dev['kappa'], dev['gamma'],
            "BROKEN" if broken else "UNBROKEN"))
        if broken:
            print("  analytic: t_c=%.3f cm  floor=%.4f /cm" % (
                analytic_tc(a, k), analytic_floor(a, k)))
        else:
            print("  analytic: first det crossing z1=%.3f cm  window "
                  "period=%.3f cm" % (
                      analytic_tc(a, k),
                      np.pi / np.sqrt(k ** 2 - a ** 2)))
        print("  %-18s | %-34s | %-34s" % ("noise", "t_c (det-crossing)",
                                           "floor L12 (cdiff)"))
        for bname, bn in budgets:
            # NB: seed via zlib.crc32, NOT the builtin hash() -- Python salts
            # str hashing per process (PYTHONHASHSEED), so hash() made every
            # budget row irreproducible run-to-run.
            r = run_mc(dev, bn,
                       seed=zlib.crc32((bname + name).encode()) % 2 ** 31)
            print("  %-18s | %s | %s" % (bname, fmt(r['tc']),
                                         fmt(r['floor'])))
        for tag, nph in (('1e4', 10 ** 4), ('1e6', 10 ** 6)):
            r = run_mc(dev, dict(dis=0.02, cal=0.03, nphot=nph, dark=1e-4),
                       seed=7 + nph % 13)
            line = "  model-fit (all,%s): t_c %s" % (tag, fmt(r['tc']))
            print(line.replace('t_c %s' % fmt(r['tc']),
                               't_c %s' % fmt(r['ftc'])))
            if broken:
                m, lo, hi, n = r['ffl']
                sig = abs(m) / max((hi - lo) / 2, 1e-12)
                print("                       floor %s  -> %5.1f sigma "
                      "below zero" % (fmt(r['ffl']), sig))
            else:
                print("                       period %s (ref %.3f)" % (
                    fmt(r['per']),
                    np.pi / np.sqrt(k ** 2 - a ** 2)))
            print("                       late-window backflow %s" %
                  fmt(r['bf']))

    # ---------------- design chart --------------------------------------
    print("\n" + "=" * 72)
    print("design chart: broken-phase devices (t_c, floor, length to rise "
          "within 10% of floor)")
    print("  kappa[/cm] gamma[/cm] gamma[dB/cm,power]   t_c[cm]  "
          "floor[/cm]  z90[cm]")
    for kappa in (0.05, 0.10, 0.15, 0.20):
        for ratio in (3.0, 4.0, 6.0):
            gamma = ratio * kappa
            a = gamma / 2
            if a <= kappa:
                continue
            kt = np.sqrt(a ** 2 - kappa ** 2)
            tc = analytic_tc(a, kappa)
            fl = analytic_floor(a, kappa)
            # z at which L12 has risen to within 10% of its floor value.
            # L12 approaches the (negative) floor fl from below, so "within
            # 10%" is L12 >= 1.1*fl (using L12 < 0.9*fl here would trigger
            # at t_c, since L12 -> -inf as z -> t_c+).
            # start just past t_c: at z=t_c the divisor entry 1-2r^2 vanishes
            # and L12 diverges, so the scan must skip the singular point.
            z = tc
            zg = np.nan
            for z in np.arange(tc + 0.05, 40, 0.05):
                p, q, r = pqr(z, a, kappa)
                L12 = 2 * kappa * p * r / (1 - 2 * r ** 2)
                if L12 > 1.1 * fl:
                    zg = z
                    break
            dbcm = 2 * gamma * 10 / np.log(10)   # power dB/cm
            print("  %8.2f %9.2f %17.1f %9.2f %10.3f %8.1f" % (
                kappa, gamma, dbcm, tc, fl, zg))

    # ---------------- [C6] D2 depth: the r-sweep ------------------------
    # Why D2 sits at r = gamma/2kappa = 4 and not deeper. The paper states
    # that by r ~ 5-6 the det-crossing estimator degrades beyond usefulness,
    # its bias and spread exceeding the signal. That claim previously lived
    # only in a comment above DEVICES, with no public path to it; this block
    # is that path. gamma is pinned at its maximum (0.90) and kappa is varied.
    print("\n[C6] D2 depth: det-crossing estimator vs r = gamma/(2 kappa)")
    print("     (gamma pinned at 0.90; all-noise at 1e4 photons; %d trials)"
          % NTRIALS)
    print("  %6s %9s %10s %10s %8s" % ("r", "kappa", "bias", "spread",
                                       "dead"))
    gamma_fix = 0.90
    a_fix = gamma_fix / 2
    noise_all = dict(dis=0.02, cal=0.03, nphot=10 ** 4, dark=1e-4)
    for r in (3.0, 4.0, 4.5, 5.0, 6.0):
        kap = gamma_fix / (2 * r)
        tc_true = analytic_tc(a_fix, kap)
        rng = np.random.default_rng(20260711 + int(round(10 * r)))
        vals = []
        dead = 0
        for _ in range(NTRIALS):
            mats = measure_ladder(ZS, a_fix, kap, noise_all, rng)
            t = est_tc(ZS, mats)
            if not np.isfinite(t):
                dead += 1
            else:
                vals.append(t)
        v = np.array(vals, dtype=float)
        if len(v):
            bias = float(np.median(v) - tc_true)
            spread = float((np.percentile(v, 84) - np.percentile(v, 16)) / 2)
        else:
            bias = spread = float('nan')
        print("  %6.1f %9.4f %+10.3f %10.3f %8d" % (r, kap, bias, spread,
                                                    dead))
    print("     => bias and spread grow faster than the lever; by r ~ 5-6 the")
    print("        determinant stops cleanly crossing zero and realizations die.")
    print("        r = 4 keeps the estimator alive on every trial. This is what")
    print("        sets D2's depth.")

    print("\ndone.")


if __name__ == '__main__':
    main()
