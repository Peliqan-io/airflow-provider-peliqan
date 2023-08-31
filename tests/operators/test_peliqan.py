from __future__ import annotations

import unittest
from unittest import mock

from peliqan_provider.operators.peliqan import PeliqanOperator


class TestPeliqanOperator(unittest.TestCase):
    """
    Test execute function from Peliqan Operator
    """

    peliqan_conn_id = "test_peliqan_conn_id"
    script_id = 3
    job_id = 1

    @mock.patch("peliqan_provider.hooks.peliqan.PeliqanHook.submit_job")
    def test_execute(self, mock_submit_job):
        mock_submit_job.return_value = mock.Mock(
                **{"json.return_value":  {"id": self.job_id}}
                )

        op = PeliqanOperator(
                task_id="test_peliqan_op",
                peliqan_conn_id=self.peliqan_conn_id,
                script_id=self.script_id,
                )
        op.execute({})

        mock_submit_job.assert_called_once_with(script_id=self.script_id)
