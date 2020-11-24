# How to use

The PrestaShop Docker tool aims to easily configure, build and tag PrestaShop Docker images.
It requires Python 3.6+.

## Installation

```bash
$ pip install -r requirements.txt
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
