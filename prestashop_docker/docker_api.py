# -*- coding: utf-8 -*-
import requests_cache
import logging
import requests
import ssl
import time
from urllib.parse import urljoin

logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context


class DockerApi():
    retries = 0

    def __init__(self, cache, debug):
        """Constructor

        @param cache: Enable cache
        @type cache: bool
        @param debug: Is debug mode enabled
        @type debug: bool
        """
        self.sleep_time = 1
        self.auth_url = 'https://auth.docker.io/token'
        self.registry_url = 'https://registry-1.docker.io/v2/'
        self.cache = cache
        self.is_debug = debug

        if self.cache:
            requests_cache.install_cache('cache')

    def get_tags(self, image_name):
        """Generate return tags

        The registry API is used instead of the Docker Hub one because
        Docker Hub refuses to paginate large tag lists for anonymous
        requests, while the registry returns them in a single response.

        @param image_name: Name of the image (e.g. library/php)
        @type image_name: str
        @return: The tags, as a list of {'name': <tag>} dicts
        @rtype: list
        """
        logger.debug(
            'Processing request for tags'
        )

        headers = {'Authorization': 'Bearer ' + self.get_token(image_name)}
        request_url = self.registry_url + image_name + '/tags/list'

        tags = []
        while request_url is not None:
            resp = self.execute(request_url, headers)
            tags += resp.json()['tags']
            if 'next' in resp.links:
                request_url = urljoin(request_url, resp.links['next']['url'])
            else:
                request_url = None

        return [{'name': name} for name in tags]

    def get_token(self, image_name):
        """Get an anonymous pull token for the registry API

        @param image_name: Name of the image the token grants access to
        @type image_name: str
        @return: The token
        @rtype: str
        """
        # Tokens are short-lived, never serve one from the cache
        with requests_cache.disabled():
            resp = self.execute(
                self.auth_url + '?service=registry.docker.io&scope=repository:' + image_name + ':pull'
            )

        return resp.json()['token']

    def execute(self, request_url, headers=None):
        """Execute url

        @param request_url: The url to execute
        @param headers: Optional HTTP headers
        @return: The HTTP Response
        @rtype: requests.Response
        """
        logger.debug(
            'Execute URL: ' + request_url
        )

        resp = requests.get(
            request_url,
            headers=headers
        )

        if resp.status_code != 200:
            # Something went wrong, retry
            time.sleep(self.sleep_time)
            DockerApi.retries += 1
            if DockerApi.retries >= 10:
                raise requests.HTTPError(resp.text)

            return self.execute(request_url, headers)

        DockerApi.retries = 0
        # Data not in cache
        if not hasattr(resp, 'from_cache') or not resp.from_cache:
            time.sleep(self.sleep_time)

        return resp
