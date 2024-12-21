from datetime import timedelta

from config.settings import DEFAULT_DAG_ARGS, DIRECTORY_TO_MONITOR

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from create_files import create_files_workflow
from monitoring import monitoring_workflow

with DAG(
    dag_id="monitoring_dag",
    default_args=DEFAULT_DAG_ARGS,
    description="DAG for monitoring files",
    schedule_interval=timedelta(seconds=10),
):
    task_monitoring = PythonOperator(
        task_id="task_monitoring",
        python_callable=monitoring_workflow,
    )


with DAG(
    "creating_files_dag",
    default_args=DEFAULT_DAG_ARGS,
    description="DAG for creating files",
    schedule_interval=timedelta(seconds=10),
):
    # Определение вспомогательного PythonOperator для создания файлов
    task_creating = PythonOperator(
        task_id="task_create_files",
        python_callable=create_files_workflow,
        op_kwargs={
            "directory": DIRECTORY_TO_MONITOR,
            "num_files": 1,
            "file_size_range": (10_000_000, 50_000_000),
            "change_file_content_index": 2,
        },
    )
