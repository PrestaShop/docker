# PrestaShop on Docker

[![Build Status](https://travis-ci.org/PrestaShop/docker.svg?branch=master)](https://travis-ci.org/PrestaShop/docker)

## Supported tags

### Image by PrestaShop version
* `1.7`, `1.7.1.1`, `latest`
* `1.6`, `1.6.1.13`
* `1.5`, `1.5.6.3`
* `1.4`, `1.4.11.1`

### Other PHP versions
By default, our images are running with PHP 5.6. But each major version can be launched with another PHP version if you want to.
* PHP 5.5: `1.5-5.5`, `1.6-5.5`, `1.7-5.5`
* PHP 7.0: `1.5-7.0`, `1.6-7.0`, `1.7-7.0`

## What is PrestaShop

PrestaShop is a free and open-source e-commerce web application, committed to providing the best shopping cart experience for both merchants and customers. It is written in PHP, is highly customizable, supports all the major payment services, is translated in many languages and localized for many countries, has a fully responsive design (both front and back office), etc. See all the available features.

> [www.prestashop.com](https://www.prestashop.com)

![PrestaShop's back office dashboard](http://www.prestashop.com/images/banners/general/ps161-screenshot-github.png "PrestaShop's back office dashboard")

## How to run this image

This image is running with the latest Apache version in the [official PHP repository](https://registry.hub.docker.com/_/php/).
For the database, you can use and link any SQL server related to MySQL.

Currently if you do not have any MySQL server, the most simple way to run this container is:
```
$ docker run -ti --name some-mysql -e MYSQL_ROOT_PASSWORD=admin -d mysql
$ docker run -ti --name some-prestashop --link some-mysql -e DB_SERVER=some-mysql -p 8080:80 -d prestashop/prestashop
```

A new shop will be built, ready to be installed. You can then use it by reaching `http://localhost:8080`. The MySQL server can be reached with the URL `some-mysql:3306`.
However, if you want to customize the container execution, here are many available options:

* **PS_DEV_MODE**: The constant `_PS_MODE_DEV_` will be set at `true` *(default value: 0)*
* **PS_HOST_MODE**: The constant `_PS_HOST_MODE_` will be set at `true`. Usefull to simulate a PrestaShop Cloud environment. *(default value: 0)*
* **DB_SERVER**: If set, the external MySQL database will be used instead of the volatile internal one *(default value: localhost)*
* **DB_USER**: Override default MySQL user *(default value: root)*
* **DB_PASSWD**: Override default MySQL password *(default value: admin)*
* **DB_PREFIX**: Override default tables prefix *(default value: ps_)*
* **DB_NAME**: Override default database name *(default value: prestashop)*
* **PS_INSTALL_AUTO=1**: The installation will be executed. Useful to initialize your image faster. (Please note that PrestaShop can be installed automatically from PS 1.5)
* **PS_LANGUAGE**: Change the default language installed with PrestaShop *(default value: en)*
* **PS_COUNTRY**: Change the default country installed with PrestaShop *(default value: gb)*
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
