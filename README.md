# YouTube Downloader
Youtube video downloader service based on VueJS and Python 3.7 Aiohttp stack.

## Requirements

Note: Full packages requirements can be found in **requirements.txt** and **package.json** for **backend** and **frontend** respectively.

### Backend
- python3.7
- aiohttp
- pytube
### Frontend
- VueJS
- vuex
- vue-router
- axios
- vuetify

`Note` Frontend part is basically a PWA project. It uses Android's **Share To** feature to simply copy links from Youtube app for example. It utilizes **Share Target API** (`share_target` manifest key) which was introduced in Chrome 71. This feature requires server to be hosted using SSL.

## Installing

### Frontend
#### development
```
npm run serve
```
This will run server on open port starting from 8080 for development with hot reload enabled. 

#### production
```
npm run build
```
This will generate `dist/` folder with production build. You need to deploy this folder on the server.
Server should be configured correctly to support **history mode**

Next step relates to Nginx configuration.

```
server {
    #... server configuration, ssl and etc

    location / {
            root /path/to/frontend/;
            index index.html index.htm;
            include /etc/nginx/mime.types;
            default_type application/octet-stream;

            try_files $uri $uri/ /index.html; # this is for history mode
    }
}
```


### Backend

#### Development

1. Firstly you need to install Python 3.7.
2. Create virtualenv: `python3.7 -m venv venv`
3. And activate it: `source venv/bin/activate`
4. Run `pip3.7 install -r requirements.txt` to install project dependencies in the current virtual environment.
    1. `Note` Since there's a bug with pytube module you need to manually edit `pytube/mixin.py` file in your venv folder. [GitHub PyTube Issue 402 for it.](https://github.com/nficano/pytube/issues/402#issuecomment-501382533)
5. Run `python3.7 -m backend` with optional parameters `--port=<port>` and `--host=<host>` to start backend server. Default port is `8089`
