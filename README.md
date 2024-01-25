# DF_FILTER
This is a dataframe filter with conditions in json format. The project uses flask to build APIs and also a simple web page to download filtered data to a csv file.

## Deploy
Clone this REPO and go to df_filter dir.  Run the following docker command to build image and run container.
```
cd df_filter
docker build -t df_filter .
docker run -p 5000:5000 -v .:/code df_filter
```

## APIs
### /login
After sending username and password via post request, a JWT Token will return when user's credential is correct.
This is a sample curl command calling this API.
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' http://0.0.0.0:5000/login
```

### /query_api
With token generated from /login API, backend dataFrame will be filtered according to conditions within json format. And filtered result is returned in json format.
This is a sample curl command calling this API.
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: [jwt token]" -d '{ "date": {"late": "2020-01-01","before": "2020-01-31"}, "numerical_0": {"greater equal": 0.01,"less equal": 0.1}, "numerical_1": {"greater equal": 0.2,"less equal": 0.7}, "categorical_0": ["1"]}' http://127.0.0.1:5000/query_api
```

## web page to download csv file
Open the following url in broswer: http://localhost:5000/. Populate JWT Token and filter conditions in json format. It should generate a csv file after click on 'Submit & Export' button.
