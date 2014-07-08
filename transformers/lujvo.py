from collections import OrderedDict
from parsimonious.nodes import NodeVisitor
from compiler.ast import flatten
import lxml.etree as et
import os, sys

with open(os.path.join(os.path.dirname(sys.argv[0]), "jvs/en.xml")) as xml:
  tree = et.parse(xml)

known = {}
def find(rafsi):
  if rafsi in known:
    return known[rafsi]

  # short rafsi
  results = tree.xpath('//rafsi[text()="%s"]' % rafsi)
  if len(results) > 0:
    r = results[0].getparent().get('word')
    known[rafsi] = r
    return r

  # long rafsi
  for vowel in 'aeiou':
    results = tree.xpath('//valsi[@word="%s%s"]' % (rafsi, vowel))
    if len(results) > 0:
      r = results[0].get('word')
      known[rafsi] = r
      return r
  
  known[rafsi] = rafsi
  return rafsi

class Transformer:

  def transform(self, parsed):
    return Visitor().visit(parsed)

class Visitor(NodeVisitor):

  def generic_visit(self, node, visited_children):
    if node.expr_name and ("rafsi" in node.expr_name or "gismu" in node.expr_name):
      if "rafsi" in node.expr_name:
        if node.text[-1] == "y":
          return find(node.text[:-1])
        else:
          return find(node.text)
      else:
        return node.text
    else:
      return flatten(visited_children)


