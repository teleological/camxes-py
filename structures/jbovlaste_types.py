
from structures.gensuha \
  import Cmevla, Gismu, Lujvo, Fuhivla, Fuhivla3, Fuhivla35, Fuhivla4, \
         Cmavo, ZeiLujvo, BuLetteral, Tosmabru, Slinkuhi

# legacy classifications
CMEVLA        = "cmevla"
GISMU         = "gismu"
LUJVO         = "lujvo"
FUHIVLA       = "fu'ivla"
CMAVO         = "cmavo"
NALVLA        = "nalvla"

# new classifications
CMAVO_COMPOUND = "cmavo-compound"
BU_LETTERAL    = "bu-letteral"
ZEI_LUJVO      = "zei-lujvo"

# non-jvs types
TOSMABRU       = "valrtosmabru"
SLINKUHI       = "valslinku'i"
FUHIVLA3       = "type-3 fu'ivla"
FUHIVLA35      = "type-3.5 fu'ivla"
FUHIVLA4       = "type-4 fu'ivla"

def classify(gensuha):
  if gensuha is None or len(gensuha) < 1:
    return NALVLA
  elif len(gensuha) == 1:
    return classify_gensuha(gensuha[0])
  else:
    return classify_gensuha_sequence(gensuha)

def classify_gensuha(gensuha):
  if isinstance(gensuha, Cmevla):
    return CMEVLA
  elif isinstance(gensuha, Gismu):
    return GISMU
  elif isinstance(gensuha, Lujvo):
    return LUJVO
  elif isinstance(gensuha, Fuhivla):
    if isinstance(gensuha, Fuhivla3):
      return '%s/%s/%s-%s-%s' % (FUHIVLA, gensuha.type, gensuha.rafsi, gensuha.hyphen, gensuha.payload)
    else:
      return '%s/%s' % (FUHIVLA, gensuha.type)
  elif isinstance(gensuha, Cmavo):
    return '%s/%s' % (CMAVO, gensuha.selmaho)
  elif isinstance(gensuha, ZeiLujvo):
    return ZEI_LUJVO
  elif isinstance(gensuha, BuLetteral):
    return BU_LETTERAL
  elif isinstance(gensuha, Tosmabru):
    return TOSMABRU
  elif isinstance(gensuha, Slinkuhi):
    return SLINKUHI
  else:
    return NALVLA

def classify_gensuha_sequence(gensuha):
  if is_cmavo_sequence(gensuha):
    return ' '.join(map(classify_gensuha, gensuha))
  else:
    return NALVLA

def is_cmavo_sequence(gensuha):
  return all(map(lambda g : isinstance(g, Cmavo), gensuha))

