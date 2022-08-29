from versions import VERSIONS
from . import CONTAINERS
from . import PREFERED_CONTAINER
from pathlib import Path
import logging
import re
import semver

logger = logging.getLogger(__name__)


class VersionManager:
    def __init__(self, directory_path):
        '''
        Constructor

        @param directory_path: Path where images are stored
        @type directory_path: str
        '''
        self.directory_path = Path(directory_path)

    def get_versions(self):
        '''
        Return list of versions based on the images directory

        @return: Return list of versions
        @rtype: dict
        '''
        versions = {}
        for ps_version, php_versions in VERSIONS.items():
            versions = {**versions, **self.get_containers_versions(
                ps_version,
                php_versions
            )}
        return versions

    def get_containers_versions(self, ps_version, php_versions):
        '''
        Get containers versions

        :param path:
        '''
        versions = {}
        for php_version in php_versions:
            for container_version in CONTAINERS:
                versions[self.create_version(ps_version, php_version, container_version)] = str(self.directory_path / ps_version / (php_version + '-' + container_version))
        return versions

    def parse_version(self, version):
        '''
        Parse version and return associated paths.

        1. Only with PrestaShop version
          - 1.7.6.8 => {'1.7.6.8-5.6-fpm': '/path/to/prestashop/docker/images/1.7.6.8/5.6-fpm', '1.7.6.8-7.2-fpm': '/path/to/prestashop/docker/images/1.7.6.8/7.2-fpm', '1.7.6.8-7.1-fpm': '/path/to/prestashop/docker/images/1.7.6.8/7.1-fpm', '1.7.6.8-7.2-apache': '/path/to/prestashop/docker/images/1.7.6.8/7.2-apache', '1.7.6.8-7.1-apache': '/path/to/prestashop/docker/images/1.7.6.8/7.1-apache', '1.7.6.8-5.6-apache': '/path/to/prestashop/docker/images/1.7.6.8/5.6-apache'}

        2. With specific version
          - 1.7.6.8-5.6-fpm => {'1.7.6.8-5.6-fpm': PosixPath('/path/to/prestashop/docker/images/1.7.6.8/5.6-fpm')}

        @param version: The version you want
        @type version: str
        @return: A list with tags and their paths
        @rtype: dict
        '''

        data = self.get_version_from_string(version)
        if data is None or not (self.directory_path / data['ps_version']).exists():
            raise ValueError('{} is not a valid version'.format(version))

        if data['container_version'] is None:
            containers = ('fpm', 'apache',)
        else:
            containers = (data['container_version'],)

        ps_version_path = self.directory_path / data['ps_version']
        result = {}
        for php_version in data['php_versions']:
            for container in containers:
                container_path = ps_version_path / (php_version + '-' + container)
                if container_path.exists():
                    result[self.create_version(data['ps_version'], php_version, container)] = str(container_path)

        return result

    def get_version_from_string(self, version):
        '''
        Split version to find PrestaShop version, PHP version and container type

        @param version: The version you want
        @type version: str
        @return: A tuple containing ('PS_VERSION', (PHP_VERSIONS), 'CONTAINER_TYPE')
                 or ('PS_VERSION', 'PHP_VERSION', 'CONTAINER_TYPE')
        @rtype: tuple
        '''
        matches = self.parse_version_from_string(version)
        if not matches:
            return None

        ps_version = matches.group('version')
        if matches.group('php'):
            php_versions = (matches.group('php'),)
        else:
            if ps_version not in VERSIONS:
                return None

            php_versions = VERSIONS[ps_version]

        container_version = None
        if matches.group('container'):
            container_version = matches.group('container')

        return {
            'ps_version': ps_version,
            'php_versions': php_versions,
            'container_version': container_version
        }

    def parse_version_from_string(self, version):
        '''
        Parse version from string based on a regex
        @param version: The version you want to parse
        @type version: str
        @return: Return None if no position in the string matches the pattern otherwise a Match object.
        @rtpe: None|Match
        '''
        regex = r"^(?P<version>(?:[0-9]+\.){0,3}(?:[0-9]+|nightly)(?:-(?:alpha|beta|rc)(?:\.\d+)?(?:\+\d+)?)?)(?:-(?P<php>\d+\.\d+))?(?:-(?P<container>fpm|apache))?$"
        return re.search(regex, version)

    def get_aliases(self):
        '''
        Build aliases from VERSIONS constants

        @return: All aliases associated to their image name
        @rtype: dict
        '''

        aliases_ps_version = self.get_ps_versions_aliases()

        aliases = {}
        for alias_version, ps_version_data in aliases_ps_version.items():
            ps_version = ps_version_data['value']
            previous_php_version = None
            # Check PHP versions
            for php_version in VERSIONS[ps_version]:
                current_php_version = semver.VersionInfo.parse(php_version + '.0')

                if previous_php_version is None or previous_php_version < current_php_version:
                    alias_php_version = php_version
                    previous_php_version = current_php_version

                if alias_version != 'latest':
                    self.append_to_aliases(aliases, ps_version, php_version, PREFERED_CONTAINER, alias_version + '-' + php_version)

            # Check prefered container
            self.append_to_aliases(aliases, ps_version, alias_php_version, PREFERED_CONTAINER, alias_version)

            # Check containers
            if alias_version != 'latest':
                for container_version in CONTAINERS:
                    self.append_to_aliases(aliases, ps_version, alias_php_version, container_version, alias_version + '-' + container_version)

        return aliases

    def append_to_aliases(self, aliases, ps_version, php_version, container_version, alias_version):
        created_version = self.create_version(ps_version, php_version, container_version)
        if created_version not in aliases:
            aliases[created_version] = []

        aliases[created_version].append(alias_version)

    def get_ps_versions_aliases(self):
        '''
        Get list of PrestaShop aliases associated with their real version

        @return: List of aliases
        @rtype: dict
        '''
        aliases = {}
        previous_version = {}
        for ps_version in VERSIONS.keys():
            full_splitted_version = ps_version.split('.')
            if len(full_splitted_version) < 3 or int(full_splitted_version[0]) < 8 and len(full_splitted_version) < 4:
                aliases[ps_version] = {
                    'value': ps_version
                }
                continue

            # PrestaShop versions before 8 are in format 1.MAJOR.MINOR.PATCH
            # Starting version 8, format is MAJOR.MINOR.PATCH
            splitted_version = ps_version.split('.', 1)
            if int(splitted_version[0]) >= 8:
                current_version = semver.VersionInfo.parse(ps_version)
            else:
                current_version = semver.VersionInfo.parse(splitted_version[1])
            # Ignore prerelease versions
            if current_version.prerelease:
                aliases[ps_version] = {
                    'value': ps_version
                }
                continue

            if int(splitted_version[0]) >= 8:
                version_name = str(current_version.major)
            else:
                version_name = splitted_version[0] + '.' + str(current_version.major)
            if version_name not in previous_version or aliases[version_name]['version'] < current_version:
                aliases[version_name] = {
                    'version': current_version,
                    'value': ps_version
                }

            if int(splitted_version[0]) >= 8:
                version_with_major_name = str(current_version.major) + '.' + str(current_version.minor)
            else:
                version_with_major_name = splitted_version[0] + '.' + str(current_version.major) + '.' + str(current_version.minor)
            if version_with_major_name not in aliases or aliases[version_with_major_name]['version'] < current_version:
                aliases[version_with_major_name] = {
                    'version': current_version,
                    'value': ps_version
                }
                aliases[ps_version] = aliases[version_name]
                aliases['latest'] = aliases[version_name]

        return aliases

    def create_version(self, ps_version, php_version, container_version):
        '''
        Create version string
        @param ps_version: PrestaShop version
        @type ps_version: str
        @param php_version: PHP version
        @type php_version: str
        @param container_version: Container version
        @type container_version: str
        '''
        return ps_version + '-' + php_version + '-' + container_version
