from __future__ import annotations
import logging

from airflow.models import Connection
from airflow.utils import db
from peliqan_provider.hooks.peliqan import PeliqanHook

import requests_mock
import unittest

conn = Connection(
        conn_id="peliqan_conn_id_test",
        conn_type="peliqan",
        password="jwt",
        host="https://staging.peliqan.io/",
        )

db.merge_conn(conn)
# conn_uri = conn.get_uri()

logger = logging.getLogger()


class TestPeliqanHook(unittest.TestCase):
    """
    Test all functions from Peliqan Hook
    """

    peliqan_conn_id = "peliqan_conn_id_test"
    script_id = "3"
    job_id = 1
    submit_job_endpoint = f"https://staging.peliqan.io/api/interfaces/{script_id}/schedule_run/"
    get_job_endpoint = f"https://staging.peliqan.io/api/interfaces/schedule_run/{job_id}"

    _mock_submit_job_success_response_body = {"id": 1}
    _mock_get_job_status_success_response_body = {"status": "finished"}
    _mock_get_job_status_running_response_body = {"status": "running"}

    @requests_mock.mock()
    def test_submit_job(self, requests_mock):
        requests_mock.post(
            self.submit_job_endpoint, status_code=200, json=self._mock_submit_job_success_response_body
        )
        self.hook = PeliqanHook(peliqan_conn_id=self.peliqan_conn_id)
        resp = self.hook.submit_job(script_id=self.script_id)
        logger.info(f"Submited Peliqan job with job_id {resp.json()} ")
        assert resp.status_code == 200
        assert resp.json() == self._mock_submit_job_success_response_body

    @requests_mock.mock()
    def test_get_job_status(self, requests_mock):
        requests_mock.get(
            self.get_job_endpoint, status_code=200, json=self._mock_get_job_status_success_response_body
        )
        self.hook = PeliqanHook(peliqan_conn_id=self.peliqan_conn_id)
        resp = self.hook.get_job(job_id=self.job_id)
        logger.info("Poking Peliqan job %s", self.job_id)
        logger.info(f"get job response {resp.json()}")
        assert resp.status_code == 200
        assert resp.json() == self._mock_get_job_status_running_response_body
