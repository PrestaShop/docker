# How to use

The PrestaShop Docker tool aims to easily configure, build and tag PrestaShop Docker images.
It requires Python 3.6+.

## Installation

```bash
$ pip install -r requirements.txt --break-system-packages
```

## Usage

Display the help:

```bash
$ ./prestashop_docker.py --help
usage: prestashop_docker.py [-h] [--debug] [--cache] [subcommand] ...

PrestaShop Docker manager.

positional arguments:
  [subcommand]
    tag         Tag managment
    generate    Generate Dockerfile

optional arguments:
  -h, --help    show this help message and exit
  --debug       Use Debug
  --cache    Enable cache
```

### Generate

It allows you to generate Dockerfile files related on what you defined in `versions.py` file.

```bash
$ ./prestashop_docker.py generate --help
usage: prestashop_docker.py generate [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### Tag

It builds docker images on local et allows you to push them on DockerHub.

```bash
$ ./prestashop_docker.py tag --help
usage: prestashop_docker.py tag [-h] {exists,build,push,aliases} ...

positional arguments:
  {exists,build,push,aliases}
    exists              Check if tag exists on Docker Hub
    build               Build container and create docker tag
    push                Push docker tags
    aliases             Get aliases

optional arguments:
  -h, --help            show this help message and exit
```

## Using docker compose

To generate the new base files, you need to update the `versions.py` file, add a section ith your new version along with the associated PHP versions, then run

```php
docker compose up generate
```

This will create new folders for the new version you just added.

## Running tests locally

To run the python tests you need to install requirements

```bash
$ pip install -r requirements.txt
```

Then you can run the tests:

```bash
$ nosetests
```

Locally you may have an error like ``, running these commands may help running tests locally:

```bash
$ pip uninstall -y nose
$ pip install -U nose --no-binary :all:
```

or alternatively:

```bash
$ pip install nose-py3
```

If you need to debug one specific test you first need to run

```
$ nosetests --with-id
```

This will execute tests and each test method will be assigned an ID that you can then use to filter it specifically:

```
$ nosetests --with-id 7
```

This will also generate a `.nodeids` binary file, when you add new test methods you need to remove this file to re-generate the list of IDs.
