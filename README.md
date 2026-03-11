# iyp-downloader
Query IYP and save results to a file.

## Installation
Install all dependencies using the `uv` command:
```
uv sync
```

## Usage
First you should create a configuration file, that provide the url to IYP (and
credentials if needed), the query to execute, and the name of the file to save
the results. See examples in the `configs/` folder.

Then run the query with the following command (replace the last argument with
the name of your configuration file):
```bash
uv run download.py configs/as_name_country_rir.yaml
```

