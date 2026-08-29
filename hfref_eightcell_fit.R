###############################################################################
# HFrEF EIGHT-CELL MULTIVERSE -- REAL FIT PASS
# =============================================================================
# Written 2026-07-22.  Non-commercial evidence synthesis, RCT-only. PROTOTYPE.
#
# WHAT THIS DOES, AND WHY IT EXISTS
#   DUAL-FAMILY-REVIEW-2026-07-22.md D-2 ruled the eight-cell multiverse
#   "vaporware": designed, contracted, and NOT COMPUTED.  This script computes
#   it.  Every number the app renders is produced HERE, in R, by netmeta, from
#   the ledger's per-arm counts -- or it is not rendered at all.
#
# ESTIMATOR
#   Contrast-based GLS network meta-analysis (netmeta 3.6.1), log-RR scale,
#   common additive tau^2, tau^2 estimator set per cell by the `model` axis
#   coordinate (fe / dl / reml), HKSJ per the `hksj` coordinate.  Multi-arm
#   trials (CARMEN) enter as a correlated block: all three contrasts supplied,
#   netmeta reconstructs the covariance.
#
# WHAT IS *NOT* DONE HERE  (declared, not hidden)
#   - No inconsistency TEST is fitted or interpreted.  Per the retirement
#     decision the loop is not a testable claim: the direct Placebo->ARB leg
#     carries ~9-20 events and the minimum detectable inconsistency is a
#     multi-fold disagreement.  Row B reports STRUCTURE ONLY, and reports the
#     test as UNINFORMATIVE.
#   - No cell at outcome != acm.  Those layers are DATA-OWED (spec section 5).
#   - Cell 6 is NOT re-based onto van Essen's own 89-trial set: we do not hold
#     it as arm-level data in this repo.  Cell 6 is fitted on OUR set under his
#     coordinates and is flagged coordinate-identical to cell 4.
#
# GOVERNANCE
#   Reads: hfref-trial-ledger.jsonl (counts + PICO), netfit_hfref.py (the
#   frozen primary, used as the calibration target).  Writes: two new files,
#   hfref-eightcell-cells.json and hfref-eightcell-fit-log.txt.  Mutates no
#   ledger, no *-PROPOSED.jsonl, no git state.
###############################################################################

suppressMessages({
  library(netmeta)
  library(jsonlite)
})

options(stringsAsFactors = FALSE, width = 200)
LOG <- character(0)
say <- function(...) { s <- paste0(...); cat(s, "\n", sep = ""); LOG <<- c(LOG, s) }

say(strrep("=", 100))
say("HFrEF EIGHT-CELL MULTIVERSE -- REAL FIT PASS  (netmeta ",
    as.character(packageVersion("netmeta")), " / R ", getRversion(), ")")
say(strrep("=", 100))

###############################################################################
# 1. ARM-LEVEL DATA
#    Every count below is the ledger's, carried verbatim from
#    hfref-trial-ledger.jsonl data{deaths_t,n_t,deaths_c,n_c} and cross-checked
#    against netfit_hfref.py's frozen contrast list.  Nothing is invented here.
###############################################################################

arm <- function(id, trial, treat, event, n)
  data.frame(id = id, trial = trial, treat = treat, event = event, n = n)

