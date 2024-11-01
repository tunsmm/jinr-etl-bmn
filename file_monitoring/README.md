# Airflow File Monitoring

Automating the Copying of Experimental Files to 'Cold' Storage.

## Contents

- [docker-compose.yml](docker-compose.yml) — An example of Airflow cluster with Celery executor. Contains:
  - Apache Airflow
  - PostgreSQL (Airflow metadata)
  - Redis (Task broker)
  - Celery workers
  - Flower (Celery monitoring)
- [dags/](app/dags) — Sample DAGs and common libraries.


## Start and stop

The easiest way is just run these two commands, but read all docs to get sure that you will reach the proper behaviour of system
```bash
docker compose up airflow-init
docker compose --profile flower up -d
```

To configure all Airflow components use:

```bash
docker compose up airflow-init
```

To break down containers press `Ctrl+C` or `Command+C` and the following command:

```bash
docker-compose down
```

After initialization is complete, you should see a message like this:

```bash
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.9.1
start_airflow-init_1 exited with code 0
```

The account created has the login **airflow** and the password **airflow**, but you can change it in .yaml file.

The docker-compose environment we have prepared is a “quick-start” one. It was not designed to be used in production and it has a number of caveats - one of them being that the best way to recover from any problem is to clean it up and restart from scratch.

The best way to do this is to:

Run docker compose down --volumes --remove-orphans command in the directory you downloaded the docker-compose.yaml file

Remove the entire directory where you downloaded the docker-compose.yaml file rm -rf '<DIRECTORY>'

Run through this guide from the very beginning, starting by re-downloading the docker-compose.yaml file

Now you can start all services:

- default way (this will block your current console application for showing all logs)
```bash
docker compose up
```

- background all containers (you can use this to not block your conlose application)
```bash
docker compose up -d
```

- enable profile Flower for Celery (**prefer way**)
```bash
docker compose --profile flower up -d
```

Then you can stop it if you need:

```bash
docker stop $(docker ps -a -q)
```

And remove all containers:

```bash
docker rm $(docker ps -a -q)
```


## Usage

Containers exposes a couple of WebUI's:

- Airflow Webserver: [127.0.0.1:8080](http://127.0.0.1:8080/)
- Flower: [127.0.0.1:5555](http://127.0.0.1:5555/)
