#!/usr/bin/env python

from errno import EEXIST
from os import path, makedirs
from string import Template
from versions import VERSIONS

CONTAINERS = ('fpm', 'apache')

class Generator:
    def __init__(self):
        self.download_url = 'https://www.prestashop.com/download/old/prestashop_{}.zip'
        self.directory_path = path.join(path.dirname(path.realpath(__file__)), 'images')
        self.template = Template(open('./Dockerfile.model').read())
        self.nightly_template = Template(open('./Dockerfile-nightly.model').read())

    def create_directory(self, directory_path):
        try:
            makedirs(directory_path, 0o755, exist_ok=True)
        except OSError as e:
            if e.errno != EEXIST:
                raise
            pass

    def generate_image(self, ps_version, container_version):
        directory_path = path.join(
            self.directory_path,
            ps_version,
            container_version
        )

        self.create_directory(directory_path)

        file_path = path.join(directory_path, 'Dockerfile')
        template = self.nightly_template if ps_version == 'nightly' else self.template

        with open(file_path, 'w+') as f:
            f.write(
                template.substitute(
                    {
                        'ps_version': ps_version,
                        'container_version': container_version,
                        'ps_url': self.download_url.format(ps_version)
                    }
                )
            )

    def generate_all(self, versions):
        for ps_version, php_versions in versions.items():
            print(
                'Generate Dockerfile for PrestaShop {}'.format(
                    ps_version,
                )
            )
            for php_version in php_versions:
                for container in CONTAINERS:
                    container_version = '{}-{}'.format(php_version, container)
                    print(
                        "\tContainer - {}".format(
                            container_version
                        )
                    )

                    self.generate_image(ps_version, container_version)


if __name__ == '__main__':
    generator = Generator()
    generator.generate_all(VERSIONS)