ARMS <- rbind(
  # --- Placebo -> ACEI ------------------------------------------------------
  arm("HF-001", "SOLVD-Treatment",   "Placebo", 510, 1284),
  arm("HF-001", "SOLVD-Treatment",   "ACEI",    452, 1285),
  arm("HF-002", "FEST",              "Placebo",   3,  153),
  arm("HF-002", "FEST",              "ACEI",      5,  155),
  arm("HF-003", "CASSIS",            "Placebo",   6,   48),
  arm("HF-003", "CASSIS",            "ACEI",      7,  200),
  arm("HF-004", "Brown 1995",        "Placebo",   4,  125),
  arm("HF-004", "Brown 1995",        "ACEI",      3,  116),
  arm("HF-005", "Captopril-Digoxin", "Placebo",   6,  100),
  arm("HF-005", "Captopril-Digoxin", "ACEI",      8,  104),
  arm("HF-006", "Beller 1995",       "Placebo",   5,   63),
  arm("HF-006", "Beller 1995",       "ACEI",      4,  130),
  arm("HF-007", "van Veldhuisen 1998","Placebo",  1,   62),
  arm("HF-007", "van Veldhuisen 1998","ACEI",     2,  182),
  # --- Placebo -> ARB -------------------------------------------------------
  arm("HF-008", "SPICE",             "Placebo",   3,   91),
  arm("HF-008", "SPICE",             "ARB",       6,  179),
  arm("HF-009", "STRETCH",           "Placebo",   1,  211),
  arm("HF-009", "STRETCH",           "ARB",      10,  633),
  # --- ACEI -> ARB ----------------------------------------------------------
  arm("HF-010", "ELITE",             "ACEI",     32,  370),
  arm("HF-010", "ELITE",             "ARB",      17,  352),
  arm("HF-011", "ELITE-II",          "ACEI",    250, 1574),
  arm("HF-011", "ELITE-II",          "ARB",     280, 1578),
  arm("HF-012", "REPLACE",           "ACEI",      2,   77),
  arm("HF-012", "REPLACE",           "ARB",       4,  301),
  # --- ACEI -> ACEI+BB ------------------------------------------------------
  arm("HF-013", "CIBIS-I",           "ACEI",     67,  321),
  arm("HF-013", "CIBIS-I",           "ACEI+BB",  53,  320),
  arm("HF-014", "CIBIS-II",          "ACEI",    228, 1320),
  arm("HF-014", "CIBIS-II",          "ACEI+BB", 156, 1327),
  arm("HF-015", "MERIT-HF",          "ACEI",    217, 2001),
  arm("HF-015", "MERIT-HF",          "ACEI+BB", 145, 1990),
  arm("HF-016", "COPERNICUS",        "ACEI",    190, 1133),
  arm("HF-016", "COPERNICUS",        "ACEI+BB", 130, 1156),
  arm("HF-017", "BEST",              "ACEI",    449, 1354),
  arm("HF-017", "BEST",              "ACEI+BB", 411, 1354),
  arm("HF-018", "US-Carvedilol",     "ACEI",     31,  398),
  arm("HF-018", "US-Carvedilol",     "ACEI+BB",  22,  696),
  arm("HF-019", "RESOLVD",           "ACEI",     17,  212),
  arm("HF-019", "RESOLVD",           "ACEI+BB",   8,  214),
  # --- ACEI -> BB -----------------------------------------------------------
  arm("HF-020", "He 2015",           "ACEI",     19,  198),
  arm("HF-020", "He 2015",           "BB",       14,   96),
  # --- CARMEN, the only multi-arm trial: 3 arms, correlated block -----------
  arm("HF-021", "CARMEN",            "ACEI",     14,  190),
  arm("HF-021", "CARMEN",            "ACEI+BB",  14,  191),
  arm("HF-021", "CARMEN",            "BB",       14,  191),
  # --- MRA ------------------------------------------------------------------
  arm("HF-022", "RALES",             "ACEI",     386,  841),
  arm("HF-022", "RALES",             "ACEI+MRA", 284,  822),
  arm("HF-023", "EMPHASIS-HF",       "ACEI+BB",  213, 1373),
  arm("HF-023", "EMPHASIS-HF",       "ACEI+BB+MRA", 171, 1364),
  arm("HF-024", "J-EMPHASIS-HF",     "ACEI+BB",   10,  110),
  arm("HF-024", "J-EMPHASIS-HF",     "ACEI+BB+MRA", 17,  111),
  arm("HF-025", "Vizzardi 2014",     "ACEI+BB",    8,   65),
  arm("HF-025", "Vizzardi 2014",     "ACEI+BB+MRA",  8,   65),
  arm("HF-026", "EPHESUS",           "ACEI+BB",  554, 3313),
  arm("HF-026", "EPHESUS",           "ACEI+BB+MRA", 478, 3319),
  arm("HF-027", "AREA IN-CHF",       "ACEI+BB",   12,  236),
  arm("HF-027", "AREA IN-CHF",       "ACEI+BB+MRA",  6,  231),
  # --- ARB add-on -----------------------------------------------------------
  arm("HF-028", "Val-HeFT",          "ACEI",     484, 2499),
  arm("HF-028", "Val-HeFT",          "ACEI+ARB", 495, 2511),
  arm("HF-029", "CHARM-Added",       "ACEI+BB",  412, 1272),
  arm("HF-029", "CHARM-Added",       "ACEI+BB+ARB", 377, 1276),
  # --- ARNI -----------------------------------------------------------------
  arm("HF-030", "PARADIGM-HF",       "ACEI+BB",  835, 4212),
  arm("HF-030", "PARADIGM-HF",       "ARNI+BB",  711, 4187),
  arm("HF-031", "PARACHUTE-HF",      "ACEI+BB",  134,  460),
  arm("HF-031", "PARACHUTE-HF",      "ARNI+BB",  129,  462),
  # --- add-ons on triple ----------------------------------------------------
  arm("HF-032", "DAPA-HF",           "ACEI+BB+MRA", 329, 2371),
  arm("HF-032", "DAPA-HF",           "+SGLT2i",     276, 2373),
  arm("HF-033", "EMPEROR-Reduced",   "ACEI+BB+MRA", 266, 1867),
  arm("HF-033", "EMPEROR-Reduced",   "+SGLT2i",     249, 1863),
  arm("HF-034", "GALACTIC-HF",       "ACEI+BB+MRA", 1078, 4112),
  arm("HF-034", "GALACTIC-HF",       "+Omecamtiv",  1078, 4120),
  arm("HF-035", "VICTORIA",          "ACEI+BB+MRA", 561, 2524),
  arm("HF-035", "VICTORIA",          "+Vericiguat", 553, 2526),
  arm("HF-036", "VICTOR",            "ACEI+BB+MRA", 440, 3052),
  arm("HF-036", "VICTOR",            "+Vericiguat", 377, 3053),
  arm("HF-037", "DIGIT-HF",          "ACEI+BB+MRA", 177,  599),
  arm("HF-037", "DIGIT-HF",          "+Digitoxin",  167,  613),
  arm("HF-038", "QUEST",             "ACEI+BB+MRA", 262, 1555),
  arm("HF-038", "QUEST",             "+QLQX",       221, 1555),
  # --- H-ISDN ---------------------------------------------------------------
  arm("HF-039", "A-HeFT",            "Placebo",    54,  532),
  arm("HF-039", "A-HeFT",            "H-ISDN",     32,  518),
  # --- the four US-Carvedilol protocol papers.  Ledger status DOESN'T-BELONG
  #     (double-count-of-HF-018).  They enter ONLY at dupes = "protocols",
  #     ALONGSIDE the pooled report -- reproducing the field's shared error so
  #     the reader can see its size rather than take our word for it.
  arm("HF-052", "Colucci 1996",      "ACEI",       5,  134),
  arm("HF-052", "Colucci 1996",      "ACEI+BB",    2,  232),
  arm("HF-053", "MOCHA",             "ACEI",      13,   84),
  arm("HF-053", "MOCHA",             "ACEI+BB",   12,  261),
  arm("HF-054", "PRECISE",           "ACEI",      11,  145),
  arm("HF-054", "PRECISE",           "ACEI+BB",    6,  133),
  arm("HF-055", "Cohn 1997",         "ACEI",       2,   35),
  arm("HF-055", "Cohn 1997",         "ACEI+BB",    2,   70)
)

