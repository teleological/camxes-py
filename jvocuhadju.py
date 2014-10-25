#!/usr/bin/env python

import os, sys, re
import lxml.etree as et
from collections import OrderedDict, Hashable
import itertools, functools

from optparse import OptionParser
from camxes import VERSION
from parsimonious.exceptions import ParseError

from structures import jbovlaste_types
from structures.gensuha import Lerpoi, Vlapoi
from camxes import configure_platform
from parsers.camxes_ilmen import Parser
from transformers.vlatai import Visitor

# from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
class memoize(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
   def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


# load jbovlaste dump
with open(os.path.join(os.path.dirname(sys.argv[0]), "jvs/en.xml")) as xml:
  tree = et.parse(xml)

# utility functions
@memoize
def all_rafsi(word):
  return map(lambda e: e.text, tree.xpath('//valsi[@word="%s"]/rafsi' % word))

@memoize
def allowed_pair(pair):
  return (not all(map(lambda c: parse_as("consonant", c), pair))) or parse_as("cluster", pair)

def expand_all(visited):
  if isinstance(visited, Vlapoi):
    return map(expand_all, visited.vlapoi)
  elif isinstance(visited, Lerpoi):
    return visited.lerpoi
  else:
    return visited

@memoize
def parse_as(rule, text):
  try:
    visited = Visitor().visit(Parser(rule).parse(text))
    return expand_all(visited)
  except ParseError as e:
    return False

def lujvo_score(lujvo):
    l = len(lujvo)
    a = lujvo.count("'")
    h = lujvo.count("y")
    v = sum(lujvo.count(v) for v in 'aeiou')
    r = 0

    def mapti(r, p):
        p = p.replace('V', '[aeiou]')
        p = p.replace('C', '[bcdfgjklmnprstvxz]')
        p = '^' + p + '$'
        return re.match(p, r) is not None

    for rafsi in Visitor().visit(Parser('lujvo').parse(lujvo)).raw_rafsi:
        if mapti(rafsi, "CVV[rn]"):
            h += 1
            r += 8
        elif mapti(rafsi, "CV'V[rn]"):
            h += 1
            r += 6
        elif mapti(rafsi, 'CVCCV'):   r += 1
        elif mapti(rafsi, 'CVCCy'):    r += 2
        elif mapti(rafsi, 'CCVCV'):   r += 3
        elif mapti(rafsi, 'CCVCy'):    r += 4
        elif mapti(rafsi, 'CVC'):     r += 5
        elif mapti(rafsi, "CV'V"):    r += 6
        elif mapti(rafsi, 'CCV'):     r += 7
        elif mapti(rafsi, 'CVV'):     r += 8

    return (1000 * l) - (500 * a) + (100 * h) - (10 * r) - v

def main(words):
  rafsi = OrderedDict()
  for i, word in zip(range(len(words)), words):
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
  
  good_lujvo = []
  for lujvo in itertools.product(*rafsi.values()):
    s = lujvo[0]
    for component in lujvo[1:]:
      if allowed_pair(s[-1] + component[0]):
        s += component
      else:
        s += "y" + component

    if parse_as("lujvo", s):
      good_lujvo += [s]

  print '\n'
  print "\n".join(map(lambda s: '%s\t%d' % s, sorted(zip(good_lujvo, map(lujvo_score, good_lujvo)), key=lambda x: x[1])))

if __name__ == '__main__':
  usage_fmt = "usage: %prog [ options ] { input }"
  options = OptionParser(usage=usage_fmt, version="%prog " + VERSION)
  (params, argv) = options.parse_args()

  configure_platform()
  main(argv)

