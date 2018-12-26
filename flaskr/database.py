import sqlite3
from flask import current_app, g

from flaskr.g_proxy import PopG, IsInG
from flaskr.helpers import IsNone



def GetDatabase():
  if IsInG("database"):
    return g.database
  else:
    CreateDatabase()
    return g.database

def CreateDatabase():
  database_path = current_app.config["DATABASE"]
  detection = sqlite3.PARSE_DECLTYPES
  
  tuple_result_format = sqlite3.Row
  
  g.database = sqlite3.connect(database_path,
                               detect_types=detection)
  g.database.row_factory = tuple_result_format
  
  

def ExecuteSelect(query, parameters, fetch="one"):
  if fetch not in ("one", "all"):
    fetch = "one"
    
  database = GetDatabase()
  cursor = database.execute(query, parameters)
  
  if (fetch == "one"):
    return cursor.fetchone()
  if (fetch == "all"):
    return cursor.fetchall()
  
def ExecuteNonSelect(query, parameters):
  database = GetDatabase()
  
  database.execute(query, parameters)
  database.commit()



def CloseDatabase(e=None):
  database = PopG("database")

  if (not IsNone(database)):
    database.close()