###############################################################################
# 2. TRIAL METADATA -- the axis inputs.  ef_ceiling and population are parsed
#    from the ledger's pico fields exactly as multiverse_precompute.py parses
#    them; elig level membership is INCLUSION-PASS section 2/4 as executed plus
#    X-8 (DECIDED: EXECUTE) and X-10 (RESOLVED: HOLD-AND-FLAG).
###############################################################################

m <- function(id, efceil, pop, drop_at, dupe = FALSE)
  data.frame(id = id, efceil = efceil, pop = pop, drop_at = drop_at, dupe = dupe)

# drop_at: the FIRST elig level at which the trial is evicted. "never" = kept
# at every level. L1 = INCLUSION-PASS era rule as executed (4 trials).
# L2 = L1 + X-8 symmetric eviction (FEST, van Veldhuisen 1998).
# L3 = L2 + X-10 (SPICE, STRETCH) -- computed and displayed, NOT executed.
META <- rbind(
  m("HF-001", 35, "chronic", "never"),
  m("HF-002", 35, "chronic", "L2"),      # FEST      -- X-8
  m("HF-003", NA, "chronic", "L1"),      # CASSIS
  m("HF-004", 45, "chronic", "L1"),      # Brown 1995
  m("HF-005", NA, "chronic", "L1"),      # Captopril-Digoxin
  m("HF-006", 45, "chronic", "L1"),      # Beller 1995
  m("HF-007", 45, "chronic", "L2"),      # van Veldhuisen 1998 -- X-8
  m("HF-008", 35, "chronic", "L3"),      # SPICE     -- X-10 (held)
  m("HF-009", 45, "chronic", "L3"),      # STRETCH   -- X-10 (held)
  m("HF-010", 40, "chronic", "never"),
  m("HF-011", 40, "chronic", "never"),
  m("HF-012", 40, "chronic", "never"),
  m("HF-013", 40, "chronic", "never"),
  m("HF-014", 35, "chronic", "never"),
  m("HF-015", 40, "chronic", "never"),
  m("HF-016", 25, "chronic", "never"),
  m("HF-017", 35, "chronic", "never"),
  m("HF-018", 35, "chronic", "never"),
  m("HF-019", 40, "chronic", "never"),
  m("HF-020", 40, "chronic", "never"),
  m("HF-021", 40, "chronic", "never"),
  m("HF-022", 35, "chronic", "never"),
  m("HF-023", 35, "chronic", "never"),
  m("HF-024", 35, "chronic", "never"),
  m("HF-025", 40, "chronic", "never"),
  m("HF-026", 40, "postmi",  "never"),   # EPHESUS
  m("HF-027", 45, "chronic", "never"),
  m("HF-028", 40, "chronic", "never"),
  m("HF-029", 40, "chronic", "never"),
  m("HF-030", 40, "chronic", "never"),
  m("HF-031", 40, "chronic", "never"),
  m("HF-032", 40, "chronic", "never"),
  m("HF-033", 40, "chronic", "never"),
  m("HF-034", 35, "chronic", "never"),
  m("HF-035", 45, "chronic", "never"),
  m("HF-036", 40, "chronic", "never"),
  m("HF-037", 40, "chronic", "never"),
  m("HF-038", 40, "chronic", "never"),
  m("HF-039", 45, "chronic", "never"),   # A-HeFT
  m("HF-052", 35, "chronic", "never", TRUE),
  m("HF-053", 35, "chronic", "never", TRUE),
  m("HF-054", 35, "chronic", "never", TRUE),
  m("HF-055", 35, "chronic", "never", TRUE)
)

ELIG_ORDER <- c(L0 = 0, L1 = 1, L2 = 2, L3 = 3)

###############################################################################
# 3. NODE -> COMPONENT MAP (11 components over 16 nodes), for the CNMA cells.
#    ARNI REPLACES ACEI, so ARNI+BB carries N and B but not A.
#    Source: HFREF-COMPONENT-NMA-2026-07-19.md section 1, extended to the full
#    16-node network.  rank(node->component map) = 15 - 11 = 4 additivity df,
#    which is the UPPER BOUND the board records (X-7); 7 of 11 components are
#    single-node and untestable.
###############################################################################

NODES <- c("Placebo","ACEI","ARB","ACEI+BB","BB","ACEI+MRA","ACEI+ARB",
           "ACEI+BB+ARB","ACEI+BB+MRA","ARNI+BB","+SGLT2i","+Omecamtiv",
           "+Vericiguat","H-ISDN","+Digitoxin","+QLQX")
