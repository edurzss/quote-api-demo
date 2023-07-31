# Quotes API
Bookairfreight's takehome assignment

## Install and run

To run the services using docker compose:

```bash
$ docker-compose up --build -d
```

Docker compose 3.5+ is required (Docker engine 17.12.0+).

The API endpoint will be available at your **localhost port 80**.

## Loading shipping rates data
Get inside the quotes API container by running in your terminal:

```bash
$ docker exec -it quote_api bash
```
Then execute the script `load_rates.py` inside the `scripts` folder:

```bash
$ python scripts/load_rates.py
```

Note: The rates file must be in JSON format and the name `rates.json` in the `/src` folder of the container (`/quote-api` folder in host).

## Integrations Tests (optional)
You must have the full app running.

Again, get inside the quotes API container, if not already, by running in your terminal:

```bash
$ docker exec -it quote_api bash
```

Then, to start the tests, run:

```bash
$ pytest -v tests
```

## API Docs
You can view API's web documentation through the route `/v1/docs`

## Technologies used
* Web framework: Flask
* REST API framework: Flask Smorest
    * Marshmallow
    * Apispec (OpenAPI)
* Database: PostgreSQL
* Database toolkit: SQLAlchemy
* Testing: pytest
* Production WSGI: Gunicorn