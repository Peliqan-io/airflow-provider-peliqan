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
            base_url: str = "https://app.eu.peliqan.io/",
            ) -> None:

        super().__init__()
        self.peliqan_conn_id = peliqan_conn_id
        self.base_url = base_url

    def set_url(self):
        conn = self.get_connection(self.peliqan_conn_id)
        if not conn.base_url:
            raise AirflowNotFoundException(
                    f"Connection ID {self.peliqan_conn_id} does not have base_url"
                    )
        url = conn.base_url
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
        auth_header = {"Authorization": f"JWT {token}"}
        endpoint = f"api/interfaces/{script_id}/schedule_run/"
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=auth_header)

        return response

    def get_job(self, job_id):

        token = self.get_jwt()
        auth_header = {"Authorization": f"JWT {token}"}
        endpoint = f"api/interfaces/schedule_run/{job_id}"
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=auth_header)

        return response

    @classmethod
    def get_connection_form_widgets(cls) -> dict[str, Any]:
        """Returns dictionary of widgets to be added for the hook to handle extra values."""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import StringField

        return {
            "base_url": StringField(
                lazy_gettext("Base URL"),
                widget=BS3TextFieldWidget(),
                description="Optional. A string representing the Peliqan API base URL.",
            ),
        }

    @classmethod
    def get_ui_field_behaviour(cls) -> dict[str, Any]:
        """Returns custom field behaviour."""
        return {
            "hidden_fields": ["login", "port", "host", "schema", "extra"],
            "relabeling": {
                "password": "Peliqan API Token",
            },
            "placeholders": {
                "password": "<your-token> don't include `JWT` just token",
                "base_url": "https://app.eu.peliqan.io/",
            },
        }
