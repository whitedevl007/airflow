import airflow 
from datetime import timedelta 
from airflow import DAG 
from datetime import datetime, timedelta 
from airflow.operators.python import PythonOperator 
from airflow.operators.email import EmailOperator


default_args = { 
'owner': 'airflow', 
#'start_date': airflow.utils.dates.days_ago(2), 
# 'end_date': datetime(), 
# 'depends_on_past': False, 
# 'email': ['airflow@example.com'], 
# 'email_on_failure': False, 
#'email_on_retry': False, 
# If a task fails, retry it once after waiting 
# at least 5 minutes 
#'retries': 1, 'retry_delay': timedelta(minutes=5), 
}

dag_email = DAG( 
dag_id = 'emailoperator_demo1', 
default_args=default_args, 
schedule_interval='@once', 
dagrun_timeout=timedelta(minutes=60), 
description='use case of email operator in airflow', 
start_date = airflow.utils.dates.days_ago(1))

def start_task(): 
    print("task started") 

start_task = PythonOperator( 
task_id='executetask', 
python_callable=start_task, 
dag=dag_email) 

send_email = EmailOperator( 
task_id='send_email', 
to='officialark11@gmail.com', 
subject='ingestion complete', 
html_content="Date: {{ ds }}", 
dag=dag_email)

send_email.set_upstream(start_task) 

if __name__ == "__main__":
    dag_email.cli()