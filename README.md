This is a project to develop ETL system for JINR's experiment BM@N. There we develop automated system for distributed processing of BM@N experiment data based on the task chain scheduling service.

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


## Project structure

The overall structure of the project looks like this:
```
├── README.md
├── app
│   ├── dags
│   │   ├── config
│   │   │   ├── .env
│   │   │   └── settings.py
│   │   ├── dags.py
│   │   └── monitoring.py
│   ├── logs*
│   │   ├── dag_processor_manager
│   │   │   └── dag_processor_manager.log
│   │   └── scheduler
│   │       ├── 2024-10-25
│   │       └── latest -> 2024-10-25
│   └── requirements.txt
├── dir_with_copied_files*
├── dir_to_monitor*
├── docker-compose.yml
└── monitoring.log
```

Files and directories marked with an asterisk may not exist before deploying docker images.

.env file must be created independently in the root directory. The database must have the same access rights.

monitoring.log – a file responsible for all logs that were added independently as part of the system's development

Log files from open-source Airflow components are stored in the app/logs/ directory:
- the dag_processor_manager directory stores information about the regular analysis of the app/dags directory for new DAGs, 
- the scheduler directory stores information about the scheduled launch of found DAGs.

## Start and stop

The easiest way is just run these two commands, but read all docs to get sure that you will reach the proper behaviour of system
```bash
docker compose up airflow-init
docker compose --profile flower up -d
```

But if you want to run with some specific way, you can execute these commands:

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

Then you can stop it if you need stop and remove all containers:

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```


## Usage

Containers exposes a couple of WebUI's:

- Airflow Webserver: [127.0.0.1:8080](http://127.0.0.1:8080/)
- Flower: [127.0.0.1:5555](http://127.0.0.1:5555/)

## Contacts
- [Nikita Ilin](t.me/tunsmm)
