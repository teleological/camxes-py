from collections import OrderedDict
from parsimonious.nodes import NodeVisitor
from compiler.ast import flatten
import lxml.etree as et
import os, sys

def memoize(f):
  memory = {}
  def g(*args):
    if args not in memory:
      memory[args] = f(*args)
    return memory[args]
  return g

with open(os.path.join(os.path.dirname(__file__), "../jvs/en.xml")) as xml:
  tree = et.parse(xml)

@memoize
def find(rafsi):
  # short rafsi
  results = tree.xpath('//rafsi[text()="%s"]' % rafsi)
  if len(results) > 0:
    return results[0].getparent().get('word')

  # long rafsi
  for vowel in 'aeiou':
    results = tree.xpath('//valsi[@word="%s%s"]' % (rafsi, vowel))
    if len(results) > 0:
      return results[0].get('word')
  
  return rafsi

class Transformer:

  def __init__(self, expand):
    self.expand = expand

  def transform(self, parsed):
    return Visitor(expand=self.expand).visit(parsed)

class Visitor(NodeVisitor):

  def __init__(self, expand):
    self.expand = expand

  def generic_visit(self, node, visited_children):
    if node.expr_name and ("rafsi" in node.expr_name or "gismu" in node.expr_name):
      if self.expand and "rafsi" in node.expr_name:
        if node.text[-1] == "y":
          return find(node.text[:-1])
        else:
          return find(node.text)
      else:
        return node.text
    else:
      return flatten(visited_children)



