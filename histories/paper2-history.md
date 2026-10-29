# Process history — Paper 2 (measurable): "Experimental proposal: divisibility onset, generator floor, and the backflow–divisibility dissociation in a passive PT photonic coupler"

Repo slot: `p09-measurable-ghosts`. Drafted 2026-07-11 as `proposal/`;
**promoted to paper 9 on 2026-07-15** (author decision). This ledger opens
at the promotion; the pre-promotion history lives in notes.md (2026-07-11
"T2 DONE", 2026-07-12 "ARC-C DONE: devices D4 + D5") and in the p5/p6
histories, whose fixes rippled into it.

## Counters
claims 0/4 · biblio 0/3 · numerics 0/3 — **first pass DONE 2026-07-15**; all
three lanes had applied findings, so all three stay at 0.

> **NOTE ON NUMBERING.** This file keeps the name `paper2-history.md` because the
> local working directory is `paper2/`. The paper is **paper 2** of the series
> (`p02-measurable-ghosts`). Local dirs stay in drafting order; `repo-reorg.md` +
> the `assemble_repos.ps1` paper table are the source of truth for the mapping.

## PASS 1 — 2026-07-15 (three fresh Opus agents; counter 0). NOT CLEAN.
Fresh-eyes Opus x3, no histories. The document had **never been audited in any
lane**; findings below are its first.

**Structural outcome (author-directed, same session):** the paper was SPLIT. Its
"Extension: D4/D5" paragraph (61 lines) was deleted — verified first that paper 6
is a **strict superset** of that content (all 38 claims independently present;
p6 also carries the Weidemann2020 realized-asymmetry cite and the feasibility
hedge this paper lacked). The split alone resolved five findings, including the
biblio lane's CRITICAL. What remains is a p1-only-dependent core, now paper 2.

**Claims (Opus).** Closed forms CLEAN — det Γ = 1 − 2κ²sinh²(κ̃z)/κ̃² re-derived
independently; all four table rows, the EP limit, and the dB conversion reproduce.
- **CRITICAL — REJECTED under rule 7** (see `auditor-error-log.md`): "t_c is
  protocol-dependent; the onset is ~0, not t_c". The arithmetic was reproduced
  exactly, but it used an all-pairs-over-all-z2 notion, not p1's interval-
  restricted P-divisibility. Orchestrator tested ~125k pairs strictly inside
  [0,t_c): **min entry exactly 0.0** → p1 thm (i) TRUE and **paper 1 not
  implicated**. Both proposed fixes would have introduced errors — notably a
  phantom 0.48 cm "finite-Δz bias" for an estimator that is single-length
  det-crossing (real ladder bias: −0.032 cm). Survives as a MINOR: the bullet
  garbled p1's theorem. **APPLIED** — now states "P-divisible precisely on
  [0,t_c)", matching p1 (i) verbatim.
- MAJOR (cross-confirmed by the numerics lane) **D2 "broken (deep)" is FALSE** —
  see the re-spec below. APPLIED.
- MAJOR firstness/result-voice ×2 → "would be the first". APPLIED.
- MAJOR "immune to the dominant calibration systematics" — self-contradicted by
  the paper's own dark-floor sentence. APPLIED (scoped to per-launch
  transmission-calibration; dark floor named as the one it does not absorb).
- MAJOR generator-floor bullet stated with no phase hypothesis (κ̃ imaginary in
  the unbroken phase → the claim is meaningless there). APPLIED.
- MINOR "two orders of magnitude" (actually ~27×). APPLIED → "more than an order".
- The D5-paragraph findings (dimensional θ/rate mismatch, 0.486 provenance, the
  dead `p6_d4_device.py` reference) all vanished with the split.

