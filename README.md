# 💰 Wallets

[![Deploy](https://github.com/pablo-moreno/wallets/workflows/Docker/badge.svg)](https://github.com/pablo-moreno/wallets/actions/workflows/publish-docker.yml)
[![codecov](https://codecov.io/gh/pablo-moreno/wallets/branch/main/graph/badge.svg?token=67nZVOwX2B)](https://codecov.io/gh/pablo-moreno/wallets)

https://wallets.spookydev.com

## Respuestas prueba técnica

**1.Indica cómo se puede optimizar el rendimiento del servicio de listado de operaciones.**

> El servicio de listado de operaciones más conflictivo es el listado de operaciones de un negocio,
> ya que puede tener potencialmente cientos o miles de operaciones realizadas cada día por, mientras 
> que los clientes puede que hagan una o varias al día (dependiendo, por supuesto, del tipo de cliente). 
> 
> Una vez analizado esto, se tiene que hacer una query específica para este servicio de listado de operaciones 
> de un negocio, con la premisa de que se haga el mínimo número de queries en la base de datos.
> 
> Tendremos que indexar en base de datos los campos sobre los que se podría filtrar, como es el estado de la operación,
> el tipo, y el negocio (o, si hiciera falta, también el cliente) que han realizado la operación.
>
> Además de esto, se tiene que tener en cuenta relaciones de clave foránea a otras tablas e intentar que si las hay se
> haga en una sola query o por lo menos en el mínimo (en `Django` se pueden usar las funciones `select_related` y `prefetch_related`).
>
> Si ninguna de estas opciones optimizara de forma significativa la consulta a nivel de base de datos, se puede pasar 
> a realizar una desnormalización de datos, aunque eso añadiría complejidad al tener que mantenerse la consistencia 
> de datos.
> 
> Otra cuestión a tener en cuenta es la de minimizar la respuesta serializada de datos, pues en cuanto tenemos varios 
> niveles de tablas, Django Rest Framework se vuelve relativamente lento, por lo tanto se tiene que enviar el mínimo
> de información necesaria para el cliente, además de marcar los campos de solo lectura como corresponda, o directamente 
> usar un serializador de solo lectura. Más info sobre esto [aquí](https://hakibenita.com/django-rest-framework-slow)

**2. ¿Qué alternativas planteas en el caso que la base de datos relacional de la aplicación se convierta en un cuello de 
botella por saturación en las operaciones de lectura? ¿Y para las de escritura?**

> **Operaciones de lectura:**
>
> Podemos añadir una herramienta de caché para que ni siquiera llegue a ejecutarse la consulta en la base de datos. 
> En este sentido, tenemos [Varnish](https://varnish-cache.org/) que puede mejorar el tiempo de respuesta hasta 
> 300 veces (según dicen ellos :sweat_smile:). Con esta herramienta añadimos complejidad a la infraestructura pero no 
> al código y hay que tener cuidado con el tiempo que se mantiene el cacheo porque se puede dar información no 
> del todo precisa en todo momento.
>
> Utilizar bases de datos replicadas de solo lectura, de modo que las consultas se realicen en estas y la base de datos
> principal no se vea afectada.
>
> **Operaciones de escritura:**
>
> El punto más crítico de las operaciones de escritura son las transacciones atómicas, por lo tanto es importante utilizar
> correctamente la consulta `SELECT FOR UPDATE SKIP LOCK` de forma que si una fila está bloqueada en un proceso de 
> escritura no impacte en el resto de filas.
> 

**3. Dicen que las bases de datos relacionales no escalan bien, se me ocurre montar el proyecto con alguna NoSQL, 
¿qué me recomiendas?**

> No veo razón para pensar que una base de datos relacional no escala bien. De hecho Postgres, con su campo JSONField, 
> tiene un rendimiento realmente bueno y en algún benchmark supera incluso a MongoDB con un volumen de datos muy alto.
> 
> Para montar este proyecto en NoSQL lo ideal sería MongoDB, pero hay que tener en cuenta la [atomicidad de las operaciones](https://docs.mongodb.com/manual/core/write-operations-atomicity/).
> y estudiar bien la estructura del modelo de datos para que sea consistente.
>
> Si queremos hacerlo en Django, tenemos el proyecto [Djongo](https://www.djongomapper.com/) que prácticamente te da
> la misma interfaz del ORM de Django con soporte para MongoDB.
>
> Otras opciones pueden ser [PyMongo](https://pymongo.readthedocs.io/en/stable/) o [MongoEngine](http://mongoengine.org/).
>

**4.¿Qué tipo de métricas y servicios nos pueden ayudar a comprobar que la API y el servidor funcionan correctamente?**

> - **[Sentry](https://sentry.io)**: Manejo de errores y excepciones en entornos de producción.
>
> - **[Elasticsearch + Logstash + Kibana](https://www.elastic.co/es/what-is/elk-stack)**: Gráficas, logs y estado de la 
> aplicación en general.
>
> - **[Status Page](https://www.atlassian.com/es/software/statuspage)**: Servicio de health checks que además te permite
> enlazarlo con incidencias en Jira.
>

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
