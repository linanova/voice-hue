# voice-hue


## Development

### Requirements
- Docker
- awscli
- pre-commit
- Raspberry Pi with NeoPixel LEDs

### Setup
To configure environment variables, copy the `.env.local` file to `.env` and fill in the necessary values.

To run the API and dashboard:
```
docker compose --profile local up --build
```

To run the client on a Raspberry Pi:
```
docker compose --profile rpi up --build
```

LocalStack is used to mock out AWS services (DynamoDB) for local development of the API. After starting up the docker containers, run the following script to initialize necessary data in LocalStack.

```
scripts/init-localstack.sh
```

To install (using brew) and configure pre-commit for linting and formatting hooks:
```
brew install pre-commit
pre-commit install
```