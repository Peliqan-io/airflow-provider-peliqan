from __future__ import annotations
from unittest import mock
import unittest
import logging

from peliqan_provider.sensors.peliqan import PeliqanSensor

logger = logging.getLogger()


class TestPeliqanSensor(unittest.TestCase):

    task_id = "task-id"
    peliqan_conn_id = "peliqan-conn-test"
    job_id = 1
    timeout = 120

    def get_job(self, status):
        response = mock.Mock()
        response.json.return_value = {"status": status}
        return response

    @mock.patch("peliqan_provider.hooks.peliqan.PeliqanHook.get_job")
    def test_done(self, mock_get_job):
        mock_get_job.return_value = self.get_job("finished")

        sensor = PeliqanSensor(
            task_id=self.task_id,
            job_id=self.job_id,
            peliqan_conn_id=self.peliqan_conn_id,
        )
        ret = sensor.poke(context={})

        mock_get_job.assert_called_once_with(job_id=self.job_id)

        self.assertEqual(ret, True)

    @mock.patch("peliqan_provider.hooks.peliqan.PeliqanHook.get_job")
    def test_running(self, mock_get_job):
        mock_get_job.return_value = self.get_job("running")

        sensor = PeliqanSensor(
            task_id=self.task_id,
            job_id=self.job_id,
            peliqan_conn_id=self.peliqan_conn_id,
        )
        ret = sensor.poke(context={})

        mock_get_job.assert_called_once_with(job_id=self.job_id)

        self.assertEqual(ret, False)