COMPS <- c("A","R","B","M","N","S","O","V","H","D","Q")
CMAP <- list(
  "Placebo"      = c(),
  "ACEI"         = c("A"),
  "ARB"          = c("R"),
  "ACEI+BB"      = c("A","B"),
  "BB"           = c("B"),
  "ACEI+MRA"     = c("A","M"),
  "ACEI+ARB"     = c("A","R"),
  "ACEI+BB+ARB"  = c("A","B","R"),
  "ACEI+BB+MRA"  = c("A","B","M"),
  "ARNI+BB"      = c("N","B"),
  "+SGLT2i"      = c("A","B","M","S"),
  "+Omecamtiv"   = c("A","B","M","O"),
  "+Vericiguat"  = c("A","B","M","V"),
  "H-ISDN"       = c("H"),
  "+Digitoxin"   = c("A","B","M","D"),
  "+QLQX"        = c("A","B","M","Q")
)

build_C <- function(trts) {
  C <- matrix(0, nrow = length(trts), ncol = length(COMPS),
              dimnames = list(trts, COMPS))
  for (t in trts) C[t, CMAP[[t]]] <- 1
  keep <- colSums(C) > 0
  C[, keep, drop = FALSE]
}

###############################################################################
# 4. CONTRAST CONSTRUCTION
#    log RR with SE = sqrt(1/e1 - 1/n1 + 1/e0 - 1/n0), 0.5 continuity
#    correction ONLY when a cell is zero (advanced-stats rule: unconditional
#    correction biases RR toward the null).  No zero cell exists in this set;
#    the branch is kept so a future extraction cannot silently change meaning.
###############################################################################

lrr <- function(e1, n1, e0, n0) {
  if (e1 == 0 || e0 == 0) { e1 <- e1 + 0.5; n1 <- n1 + 1; e0 <- e0 + 0.5; n0 <- n0 + 1 }
  c(log((e1 / n1) / (e0 / n0)), sqrt(1 / e1 - 1 / n1 + 1 / e0 - 1 / n0))
}

# EMPEROR-Reduced alternative representation (the `emperor` axis).
# "hr": log(0.92) with SE from the published 95% CI 0.77-1.10, exactly as
# netfit_hfref.py entered it.  "rr": the per-arm counts above.
EMPEROR_HR   <- log(0.92)
EMPEROR_HRSE <- (log(1.10) - log(0.77)) / (2 * qnorm(0.975))

mk_contrasts <- function(d, emperor = "rr") {
  out <- NULL
  for (tr in unique(d$trial)) {
    a <- d[d$trial == tr, ]
    if (nrow(a) < 2) next
    for (i in 1:(nrow(a) - 1)) for (j in (i + 1):nrow(a)) {
      # direction: treat1 vs treat2, treat2 = the row nearer placebo in the
      # order the arms were entered (arm 1 is always the comparator side).
      s <- lrr(a$event[j], a$n[j], a$event[i], a$n[i])
      out <- rbind(out, data.frame(
        studlab = tr, id = a$id[1],
        treat1 = a$treat[j], treat2 = a$treat[i],
        TE = s[1], seTE = s[2],
        event1 = a$event[j], n1 = a$n[j], event2 = a$event[i], n2 = a$n[i]))
    }
  }
  if (emperor == "hr" && any(out$studlab == "EMPEROR-Reduced")) {
    k <- which(out$studlab == "EMPEROR-Reduced")
    out$TE[k] <- EMPEROR_HR; out$seTE[k] <- EMPEROR_HRSE
  }
  out
}

###############################################################################
# 5. STRUCTURE  -- reported, never tested.
#    ICDF (Lu-Ades independent-loop count) = cyclomatic number of the treatment
#    graph MINUS loops closed entirely inside a single multi-arm study (such a
#    loop supplies no between-trial inconsistency information).  CARMEN is the
#    only multi-arm trial in this evidence base.
###############################################################################

structure_of <- function(cn) {
  edges <- unique(apply(cn[, c("treat1","treat2")], 1,
                        function(r) paste(sort(r), collapse = "|")))
  trts  <- sort(unique(c(cn$treat1, cn$treat2)))
  V <- length(trts); E <- length(edges)
  # designs = distinct treatment sets compared within a study
  des <- tapply(seq_len(nrow(cn)), cn$studlab,
                function(ix) paste(sort(unique(c(cn$treat1[ix], cn$treat2[ix]))),
                                   collapse = "|"))
  ndes <- length(unique(des))
  multi <- names(which(table(cn$studlab) > 1))   # >1 contrast => multi-arm
  internal <- 0
  for (s in multi) {
    a <- cn[cn$studlab == s, ]
    vt <- length(unique(c(a$treat1, a$treat2)))
    internal <- internal + (nrow(a) - (vt - 1))  # loops inside the study
  }
  cyclo <- E - V + 1
  list(V = V, E = E, designs = ndes, cyclomatic = cyclo,
       icdf = cyclo - internal, multiarm_internal_loops = internal,
       treatments = trts)
}

###############################################################################
# 6. CELL DEFINITIONS -- coordinates only.  No cell may carry a free-text
#    specification field (contract C1).
###############################################################################

cell <- function(cell_id, label, review, tier, repro, model, ef, pop, dupes,
                 elig, atype, hksj, scale, emperor = "rr", note = "")
  list(cell_id = cell_id, label = label, review = review, tier = tier,
       repro_label = repro,
       coords = list(estimand = model, ef = ef, atype = atype, elig = elig,
                     pop = pop, dupes = dupes, outcome = "acm", hksj = hksj,
                     emperor = emperor),
       scale = scale, note = note)

