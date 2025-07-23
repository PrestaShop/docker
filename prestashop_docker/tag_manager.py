import logging
import shutil
import subprocess
from .stream import Stream

logger = logging.getLogger(__name__)


class TagManager():
    def __init__(self, docker_api, docker_client, version_manager, cache, quiet):
        '''
        Constructor

        @param docker_api: Customer docker API
        @type docker_api: DockerApi
        @param docker_client: Docker client
        @type docker_client: docker
        @param version_manager: Version manager
        @type version_manager: VersionManager
        @param cache: Use cache
        @type cache: bool
        @param quiet: Quiet mode
        @type quiet: bool
        '''
        self.docker_api = docker_api
        self.docker_client = docker_client
        self.stream = Stream(quiet)
        self.version_manager = version_manager
        self.cache = cache
        self.tags = None

    def build(self, version=None, force=False, push=False):
        '''
        Build version on the current machine

        @param version: Optional version you want to build
        @type version: str
        '''
        versions = self.get_versions(version)

        for version, version_path in versions.items():
            print(
                'Building {}'.format(version)
            )

            if not force and self.exists(version):
                print('Image already exists')
                # Do not build images that already exists on Docker Hub
                continue

            if not shutil.which("docker"):
                raise RuntimeError("The docker client must be installed")

            tags = ["--tag", "prestashop/prestashop:" + version]
            aliases = self.version_manager.get_aliases()
            if version in aliases:
                for alias in aliases[version]:
                    print('Will be aliased as tag {}'.format(alias))
                    tags = tags + ["--tag", "prestashop/prestashop:" + alias]

            args = []
            if push:
                args.append('--push')
            if not self.cache:
                args.append('--no-cache')

            cmd_args = [
                "docker", "buildx", "build",
                "--platform", "linux/arm/v7,linux/arm64/v8,linux/amd64",
                "--builder", "container",
            ] + tags + args + [
                str(version_path)
            ]

            log = subprocess.Popen(cmd_args, shell=True, stdout=subprocess.PIPE).stdout.read()

            self.stream.display(log)

    def exists(self, version):
        '''
        Test if a version is already on Docker Hub

        @param version: The version you want to check
        @type version: str
        @return: True if tag exists
        @rtype: dict
        '''

        if self.tags is None:
            self.tags = self.docker_api.get_tags()

        for tag in self.tags:
            if tag['name'] == version:
                return True

        return False

    def get_versions(self, version):
        '''
        Version checker

        @param version: Version
        @type version: str
        @return: List of versions
        @rtype: dict
        '''
        if version is None:
            return self.version_manager.get_versions()

        return self.version_manager.parse_version(version)

    def get_aliases(self, version):
        '''
        Get all aliases

        @param version: Version
        @type version: str
        '''
        versions = self.get_versions(version)
        aliases = self.version_manager.get_aliases()
        for version in versions:
            if version in aliases:
                print('Aliases for {}'.format(version))
                [print("\t{}".format(alias)) for alias in aliases[version]]
