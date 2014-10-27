
from collections import OrderedDict

# Glossary

# genturfa'i : parser ("grammar-structure discoverer")

# terge'a : grammatical-text

# A text which is accepted by a {genturfa'i} is a {terge'a}, a grammatical
# text according to the {gerna} of the {genturfa'i}.

# gensu'a : grammar-structure

# This describes the structures discoved by the parser, with complex {gensu'a}
# being composed of less complex {gensu'a}.

# genturtai : grammar-structure form

# Parsed {gensu'a} may be classified by form of composition, {genturtai}.
# Individual characters, {lerfu}, are atomic {gensu'a}. A sequence of {lerfu}
# compose a {lerpoi}. Lojban's rules of morphology define specific {lerpoi}
# forms, such as {cmevla}, {brivla} and {cmavo}. Different forms of {brivla}
# are distinguished as {gismu}, {lujvo} and {fu'ivla}. A sequence of {brivla}
# compose a {tanru}.

class Gensuha:

  GENTURTAI = "naltarmi"

class Lerpoi(Gensuha):

  GENTURTAI = "lerpoi"

  def __init__(self, lerpoi):
    self.lerpoi = lerpoi

  def as_json(self):
    return OrderedDict([
      ( "genturtai", self.GENTURTAI ),
      ( "lerpoi",    self.lerpoi    )
    ])

  def __str__(self):
    return self.lerpoi

class Naljbo(Lerpoi):

  GENTURTAI = "naljbo"

class Valsi(Lerpoi):

  GENTURTAI = "valsi"

class Cmevla(Valsi):

  GENTURTAI = "cmevla"

class Selbri: # not itself a structure, but a property of some structures
  pass

class Brivla(Valsi, Selbri):
  pass

class Gismu(Brivla):

  GENTURTAI = "gismu"

class Jvodunlei: # not a structure
  pass

class Lujvo(Brivla, Jvodunlei):

  GENTURTAI = "lujvo"

class Fuhivla(Brivla):

  GENTURTAI = "fuhivla"

class Cmavo(Valsi):

  GENTURTAI = "cmavo"

  def __init__(self, lerpoi, selmaho):
    self.lerpoi = lerpoi
    self.selmaho = selmaho

  def as_json(self):
    return OrderedDict([
      ( "genturtai", self.GENTURTAI ),
      ( "selmaho",   self.selmaho   ),
      ( "lerpoi",    self.lerpoi    )
    ])

class Vlapoi(Gensuha):

  GENTURTAI = "vlapoi"

  def __init__(self, vlapoi):
    self.vlapoi = vlapoi

  def as_json(self):
    return OrderedDict([
      ( "genturtai", self.GENTURTAI ),
      ( "vlapoi",    self.vlapoi    )
    ])

class ZeiLujvo(Vlapoi, Jvodunlei):

  GENTURTAI = "zei-lujvo"

class Lerdunlei: # not a structure
  pass

class BuLetteral(Vlapoi, Lerdunlei):

  GENTURTAI = "bu-letteral"

class Tosmabru(Vlapoi):

  GENTURTAI = "tosmabru"

class Slinkuhi(Vlapoi):

  GENTURTAI = "slinku'i"

