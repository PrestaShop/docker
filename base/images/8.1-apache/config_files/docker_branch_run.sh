#!/bin/bash

# Clone repository
if [ ! -f /var/www/html/composer.json ]; then
  echo Clone PrestaShop $PS_BRANCH
  git clone -b $PS_BRANCH https://github.com/PrestaShop/PrestaShop.git /var/www/html
  chown -R www-data:www-data /var/www/html
fi

# Install composer
if [ ! -f /usr/local/bin/composer ]; then
  echo "\n* Install composer ...";
  mkdir -p /var/www/.composer
  chown -R www-data:www-data /var/www/.composer
  runuser -g www-data -u www-data -- php -r "copy('https://getcomposer.org/installer', '/tmp/composer-setup.php');" && php /tmp/composer-setup.php --no-ansi --install-dir=/usr/local/bin --filename=composer && rm -rf /tmp/composer-setup.php
  if [ ! -f /usr/local/bin/composer ]; then
    echo Composer installation failed
    exit 1
  fi
fi

# Install vendor dependencies
if [ ! -f /var/www/html/vendor/autoload.php ]; then
  echo "\n* Running composer ...";
  pushd /var/www/html
  # Execute composer as default user so that we can set the env variables to increase timeout, also disable default_socket_timeout for php
  COMPOSER_PROCESS_TIMEOUT=600 COMPOSER_IPRESOLVE=4 php -ddefault_socket_timeout=-1 /usr/local/bin/composer install --ansi --prefer-dist --no-interaction --no-progress
  # Update the owner of composer installed folders to be www-data
  chown -R www-data:www-data vendor modules themes
  popd
fi

# Build assets
if [ "${DISABLE_MAKE}" != "1" ]; then
  mkdir -p /var/www/.npm
  chown -R www-data:www-data /var/www/.npm

  echo "\n* Install node $NODE_VERSION...";
  export NVM_DIR=/usr/local/nvm
  mkdir -p $NVM_DIR \
      && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash \
      && . $NVM_DIR/nvm.sh \
      && nvm install $NODE_VERSION \
      && nvm alias default $NODE_VERSION \
      && nvm use default

  export NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin
  export PATH=$PATH:$NODE_PATH

  pushd /var/www/html
  echo "\n* Build assets ...";
  runuser -g www-data -u www-data -- /usr/bin/make assets

  echo "\n* Wait for assets built...";
  runuser -g www-data -u www-data -- /usr/bin/make wait-assets
  popd
else
  echo "\n* Build of assets was disabled...";
fi

/tmp/docker_run.sh
