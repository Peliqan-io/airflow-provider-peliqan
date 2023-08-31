from typing import TYPE_CHECKING, Sequence

from airflow.models import BaseOperator
from peliqan_provider.hooks.peliqan import PeliqanHook

# if TYPE_CHECKING:
from airflow.utils.context import Context


class PeliqanOperator(BaseOperator):
    """
    Execute Peliqan API Resource.

    ..code-block :: Python

    peliqan = PeliqanOperator(
            task_id="script53",
            peliqan_conn_id="peliqan_default",
            dag=dag,
            script_id=53,
            )

    :param script_id: script ID of the python file you want to run on
           peliqan cloud.
    """

    template_fields: Sequence[str] = ("script_id",)

    def __init__(
            self,
            script_id: int,
            peliqan_conn_id: str = "peliqan_default",
            **kwargs
            ) -> None:

        super().__init__(**kwargs)
        self.script_id = script_id
        self.peliqan_conn_id = peliqan_conn_id

    def execute(self, context: Context) -> None:

        self.hook = PeliqanHook(peliqan_conn_id=self.peliqan_conn_id)
        job_object = self.hook.submit_job(script_id=self.script_id)
        self.job_id = job_object.json()["id"]

        return self.job_id