CELLS <- list(
  cell("T24-tang-2024",     "1. Tang 2024",       "Tang 2024",       "EXPLORATORY", "APPROXIMATE",
       "reml", "le45", "postmi",  "protocols", "L0", "nma-network", FALSE, "RR"),
  cell("B17-burnett-2017",  "2. Burnett 2017",    "Burnett 2017",    "EXPLORATORY", "INSPIRED-BY",
       "reml", "le45", "chronic", "once",      "L0", "nma-network", FALSE, "HR"),
  cell("K18-komajda-2018",  "3. Komajda 2018",    "Komajda 2018",    "EXPLORATORY", "INSPIRED-BY",
       "reml", "le45", "chronic", "protocols", "L0", "nma-network", FALSE, "HR"),
  cell("T21-tromp-2021",    "4. Tromp 2021/22",   "Tromp 2021/22",   "EXPLORATORY", "INSPIRED-BY",
       "fe",   "any",  "chronic", "once",      "L0", "cnma",        FALSE, "HR"),
  cell("DM22-demarzo-2022", "5. De Marzo 2022",   "De Marzo 2022",   "EXPLORATORY", "INSPIRED-BY",
       "reml", "le45", "chronic", "protocols", "L0", "nma-network", FALSE, "HR"),
  cell("vE25-vanessen-2025","6. van Essen 2025",  "van Essen 2025",  "EXPLORATORY", "INSPIRED-BY",
       "fe",   "any",  "chronic", "once",      "L0", "cnma",        FALSE, "HR"),
  cell("OURS-STRICT",       "7a. OURS-STRICT",    "ours",            "PRIMARY",     "OURS",
       "reml", "le40", "chronic", "once",      "L2", "nma-network", TRUE,  "RR"),
  cell("OURS-INCLUSIVE",    "8. OURS-INCLUSIVE",  "ours",            "SENSITIVITY", "OURS",
       "reml", "le40", "chronic", "once",      "L0", "nma-network", TRUE,  "RR"),
  # mandatory displayed branches of cell 7 (X-10 executed); NOT the primary
  cell("OURS-STRICT-7b",    "7b. X-10 executed",  "ours",            "BRANCH",      "OURS",
       "reml", "le40", "chronic", "once",      "L3", "nma-network", TRUE,  "RR"),
  cell("OURS-STRICT-7c",    "7c. X-10, -CARMEN",  "ours",            "BRANCH",      "OURS",
       "reml", "le40", "chronic", "once",      "L3", "nma-network", TRUE,  "RR",
       note = "CARMEN inadmissible (its primary reports LVESVI and no deaths)"),
  # calibration: reproduce netfit_hfref.py's frozen primary coordinates exactly
  cell("CAL-netfit-v1.3",   "CAL. frozen v1.3",   "ours",            "CALIBRATION", "OURS",
       "dl",   "any",  "postmi",  "once",      "L0", "nma-network", TRUE,  "RR",
       emperor = "hr",
       note = "R re-implementation target: netfit_hfref.py (Python/numpy)")
)
DROP_CARMEN <- c("OURS-STRICT-7c")

###############################################################################
# 7. THE FIT
###############################################################################

REPORT_NODES <- c("ACEI","ACEI+BB","ACEI+MRA","ACEI+BB+MRA","ARNI+BB","+SGLT2i",
                  "ARB","ACEI+ARB","ACEI+BB+ARB","BB","+Omecamtiv","+Vericiguat",
                  "H-ISDN","+Digitoxin","+QLQX")

select_trials <- function(co) {
  keep <- META
  if (co$dupes == "once") keep <- keep[!keep$dupe, ]
  if (co$ef == "le40")    keep <- keep[is.na(keep$efceil) | keep$efceil <= 40, ]
  if (co$pop == "chronic") keep <- keep[keep$pop == "chronic", ]
  lvl <- ELIG_ORDER[[co$elig]]
  keep <- keep[keep$drop_at == "never" | ELIG_ORDER[keep$drop_at] > lvl, ]
  keep$id
}

