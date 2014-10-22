#!/usr/bin/env python

from parsimonious.exceptions import ParseError

from structures import jbovlaste_types
from camxes import configure_platform
from parsers.camxes_ilmen import Parser
from transformers.vlatai import Visitor

VLATAI_RULE = "vlatai"

def main(text):
  for word in text:
    gensuha = analyze_morphology(word)
    print '%s:' % word, jbovlaste_types.classify(gensuha)

def analyze_morphology(text):
  parser = Parser(VLATAI_RULE)
  visitor = Visitor()
  gensuha = None
  try:
    parsed = parser.parse(text)
    gensuha = visitor.visit(parsed)
  except ParseError as e:
    pass
  return gensuha

if __name__ == '__main__':
  import sys
  import itertools
  text = itertools.chain(*map(lambda s: s.split(' '), sys.argv[1:]))
  configure_platform()
  main(text)

