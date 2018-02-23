PARENS = {
  "(": ")",
  "{": "}",
  "[": "]"
}
 
def check_parens(text, i=0, p=None):
  while i < len(text):
    c = text[i]
    if c == p:
      return True, i + 1
    elif c in PARENS.values():
      return False, i
    elif c in PARENS.keys():
      b, i = check_parens(text, i + 1, PARENS[c])
      if not b:
        return False, i
    else:
      i += 1
  return p == None, len(text)

print(check_parens("({}b[(c)]d{})"))
