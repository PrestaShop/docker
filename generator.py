#!/usr/bin/env python

from errno import EEXIST
from os import path, mkdir
from string import Template
from versions import VERSIONS

class Generator:
    def __init__(self):
        self.download_url = 'https://www.prestashop.com/download/old/prestashop_{}.zip'
        self.directory_path = path.join(path.dirname(path.realpath(__file__)), 'images')
        self.template = Template(open('./Dockerfile.model').read())
        self.nightly_template = Template(open('./Dockerfile-nightly.model').read())

    def generate_image(self, ps_version, folder, container_version):
        print(
            'Generate Dockerfile for PrestaShop {} - PHP {}'.format(
                ps_version,
                container_version
            )
        )

        try:
            mkdir(path.join(self.directory_path, folder), 0o755)
        except OSError as e:
            if e.errno != EEXIST:
                raise
            pass

        file_path = path.join(self.directory_path, folder, 'Dockerfile')
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
            for php_version in php_versions:
                self.generate_image(ps_version, ps_version, '{}'.format(php_version))
                # self.generate_image(ps_version, '{}'.format(php_version))


if __name__ == '__main__':
    generator = Generator()
    generator.generate_all(VERSIONS)