fit_cell <- function(cl) {
  co  <- cl$coords
  ids <- select_trials(co)
  if (cl$cell_id %in% DROP_CARMEN) ids <- setdiff(ids, "HF-021")
  d  <- ARMS[ARMS$id %in% ids, ]
  cn <- mk_contrasts(d, emperor = co$emperor)
  st <- structure_of(cn)

  net <- try(netmeta(TE = TE, seTE = seTE, treat1 = treat1, treat2 = treat2,
                     studlab = studlab, data = cn, sm = "RR",
                     common = (co$estimand == "fe"),
                     random = (co$estimand != "fe"),
                     method.tau = if (co$estimand == "reml") "REML" else "DL",
                     reference.group = "Placebo", warn = FALSE,
                     details.chkmultiarm = FALSE), silent = TRUE)
  if (inherits(net, "try-error")) {
    return(list(cell = cl, computed = FALSE,
                not_computed_reason = paste("netmeta failed:", as.character(net))))
  }

  rnd <- (co$estimand != "fe")
  TEm <- if (rnd) net$TE.random  else net$TE.common
  SEm <- if (rnd) net$seTE.random else net$seTE.common
  LOm <- if (rnd) net$lower.random else net$lower.common
  HIm <- if (rnd) net$upper.random else net$upper.common

  # --- HKSJ.  netmeta 3.6.1 offers only "classic" and "t-dist" CIs, neither of
  # --- which is the Hartung-Knapp VARIANCE INFLATION.  The house standard
  # --- (recon_hfref.py / netfit_hfref.py) is the full HKSJ: multiply the
  # --- network variances by q = max(1, r'Wr/df) and take the t_df critical
  # --- value.  The max(1, .) floor is mandatory -- without it HKSJ NARROWS the
  # --- interval below the uncorrected one when Q < df (advanced-stats rule).
  hk <- list(applied = FALSE, q = 1, df = unname(net$df.Q), crit = qnorm(0.975))
  if (co$hksj) {
    fitted <- if (rnd) net$TE.nma.random else net$TE.nma.common
    w   <- 1 / (net$seTE^2 + (if (rnd) net$tau2 else 0))
    dfq <- unname(net$df.Q)
    q   <- if (dfq > 0) max(1, sum(w * (net$TE - fitted)^2) / dfq) else 1
    hk  <- list(applied = TRUE, q = unname(q), df = dfq,
                crit = if (dfq > 0) qt(0.975, dfq) else qnorm(0.975))
    LOm <- TEm - hk$crit * sqrt(hk$q) * SEm
    HIm <- TEm + hk$crit * sqrt(hk$q) * SEm
  }

  rows <- list()
  for (nd in REPORT_NODES) {
    if (!(nd %in% st$treatments)) {
      rows[[nd]] <- list(node = nd, present = FALSE,
                         reason = "node absent from this cell's trial set")
      next
    }
    rows[[nd]] <- list(node = nd, present = TRUE,
                       rr = unname(exp(TEm[nd, "Placebo"])),
                       lo = unname(exp(LOm[nd, "Placebo"])),
                       hi = unname(exp(HIm[nd, "Placebo"])))
  }

  # ranking -- P-scores.  Cell 3 (K18) is the one review that DECLINES to rank;
  # its ranking row is stamped, not blanked, at render time.
  rk <- try(netrank(net, small.values = "desirable"), silent = TRUE)
  pscore <- if (inherits(rk, "try-error")) NULL else {
    v <- if (rnd) rk$ranking.random else rk$ranking.common
    as.list(round(v[order(-v)], 4))
  }

  # per-edge k and heterogeneity
  edge_k <- table(apply(cn[, c("treat1","treat2")], 1,
                        function(r) paste(sort(r), collapse = " vs ")))
  dd <- try(decomp.design(net), silent = TRUE)
  qw <- NULL; qb <- NULL
  if (!inherits(dd, "try-error") && !is.null(dd$Q.decomp)) {
    Q <- dd$Q.decomp
    if ("Within designs" %in% rownames(Q))
      qw <- list(Q = unname(Q["Within designs","Q"]),
                 df = unname(Q["Within designs","df"]),
                 p  = unname(Q["Within designs","pval"]))
    if ("Between designs" %in% rownames(Q))
      qb <- list(Q = unname(Q["Between designs","Q"]),
                 df = unname(Q["Between designs","df"]),
                 p  = unname(Q["Between designs","pval"]))
  }

  # per-design I^2 -- find the worst-fitting edge (the network's real problem)
  i2max <- NULL
  for (e in names(edge_k)) {
    if (edge_k[[e]] < 2) next
    tt <- strsplit(e, " vs ", fixed = TRUE)[[1]]
    sub <- cn[(cn$treat1 == tt[1] & cn$treat2 == tt[2]) |
              (cn$treat1 == tt[2] & cn$treat2 == tt[1]), ]
    w <- 1 / sub$seTE^2; mu <- sum(w * sub$TE) / sum(w)
    Qe <- sum(w * (sub$TE - mu)^2); dfe <- nrow(sub) - 1
    I2 <- max(0, (Qe - dfe) / Qe)
    if (is.null(i2max) || I2 > i2max$i2)
      i2max <- list(edge = e, k = unname(edge_k[[e]]), Q = Qe, df = dfe, i2 = I2)
  }

  # ---- MDE: how big a direct-vs-indirect disagreement could this network
  # ---- even detect?  Reported INSTEAD of an inconsistency test.
  mde <- NULL
  if (st$icdf >= 1) {
    ns <- try(netsplit(net), silent = TRUE)
    if (!inherits(ns, "try-error")) {
      dir <- if (rnd) ns$direct.random else ns$direct.common
      ind <- if (rnd) ns$indirect.random else ns$indirect.common
      ok <- which(!is.na(dir$seTE) & !is.na(ind$seTE) &
                  is.finite(dir$seTE) & is.finite(ind$seTE))
      if (length(ok)) {
        z  <- qnorm(0.975) + qnorm(0.80)
        se <- sqrt(dir$seTE[ok]^2 + ind$seTE[ok]^2)
        allc <- lapply(seq_along(ok), function(i)
          list(comparison = as.character(ns$comparison[ok][i]),
               fold = unname(exp(z * se[i])),
               direct_share_of_loop_variance =
                 unname(dir$seTE[ok][i]^2 / (dir$seTE[ok][i]^2 + ind$seTE[ok][i]^2))))
        j <- which.min(se)   # the BEST-POWERED comparison in the whole network
        # the loop-bearing leg specifically (Placebo-ACEI-ARB is the only
        # between-trial loop in every cell that has one)
        arb <- grep("ARB", sapply(allc, function(x) x$comparison))
        arb <- arb[grepl("Placebo", sapply(allc, function(x) x$comparison))[arb]]
        mde <- list(best_powered = allc[[j]],
                    se_loop = unname(se[j]),
                    comparison = allc[[j]]$comparison,
                    fold = allc[[j]]$fold,
                    direct_share_of_loop_variance =
                      allc[[j]]$direct_share_of_loop_variance,
                    placebo_arb_leg = if (length(arb)) allc[[arb[1]]] else NULL,
                    all_splittable = allc,
                    n_splittable = length(ok),
                    basis = paste0("80% power, two-sided 5%; ",
                                   "MDE = exp((z_.975 + z_.80) * sqrt(var_direct + var_indirect)). ",
                                   "Reported INSTEAD of an inconsistency test, not alongside one."))
      }
    }
  }

  # ---- direct evidence on the loop-bearing leg, for the honest power line
  arb_leg <- cn[(cn$treat1 == "ARB" & cn$treat2 == "Placebo") |
                (cn$treat2 == "ARB" & cn$treat1 == "Placebo"), ]
  arb_events <- if (nrow(arb_leg)) sum(arb_leg$event1 + arb_leg$event2) else 0

  # ---- component (additive CNMA) row, for atype == "cnma"
  comp <- NULL
  if (co$atype == "cnma") {
    Cm <- build_C(st$treatments)
    nc <- try(netcomb(net, C.matrix = Cm), silent = TRUE)
    if (!inherits(nc, "try-error")) {
      cr <- if (rnd) exp(nc$Comp.random) else exp(nc$Comp.common)
      cl_ <- if (rnd) exp(nc$lower.Comp.random) else exp(nc$lower.Comp.common)
      cu <- if (rnd) exp(nc$upper.Comp.random) else exp(nc$upper.Comp.common)
      cnames <- nc$comps
      if (is.null(cnames) || length(cnames) != length(cr)) cnames <- colnames(Cm)
      if (is.null(cnames) || length(cnames) != length(cr)) cnames <- names(cr)
      comp <- list(
        components = lapply(seq_along(cr), function(i)
          list(comp = as.character(cnames[i]), rr = unname(cr[i]),
               lo = unname(cl_[i]), hi = unname(cu[i]))),
        additivity = list(
          Q = unname(if (rnd) nc$Q.diff else nc$Q.diff),
          df = unname(nc$df.Q.diff),
          p  = unname(nc$pval.Q.diff),
          note = paste0("additivity df is an UPPER BOUND (rank of the ",
                        "node->component map); it is a SEPARATE CURRENCY from ",
                        "inconsistency df and the two are never summed")))
    } else {
      comp <- list(not_computed_reason = paste("netcomb failed:", as.character(nc)))
    }
  }

  list(cell = cl, computed = TRUE,
       trials = list(n = length(unique(cn$studlab)), ids = sort(unique(ids)),
                     names = sort(unique(cn$studlab))),
       contrasts = nrow(cn),
       structure = st,
       tau2 = unname(if (rnd) net$tau2 else 0),
       i2 = unname(net$I2),
       nodes = unname(rows),
       pscore = pscore,
       edge_k = as.list(edge_k),
       q_within = qw, q_between_designs = qb,
       i2_max_edge = i2max,
       mde = mde,
       placebo_arb_leg = list(k = nrow(arb_leg), events = arb_events),
       component_row = comp)
}

