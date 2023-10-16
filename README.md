**Objective:**
===============

What is Magic?
"Magic is a collectible trading card game of fun-filled, strategic games to play with friends old and new. Welcoming worldbuilders, narrative lovers, and gameplay enthusiasts alike, Magic has something for everyone and countless ways to play. Whether you're sitting at the kitchen table, playing online, or battling in a high-stakes competition, there's a place for you in the world of Magic: The Gathering." - [Intro](https://magic.wizards.com/en/intro)


The purpose of the application is to collect data from the endpoints of the [api](https://docs.magicthegathering.io/) which contains card data from the magic game, at the following endpoints:

 - https://api.magicthegathering.io/v1/cards
 - https://api.magicthegathering.io/v1/sets

Using the following structure:
`this folders will be created locally at first run.`
 * Use `data/tlz` json raw data (Temporary Landing Zone).
 * Use `data/raw` Raw Data with schema enforcement in parquet format.
 * Use `data/ref` for data already modeled and/or with business rules applied also in parquet.

This entire structure of code can be used to collect Data from others API, Databases SQL and noSql,
structured and non-structered Data with little effort to adapt to these needs, and also implement Pyspark tuning and better practices for each case.

**Setup:**
===============

**Requirements:**
Linux Distro, or WSL (Windows Subsystem for Linux)
 - docker
 - python=3.9
 - poetry

I recommend using a tool to create python environments (pyenv, miniconda, anaconda).

To install the dependencies.:
```
poetry install
```

If you prefer, you can use the Makefile to run directly in docker.
```
make docker-run
```

If you want, you can just do the build
```
make docker-build
```

If you wanna see all make options open the file or type `make help` in your terminal.

**Running the application**
=============

**Api Requests**

 args
 ```
'--api_task'

'--api_url_task'

'--page_limit'

 ```

Os dados das tasks abaixo serão salvos no diretorio `tlz`.

 * Running to collect cards api:
    ```
    python runner.py --api_task cards --api_url_task https://api.magicthegathering.io/v1/cards --page_limit 5
    ```

 * Running to collect api from sets:
    ```
    python runner.py --api_task sets --api_url_task https://api.magicthegathering.io/v1/sets
    ```

**Running spark process**

args
```
--spark_task'
--config_path'
```

 * cards_raw: Generates the raw data parquet for card data.
    ```
    python runner.py --spark_task cards_raw --config_path configs/raw/cards.json
    ```

 * sets_raw: Generates the raw data parquet for set data.
    ```
    python runner.py --spark_task sets_raw --config_path configs/raw/sets.json
    ```

 * cards_ref: Generates data parquet ref for card data.
    ```
    python runner.py --spark_task cards_ref --config_path configs/ref/cards.json
    ```

 * sets_ref: Generates the data parquet ref for set data.
    ```
    python runner.py --spark_task sets_ref --config_path configs/ref/sets.json
    ```

**Folder structure**
```
.
├── configs
│   ├── raw
│   │   ├── cards.json
│   │   └── sets.json
│   └── ref
│       ├── cards.json
│       └── sets.json
├── data
│   ├── raw
│   │   ├── cards
│   │   └── sets
│   ├── ref
│   │   ├── cards
│   │   └── sets
│   └── tlz
│       ├── cards
│       └── sets
├── definitions.py
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements.txt
├── runner.py
└── source
    ├── api
    │   ├── api_request_object.py
    │   ├── __init__.py
    │   └── save_json_files.py
    ├── __init__.py
    ├── tasks
    │   ├── __init__.py
    │   ├── raw
    │   │   ├── cards_raw.py
    │   │   ├── __init__.py
    │   │   └── sets_raw.py
    │   └── ref
    │       ├── cards_ref.py
    │       ├── __init__.py
    │       └── sets_ref.py
    └── utils
        ├── api_task.py
        ├── config.py
        ├── files_helper.py
        ├── __init__.py
        ├── logging.py
        ├── spark_task.py
        └── task_config.py
```


