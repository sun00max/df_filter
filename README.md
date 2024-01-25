# DF_FILTER
This is a dataframe filter with json as input. The project uses flask to build API and a simple web page to download filtered result.

## Deploy
Run the following docker command to build image and run container.
docker build -t df_filter .
docker run -p 5000:5000 -v .:/code df_filter

## APIs
### /login
After sending username and password via post request, a jwt token will be returned when user's credential is correct.
This is a sample curl command calling this API.
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "password123"}' http://0.0.0.0:5000/login

### /query_api
With token generated from /login API, backend dataFrame data will be filtered according to conditions in json format. And filtered result is returned in json format.
This is a sample curl command calling this API.
curl -X POST -H "Content-Type: application/json" -H "Authorization: [jwt token]" -d '{ "date": {"late": "2020-01-01","before": "2020-01-31"}, "numerical_0": {"greater equal": 0.01,"less equal": 0.1}, "numerical_1": {"greater equal": 0.2,"less equal": 0.7}, "categorical_0": ["1"]}' http://127.0.0.1:5000/query_api

## web page to download csv file
Open the following url in broswer http://localhost:5000/. Populate jwt token and filter conditions in json format. A csv file will be downloaded after click on 'Submit & Export' button.



eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoidGVzdHVzZXIiLCJleHAiOjE3MDYxNzg0NTB9.UbWr7nzTA69Gye7MLVrxV22sMZ46Y3pLMcuONiTsnSUNDhJ7Pn5oXSTCotbeOYs5oPoekf6a84duRyaCrmMs-Y8X8tI17EINxabmsrdFm5ceYUd-5dNvP9VW22wX9ea-OS9lOBQgQPP45L8wbR_jYdv9_aIkHHxLTLeteZio_dLOcVYzBa-GiFBu95dw_Rdvy6cg7s-_Gv0nt02cCF8UUxYQwMKEnHUgeLu8BnfUoaw0WMpMfIgCDF7R6oaIi2mMuC6Wp1qZgpiSRi22K0JenfnC4coc2AGwVOn9a5vJ8kjVhkiM94HJD_BRcwpS-mfi0KCDdbkiSK2ZZnpRn4cmOA