import re

def find_all(node, regex):
  if re.match(regex, node.expr_name) is not None:
    yield node
  else:
    for child in node.children:
      for f in find_all(child, regex):
        yield f

def find(node, regex):
  try:
    return next(find_all(node, regex))
  except:
    return None

