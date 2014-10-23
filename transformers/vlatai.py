from compiler.ast import flatten

from transformers import camxes_morphology, find
from structures.gensuha import BuLetteral, ZeiLujvo, Tosmabru, Slinkuhi, Fuhivla3, Fuhivla35, Fuhivla4

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

