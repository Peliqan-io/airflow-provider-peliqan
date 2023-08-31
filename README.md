# Airflow Peliqan Provider

Peliqan is an all-in-one data platform for business teams, data teams and developers. Instantly connect to your apps and databases, use your favourite BI tool,
and sync data between your apps.


## Package description

This package provides the common `PeliqanHook` class, the abstract 
`PeliqanOperator`, the `PeliqanSensor` to run script on peliqan and poll running scripts.

## Installation 

#### Using PypI

```bash
pip install airflow-peliqan-provider
```

## Setting up Peliqan Provider in Apache Airflow

Follow these steps to configure the Peliqan provider in Apache Airflow using the web UI.

### Step 1: Add a Provider

1. Open the Apache Airflow web UI.

2. Navigate to the "Admin" section.

3. Click on "Connections."

4. Click on the "Create" button to add a new provider.

### Step 2: Configure the Connection

Fill in the following details:

- **Connection ID**: Choose a unique identifier for your Peliqan connection (e.g., "my_peliqan_connection").

- **Connection Type**: Select "Peliqan" from the dropdown.

- **Peliqan API Token**: Obtain your Peliqan API token starting with ey from the Peliqan platform.

- **Base URL**: Provide the base URL on which API calls will be made. 
### Step 3: Save the Connection

Click the "Save" button to save your Peliqan provider connection.

Now, you can use this connection in your Apache Airflow DAGs to interact with the Peliqan API.

Example usage in an Airflow DAG:

```python
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
```

That's it! You've successfully configured a Peliqan provider in Apache Airflow and can now use it in your DAGs to make API calls to Peliqan.

## Dependencies

Python >= 3.8

| Package            | Version |
|--------------------|---------|
| requests           | 2.31.0  |
| airflow            | 2.4.0   |


