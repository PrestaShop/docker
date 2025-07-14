from errno import EEXIST
from os import path, makedirs
from string import Template
from . import CONTAINERS
from prestashop_docker.version_manager import VersionManager


class Generator:
    NIGHTLY = 'nightly'

    def __init__(self, distribution_api, directory_path, template, nightly_template, branch_template):
        """Constructor

        @param distribution_api: Distrihbution API
        @type distribution_api: DistributionApi
        @param directory_path: Directory path
        @type directory_path: str
        @param template: Base template
        @type template: str
        @param nightly_template: Nightly template
        @type nightly_template: str
        @param branch_template: Branch template
        @type branch_template: str
        """
        self.distribution_api = distribution_api
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
        ) else self.nightly_template if (
            split_version is not None and split_version['patch'] == 'x'
        ) else self.template

        # Get valid PS version (for branch versions it returns to future next patch)
        branch_version = parsed_version['branch_version']
        ps_version = branch_version if (
            split_version is not None and split_version['patch'] == 'x'
        ) else parsed_version['ps_version']

        if split_version is None:
            node_version = 'v20.17.0'
        elif split_version['major'] == '1.7':
            node_version = 'v14.20.0'
        elif split_version['major'] == '8':
            node_version = 'v16.20.2'
        else:
            node_version = 'v20.17.0'

        with open(file_path, 'w+') as f:
            ps_url = self.distribution_api.get_download_url_of(ps_version)
            f.write(
                template.substitute(
                    {
                        'ps_version': ps_version,
                        'branch_version': branch_version,
                        'container_version': container_version,
                        'node_version': node_version,
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
