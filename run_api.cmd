docker build -t proxies_api .
docker kill proxies_api
docker run -d --rm -v C:\Users\Administrator\Desktop\proxies_api:/myapp --env-file .env --name proxies_api -p 8182:8182 proxies_api
