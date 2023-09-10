from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException
import requests
from typing import Any


class PeliqanHook(BaseHook):

    conn_name_attr = "peliqan_conn_id"
    default_conn_name = "peliqan_api_default"
    conn_type = "peliqan"
    hook_name = "Peliqan"

    def __init__(
            self,
            *,
            peliqan_conn_id: str = "peliqan_api_defalut",
            ) -> None:

        super().__init__()
        self.peliqan_conn_id = peliqan_conn_id

    def get_url(self):
        conn = self.get_connection(self.peliqan_conn_id)
        if not conn.host:
            raise AirflowNotFoundException(
                    f"Connection ID {self.peliqan_conn_id} does not have base_url"
                    )
        url = conn.host
        return url

    def get_jwt(self):
        conn = self.get_connection(self.peliqan_conn_id)
        if not conn.password:
            raise AirflowNotFoundException(
                    f"Connection ID {self.peliqan_conn_id} does not have password (Peliqan API Token)"
                    )
        token = conn.password
        return token

    def submit_job(self, script_id):
        token = self.get_jwt()
        base_url = self.get_url()
        auth_header = {"Authorization": f"JWT {token}"}
        endpoint = f"api/interfaces/{script_id}/schedule_run/"
        url = f"{base_url}{endpoint}"
        response = requests.post(url, headers=auth_header)

        return response

    def get_job(self, job_id):

        token = self.get_jwt()
        base_url = self.get_url()
        auth_header = {"Authorization": f"JWT {token}"}
        endpoint = f"api/interfaces/schedule_run/{job_id}"
        url = f"{base_url}{endpoint}"
        response = requests.get(url, headers=auth_header)

        return response

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        """Returns custom field behaviour."""
        return {
            "hidden_fields": ["login", "port", "schema", "extra"],
            "relabeling": {
                "password": "Peliqan API Token",
                "host": "Base url",
            },
            "placeholders": {
                "password": "<your-token> don't include `JWT` just token",
                "host": "https://app.eu.peliqan.io/",
            },
        }
