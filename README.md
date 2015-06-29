# prestashop on Docker

## Supported tags

* 1.6, 1.6.0, 1.6.0.14, latest
* 1.5, 1.5.6, 1.5.6.2
* 1.4, 1.4.11, 1.4.11.0

## What is PrestaShop

PrestaShop is a free and open-source e-commerce web application, committed to providing the best shopping cart experience for both merchants and customers. It is written in PHP, is highly customizable, supports all the major payment services, is translated in many languages and localized for many countries, has a fully responsive design (both front and back office), etc. See all the available features.

> www.prestashop.com

<p align="center">
  <img src="http://www.prestashop.com/images/banners/general/ps16-screenshot-github.png" alt="PrestaShop's back office dashboard"/>
</p>

## How to run this image

This image is running with the latest Apache version in the [official PHP repository](https://registry.hub.docker.com/_/php/).

The most simple way to run this container is:
```
$ docker run -ti --name some-prestashop -p 8080:80 -d quetzacoalt/prestashop
```

A new shop will be built, already installed. You can then use it by reaching `http://localhost:8080`.
However, if you want to customize the container execution, here are many available options:

* **DB_SERVER**: If set, the external MySQL database will be used instead of the volatile internal one *(default value: localhost)*
* **DB_USER**: Override default MySQL user *(default value: root)*
* **DB_PASSWD**: Override default MySQL password *(default value: admin)*
* **DB_PREFIX**: Override default tables prefix *(default value: ps_)*
* **DB_NAME**: Override default database name *(default value: prestashop)*

By default, we use the employee existing on the [PrestaShop demo](http://demo.prestashop.com). But you can change them with the following parameters:
* **ADMIN_MAIL**: Override default admin email *(default value: demo@prestashop.com)*
* **ADMIN_PASSWD**: Override default admin password *(default value: prestashop_demo)*

* **no_install=1**: The installation won't be executed. Usefull to check any issue during the installation wizard.
