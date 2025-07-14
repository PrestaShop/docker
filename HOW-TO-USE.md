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
usage: prestashop_docker.py [-h] [--debug] [--quiet] [--cache] [subcommand] ...

PrestaShop Docker manager.

positional arguments:
  [subcommand]
    backlog     Update backlog of stable versions of PrestaShop to build from data on Distribution API
    generate    Generate Dockerfile
    tag         Tag managment

options:
  -h, --help    show this help message and exit
  --debug       Use Debug
  --quiet       Use Debug
  --cache       Enable cache
```

### Backlog

Updates the info about stable releases of PrestaShop inside versions.py, based on the contents of Ditribution API.

```bash
./prestashop_docker.py backlog --help
usage: prestashop_docker.py backlog [-h]

optional arguments:
  -h, --help  show this help message and exit
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

To generate the new base files, you need to update the `versions.py` file, add a section with your new version along with the associated PHP versions, then run

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

## Building and running PrestaShop docker locally

First to make sure you will use the local docker containers and not the ones from Docker hub make sure you remove all existing PrestaShop images (including the base images)

```
# This should be empty to be extra sure
$ docker images
```

Then you'll have to build the base image for the PHP version and server you are willing to use. If you are on MacOS this is crucial that you clean any image from cache and tun this locally,
especially if your architecture is based on linux/arm64 (processor M1, M2, ...).

```shell
docker build base/images/8.3-apache -t prestashop/base:8.3-apache
# You should see an image with Repository: prestashop Tag: 8.3-apache
docker images
```

Then you can build the image of the PrestaShop version you want to use:

```
# Now build the PrestaShop version you want based on this local base image
$ docker build images/9.0.x/8.3-apache -t prestashop/prestashop:9.0.x-8.3-apache
```

Finally, you can launch your PrestaShop container using docker compose

```
$ PS_VERSION=9.0.x PHP_VERSION=8.3 docker compose -f images/docker-compose.yml up
```

Or you can use the `build-local-docker.sh` script that performs these actions based on the options

```
# Script options:
#
# -v PRESTA_SHOP_VERSION
# -s SERVER (apache|fpm)
# -p PHP_VERSION (7.1, 8.2, ...)
# -l Launch shop thanks to a docker compose (default false)
#
# Default values are nightly 8.3 apache

$ ./build-local-docker.sh -v 9.0.x -p 8.1 -s fpm
```

Adding the `-l` option will also launch a container build with docker compose so you get an accessible shop locally

```
$ ./build-local-docker.sh -v 9.0.x -p 8.1 -s fpm -l
```

Now you should be able to access a shop at this address: `http://localhost:8001/`
The BO is accessible at `http://localhost:8001/admin-dev` with the following login:
Email: `demo@prestashop.com`
Password: `Correct Horse Battery Staple`
