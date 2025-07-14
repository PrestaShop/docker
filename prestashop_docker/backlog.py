import re
from packaging.version import Version


class Backlog:
    MINIMUM_PRESTASHOP_VERSION_TO_BUILD = '1.7.7.0'

    def __init__(self, docker_api, docker_client, distribution_api, previous_state_versions, nightly_const):
        """Constructor

        @param docker_api: Customer docker API
        @type docker_api: DockerApi
        @param docker_client: Docker client
        @type docker_client: docker
        @param distribution_api: Distrihbution API
        @type distribution_api: DistributionApi
        @param previous_state_versions: Contents of the version.py file before regeneration
        @type previous_state_versions: dict
        @param nightly_const: Value of nightly case
        @type nightly_const: string
        """
        self.docker_api = docker_api
        self.docker_client = docker_client
        self.distribution_api = distribution_api
        self.previous_state_versions = previous_state_versions
        self.NIGHTLY = nightly_const

    def generate(self):
        available_php_versions = self.get_available_php_versions()
        prestashop_data = self.distribution_api.fetch_prestashop_versions()

        versions_dict = self.parse_prestashop_versions(prestashop_data, available_php_versions)
        branches_dict = self.get_branches_and_nightly_from_existing_file()
        self.write_versions_py(versions_dict | branches_dict)

    def get_available_php_versions(self):
        tags = self.docker_api.get_tags(image_name='library/php')
        available_versions = set()
        for tag in tags:
            match = re.match(r'^(\d+\.\d+)-apache$', tag['name'])
            if match:
                available_versions.add(match.group(1))
        return available_versions

    # Branches and nightly entries are manually added in versions.py file.
    # Let's reuse the existing contents on each generation.
    def get_branches_and_nightly_from_existing_file(self):
        branches = {}
        for branch, php_versions in self.previous_state_versions.items():
            if branch == self.NIGHTLY or branch.endswith('x'):
                branches[branch] = (tuple(php_versions))
        return branches

    def parse_prestashop_versions(self, prestashop_json, available_php_versions):
        versions = {}
        for entry in prestashop_json:
            if entry.get('stability') != 'stable':
                continue  # Only include stable versions

            if Version(entry.get('version')) < Version(self.MINIMUM_PRESTASHOP_VERSION_TO_BUILD):
                continue

            ps_version = entry['version']
            php_min = entry['php_min_version']
            php_max = entry['php_max_version']

            min_major, min_minor = map(int, php_min.split('.')[:2])
            max_major, max_minor = map(int, php_max.split('.')[:2])

            compatible_php_versions = []

            current_major, current_minor = min_major, min_minor
            while (current_major, current_minor) <= (max_major, max_minor):
                version_str = f"{current_major}.{current_minor}"
                if version_str in available_php_versions:
                    compatible_php_versions.append(version_str)
                # Increment minor version
                current_minor += 1
                if current_minor >= 10:
                    current_minor = 0
                    current_major += 1

            versions[ps_version] = (tuple(compatible_php_versions))

        return versions

    def write_versions_py(self, versions, output_path='versions.py'):
        with open(output_path, 'w') as f:
            f.write("VERSIONS = {\n")
            for ps_version in sorted(versions):
                php_versions = versions[ps_version]
                f.write(f"    '{ps_version}': (\n")
                for php_version in php_versions:
                    f.write(f"        '{php_version}', \n")
                f.write("    ),\n")
            f.write("}\n")
