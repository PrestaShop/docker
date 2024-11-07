### Creating new base images

To add new base versions update the `tags.txt` file to add a new version of PHP (usually one for apache and one for fpm)

Then run the generation script:

```
$ ./generate_tags.sh
```

If you wan to force the regeneration of existing base images force it:

```shell
$ ./generate_tags.sh -f
```

But be careful, for image with PHP <7.4 the installation of GD is different be careful not to remove this special line:

```
# Not this line:
RUN docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ --with-webp=/usr/include

But those lines instead:

# PHP < 7.4 have an old syntax to install GD. See https://github.com/docker-library/php/issues/912
RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ --with-webp-dir=/usr/include
```
