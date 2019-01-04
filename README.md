# PrestaShop on Docker

[![Build Status](https://travis-ci.org/PrestaShop/docker.svg?branch=master)](https://travis-ci.org/PrestaShop/docker)

## Supported tags

### Image by PrestaShop version
* `1.7`, `1.7.5.0`, `latest`
* `1.6`, `1.6.1.23`
* `1.5`, `1.5.6.3`
* `1.4`, `1.4.11.1`
* `nightly` (Latest but unstable release from git)

### Other PHP versions
By default, our images are running with PHP 5.6. But each major version can be launched with another PHP version if you want to.
* Apache
  * PHP 5.5: `1.5-5.5-apache`, `1.6-5.5-apache`, `1.7-5.5-apache`, `nightly-5.5-apache`
  * PHP 5.6: `1.5-5.6-apache`, `1.6-5.6-apache`, `1.7-5.6-apache`, `nightly-5.6-apache`
  * PHP 7.0: `1.5-7.0-apache`, `1.6-7.0-apache`, `1.7-7.0-apache`, `nightly-7.0-apache`
  * PHP 7.1: `1.5-7.1-apache`, `1.6-7.1-apache`, `1.7-7.1-apache`, `nightly-7.1-apache`
  * PHP 7.2: `1.5-7.2-apache`, `1.6-7.2-apache`, `1.7-7.2-apache`, `nightly-7.2-apache`
* FPM
  * PHP 5.5: `1.5-5.5-fpm`, `1.6-5.5-fpm`, `1.7-5.5-fpm`, `nightly-5.5-fpm`
  * PHP 5.6: `1.5-5.6-fpm`, `1.6-5.6-fpm`, `1.7-5.6-fpm`, `nightly-5.6-fpm`
  * PHP 7.0: `1.5-7.0-fpm`, `1.6-7.0-fpm`, `1.7-7.0-fpm`, `nightly-7.0-fpm`
  * PHP 7.1: `1.5-7.1-fpm`, `1.6-7.1-fpm`, `1.7-7.1-fpm`, `nightly-7.1-fpm`
  * PHP 7.2: `1.5-7.2-fpm`, `1.6-7.2-fpm`, `1.7-7.2-fpm`, `nightly-7.2-fpm`

You can use tags for this. For example:
```
$ docker run -ti --name my-docker-name -e PS_DEV_MODE=false -e PS_INSTALL_AUTO=0 -p 8080:80 -d prestashop/prestashop:1.7-7.0
```

## What is PrestaShop

PrestaShop is a free and open-source e-commerce web application, committed to providing the best shopping cart experience for both merchants and customers. It is written in PHP, is highly customizable, supports all the major payment services, is translated in many languages and localized for many countries, has a fully responsive design (both front and back office), etc. See all the available features.

> [www.prestashop.com](https://www.prestashop.com)

![PrestaShop's back office dashboard](http://www.prestashop.com/images/banners/general/ps161-screenshot-github.png "PrestaShop's back office dashboard")

## How to run this image

This image is running with the latest Apache version in the [official PHP repository](https://registry.hub.docker.com/_/php/).
For the database, you can use and link any SQL server related to MySQL. We advise MySQL 5.6 for PrestaShop 1.6 and MySQL 5.7 for Prestashop 1.7 . MySQL 8 can be used with additional configuration.

Currently if you do not have any MySQL server, the most simple way to run this container is:
```bash
# create a network for containers to communicate
$ docker network create prestashop-net
# launch mysql 5.7 container
$ docker run -ti --name some-mysql --network prestashop-net -e MYSQL_ROOT_PASSWORD=admin -p 3307:3306 -d mysql:5.7
# launch prestashop container
$ docker run -ti --name some-prestashop --network prestashop-net -e DB_SERVER=some-mysql -p 8080:80 -d prestashop/prestashop
```

A new shop will be built, ready to be installed.

You can then use the shop by reaching [http://localhost:8080](http://localhost:8080).

The MySQL server can be reached:
- from the host using port 3307 (example: `$ mysql -uroot -padmin -h localhost --port 3307`)
- from a container in the network using the URL `some-mysql`.

For example, when you reach the "database configuration" install step, the installer will ask for the "server database address": input `some-mysql`.

<hr>

However, if you want to customize the container execution, here are many available options:

* **PS_DEV_MODE**: The constant `_PS_MODE_DEV_` will be set at `true` *(default value: 0)*
* **PS_HOST_MODE**: The constant `_PS_HOST_MODE_` will be set at `true`. Useful to simulate a PrestaShop Cloud environment. *(default value: 0)*
* **PS_DEMO_MODE**: The constant `_PS_DEMO_MODE_` will be set at `true`. Use it to create a demonstration shop. *(default value: 0)*
* **DB_SERVER**: If set, the external MySQL database will be used instead of the volatile internal one *(default value: localhost)*
* **DB_USER**: Override default MySQL user *(default value: root)*
* **DB_PASSWD**: Override default MySQL password *(default value: admin)*
* **DB_PREFIX**: Override default tables prefix *(default value: ps_)*
* **DB_NAME**: Override default database name *(default value: prestashop)*
* **PS_INSTALL_AUTO=1**: The installation will be executed. Useful to initialize your image faster. In some configurations, you may need to set **PS_DOMAIN** or **PS_HANDLE_DYNAMIC_DOMAIN** as well. (Please note that PrestaShop can be installed automatically from PS 1.5)
* **PS_ERASE_DB**: Only with **PS_INSTALL_AUTO=1**. Drop and create the mysql database. All previous mysql data will be lost *(default value: 0)*
* **PS_DOMAIN**: When installing automatically your shop, you can tell the shop how it will be reached. For advanced users only *(no default value)*
* **PS_LANGUAGE**: Change the default language installed with PrestaShop *(default value: en)*
* **PS_COUNTRY**: Change the default country installed with PrestaShop *(default value: GB)*
* **PS_ALL_LANGUAGES**: Install all the existing languages for the current version. *(default value: 0)*
* **PS_FOLDER_ADMIN**: Change the name of the `admin` folder *(default value: admin. But will be automatically changed later)*
* **PS_FOLDER_INSTALL**: Change the name of the `install` folder *(default value: install. But must be changed anyway later)*

By default, we use the employee existing on the [PrestaShop demo](http://demo.prestashop.com). But you can change it with the following parameters:

* **ADMIN_MAIL**: Override default admin email *(default value: demo@prestashop.com)*
* **ADMIN_PASSWD**: Override default admin password *(default value: prestashop_demo)*

If your IP / port (or domain) change between two executions of your container, you will need to modify this option:

* **PS_HANDLE_DYNAMIC_DOMAIN**: Add specific configuration to handle dynamic domain *(default value: 0)*

## License

View [license information](https://www.prestashop.com/en/osl-license) for the software contained in this image.

## Documentation

The documentation (in English by default) is available at the following addresses:

* [PrestaShop 1.7](http://doc.prestashop.com/display/PS17)
* [PrestaShop 1.6](http://doc.prestashop.com/display/PS16)
* [PrestaShop 1.5](http://doc.prestashop.com/display/PS15)
* [PrestaShop 1.4](http://doc.prestashop.com/display/PS14)

## Troubleshooting

#### Prestashop cannot be reached from the host browser

When using Docker for Mac, Prestashop cannot be reached from the host browser (gets redirected to "dockeripaddress:8080")

Docker for Mac has an issue with bridging networking and consequently cannot reach the container on its internal IP address. After installation, the browser on the host machine will be redirected from `http://localhost:8080` to `http://<internal_prestashop_container_ip>:8080` which fails.

You need to set the `PS_DOMAIN` and `PS_SHOP_URL` variables to `localhost:8080` for it to work correctly when browsing from the host computer. The command looks something like this:
```
$ docker run -ti --name some-prestashop --network prestashop-net -e DB_SERVER=some-mysql -e PS_DOMAIN=localhost:8080 -e PS_SHOP_URL=localhost:8080 -p 8080:80 -d prestashop/prestashop
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
