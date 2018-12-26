from flask import session



def ClearSession():
  session.clear()
  
def SetKeyValueInSession(key, value):
  session[key] = value

def GetValueForKeyInSession(key):
  return session.get(key)