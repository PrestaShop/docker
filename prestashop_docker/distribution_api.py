import requests
from packaging.version import Version


class DistributionApi():
    PRESTASHOP_API_URL = "https://api.prestashop-project.org/prestashop"

    def __init__(self, data=None):
        self.prestashop_versions = data

    def fetch_prestashop_versions(self):
        if self.prestashop_versions is None:
            response = requests.get(self.PRESTASHOP_API_URL)
            response.raise_for_status()
            self.prestashop_versions = response.json()

        return self.prestashop_versions

    def get_download_url_of(self, version):
        url = None
        distribution_version = None
        for entry in self.prestashop_versions:
            if version == entry.get('version') and (url is None or Version(entry.get('distribution_version')) > Version(distribution_version)):
                # We can have different distribution releases for the same PrestaShop version. We look for the most recent.
                url = entry.get('zip_download_url')
                distribution_version = entry.get('distribution_version')

        return url
