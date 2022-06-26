# wells-fargo

## Overview

This is your new Kedro project, which was generated using `Kedro 0.18.1`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.

## Create a Virtual Environment
```
python -m venv .venv
.\.venv\scripts\activate
```
## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
pip install -r src/requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### Configuration
All configuration for running the pipeline is parsed from:
```
conf/base/catalog.yml
conf/base/parameters/data_processing.yml
```

### Credentials
* These files are present in conf/local.
* As from the name, these are local to a project and are not pushed to git.
* But we made changes to .gitignore for pushing these files too for safe running of the pipeline.
* Below file stores all the credentials required for pipeline.
```
conf/local/credentials.yml
```

