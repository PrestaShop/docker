import requests


class DistributionApi():
    PRESTASHOP_API_URL = "https://api.prestashop-project.org/prestashop"

    def __init__(self, version_manager, data=None):
        self.version_manager = version_manager
        self.prestashop_versions = data

    def fetch_prestashop_versions(self):
        if self.prestashop_versions is None:
            response = requests.get(self.PRESTASHOP_API_URL)
            response.raise_for_status()
            self.prestashop_versions = response.json()

        return self.prestashop_versions

    def get_download_url_of(self, version):
        prestashop_versions = self.fetch_prestashop_versions()

        for entry in prestashop_versions:
            if version == self.version_manager.create_version_from_distribution_api(entry.get('version'), entry.get('distribution'), entry.get('distribution_version')):
                return entry.get('zip_download_url')
