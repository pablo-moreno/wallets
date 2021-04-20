# 💰 Wallets

[![Deploy](https://github.com/pablo-moreno/wallets/workflows/Docker/badge.svg)](https://github.com/pablo-moreno/wallets/actions/workflows/publish-docker.yml)
[![codecov](https://codecov.io/gh/pablo-moreno/wallets/branch/main/graph/badge.svg?token=67nZVOwX2B)](https://codecov.io/gh/pablo-moreno/wallets)

https://wallets.spookydev.com

## 📖 Documentation

[![Netlify Status](https://api.netlify.com/api/v1/badges/3d2a724f-1ac3-40a6-b904-ab25919fba24/deploy-status)](https://app.netlify.com/sites/wallets-docs/deploys)

Full API documentation is hosted in [Netlify](https://wallets-docs.netlify.app)

## 🖥️ Development

> The environment is ready to develop within an Docker Compose environment

First of all, build everything
```bash
docker-compose build
```

Then you can run the docker compose file

```bash
docker-compose up
```

**Useful commands**

> Run tests with coverage
```bash
docker-compose -f docker-compose.test.yml run wallets pytest --cov
```

> Create migrations
```bash
docker-compose -f docker-compose.test.yml run wallets python manage.py makemigrations
```

> Run migrations
```bash
docker-compose -f docker-compose.test.yml run wallets python manage.py migrate
```

> Collect static files
```bash
docker-compose -f docker-compose.test.yml run wallets python manage.py collectstatic --noinput
```

## 🚀 Deployment

Wallets is deployed automatically with Github Actions, in a 🐳 Docker Swarm environment

To setup the deployment enviroment, you need to copy the `docker-compose.stack.yml` and the `nginx` directory with this structure:

```bash
docker-compose.yml
nginx/
├── default.conf
├── general.conf
└── proxy.conf
```

Then you need to setup the environment variables:

**🌵 Environment variables**

```bash
DATABASE_URL: postgres://admin:development@postgres:5432/wallets
SENTRY_DSN: "sentry dsn"
DJANGO_SETTINGS_MODULE: "config.settings.production"
SECRET_KEY: "secret key"
```

**Deploy stack**

To deploy the stack, you have to run:

```bash
docker stack deploy -c docker-compose.yml wallets
```

**CI/CD Github Settings**

You need to set this Github Secrets in `Settings / Secrets`

```bash
CODECOV_TOKEN: Code coverage token
HOST: Remote server ssh IP address
KEY: Private key
PORT: SSH Port
USERNAME: SSH Username
```
