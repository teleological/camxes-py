
import re

from compiler.ast import flatten

from parsimonious.nodes import NodeVisitor

from parsimonious_ext.node_types import LITERAL, REGEX

from structures.gensuha \
  import Gensuha, Cmevla, Gismu, Lujvo, Fuhivla, Cmavo, Naljbo

SELMAHO_UNKNOWN = "TOLSLABU"
SELMAHO_Y       = "Y"

# flatten and join textual nodes
def lerpoi(children):
  return "".join(flatten(map(str, children)))

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

  def default_serializer(self):
    return lambda x : x.as_json()

class Visitor(NodeVisitor):

  def visit_space_char(self, node, visited_children):
    return []

  def visit_EOF(self, node, visited_children):
    return []

  def visit_CMEVLA(self, node, visited_children):
    return Cmevla(lerpoi(visited_children))

  def visit_BRIVLA(self, node, visited_children):
    return flatten(visited_children)

  def visit_gismu_2(self, node, visited_children):
    return Gismu(lerpoi(visited_children))

  def visit_lujvo(self, node, visited_children):
    return Lujvo(lerpoi(visited_children))

  def visit_fuhivla(self, node, visited_children):
    return Fuhivla(lerpoi(visited_children))

  # handle by selmaho in generic_visit()
  def visit_CMAVO(self, node, visited_children):
    return flatten(visited_children)

  def visit_BY(self, node, visited_children):
    children = flatten(visited_children)
    if isinstance(children[0], Gensuha):
      value = children # ybu = Y + BU
    else:
      value = Cmavo("".join(children), node.expr_name)
    return value

  def visit_zoi_word(self, node, visited_children):
    return Naljbo(lerpoi(visited_children))

  def visit_non_lojban_word(self, node, visited_children):
    return Naljbo(lerpoi(visited_children))

  def visit_cmavo(self, node, visited_children):
    text = lerpoi(visited_children)
    if re.match(r"[yY]+$", text):
      selmaho = SELMAHO_Y
    else:
      selmaho = SELMAHO_UNKNOWN
    return Cmavo(text, selmaho)

  def generic_visit(self, node, visited_children):

    # CMAVO by selmaho
    if node.expr_name and re.match(r"[A-Z]+(h[AEIOU])?$", node.expr_name):
      value = Cmavo(lerpoi(visited_children), node.expr_name)

    elif node.node_type == LITERAL:
      value = node.text

    elif node.node_type == REGEX:
      value = node.text

    else:
      value = flatten(visited_children)

    return value

