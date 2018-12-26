import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from flaskr.request_handling import ExtractUsernameAndPassword, IsMethodPOST
from flaskr.helpers import IsNone
from flaskr.session_proxy import ClearSession, SetKeyValueInSession, GetValueForKeyInSession
from flaskr.password_handling import HashPassword, IsPasswordHashesEqual
from flaskr.sql_queries import SetUsernameAndPassword, GetUserByName, GetUserById



blueprint_name = "authentication"
module_name = __name__
request_url_prefix = "/authentication"
blueprint = Blueprint(blueprint_name,
                      module_name,
                      url_prefix=request_url_prefix)
  
  
  
@blueprint.before_app_request
def LogInLoggedInUser():
  user_id = GetValueForKeyInSession("user_id")

  if IsNone(user_id):
    g.user = None
  else:
    g.user = GetUserById(user_id)
  
  
  
@blueprint.route("/register", methods=("GET", "POST"))
def Register():
  if IsMethodPOST():
    username, password = ExtractUsernameAndPassword()
    
    error = CheckRegister(username, password)
    
    if IsNone(error):
      SetUsernameAndPassword(username, password)
      url = GetEndpointUrl("authentication.Login")
      return redirect(url)

    SendFlashMessage(error)

  template_path = "authentication/register.html"
  return render_template(template_path)

@blueprint.route("/login", methods=("GET", "POST"))
def Login():
  if IsMethodPOST():
    username, password = ExtractUsernameAndPassword()
    
    user = GetUserByName(username)
    
    error = CheckLogin(user, password)

    if IsNone(error):
      ClearSession()
      SetKeyValueInSession("user_id", user["id"])
      url = GetEndpointUrl("Index")
      return redirect(url)

    SendFlashMessage(error)

  template_path = "authentication/login.html"
  return render_template(template_path)

@blueprint.route("/logout")
def Logout():
  ClearSession()
  url = GetEndpointUrl("Index")
  return redirect(url)



def LoginRequired(view):
  @functools.wraps(view)
  def WrappedView(**kwargs):
    if g.user is None:
      url = GetEndpointUrl("authentication.Login")
      return redirect(url)

    return view(**kwargs)

  return WrappedView



def CheckRegister(username, password):
  error = None
  
  if IsNone(username):
    error = "Username is required."
  elif IsNone(password):
    error = "Password is required."
  else:
    user = GetUserByName(username)
    if (not IsNone(user)):
      error = "User {} is already registered.".format(username)
      
  return error

def CheckLogin(user, password):
  error = None
  
  if IsNone(user):
    error = "Incorrect username."
  elif (not IsPasswordHashesEqual(user["password"], password)):
    error = "Incorrect password."
    
  return error
  

  
def GetEndpointUrl(endpoint):
  return url_for(endpoint)
  
  
  
def SendFlashMessage(message):
  flash(message)
  
  
