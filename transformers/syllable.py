from parsimonious.nodes import NodeVisitor
from compiler.ast import flatten
from transformers import find_all

class Transformer:

  def __init__(self, trim):
    self.trim = trim

  def transform(self, parsed):
    return Visitor(self.trim).visit(parsed)

class Visitor(NodeVisitor):

  def __init__(self, trim):
    self.trim = trim

  def generic_visit(self, node, visited_children):
    if node.expr_name and 'syllable' in node.expr_name:
      if self.trim < 0 and node.end == len(node.full_text):
        return node.text[:self.trim]
      if self.trim > 0 and node.start < self.trim:
        return node.text[self.trim:]
      return node.text
    else:
      return flatten(visited_children)



