import click
from flask.cli import with_appcontext
from flask import current_app

from flaskr.database import GetDatabase



@click.command("initialise-database")
@with_appcontext
def InitialiseDatabaseCommand():
  InitialiseDatabase()
  click.echo("Initialized the database.")
  
def InitialiseDatabase():
  database = GetDatabase()

  sql_file = "schema.sql"
  with current_app.open_resource(sql_file) as file:
    script = file.read().decode("utf8")
    database.executescript(script)

