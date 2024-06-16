# Install

- You can observe the execution status based on the `Log.log` file generated in the same folder.

## Run locally

- Create a file named '.env' within the project directory with the following contents:
- If LOGGING_LEVEL is not specified, it will neither write to FILE nor print anything. You have five options available. Usually, INFO is sufficient. The PRINT option also has the `INFO` logging level.
    - "DEBUG"
    - "INFO"
    - "WARNING"
    - "ERROR"
    - "CRITICAL"
    - "PRINT"
- Setting `FIRST_CRAWL` to `True` will initialize the database and import data from the past six months. If not set, the crawler will only scrape data from the last two days on a daily basis.
- Here, the DB is using MySQL.

```
LOGGING_LEVEL = "INFO"
FIRST_CRAWL = "True"
DATABASE_URL = "mysql://{User}:{passwd}@127.0.0.1/{DB_SCHEMA}"
```
