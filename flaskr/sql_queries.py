from flaskr.database import ExecuteSelect, ExecuteNonSelect
from flaskr.password_handling import HashPassword, IsPasswordHashesEqual




def GetUserByName(username):
  query = ("""SELECT * FROM user WHERE username = ?""")
  parameters = (username,)
  result = ExecuteSelect(query, parameters)
  
  return result

def GetUserById(id):
  query = ("""SELECT * FROM user WHERE id = ?""")
  parameters = (id,)
  result = ExecuteSelect(query, parameters)
  
  return result
  
def SetUsernameAndPassword(username, password):
  query = ("""INSERT INTO user (username, password)
                VALUES (?, ?)""")
  hash = HashPassword(password)
  parameters = (username, hash)
  ExecuteNonSelect(query, parameters)
  
  
  
def GetPosts():
  query = ("""SELECT p.id, title, body, created, author_id, username
                FROM post p JOIN user u ON p.author_id = u.id
                ORDER BY created DESC""")
  parameters = ()
  posts = ExecuteSelect(query, parameters, fetch="all")
  return posts

def GetPostById(id):
  query = ("""SELECT p.id, title, body, created, author_id, username
                FROM post p JOIN user u ON p.author_id = u.id
                WHERE p.id = ?""")
  parameters = (id,)
  post = ExecuteSelect(query, parameters)
  return post
  
def SetTitleBodyAndId(title, body, id):
  query = ("""INSERT INTO post (title, body, author_id)
                VALUES (?, ?, ?)""")
  parameters = (title, body, id)
  ExecuteNonSelect(query, parameters)
  
def UpdateTitleBodyAndId(title, body, id):
  query = ("""UPDATE post SET title = ?, body = ?
                WHERE id = ?""")
  parameters = (title, body, id)
  ExecuteNonSelect(query, parameters)
  
def DeletePostById(id):
  query = ("""DELETE FROM post WHERE id = ?""")
  parameters = (id,)
  ExecuteNonSelect(query, parameters)