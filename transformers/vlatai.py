import re

from parsers import camxes_ilmen
from transformers.camxes_morphology import flatten

from transformers import camxes_morphology, find
from structures.gensuha import BuLetteral, ZeiLujvo, Tosmabru, Slinkuhi, Fuhivla3, Fuhivla35, Fuhivla4

def swallow(fn, ret):
  try:
    return fn()
  except:
    return ret

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

  def default_serializer(self):
    return lambda x : x.as_json()

class Visitor(camxes_morphology.Visitor):

  def visit_vlatai(self, node, visited_children):
    return visited_children[1]

  def visit_tosmabru(self, node, visited_children):
    return Tosmabru(flatten(visited_children))

  def visit_slinkuhi_no_recurse(self, node, visited_children):
    return Slinkuhi(flatten(visited_children))

  def visit_vlatai_bu_clause(self, node, visited_children):
    return BuLetteral(flatten(visited_children))

  def visit_vlatai_zei_clause(self, node, visited_children):
    return ZeiLujvo(flatten(visited_children))

  def visit_fuhivla(self, node, visited_children):
    if len(node.text) >= 5:
      C = r'[bcdfgjklmnprstvxz]'
      V = r'[aeiou]'
      hyphen = r'[^r]r[^r]|[rl]n[^n]|[^n]n[rl]|[rn]l[^l]|[^l]l[rn]'
      
      if len(node.text) >= 6:
        if ((   re.match(C+C+V+C, node.text[:4], re.I)
             or re.match(C+V+C+C, node.text[:4], re.I))
            and re.match(hyphen, node.text[3:6], re.I)):
          return Fuhivla3(flatten(visited_children), node.text[:4], node.text[4], node.text[5:])

        if (    re.match(C+C+V, node.text[:3], re.I)
            and re.match(hyphen, node.text[2:5], re.I)):
          return Fuhivla35(flatten(visited_children), node.text[:3], node.text[3], node.text[4:])

      if (    re.match(C+V+C, node.text[:3], re.I)
          and re.match(hyphen, node.text[2:5], re.I)):
        return Fuhivla3(flatten(visited_children), node.text[:3], node.text[3], node.text[4:])

    return Fuhivla4(flatten(visited_children))

  def visit_vlatai_type3_fuhivla(self, node, visited_children):
    a = find(node, r'(stressed_)?(long|CVC)_rafsi').text
    b = find(node, r'vlatai_fuhivla_hyphen').text
    c = node.text[(len(a)+len(b)):]
    return Fuhivla3(flatten(visited_children), a, b, c)

  def visit_vlatai_type35_fuhivla(self, node, visited_children):
    a = find(node, r'(stressed_)?CCV_rafsi').text
    b = find(node, r'vlatai_fuhivla_hyphen').text
    c = node.text[(len(a)+len(b)):]
    return Fuhivla35(flatten(visited_children), a, b, c)

  def visit_vlatai_type4_fuhivla(self, node, visited_children):
    return Fuhivla4(flatten(visited_children))

