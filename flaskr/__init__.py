from flaskr.FlaskInstance import FlaskInstance
from flaskr.database import CloseDatabase
from flaskr.commands import InitialiseDatabaseCommand
from flaskr import authentication
from flaskr import blog



def application_factory(test_config=None):
  flask_instance = FlaskInstance(test_config)
    
  flask_instance.RegisterTeardownFunction(CloseDatabase)
  flask_instance.RegisterCommand(InitialiseDatabaseCommand)
  
  flask_instance.RegisterBlueprint(authentication.blueprint)
  flask_instance.RegisterBlueprint(blog.blueprint)

  flask_instance.AddUrlRule('/', endpoint='Index')

  return flask_instance.flask



