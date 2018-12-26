from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.authentication import LoginRequired
from flaskr.request_handling import ExtractTitleAndBody, IsMethodPOST
from flaskr.helpers import IsNone
from flaskr.sql_queries import GetPosts, SetTitleBodyAndId, UpdateTitleBodyAndId, GetPostById, DeletePostById



blueprint_name = "blog"
module_name = __name__
blueprint = Blueprint(blueprint_name,
                      module_name)



@blueprint.route("/")
def Index():
  template_path = "blog/index.html"
  posts = GetPosts()
  return render_template(template_path, posts=posts)
     
@blueprint.route("/create", methods=("GET", "POST"))
@LoginRequired
def Create():
  if IsMethodPOST():
    title, body = ExtractTitleAndBody()
    id = g.user["id"]
    
    error = CheckCreate(title)

    if IsNone(error):
      SetTitleBodyAndId(title, body, id)
      url = GetEndpointUrl("blog.Index")
      return redirect(url)
    else:
      SendFlashMessage(error)

  template_path = "blog/create.html"
  return render_template(template_path)
    
@blueprint.route("/<int:id>/update", methods=("GET", "POST"))
@LoginRequired
def Update(id):
  if IsMethodPOST():
    title, body = ExtractTitleAndBody()
    
    error = CheckUpdate(title)

    if IsNone(error):
      UpdateTitleBodyAndId(title, body, id)
      url = GetEndpointUrl("blog.Index")
      return redirect(url)
    else:
      SendFlashMessage(error)
  
  post = GetPost(id)
  
  template_path = "blog/update.html"
  return render_template(template_path, post=post)
    
@blueprint.route("/<int:id>/delete", methods=("POST",))
@LoginRequired
def Delete(id):
  GetPost(id)
  DeletePostById(id)
  
  url = GetEndpointUrl("blog.Index")
  return redirect(url)

def GetPost(id, check_author=True):
  post = GetPostById(id)

  if IsNone(post):
    abort(404, "Post id {0} doesn't exist.".format(id))

  if check_author and post["author_id"] != g.user["id"]:
    abort(403)

  return post
  

  
def CheckCreate(title):
  error = None

  if IsNone(title):
    error = "Title is required."
    
  return error
  
def CheckUpdate(title):
  error = None

  if IsNone(title):
    error = "Title is required."
    
  return error
  
  
  
def GetEndpointUrl(endpoint):
  return url_for(endpoint)
  
  
  
def SendFlashMessage(message):
  flash(message)
  
 
