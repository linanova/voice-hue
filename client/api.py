import os
from typing import Any, Optional, Dict

import requests


class Api():
    def __init__(self):
        self.url = os.getenv('API_BASE_URL')
        self.api_key = os.getenv('API_KEY')

    def _request(self,
                 method: str,
                 url: str,
                 data: Optional[Dict] = None,
                 params: Optional[Dict] = None,
                 headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        if headers is None:
            headers = {}

        try:
            response = requests.request(
                method,
                url,
                json=data,
                params=params,
                headers={
                    'Authorization': self.api_key,
                    **headers
                }
            )
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during {method} request to {url}: {e}")

    def get(self,
            endpoint: str,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        return self._request('GET', f'{self.url}/{endpoint}', params=params, headers=headers)

    def post(self,
             endpoint: str,
             data: Dict,
             headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        return self._request('POST', f'{self.url}/{endpoint}', data=data, headers=headers)
