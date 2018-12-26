from flask import request



def ExtractUsernameAndPassword():
  return request.form["username"], request.form["password"]
  
def ExtractTitleAndBody():
  return request.form["title"], request.form["body"]

def IsMethodPOST():
  if (request.method == "POST"):
    return True
  return False