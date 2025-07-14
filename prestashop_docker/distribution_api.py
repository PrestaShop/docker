import requests


class DistributionApi():
    PRESTASHOP_API_URL = "https://api.prestashop-project.org/prestashop"

    def fetch_prestashop_versions(self):
        response = requests.get(self.PRESTASHOP_API_URL)
        response.raise_for_status()
        return response.json()