###############################################################################
# 8. RUN
###############################################################################

RES <- list()
for (cl in CELLS) {
  say("")
  say(strrep("-", 100))
  say(sprintf("CELL %-22s  %s", cl$cell_id, cl$label))
  co <- cl$coords
  say(sprintf("  coords: estimand=%s ef=%s atype=%s elig=%s pop=%s dupes=%s outcome=%s hksj=%s emperor=%s",
              co$estimand, co$ef, co$atype, co$elig, co$pop, co$dupes,
              co$outcome, co$hksj, co$emperor))
  r <- fit_cell(cl)
  RES[[cl$cell_id]] <- r
  if (!isTRUE(r$computed)) { say("  NOT COMPUTED: ", r$not_computed_reason); next }
  st <- r$structure
  say(sprintf("  trials=%d  contrasts=%d  V=%d  E=%d  designs=%d  cyclomatic=%d  ICDF=%d  tau2=%.5f  I2=%.1f%%",
              r$trials$n, r$contrasts, st$V, st$E, st$designs, st$cyclomatic,
              st$icdf, r$tau2, 100 * r$i2))
  for (nd in r$nodes) {
    if (!isTRUE(nd$present)) next
    if (!(nd$node %in% c("ACEI","ACEI+BB","ACEI+MRA","ACEI+BB+MRA","ARNI+BB","+SGLT2i"))) next
    say(sprintf("    %-14s RR %.3f (%.3f-%.3f)", nd$node, nd$rr, nd$lo, nd$hi))
  }
  if (!is.null(r$q_within))
    say(sprintf("    Q_within  = %.3f  df %d  p %.4f", r$q_within$Q, r$q_within$df, r$q_within$p))
  if (!is.null(r$i2_max_edge))
    say(sprintf("    worst edge: %s  k=%d  I2=%.1f%%", r$i2_max_edge$edge,
                r$i2_max_edge$k, 100 * r$i2_max_edge$i2))
  if (!is.null(r$mde)) {
    say(sprintf("    MDE (best-powered of %d splittable comparisons) = %.2f-fold on %s (direct share %.1f%%)",
                r$mde$n_splittable, r$mde$fold, r$mde$comparison,
                100 * r$mde$direct_share_of_loop_variance))
    if (!is.null(r$mde$placebo_arb_leg))
      say(sprintf("    MDE on the loop-bearing Placebo-ARB leg = %.2f-fold (direct share %.1f%%)",
                  r$mde$placebo_arb_leg$fold,
                  100 * r$mde$placebo_arb_leg$direct_share_of_loop_variance))
  } else if (r$structure$icdf < 1) {
    say("    inconsistency: NOT ASSESSABLE -- no between-trial closed loop (near-tree). ",
        "Consistent by construction; this is a property of a sequential add-on ",
        "evidence base, not a failure of the fit.")
  }
  say(sprintf("    Placebo-ARB direct leg: k=%d, %d events", r$placebo_arb_leg$k,
              r$placebo_arb_leg$events))
  if (!is.null(r$component_row) && is.null(r$component_row$not_computed_reason)) {
    cs <- sapply(r$component_row$components,
                 function(x) sprintf("%s %.3f", x$comp, x$rr))
    say("    components: ", paste(cs, collapse = "  "))
  }
}