**Numerics (Opus).** Every headline closed form CLEAN; the flagged units trap
(amplitude γ → 8.686·γ dB/cm → 2.6–7.8) is **correct**. Findings:
- MAJOR **D2 γ/2κ = 3.000, identical to D1** — t_c and floor ratios exactly
  1.50000; both give κ·t_c = 0.5104. D2 re-tested only the trivial 1/κ scaling.
  **RE-SPEC'D (author-directed) to r=4** (κ=0.1125, γ=0.90), t_c=3.98,
  floor=−0.886. r chosen by measurement, not guess: sweeping r at γ=0.90 showed
  the det-crossing estimator degrading FASTER than the lever grows — r=5 bias
  +0.379, r=6 **dead on 7/400 realizations** (the dark floor swamps the weakening
  surviving diagonal). r=4 keeps det alive on all 400, holds 7.82 dB/cm and
  t_c<6 cm, and buys a 12.4% κ·t_c lever (~3σ on the model fit). A first r=6
  attempt was run and **rejected on its output**.
- MODERATE ±3% floor vs "23–29σ" arithmetically inconsistent → **±3–4%, 29σ (D1)
  / 24σ (D2)**, measured. APPLIED. Also scoped: it is the floor *parameter's*
  significance under the closed-form model, not a model-independent permanence
  test (claims lane's circularity point).
- MODERATE blanket "±0.15 cm" true only for the old D2 → per-device **±0.19 (D1)
  / ±0.28 (D2)** at 1e4; ±0.09/±0.06 at 1e6. APPLIED.
- MODERATE **`hash()` seeding is PYTHONHASHSEED-salted** → every budget row was
  irreproducible run-to-run. **FIXED** (`zlib.crc32`); verified by two
  independent full campaigns now byte-identical.
- Dark-floor bias per-device (+0.05 D1 / +0.12 D2) and the r≳5 estimator-failure
  boundary documented in-text. Backflow 0.015/0.018, period ±2.3%: APPLIED.

**Bibliography (Opus).** All 8 bibitems metadata-clean vs Crossref/arXiv (no
fabricated, chimeric, or misattributed records).
- **CRITICAL — the D5 device-feasibility citation does not exist.** No single work
  combines lossy-bus dissipative coupling with unidirectionality: Mukherjee 2017
  (Nat. Commun. 8, 1909) has the lossy bus on fs-written glass but *symmetric*
  coupling; Weidemann 2020 (Science 368, 311) has the realized HN asymmetry but in
  a *temporal mesh*. **RESOLVED BY THE SPLIT** — D5 now lives only in paper 6,
  which already cites Weidemann2020 and hedges honestly. Paper 6 had it right;
  this paper was the regression.
- **MAJOR — the novelty claim was refuted by its own citation.** "No experiment
  has … run the backflow and divisibility analyses on one data set" — Bernardes
  2015, cited one clause earlier, did exactly that (weak non-Markovianity =
  indivisibility without backflow, full process tomography, incl. the weak→strong
  transition). **APPLIED**: conjunct dropped, Bernardes reported accurately, and
  the surviving novelty (closed-form onset *length*, generator *floor*, PT-phase-
  locking on a passive coupler) narrowed and kept — no anticipation found.
- **MAJOR — "descends to" the floor inverts p1.** p1 thm (iii): L₁₂ < −(sinθ+κ̃)
  for all t>t_c, *approached from below by the signed entry* — it **rises**.
  Confirmed by orchestrator in 60-digit mpmath (−1.418 → −0.620 → −0.58296 →
  −0.5828427 vs floor −0.5828427, below throughout). APPLIED.
- MAJOR ×2 dangling companions: **paper 1** (verified against p1 thm at
  `paper1/main.tex:783–800`) — bibitem ADDED. "The companion's sequel" (paper 3) —
  it is a *pointer*, not a dependency, so softened to a no-cite mention rather
  than creating a forward edge.
- MINOR Tang2016 is not "the same platform" (bulk optics, USTC; only Ehrhardt2022
  is the Szameit written-waveguide platform). APPLIED.
- **The brief's own hypothesis was disproved**: the plural "companion papers'
  σ_max" is CORRECT — p5 originates it (`paper5/main.tex:618–622`), p6 restates.
  Vindicates not author-guessing the attributions. (Moot after the split.)
- Prior-art sweep otherwise clean; the three Klauck/Eichelkraut device-parameter
  claims (γ/2κ≈0.25, HOM 0.05 cm, the demonstrated tuning range) are
  **NOT-VERIFIED — paywalled**. The γ≤0.90 ceiling that bounds the D2 re-spec
  rests on the tuning-range claim, so it is *assumed*, not established.

Recompiled clean (**3 pp**, was 4 before the split). Counters: all lanes 0.

## Timeline

**2026-07-11 — drafted (T2).** Measurement-chain simulation
(`scripts/t2_measurement_chain.py`, ~3 min, 400-trial MC per cell) + a
2-page proposal making paper 1's Sec. 10a concrete. Device grounding from a
full-text read of Klauck 2019. Key estimator theorem-let: t_c is estimated
from the det zero-crossing of the COLUMN-NORMALIZED transfer matrix, exactly
invariant under per-launch calibration error.

**2026-07-12 — v1.1 (Arc-C).** D4 (dimer at its own EP) + D5 (unidirectional
cascade cell via coherent + dissipative coupling, one-way at J = Γ_d) added,
making it the first proposal for a laboratory observable of indivisibility by
conditional mass creation. **Standing gate opened here and still OPEN:**
HatanoNelson1996 is cited for the CONCEPT of the asymmetry only — a
DEVICE-FEASIBILITY citation for the photonic realization was marked
"do not circulate before verifying one" (notes.md 2026-07-12), re-confirmed
as a standing circulation gate 2026-07-13, and queued for "the proposal audit
pass" that never came.

**2026-07-12/13/14 — fixes rippled IN, never audited.** The σ_max minimal-
contraction convention (shared p5/p6 pass-9 F2), the 0.486 constant (p6 pass-4
fix-propagation MAJOR — the proposal was the surface the fix had NOT reached),
the η two-channel certification (p6 pass-17 MAJOR), the z* protocol labeling
(p6 pass-10), and the Δ→δ rename (p6 pass-14) all landed here as ripples from
other papers' audits. None was ever independently verified IN this document.

**2026-07-15 — PROMOTED to paper 9** (author decision; major-findings-ledger
entry 31, methodology-timeline Stage 17). Trigger: the author asked why p6 may
cite a document that has never been audited. Investigation found p6's biblio
lane CERTIFIED 3/3 on 22 of 27 bibitems — the five `Companion*` self-cites got
existence-checks only, never rule-6 claim-support, and one pointed here.

Applied at promotion (counter-neutral, rule-3 reorg exception + DECIDED policy):
- `git mv proposal/ → paper2/`; own repo `p09-measurable-ghosts`; added to the
  assemble_repos.ps1 paper table (the `Proposal=$true` p06-pooling special case
  is deleted); repo-reorg.md row 9; dissemination-strategy.md section (it had
  been absent from that document ENTIRELY — no venue, no reviewer, no sequence).
- `\date` stripped to a plain `July 11, 2026` per the DECIDED corpus-wide
  plain-date policy. It had still carried `--- companion to arXiv-pending
  <paper 1 title> (Sec. 10a)`. Two defects in one: (a) the plain-date sweep
  had reached p1/p5/p7/p6 only because each paper's OWN audit stripped it —
  no audit, no strip; (b) **"arXiv-pending" was false** — nothing is submitted,
  and dissemination step 3 requires an arXiv endorser who has not been
  identified. NOTE for the biblio lane: this line was the document's only link
  to paper 1; removing it makes the dangling-companion defect below explicit,
  it does not create it.
- Own provenance URL p06-unfolded-ghosts → p09-measurable-ghosts.
- Citing-paper ripples: **p4** L456 ("a companion experimental proposal
  (`proposal/main.tex` in the same repository)" — false after promotion, and it
  carried NO bibitem) → now names paper 9 + its repo. **p6** `Companion3prop`
  bibitem → p09 repo, "source in `proposal/`" dropped. p7's p06 URL hit was a
  false positive (that is `Companion6`, p6's own repo — correct).
- Recompiled clean: **p2 4pp, p4 8pp, p6 15pp**, zero errors, no undefined
  refs/cites.

## Post-pass-1: the "paywalled" claims, CLOSED 2026-07-15 (2 of 3)
The biblio lane reported three device-parameter claims as NOT-VERIFIED (no source
access). Two were **not paywalled at all** — Klauck 2019 is free on arXiv
(**arXiv:1904.08135**, the published Nat. Photonics version is the paywalled one).
Full text pulled and checked against the primary source:

| claim (paper 2) | Klauck's own text | verdict |
|---|---|---|
| "Klauck operated at γ/2κ≈0.25" | κ = 0.26 cm⁻¹ (L_c = 6.0 cm); γ = (0.13 ± 0.04) cm⁻¹. 0.13/(2·0.26) = **0.25** | **VERIFIED** |
| "Klauck's HOM-dip benchmark: 0.05 cm" | "The observed shift of 0.2 cm clearly exceeds the prediction uncertainty of our fitted theory for the minimum of the HOM dip of **0.05 cm**" | **VERIFIED** (it is a theory-fit prediction uncertainty, which is the right thing to benchmark a fit spread against) |
| λ=815 nm, fused silica, PT-breaking at γ=2κ | all stated verbatim | **VERIFIED** |

**Bonus corroboration of the D4 row from the primary source.** Klauck: "the HOM
dip occurs at z < z_H, approaching **z = 1/(√2 κ)** for γ → 2κ." That is exactly
this paper's D4 onset formula, t_c = 1/(κ√2) = 2.36 cm at the EP — arrived at
independently, and confirmed by the cited experiment's own analysis. arXiv ID
added to the bibitem.

## STILL OPEN after pass 1
1. **Eichelkraut's demonstrated loss-tuning range — genuinely paywalled.**
   Opt. Lett. 39, 6831 (2014), Optica; no arXiv preprint, no repository copy
   found. The abstract claims only "well-controllable radiation losses of almost
   arbitrary amount" — qualitative, no numbers. This one is **load-bearing**: the
   in-text "2.6-7.8 dB/cm ... within the demonstrated tuning range" is what sets
   the γ ≤ 0.90 ceiling, which is in turn why the D2 re-spec had to reach depth by
   lowering κ rather than raising γ. Until the full text is read, that ceiling is
   *assumed*, not established. **ACTION TAKEN 2026-07-15: reprint request emailed
   to Szameit** (alexander.szameit@uni-rostock.de — senior author on both
   Eichelkraut 2014 and Klauck 2019). Awaiting reply; his answer closes this item.
   Fallback routes if it goes unanswered: Nolte (stefan.nolte@uni-jena.de), Optica
   pay-per-view, interlibrary loan. See `publish/dissemination-strategy.md` for the
   reception log and the standing note on that thread.
2. **p6 biblio CERT 3/3** — held pending an author ruling (ledger 31).
3. The D2 re-spec is new content and carries its own error rate (Stage 16:
   fixes are new content) — it should be re-audited on the next pass.

## KNOWN-OPEN at promotion — RESOLVED by pass 1 (kept for the record)
1. **Dangling companions (biblio lane).** The document makes THREE uncited
   "companion" references and its bibliography has **zero** `Companion*`
   entries — an entirely one-way citation (p4 + p6 cite it; it cites nothing
   back). Verified referents so far: L48 "The companion paper proves..." is
   **paper 1** (p1 proves the floor −(sinθ+κ̃) and the dissociation; p1 §10a
   says "What has not been extracted is precisely this paper's observable set:
   a closed-form divisibility-onset length, a generator floor, and the
   recurrent-window period"). The other two are NOT resolved and must not be
   guessed: L176 "the companion papers'" (plural) minimal contraction
   normalization — that phrase is defined in **p6** (L377) and has **no match
   in p5**, so the plural may be wrong; L114 "the conditioning-signal
   observable of the companion's sequel" — no matching phrase found in p4.
   Left in place deliberately: author-guessing attributions is precisely the
   entry-13 (GarrigaVilenkin) failure mode. Rule 6 + the new self-cite clause
   apply.
2. **D5 device-feasibility citation** — the standing "do not circulate"
   gate above. p6 already carries the honest hedge ("a design exercise ...
   itself not yet tested end-to-end"); paper 9's own D5 paragraph does not.
3. **p6 biblio CERT 3/3 basis** — incomplete (22/27). Recommended: one
   self-cite-aware biblio pass over p6 rather than a 3→0 reset; the 22
   external records are verified three times over and the verdict on them is
   not in question. Author ruling pending.


## SESSION 2026-07-18/19 (numbering unification + claim-support)
- Folder paper9/ -> paper2/ (series 2, the experimental proposal); cite keys -> codenames.
- Claim-support (Opus): CLEAN; device claims verified against Klauck full text (PT threshold gamma=2kappa; operating point gamma/2kappa=0.25; HOM-dip 0.05cm; sinusoidal-modulation loss). Eichelkraut 2.6-7.8 dB/cm "demonstrated tuning range" NOT web-verifiable (Opt. Lett. paywalled, no arXiv) -> reworded to "set by the tunable-bending-loss modulation technique" (technique verified; specific upper range scoped, not asserted). VanWesemael jref unconfirmable (biblio-metadata note).

## OPUS 3-LANE WAVE 2026-07-19 (fresh out-of-rotation cross-model audit) -- SOUND
- **Claims: SOUND, zero CRITICAL/MAJOR.** All core math re-derived: t_c=κ̃⁻¹arcsinh(κ̃/(κ√2)) and every device table value (D1 5.10/−0.583, D2 3.98/−0.886, D3 window 1.55 + period 6.59, D4 EP 2.36/−0.30 continuous through EP), floor −(a+κ̃), dimensionless κt_c/flo/κ (D1≠D2 confirmed), feasibility dB/cm, novelty-vs-Bernardes (resolved -- Bernardes credited as prior art). **Prior floor inversion confirmed FIXED; the calibration-invariance is correctly NOT the definition-vs-estimator confusion a past audit wrongly flagged (not repeated).** Framing note: paper has NO "D1/D2 estimators"; D1-D4 are DEVICES (coupler families), r=γ/2κ the device ratio -- the two estimators are the column-normalized det zero-crossing (t_c) + closed-form floor fit. Applied 4 NITs: floor phrasing -> paper1's "approached from below by the signed entry"; dissociation bullet + "late (z>t_c) window" qualifier; abstract 3rd item + "phase-locked to the PT transition"; "D2 ... within 6cm chips" -> "D2, the deepest working device, ...".
- **Numerics: CLEAN.** Every claim reproduces from t2_measurement_chain.py; DETERMINISTIC (byte-identical across PYTHONHASHSEED default/12345/99 -- the prior salted-seed defect stays fixed); D2 HEALTHY at r=4 (n=400/row, no dead realizations; the r=6 7/400-dead degeneracy does not occur at r=4). Error budget, dark-floor bias, backflow ratios, D3 window/period, κt_c all trace.
- **Biblio: 7/7 external cites CLEAN** (Klauck2019/Eichelkraut2014/Xiao2019/Bernardes2015 verified vs primary; Tang2016/Ehrhardt2022/KAU2017 agree with paper4's same-session check). All claim-support passes. Softened one LOW flag: "Klauck operated at γ/2κ≈0.25" (exact ratio unverifiable behind paywall) -> "well inside the unbroken phase (far from the EP at γ/2κ=1)", keeping the confirmed qualitative point per pdf-reads-provisional.
- Recompiled clean; both gates PASS. Fully SOUND across all 3 lanes -- strong cross-model convergence for the experimental proposal.

## OPUS CLAIMS REVALIDATION 2026-07-20 (Wave B; 2nd Opus pass) -- SOUND
- Every device value re-derived from scratch again (t_c, D1-D4 table, floor, EP continuity, both dimensionless points D1≠D2, feasibility dB/cm). The calibration-invariance again confirmed NOT a definition-vs-estimator artifact (prior wrong-CRITICAL stays rejected). Session NITs read fine. No findings, no change.

## OPUS DEEP CLAIMS 2026-07-20 (Wave E; Nth adversarial pass) -- SOUND, 3 scope NITs applied
- No CRITICAL/MAJOR. Devices all re-derived; calibration-invariance again confirmed NOT a def-vs-estimator artifact. Applied: (1) MINOR falsification scope -- "null result would falsify" reworded so the MODEL-INDEPENDENT signal is recurrent negativity/t_c-crossing (floor-relax is model-relative, per item-2 hedge); (2) "three coupler families" -> "four couplers (D1-D4) spanning three PT regimes"; (3) late-window "z>=5cm" -> "at or just past each t_c" (D1 t_c=5.10 straddled 5.0).

## OPUS DEEP CLAIMS 2026-07-20 (hunt-what-was-rationalized wave, p1-p4) -- SOUND, 3 MINOR + 2 NIT applied
- No CRITICAL/MAJOR; all device numerics + the def-vs-estimator distinction re-verified (again NOT a conflation: column-normalization divides by positive column sums, cannot move the det zero-crossing). All fixes are in the intro summary of paper1's results (theorem spine untouched):
  - **Dissociation bullet (MINOR):** "is \emph{monotone} (no backflow) in the late ($z>t_c$) window" overstated a small NONZERO measured backflow (0.015 D1 / 0.018 D2) and mislabeled the window vs $t_c$ -> "shows \emph{negligible} backflow in the late window (for onsets $t_c$ preceding it)". Now matches paper1's own "conditional backflow confined to a neighborhood of $t_c(s)$".
  - **Umbrella verb (MINOR):** "\cite{indivisible} proves ..." -> "establishes ..." (the three bullets are two theorems + one NUMERICAL finding; "proves" over-attributed theorem status to the dissociation; bullet reworded "...---numerically, the two ... come apart").
  - **Onset bullet (MINOR):** "the process is P-divisible precisely on $[0,t_c)$" is a GLOBAL claim contradicted by the unbroken-phase recurrence in the same sentence -> "P-divisibility first fails at $t_c$ ... \emph{permanent} (P-divisible precisely on $[0,t_c)$)" scoped to the broken phase.
  - **NITs:** late-window "($z\ge5$cm, at or just past each $t_c$)" -> "($z\ge5$cm)" -- **reverts the imprecise annotation ADDED by Wave E this session** ("just past" is wrong for D1, whose window [5,10] straddles $t_c=5.10$; D2 $t_c=3.98$ is fully below). Plain "$z\ge5$cm" is accurate for both. Also ">24\sigma negative for D1/D2" -> ">=24\sigma" (D2 is exactly 24\sigma).
- Recompiled 3pp, 0 undefined. Both gates PASS. No MAJOR (ledger stays 59).

## RE-VERIFY 2026-07-20 (adversarial Opus check of this session's p2 intro edits) -- CONFIRMED + 1 sibling NIT
- Fresh Opus verifier confirmed all 4 intro-summary edits CORRECT + COMPLETE against this paper's device numbers AND paper1's dissociation section / thm:terminal; no stale sibling, no new inconsistency ("monotone" fully removed corpus-wide in p2). Surfaced 1 PRE-EXISTING sibling NIT (not from the edits): abstract "divisibility is permanently lost" was unscoped → "first lost (permanently, in the broken phase)" (the abstract sibling of the onset-bullet broken-phase scoping; the other 2 "permanent" sites at L59/L180 already scoped). minor-findings-ledger #8. Recompiled 3pp, both gates PASS.

## FABLE CLAIMS 2026-07-20 (cross-model wave p2/p4/p7) -- 1 MAJOR (ledger 61) + 5 MINOR + 1 NIT applied
- Fable re-ran t2_measurement_chain.py (every number reproduced) + re-derived thm:terminal cross-paper. **MAJOR (ledger 61):** D1 mischaracterized as "backflow-Markovian" -- its t_c=5.10cm sits INSIDE the z>=5cm window, so its 0.015 is mostly the theory-predicted onset-neighborhood tail (0.009 irreducible at 1e6), NOT noise; D2 (t_c=3.98) is the clean instance. Corrects the orchestrator's OWN Wave-1 simplification (dropping "at or just past t_c" buried the issue); Wave-3 re-verify then graded the nuance "informational" -- cross-model + numerics escalated it. Dissociation bullet reworded.
- Applied MINOR/NIT (#62-67): falsifier "fitted floor -> zero" structurally inoperable (floor=-(a+kt)<0 always) -> late-window lack-of-fit; "recurrent negativity" -> "divisor-entry negativity"; EP-continuity clause unsupported (D4 not simulated) -> scoped; Duhem hedge; guide-index convention; t_c arcsin continuation; per-config->per-launch.
- HELD (#68): F9 (6cm D2 not script-demonstrated -- re-run gives 24.8sigma), F10 (1e4 all-systematics qualifier), p1-spillover fig:generator caption (defensible).
- Recompiled 3pp, 0 undefined. Both gates PASS. Ledger -> 61.

## OPUS CLAIMS AUDIT 2026-07-23 (fresh, not in prior waves) — CLEAN, 1 NIT applied
- Ledger-61 (D1 backflow-Markovian) fix verified fully resolved, no stale siblings; all 4 device tables reproduce to 4 digits; calibration-invariance + two-dimensionless-points claims derived; both falsifiers operable. NIT applied: summary floor -(sinth+kt) -> -(a+kt) (gain a=gamma/2) to match body + remove forward-ref.

## (RETROACTIVE) MAJOR-ledger #74 fix — 2026-07-24 Wave 5 (was missing from this file; added W22 per reconcile-reflags hygiene)
- major-ledger #74: the "model-independent" null falsifier (divisibility "restored past t_c") is powerless on the null side — det_norm→0⁻ as z→∞ flips the late-z sign positive in most realizations even when the closed forms hold exactly. Fix: scoped the restoration test to the resolvable near-t_c window + det→0⁻ caveat + tempered "either outcome informative at 1e4". Applied 07-24; see major-findings-ledger.md #74. (Entry backfilled 2026-07-26.)

## W22 CONVERGENCE RE-CONFIRMATION 2026-07-26 (Fable, adversarial; claims+numerics+biblio) — CLEAN; convergence HOLDS
- **Both prior MAJOR fixes INTACT + independently re-derived:** #74 (null-falsifier scoping L202-214 present in full; no stale sibling reintroduces the overclaim — the only other "recurs in windows" at L62-63 is the unbroken-phase theory statement; mechanism re-derived: det=e^{−4az}(1−2r²), dark term decays only e^{−2(a−κ̃)z} and is positive, dominating late-z — D2 z=10: true −3.1e-6 vs dark +7.5e-5, deterministically positive). #61 (D1 backflow: 0.015 attributed to onset-tail, ≈0.009 irreducible matches script median; D2 named the clean instance).
- **CLAIMS CLEAN:** all 4 table rows + t_c=det-zero + floor inequality + P-divisible-on-[0,t_c) + calibration invariance + dark-bias sign all re-derived from scratch. **NUMERICS CLEAN:** ran t2_measurement_chain.py (400/400 all rows); every quoted number reproduces (precisions ±0.19/0.28 at 1e4, ±0.09/0.06 at 1e6; dark bias +0.05/+0.12; floors 3.4%/4.1%, 29.3σ/24.4σ; backflow 0.018/0.004, 0.015/0.009, 0.486; D3 period 2.29%). Congruent with paper1 (t_c under s→κ). **BIBLIO CLEAN** (8 entries; \cite{indivisible} verbatim vs paper1; Eichelkraut resolution holds).
- 3 NITs, none a regression / all defensible: "3-4%" (D2=4.1%, at edge); "±0.19 at 1e4" qualifier (held F10 defensible); + the process gap above (now closed).
- No manuscript change. Both gates PASS (unchanged). **p2 CONVERGENCE HOLDS (still 3/3).**

## W24 WIDE-OPEN AUDIT 2026-08-01 (Fable, adversarial) - NO MAJOR; 1 MINOR + 3 NIT applied; counter -> 0
- **NUMERICS CLEAN and confirmed DETERMINISTIC** (script run twice, byte-identical output, exit 0). Every quoted number reproduces. Two independent confirmations worth recording: (1) the auditor's own Monte Carlo re-established why the #74 falsifier scoping was necessary -- at 1e4 photons the late-z determinant flips positive in **79% (D1) and 100% (D2)** of realizations even with the closed forms exact; (2) the paper's unbroken-phase t_c is **identical to Klauck's published HOM-dip formula**, a nontrivial external consistency check nobody had noticed.
- **MINOR applied:** the "past gamma/2kappa ~ 5 the estimator fails outright" claim is not reproducible from the public script -- its supporting sweep survives only as a COMMENT BLOCK referencing a d2_sweep harness absent from scripts/, and the comment's own data shows 7/400 dead realizations at r=6, i.e. badly degraded rather than outright failed. Reworded to "by ~5-6 ... degrades beyond usefulness, its bias and spread exceeding the signal". (The harness itself should be published with the repos.)
- **NIT:** floor recovery "+-3-4%" -> 3.4% (D1) / 4.1% (D2), since 4.1% falls outside the stated bracket. **NIT:** the 0.009 D1 tail was called "theory-predicted" but the noiseless value is 0.0106 -- 0.009 is the simulated all-noise median, the dark floor slightly SUPPRESSING the tail; both now stated. **NIT:** "calibration errors that dominate the systematics" -> "the leading multiplicative systematic" (shot noise dominates the t_c spread at 1e4).
- **BIBLIO CLEAN**, 7/7 verified against Crossref published forms. Eichelkraut's dB/cm ceiling stays paywalled-unverifiable and is reported as such rather than asserted. minor-ledger #165.

## W26 WIDE-OPEN AUDIT 2026-08-01 (Fable) - no MAJOR on the physics; a #94-class reproducibility gap CLOSED; 2 MINOR applied; counter -> 0
- **Physics clean.** Every closed form re-derived by hand (det Gamma, t_c with its arcsin continuation, broken-phase permanence, window period, L12, the floor limit and its approach from below, EP limits and continuity). P-divisibility on [0,t_c) verified in both directions. Script run TWICE with byte-identical output -- deterministic, exit 0, nothing skipped. 8/8 bibitems Crossref-verified, claim-support taken from raw PDFs.
- **#94-class gap CLOSED:** the D2-depth claim rested on a `d2_sweep` harness that existed only as a comment quoting numbers -- the claim was TRUE but had no public path. The auditor re-implemented it independently and confirmed the numbers; the orchestrator then folded the sweep into the script as printed block **[C6]**, which reproduces both the comment and the auditor's run, matching the comment's 7/400 dead realizations at r=6 exactly. The stale pointer now names [C6].
- **MINOR (configuration provenance):** "the determinant flips positive in most realizations" carried no configuration -- 79% at 1e4 photons, 9% at 1e6. Both now stated, and the adjacent D1 backflow parenthetical (W24 orchestrator wording) gained its missing 1e6 label.
- **MINOR (feasibility honesty):** D2 needs 7.8 dB/cm, attributed to the Eichelkraut technique whose abstract promises only "almost arbitrary" loss and whose full text is paywalled and genuinely unverifiable. The highest loss demonstrated on the SAME platform in Klauck2019 is ~3 dB/cm. The paper now says plainly that D2's requirement sits ~2.6x above the published same-platform record -- an honest limitation for an experimental proposal, and better surfaced than buried.
- One orchestrator slip worth recording: the first [C6] draft used a wrong noise-dict key and crashed immediately. Caught by running it, as with #94's attempt 2 -- a script that is never executed is not a fix. minor-ledger #180.
