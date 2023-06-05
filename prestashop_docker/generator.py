from errno import EEXIST
from os import path, makedirs
from string import Template
from packaging import version
from . import CONTAINERS


class Generator:
    NIGHTLY = 'nightly'

    def __init__(self, directory_path, template, nightly_template):
        """Constructor

        @param directory_path: Directory path
        @type directory_path: str
        @param template: Base template
        @type template: str
        @param nightly_template: Nightly template
        @type nightly_template: str
        """
        self.download_url = 'https://www.prestashop.com/download/old/' \
            'prestashop_{}.zip'
        self.download_url_github = 'https://github.com/PrestaShop/PrestaShop/releases/download/{}/prestashop_{}.zip'
        self.directory_path = directory_path
        self.template = Template(template)
        self.nightly_template = Template(nightly_template)

    def create_directory(self, directory_path):
        """Try to create a directory if it's possible

        @param directory_path: Directory path
        @type directory_path: str
        """
        try:
            makedirs(directory_path, 0o755, exist_ok=True)
        except OSError as e:
            if e.errno != EEXIST:
                raise
            pass

    def generate_image(self, ps_version, container_version):
        """Generate Dockerfile image

        @param ps_version: PrestaShop version
        @type ps_version: str
        @param container_version: Container version
        @type container_version: str
        """
        directory_path = path.join(
            self.directory_path,
            ps_version,
            container_version
        )

        self.create_directory(directory_path)

        file_path = path.join(directory_path, 'Dockerfile')
        template = self.nightly_template if (
            ps_version == self.NIGHTLY
        ) else self.template

        with open(file_path, 'w+') as f:
            # We use 1.7.8.8 as the comparison base because the 1.7.8.9 is not hosted on the .com anymore but until 1.7.8.8 it still works,
            # however we can't use 8.0 as the base because 8.0.0-beta is lower than 8.0 and we need beta versions of 8 to use the new url
            if version.parse(ps_version) > version.parse('1.7.8.8'):
                ps_url = self.download_url_github.format(ps_version, ps_version)
            else:
                ps_url = self.download_url.format(ps_version)
            f.write(
                template.substitute(
                    {
                        'ps_version': ps_version,
                        'container_version': container_version,
                        'ps_url': ps_url
                    }
                )
            )

    def generate_all(self, versions):
        """Generate all Docker files from a dict

        @param versions: Versions
        @type versions: dict
        """
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
