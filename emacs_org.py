from os import popen
"""this script outputs an emacs-org-table  (simple ascii table with '-' and '|'),
    which is programmatically aggregated.
    This script is meant to be implemented with emacs-src_block."""

table_row = lambda l: f"|{'|'.join(l)}|"   # outputs the table rows -> |x|y|z|
sum_formula = lambda x,y: f":=vsum(@{x}..@{y})" # outputs a formula in a format that emacs-org can understand

emacs_link = lambda t,l,n: f"[[{t}:{l}][{n}]]"
file_link = lambda l,n: emacs_link("file", l, n)
shell_link = lambda l,n: emacs_link("shell", l.split("&")[0] + " &", n)

def org_table(rows, body_itter, line=True):
  """returns a table in emacs org format
  this is usefull to implement in org files as src_block.

  rows :
    a list of dictonaries representing rows,
    e.g. ({"head": "files",
           "body": lambda f: file_link(src + f, f),
           "tail": f"[[file:{src}][{src}]]"}, ... )
          head <optinoal> is the title of the rows
          body must be a function which resolves with the body_itter
          tail <optinoal> is the last row, usefull for sums

  body_itter:
    en itterator which provides arguments to apply the functions in the bodies

  line: weather to put a horizontal line between head and body"""
  heads = table_row(c["head"] for c in rows)
  try:
    tails = table_row(c["tail"] for c in rows)
  except KeyError:
    tails = None
  return "\n".join((heads + "\n|-" if line else "",
                   "\n".join(table_row([r["body"](f) for r in rows]) for f in body_itter),
                   tails if tails else ""))
