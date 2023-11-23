from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from monitoring import monitoring_workflow

# Аргументы для DAG
default_args = {
    'owner': 'tunsmm',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

dag = DAG(
    'monitoring_dag',
    default_args=default_args,
    description='DAG for monitoring and copying files',
    # schedule_interval=timedelta(minutes=5),
    schedule_interval=timedelta(minutes=1),
)

# Определение PythonOperator для выполнения задачи мониторинга
# Оператор task_monitoring будет выполнять мониторинг при запуске DAG
task_monitoring = PythonOperator(
    task_id='task_monitoring',
    python_callable=monitoring_workflow,
    dag=dag,
)