###############################################################################
# 9. CALIBRATION CHECK against netfit_hfref.py's frozen v1.3 primary.
#    If this fails, nothing downstream may be trusted.
###############################################################################

say(""); say(strrep("=", 100))
say("CALIBRATION -- R/netmeta vs the frozen Python fit (netfit_hfref.py)")
say(strrep("=", 100))
TARGET <- list("ACEI"        = c(0.858, 0.652, 1.128),
               "ACEI+MRA"    = c(0.646, 0.423, 0.986),
               "ACEI+BB"     = c(0.627, 0.458, 0.858),
               "ARNI+BB"     = c(0.562, 0.379, 0.835),
               "ACEI+BB+MRA" = c(0.542, 0.369, 0.797),
               "+SGLT2i"     = c(0.475, 0.301, 0.750))
cal <- RES[["CAL-netfit-v1.3"]]
calrows <- list()
maxdev <- 0
cal_ok <- isTRUE(cal$computed)
if (!cal_ok) {
  say("  CALIBRATION CELL DID NOT COMPUTE: ", cal$not_computed_reason)
  say("  VERDICT: CALIBRATION FAILED -- NOT 'passed with 0 deviation'. ",
      "An empty comparison set is a FAILURE, not a pass.")
}
for (nd in if (cal_ok) cal$nodes else list()) {
  if (!isTRUE(nd$present) || !(nd$node %in% names(TARGET))) next
  t <- TARGET[[nd$node]]
  dev <- abs(nd$rr - t[1]) / t[1]
  maxdev <- max(maxdev, dev)
  calrows[[nd$node]] <- list(node = nd$node,
                             r = c(nd$rr, nd$lo, nd$hi), python = t,
                             rel_dev_point = dev)
  say(sprintf("  %-14s R %.3f (%.3f-%.3f)   Python %.3f (%.3f-%.3f)   dev %+.2f%%",
              nd$node, nd$rr, nd$lo, nd$hi, t[1], t[2], t[3], 100 * dev))
}
CAL_PASS <- cal_ok && length(calrows) == length(TARGET) && maxdev < 0.02
if (cal_ok) {
  say(sprintf("  nodes compared: %d of %d target nodes", length(calrows), length(TARGET)))
  say(sprintf("  MAX RELATIVE DEVIATION ON THE POINT ESTIMATE: %.3f%%", 100 * maxdev))
}
say(if (CAL_PASS)
      "  VERDICT: PASS -- the R implementation reproduces the frozen Python fit to <2% on all 6 nodes."
    else if (!cal_ok)
      "  VERDICT: FAIL -- calibration cell did not compute."
    else if (length(calrows) < length(TARGET))
      sprintf("  VERDICT: FAIL -- only %d of %d target nodes were compared.",
              length(calrows), length(TARGET))
    else
      "  VERDICT: FAIL -- deviation >2%; the two implementations DISAGREE. Report it, do not smooth it.")

###############################################################################
# 10. EMIT
###############################################################################

out <- list(
  generated = "hfref_eightcell_fit.R",
  engine = paste0("R ", getRversion(), " / netmeta ", packageVersion("netmeta")),
  outcome = "all-cause mortality (acm) -- the ONLY outcome layer with a LIVE readiness state",
  scale_note = paste0("All cells are fitted on the RR scale from per-arm counts. ",
                      "Cells whose source review reports HR are NOT-LIKE-FOR-LIKE ",
                      "and no numeric difference against their published value may ",
                      "be rendered (contract C3)."),
  inconsistency_policy = paste0("RETIRED AS A TESTABLE CLAIM. Row B reports network ",
                                "STRUCTURE and the minimum detectable inconsistency ",
                                "only. No inconsistency test is fitted, quoted or ",
                                "interpreted in any cell."),
  calibration = list(target = "netfit_hfref.py frozen v1.3 primary",
                     rows = unname(calrows), nodes_compared = length(calrows),
                     nodes_required = length(TARGET),
                     max_rel_dev_point = maxdev, pass = CAL_PASS),
  cells = unname(lapply(RES, function(r) r))
)
write(toJSON(out, auto_unbox = TRUE, digits = 8, null = "null", na = "null"),
      file = "hfref-eightcell-cells.json")
writeLines(LOG, "hfref-eightcell-fit-log.txt")
say(""); say("WROTE hfref-eightcell-cells.json and hfref-eightcell-fit-log.txt")
