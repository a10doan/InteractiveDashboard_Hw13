Unit 15 | Assignment - Interactive Dashboard

Skills tested: JavaScript, DOM Manipulation, D3.js/Plotly.js, Flask, SQLalchemy, Bootstrap, Pandas (DataFrames), Heroku deployment

This exercise incorporates SQLalchemy to create a connection to a SQLite database in order to query and filter data.  The data is then stored into JSON objects where it can be organized and routed depending on the user input.  There was a portion of the Flask app where Panda was used to manipulate a CSV file for names/ids.  An HTML file with a connection to the d3 library is then used to manipulate the DOM, and take in the user input from a dropdown menu.  The dropdown event then calls a function where it pulls the json object via Flask routing.  The information from the JSON object is then, Plotly is used to present the charts and info depending on user input.  After all said and done, final version is uploaded to Heroku for deployment.  So that the entire online world will see the dashboard.  This requires modifying the requirements.txt and creating a Procfile, of which instructs Heroku on the modules needed to run the flask app.  Minor changes had to be made to the html file, as heroku will not read local host urls (ie. localhost:5000).  The command line "heroku logs" help in debugging errors in the upload.  Also when using "git commit -a -m "..."" and "git push heroku master", any changes in 'requirements.txt' it will require substantial install time, note of advice, keep the requirements list small (heroku only allows 600mb max), and delete/add any error that pops up.

Heroku Deployment Page:  https://interactivedashboard.herokuapp.com/










______________________________________________________________________________________________________________

