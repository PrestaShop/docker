# PrestaShop on Docker

![Tests](https://github.com/PrestaShop/docker/workflows/Run%20tests/badge.svg)
![Codestyle](https://github.com/PrestaShop/docker/workflows/Run%20Flake8/badge.svg)

## Supported tags

### Images by PrestaShop version
* `8`, `latest`, `8-apache`
* `8-fpm`
* `nightly` (Latest but unstable release from git)

You can use tags for this. For example:
```
$ docker run -ti --name my-docker-name -e PS_DEV_MODE=false -e PS_INSTALL_AUTO=0 -p 8080:80 -d prestashop/prestashop:8.0
```

## What is PrestaShop

PrestaShop is a free and open-source e-commerce web application, committed to providing the best shopping cart experience for both merchants and customers. It is written in PHP, is highly customizable, supports all the major payment services, is translated in many languages and localized for many countries, has a fully responsive design (both front and back office), etc. See all the available features.

> [www.prestashop-project.org](https://www.prestashop-project.org/)

![PrestaShop's back office dashboard](https://user-images.githubusercontent.com/1009343/61462749-8fb19f00-a949-11e9-801f-70ab0a84192d.png "PrestaShop's back office dashboard")

## How to run these images

These images are running with the latest version in the [official PHP repository](https://registry.hub.docker.com/_/php/).
For the database, you can use and link any SQL server related to MySQL. 

Currently if you do not have any MySQL server, the most simple way to run this container is:

```bash
# create a network for containers to communicate
$ docker network create prestashop-net
# launch mysql 5.7 container
$ docker run -ti --name some-mysql --network prestashop-net -e MYSQL_ROOT_PASSWORD=admin -p 3307:3306 -d mysql:5.7
# launch prestashop container
$ docker run -ti --name some-prestashop --network prestashop-net -e DB_SERVER=some-mysql -p 8080:80 -d prestashop/prestashop:latest
```

A new shop will be built, ready to be installed.

You can then use the shop by reaching [http://localhost:8080](http://localhost:8080).

The MySQL server can be reached:
- from the host using port 3307 (example: `$ mysql -uroot -padmin -h localhost --port 3307`)
- from a container in the network using the URL `some-mysql`.

For example, when you reach the "database configuration" install step, the installer will ask for the "server database address": input `some-mysql`.

<hr>

However, if you want to customize the container execution, here are many available options:

| Environment variable  | Description | Default value |
|---|---|---|
| PS_DEV_MODE | The constant _PS_MODE_DEV_ will be set at true | `0` |
| PS_HOST_MODE | The constant _PS_HOST_MODE_ will be set at true. Useful to simulate a PrestaShop Cloud environment. | `0` |
| PS_DEMO_MODE | The constant _PS_DEMO_MODE_ will be set at true. Use it to create a demonstration shop. | `0` |
| DB_SERVER | If set, the external MySQL database will be used instead of the volatile internal one | `localhost` |
| DB_USER | Override default MySQL user | `root` |
| DB_PASSWD | Override default MySQL password | `admin` |
| DB_PREFIX | Override default tables prefix | `ps_` |
| DB_NAME | Override default database name | `prestashop` |
| PS_INSTALL_AUTO | The installation will be executed. Useful to initialize your image faster. In some configurations, you may need to set PS_DOMAIN or PS_HANDLE_DYNAMIC_DOMAIN as well. (Please note that PrestaShop can be installed automatically from PS 1.5) | `0` |
| PS_ERASE_DB | Drop the mysql database. All previous mysql data will be lost | `0` |
| PS_INSTALL_DB | Create the mysql database. | `0` |
| PS_DOMAIN | When installing automatically your shop, you can tell the shop how it will be reached. For advanced users only | |
| PS_LANGUAGE | Change the default language installed with PrestaShop | `en` |
| PS_COUNTRY | Change the default country installed with PrestaShop | `GB` |
| PS_ALL_LANGUAGES | Install all the existing languages for the current version. | `0` |
| PS_FOLDER_ADMIN | Change the name of the admin folder | `admin` |
| PS_FOLDER_INSTALL | Change the name of the install folder | `install` |
| PS_ENABLE_SSL | Enable SSL at PrestaShop installation. | `0` |
| ADMIN_MAIL | Override default admin email | `demo@prestashop.com` |
| ADMIN_PASSWD | Override default admin password | `prestashop_demo` |

If your IP / port (or domain) change between two executions of your container, you will need to modify this option:

| Environment variable  | Description | Default value |
|---|---|---|
| PS_HANDLE_DYNAMIC_DOMAIN | Add specific configuration to handle dynamic domain | `0` |

## Documentation

The user documentation (in English by default) is available [here](https://docs.prestashop-project.org/).

The developer documentation (English only) can be found [here](https://devdocs.prestashop-project.org/).

## Troubleshooting

#### Prestashop cannot be reached from the host browser

When using Docker for Mac or Docker for Windows (throught WSL), Prestashop cannot be reached from the host browser (gets redirected to "dockeripaddress:8080")

Docker for Mac has an issue with bridging networking and consequently cannot reach the container on its internal IP address. After installation, the browser on the host machine will be redirected from `http://localhost:8080` to `http://<internal_prestashop_container_ip>:8080` which fails.

You need to set the `PS_DOMAIN` variable to `localhost:8080` for it to work correctly when browsing from the host computer. The command looks something like this:
```
$ docker run -ti --name some-prestashop --network prestashop-net -e DB_SERVER=some-mysql -e PS_DOMAIN=localhost:8080 -p 8080:80 -d prestashop/prestashop
```

#### Cannot connect to mysql from host - authentication plugin cannot be loaded

```
ERROR 2059 (HY000): Authentication plugin 'caching_sha2_password' cannot be loaded: ...
```

If your `mysql` image uses MySQL 8, the authentication plugin changed from `mysql_native_password` to `caching_sha2_password`. You can bypass this by forcing the old authentication plugin: 

```bash
$ docker run -ti -p 3307:3306 --network prestashop-net --name some-mysql -e MYSQL_ROOT_PASSWORD=admin -d mysql --default-authentication-plugin=mysql_native_password
```

#### Cannot connect to mysql from host - cannot use socket

```
ERROR 1045 (28000): Access denied for user '...'@'...' (using password: YES)
```

For some usecases, you might need to force using TCP instead of sockets:

```bash
$ mysql -u root -padmin -h localhost --port 3307 --protocol=tcp
```

#### During the installation, prestashop cannot connect to mysql - bad charset

```
Server sent charset (255) unknown to the client. Please, report to the developers
```

MySQL 8 changed the default charset to utfmb4. But some clients do not know this charset. This requires to modify the mysql configuration file.

If you are using a `mysql` container, you need to :
- modify mysql configuration file `/etc/mysql/my/cnf` and add:
```
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8


[mysqld]
collation-server = utf8_unicode_ci
character-set-server = utf8
```
- restart mysql container

## How to use the builder script

For more information, read [HOW-TO-USE.md](HOW-TO-USE.md) file
