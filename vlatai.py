#!/usr/bin/env python

from parsimonious.exceptions import ParseError

from structures import jbovlaste_types
from camxes import configure_platform
from parsers.camxes_ilmen import Parser
from transformers.vlatai import Visitor

VLATAI_RULE = "vlatai"

def main(text, simple):
  parser = Parser(VLATAI_RULE)
  visitor = Visitor()
  for word in text:
    gensuha = analyze_morphology(parser, visitor, word)
    velski = jbovlaste_types.classify(gensuha, simple)
    if simple:
      print velski
    else:
      print '%s:' % word, velski

def analyze_morphology(parser, visitor, text):
  gensuha = None
  try:
    parsed = parser.parse(text)
    gensuha = visitor.visit(parsed)
  except ParseError as e:
    pass
  return gensuha

if __name__ == '__main__':
  from optparse import OptionParser
  from camxes import VERSION
  usage_fmt = "usage: %prog [ options ] { input }"
  options = OptionParser(usage=usage_fmt, version="%prog " + VERSION)
  options.add_option("-s", "--simple",
                     help="enable simple output (for jbovlaste)",
                     action="store_true",
                     dest="simple")
  (params, argv) = options.parse_args()

  configure_platform()
  main(argv, params.simple)

