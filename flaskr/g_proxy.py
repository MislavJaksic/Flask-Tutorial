from flask import g



def PopG(field):
  return g.pop(field, None)
    
def IsInG(field):
  if (field in g):
    return True
  return False