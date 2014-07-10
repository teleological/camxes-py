#!/usr/bin/env python

import os, sys
import lxml.etree as et
from collections import OrderedDict
import itertools

from parsimonious.exceptions import ParseError

from structures import jbovlaste_types
from structures.gensuha import Lerpoi, Vlapoi
from camxes import configure_platform
from parsers.camxes_ilmen import Parser
from transformers.vlatai import Visitor

def memoize(f):
  memory = {}
  def g(*args):
    if args not in memory:
      memory[args] = f(*args)
    return memory[args]
  return g

with open(os.path.join(os.path.dirname(sys.argv[0]), "jvs/en.xml")) as xml:
  tree = et.parse(xml)

def all_rafsi(word):
  return map(lambda e: e.text, tree.xpath('//valsi[@word="%s"]/rafsi' % word))

def allowed_pair(pair):
  return (not all(map(lambda c: parse_as("consonant", c), pair))) or parse_as("cluster", pair)

def expand_all(visited):
  if isinstance(visited, Vlapoi):
    return map(expand_all, visited.vlapoi)
  elif isinstance(visited, Lerpoi):
    return visited.lerpoi
  else:
    return visited

def parse_as(rule, text):
  try:
    visited = Visitor().visit(Parser(rule).parse(text))
    return expand_all(visited)
  except ParseError as e:
    return False

def main(words):
  rafsi = OrderedDict()
  for i, word in zip(range(len(words)), words):
    print word
    rafsi[word] = all_rafsi(word)
    if parse_as("gismu", word):
      if i == len(words)-1:
        rafsi[word] += [word]
      else:
        rafsi[word] += [word[:-1] + "y"]
    if i == len(words)-1:
      rafsi[word] = filter(lambda r: r[-1] in 'aeiou', rafsi[word])
    else:
      for r in rafsi[word]:
        if parse_as("vowel", r[-1]):
          rafsi[word] += [r + "r", r + "n"]
    if len(rafsi[word]) == 0:
      raise Exception('No terminal rafsi available for %s' % word)
  
  print rafsi

  good_lujvo = []
  for lujvo in itertools.product(*rafsi.values()):
    s = lujvo[0]
    for component in lujvo[1:]:
      if allowed_pair(s[-1] + component[0]):
        s += component
      else:
        s += "y" + component

    print s
    if parse_as("lujvo", s):
      good_lujvo += [s]

  print '\n'
  print "\n".join(good_lujvo)

if __name__ == '__main__':
  configure_platform()
  main(sys.argv[1:])

