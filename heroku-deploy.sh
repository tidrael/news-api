heroku container:login
heroku container:push web --app vnnews-api
heroku container:release web --app vnnews-api
heroku container:release web --app vnnews-api