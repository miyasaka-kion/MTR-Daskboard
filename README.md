**Before you run the code, you need to make sure mongoDB is accessible via mongodb://localhost:27017/.**

We assume you have activated a virtual env.

```sh
conda install flask requests pymongo apscheduler
```

```sh
python app.py
```

Then view the web on 127.0.0.1:5000

Already Done: 

-   Interaction framework with the db;
-   Render Basic elements on web;
-   Automatically fetch data from API every 30s;
-   Pass the past 10 stations time info to the front end;



TODO:

-   Do some visualizations.