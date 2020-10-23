from versions import VERSIONS
from . import CONTAINERS
from pathlib import Path
import logging

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
                versions[ps_version + '-' + php_version + '-' + container_version] = str(self.directory_path / ps_version / (php_version + '-' + container_version))
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
                    result[data['ps_version'] + '-' + php_version + '-' + container] = str(container_path)

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
        result = None
        data = version.split('-')
        try:
            if len(data) == 1:
                result = {
                    'ps_version': data[0],
                    'php_versions': VERSIONS[data[0]],
                    'container_version': None
                }
            else:
                if data[1] in VERSIONS[data[0]]:
                    result = {
                        'ps_version': data[0],
                        'php_versions': (data[1],),
                        'container_version': data[2] if len(data) > 2 else None,
                    }
        finally:
            return result
