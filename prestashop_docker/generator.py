from errno import EEXIST
from os import path, makedirs
from string import Template
from packaging import version
from . import CONTAINERS
from prestashop_docker.version_manager import VersionManager


class Generator:
    NIGHTLY = 'nightly'

    def __init__(self, directory_path, template, nightly_template, branch_template):
        """Constructor

        @param directory_path: Directory path
        @type directory_path: str
        @param template: Base template
        @type template: str
        @param nightly_template: Nightly template
        @type nightly_template: str
        @param branch_template: Branch template
        @type branch_template: str
        """
        self.download_url = 'https://www.prestashop.com/download/old/' \
            'prestashop_{}.zip'
        self.download_url_github = 'https://github.com/PrestaShop/PrestaShop/releases/download/{}/prestashop_{}.zip'
        self.directory_path = directory_path
        self.template = Template(template)
        self.nightly_template = Template(nightly_template)
        self.branch_template = Template(branch_template)
        self.version_manager = VersionManager(directory_path)

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
        parsed_version = self.version_manager.get_version_from_string(ps_version)
        split_version = self.version_manager.split_prestashop_version(ps_version)

        template = self.nightly_template if (
            ps_version == self.NIGHTLY
        ) else self.branch_template if (
            split_version is not None and split_version['patch'] == 'x'
        ) else self.template

        # Get valid PS version (for branch versions it returns to future next patch)
        ps_version = parsed_version['ps_version']
        branch_version = parsed_version['branch_version']

        with open(file_path, 'w+') as f:
            use_github_url = True
            # We use 1.7.8.8 as the comparison base because the 1.7.8.9 is not hosted on the .com anymore but until 1.7.8.8,
            # it still works so the .com url is used
            if split_version is not None and split_version['major'] == '1.7' and version.parse(ps_version) <= version.parse('1.7.8.8'):
                use_github_url = False

            if use_github_url:
                ps_url = self.download_url_github.format(ps_version, ps_version)
            else:
                ps_url = self.download_url.format(ps_version)
            f.write(
                template.substitute(
                    {
                        'ps_version': ps_version,
                        'branch_version': branch_version,
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
