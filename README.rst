## Flask Tutorial

### Run Application

Linux and Mac:  
```
export FLASK_APP=flaskr:application_factory
export FLASK_ENV=development
```

Windows PowerShell:  
```
$env:FLASK_APP = "flaskr:application_factory"
$env:FLASK_ENV = "development"
```

```
flask run

Open: http://127.0.0.1:5000/hello
```