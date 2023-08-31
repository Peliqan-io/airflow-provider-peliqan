from airflow import DAG
import pendulum

from peliqan_provider.operators.peliqan import PeliqanOperator
from peliqan_provider.sensors.peliqan import PeliqanSensor


with DAG(
        dag_id="peliqan_test_dag",
        schedule=None,
        start_date=pendulum.datetime(2023, 1, 1),
        tags=['exaple_peliqan_dag']
        ):

    peliqan_script_32 = PeliqanOperator(
            task_id='script53',
            peliqan_conn_id='peliqan_default',
            script_id=32,
            )

    peliqan_poll_32 = PeliqanSensor(
            task_id='poll53',
            peliqan_conn_id='peliqan_default',
            job_id=peliqan_script_32.output,
            poke_interval=5,
            timeout=15,
            )

peliqan_script_32 >> peliqan_poll_32
