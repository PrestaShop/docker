import requests


class DistributionApi():
    PRESTASHOP_API_URL = "https://api.prestashop-project.org/prestashop"

    def __init__(self):
        response = requests.get(self.PRESTASHOP_API_URL)
        response.raise_for_status()
        self.prestashop_versions = response.json()

    def fetch_prestashop_versions(self):
        return self.prestashop_versions

    def get_download_url_of(self, version):
        for entry in self.prestashop_versions:
            if version == entry.get('version'):
                return entry.get('zip_download_url')
        return None
