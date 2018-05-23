
# pylint: disable=I0011, C0111, C0326

from structures.gensuha \
  import Cmevla, Gismu, Lujvo, Fuhivla, Cmavo, ZeiLujvo, BuLetteral, Tosmabru, Slinkuhi

# legacy classifications
CMEVLA        = "cmevla"
GISMU         = "gismu"
LUJVO         = "lujvo"
FUHIVLA       = "fu'ivla"
CMAVO         = "cmavo"
NALVLA        = "nalvla"

# new classifications
CMAVO_COMPOUND = "cmavo-compound"
PHRASE = "phrase"
BU_LETTERAL    = "bu-letteral"
ZEI_LUJVO      = "zei-lujvo"

# non-jvs types
TOSMABRU       = "valrtosmabru"
SLINKUHI       = "valslinku'i"

def classify(gensuha):
    if gensuha is None or len(gensuha) < 1:
        return NALVLA
    elif len(gensuha) == 1:
        return classify_gensuha(gensuha[0])
    else:
        return classify_gensuha_sequence(gensuha)

def classify_gensuha(gensuha):
    classified = None
    if isinstance(gensuha, Cmevla):
        classified = CMEVLA
    elif isinstance(gensuha, Gismu):
        classified = GISMU
    elif isinstance(gensuha, Lujvo):
        classified = LUJVO
    elif isinstance(gensuha, Fuhivla):
        classified = FUHIVLA
    elif isinstance(gensuha, Cmavo):
        classified = CMAVO
    elif isinstance(gensuha, ZeiLujvo):
        classified = ZEI_LUJVO
    elif isinstance(gensuha, BuLetteral):
        classified = BU_LETTERAL
    elif isinstance(gensuha, Tosmabru):
        classified = TOSMABRU
    elif isinstance(gensuha, Slinkuhi):
        classified = SLINKUHI
    else:
        classified = NALVLA
    return classified

def classify_gensuha_sequence(gensuha):
    if is_cmavo_sequence(gensuha):
        return CMAVO_COMPOUND
    elif is_phrase(gensuha):
        return PHRASE
    else:
        return NALVLA

def is_cmavo_sequence(gensuha):
    return all(isinstance(g, Cmavo) for g in gensuha)

def is_phrase(gensuha):
    return all(isinstance(g, (Cmevla, Gismu, Lujvo, Fuhivla, Cmavo)) for g in gensuha)
