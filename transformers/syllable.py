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

  def visit_fuhivla(self, node, visited_children):
    return self.finish(visited_children)
  def visit_jbocme(self, node, visited_children):
    return self.finish(visited_children)

  def finish(self, visited_children):
    return '-'.join(filter(lambda x: len(x) > 0, flatten(visited_children)))

  def generic_visit(self, node, visited_children):
    if node.expr_name and 'syllable' in node.expr_name:
      if node.expr_name.startswith('stressed') or any(map(lambda c: c in node.text, 'AEIOU')):
        text = node.text.upper()
      else:
        text = node.text

      if self.trim < 0 and node.end == len(node.full_text):
        return text[:self.trim]
      if self.trim > 0 and node.start < self.trim:
        return text[(self.trim-node.start):]
      return text

    else:
      return flatten(visited_children)



