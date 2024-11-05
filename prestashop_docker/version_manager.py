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

        # Initial PS version(can also be a branch like 9.0.x)
        split_version = self.split_prestashop_version(version)
        if split_version is None or not (self.directory_path / split_version['version']).exists():
            raise ValueError('{} is not a valid version'.format(version))

        data = self.get_version_from_string(version)
        if data is None or data['container_version'] is None:
            containers = ('fpm', 'apache',)
        else:
            containers = (data['container_version'],)

        ps_version_path = self.directory_path / split_version['version']
        result = {}
        for php_version in data['php_versions']:
            for container in containers:
                container_path = ps_version_path / (php_version + '-' + container)
                if container_path.exists():
                    result[self.create_version(split_version['version'], php_version, container)] = str(container_path)

        return result

    def get_version_from_string(self, version):
        '''
        Split version to find PrestaShop version, branch version, PHP version and container type

        @param version: The version you want
        @type version: str
        @return: A tuple containing ('PS_VERSION', 'BRANCH_VERSION', (PHP_VERSIONS), 'CONTAINER_TYPE')
                 or ('PS_VERSION', 'BRANCH_VERSION', 'PHP_VERSION', 'CONTAINER_TYPE')
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

        split_version = self.split_prestashop_version(ps_version)
        if split_version is None:
            branch_version = 'develop'
        elif split_version['patch'] == 'x':
            # ps_version actually already contains the branch
            branch_version = ps_version
            # We need to transform the branch into the next patch version
            patch_index = ps_version.rindex('.')
            last_patch = self.get_last_patch_from_version(ps_version)
            if last_patch is None:
                last_patch = '0'
            else:
                last_patch = str(int(last_patch) + 1)
            ps_version = ps_version[:patch_index + 1] + last_patch
        else:
            # Transform the last patch version into an x to get the branch, we ignore any -rc that may be present
            real_version = split_version['version']
            patch_index = real_version.rindex('.')
            branch_version = real_version[:patch_index + 1] + 'x'

        return {
            'ps_version': ps_version,
            'branch_version': branch_version,
            'php_versions': php_versions,
            'container_version': container_version
        }

    def get_last_patch_from_version(self, version):
        '''
        Get last patch version for the specified version based on the VERSIONS list
        @param version: The version you need the match from
        @type version: str
        @return: Return None if no patch is found otherwise an int with the patch.
        @rtpe: None|int
        '''
        split_version = self.split_prestashop_version(version)
        if (split_version is None):
            return None

        lastPatch = None
        for ps_version, php_versions in VERSIONS.items():
            split_ps_version = self.split_prestashop_version(ps_version)
            if split_ps_version is None:
                continue
            if (split_ps_version['major'] != split_version['major'] or split_ps_version['minor'] != split_version['minor']):
                continue
            if split_ps_version['patch'] == 'x':
                continue
            if (lastPatch is None or int(split_ps_version['patch']) > int(lastPatch)):
                lastPatch = split_ps_version['patch']
        return lastPatch

    def split_prestashop_version(self, version):
        '''
        Split the version into major minor patch object, it is a custom-tailed alternative to semver.VersionInfo.parse
        that can handle our development branches like 1.7.8.x, 8.0.x, ...
        @param version: The version you need to split
        @type version: str
        @return: Return None if no patch is found otherwise an int with the patch.
        @rtpe: None|tuple
        '''
        regex = r"^(?P<major>(1.)?[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9x]+)(?P<prerelease>-(alpha|beta|rc)(?:\.\d+)?(?:\+\d+)?)?"
        matches = re.search(regex, version)

        if (matches and matches.group() and matches.group('major') and matches.group('major') and matches.group('major')):
            # Remove the initial matched -
            prerelease = matches.group('prerelease')[1:] if matches.group('prerelease') else None

            return {
                'version': matches.group('major') + '.' + matches.group('minor') + '.' + matches.group('patch'),
                'major': matches.group('major'),
                'minor': matches.group('minor'),
                'patch': matches.group('patch'),
                'prerelease': prerelease,
            }
        return None

    def parse_version_from_string(self, version):
        '''
        Parse version from string based on a regex
        @param version: The version you want to parse
        @type version: str
        @return: Return None if no position in the string matches the pattern otherwise a Match object.
        @rtpe: None|Match
        '''
        regex = r"^(?P<version>(?:[0-9]+\.){0,3}(?:[0-9]+|nightly|x)(?:-(?:alpha|beta|rc)(?:\.\d+)?(?:\+\d+)?)?)(?:-(?P<php>\d+\.\d+))?(?:-(?P<container>fpm|apache))?$"
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

            # Check preferred container
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

            # Ignore branch versions
            split_version = self.split_prestashop_version(ps_version)
            if split_version['patch'] == 'x':
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
