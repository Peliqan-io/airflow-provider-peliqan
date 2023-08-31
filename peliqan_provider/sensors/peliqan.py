from typing import TYPE_CHECKING, Sequence

from airflow.sensors.base import BaseSensorOperator
from peliqan_provider.hooks.peliqan import PeliqanHook

from airflow.utils.context import Context

# if TYPE_CHECKING:
#   from airflow.utils.context import Context


class PeliqanSensor(BaseSensorOperator):
    """
    Check for the state of a previously submitted Peliqan job.

    :param peliqan_conn_id: Required. The name of the Peliqan connection to get
        connection information for Peliqan Defaults to "peliqan_default".
    :param job_id: Required. Id of the Peliqan job
    """

    template_fields: Sequence[str] = ("job_id",)

    def __init__(
            self,
            peliqan_conn_id,
            job_id,
            **kwargs,
            ) -> None:
        super().__init__(**kwargs)
        self.peliqan_conn_id = peliqan_conn_id
        self.job_id = job_id

    def poke(self, context: Context) -> bool:
        self.log.info(f"Poking peliqan job {self.job_id}")

        hook = PeliqanHook(peliqan_conn_id=self.peliqan_conn_id)
        job_object = hook.get_job(job_id=self.job_id)
        status = job_object.json()["status"]

        if status == "running":
            self.log.info(f"Waiting for job {self.job_id} to complete.")
            return False

        self.log.info(f"Job {self.job_id} Finished.")

        return True
