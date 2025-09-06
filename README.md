## Tarmez-Web
Web-client for [Tarmez API](https://github.com/x3ron-ai/tarmez-server)


### Quick start with docker

	git clone https://github.com/x3ron-ai/tarmez-server
	git clone https://github.com/x3ron-ai/tarmez-web
	cd tarmez-web
The default ports and env variables are set in `docker-compose.yml`

After editing
```bash
docker compose up
```

### Manual using
	git clone https://github.com/x3ron-ai/tarmez-web
	cd tarmez-web
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt
	cp .env.example .env
Then change `API_URL` and `SECRET_KEY` to yours values in env-file

[API manual installation guide](https://github.com/x3ron-ai/tarmez-server)
#### Run application
	uvicorn app.main:app --host 0.0.0.0 --port 8080