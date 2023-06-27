# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
# import subprocess

# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2023, 5, 16),
# }

# dag = DAG('storm_topo', default_args=default_args, schedule_interval=None)


# def read_from_mongodb_and_send_to_kafka():
#     try:
#         bash_command = 'cd /home/nizam/project/project/storm/project/my_project && python3 mongothenga.py'
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise


# def submit_topology():
#     try:
#         bash_command = 'cd /home/nizam/project/Kafka-Storm && sparse run --name first_topology'
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise


# read_task = TriggerDagRunOperator(
#     task_id='read_task',
#     trigger_dag_id='storm_topo',
#     dag=dag,
# )

# submit_task = TriggerDagRunOperator(
#     task_id='submit_task',
#     trigger_dag_id='storm_topo',
#     dag=dag,
# )

# # Remove the dependency between read_task and submit_task
# read_task
# submit_task





##################################################################################


# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python import BranchPythonOperator, PythonOperator
# import subprocess

# default_args = {
#     'owner': 'airflow',
#     'start_date': datetime(2023, 5, 16),
# }

# dag = DAG('storm_topoo', default_args=default_args, schedule=None)


# def read_from_mongodb_and_send_to_kafka():
#     try:
#         bash_command = 'cd /home/nizam/airflow/dags/Kafka-Storm/Necessary_Scripts && python3 producer2.py'
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise


# def submit_topology():
#     try:
#         bash_command = 'cd /home/nizam/airflow/dags/Kafka-Storm && sparse run --name first_topology'
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise

# def run_hdfsread():
#     try:
#         bash_command = 'cd /home/nizam/airflow/dags && python3 hdfsread.py'
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise
    
# def decide_next_task(**kwargs):
#     return ['read_task', 'submit_task','run_hdfsread_task']


# decision_task = BranchPythonOperator(
#     task_id='decision_task',
#     python_callable=decide_next_task,
#     dag=dag,
# )

# read_task = PythonOperator(
#     task_id='read_task',
#     python_callable=read_from_mongodb_and_send_to_kafka,
#     dag=dag,
# )

# submit_task = PythonOperator(
#     task_id='submit_task',
#     python_callable=submit_topology,
#     dag=dag,
# )
# run_hdfsread_task = PythonOperator(
#     task_id='run_hdfsread_task',
#     python_callable=run_hdfsread,
#     dag=dag,
# )

# decision_task >> [read_task, submit_task,run_hdfsread_task]








from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.operators.email import EmailOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 16),
}

dag = DAG('storm_top', default_args=default_args, schedule=None)


def read_from_mongodb_and_send_to_kafka():
    try:
        bash_command = 'cd /home/nizam/airflow/dags/Kafka-Storm/Necessary_Scripts && python3 producer2.py'
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


def submit_topology():
    try:
        bash_command = 'cd /home/nizam/airflow/dags/Kafka-Storm && sparse run --name first_topology'
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def run_hdfsread():
    try:
        bash_command = 'cd /home/nizam/airflow/dags && python3 hdfsread.py'
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', bash_command])
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    
def decide_next_task(**kwargs):
    return ['read_task', 'submit_task', 'run_hdfsread_task']


def send_email(to, subject, html_content):
    try:
        email_operator = EmailOperator(
            task_id='send_email',
            to=to,
            subject=subject,
            html_content=html_content,
            dag=dag
        )
        email_operator.execute(context=None)
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")
        raise


decision_task = BranchPythonOperator(
    task_id='decision_task',
    python_callable=decide_next_task,
    dag=dag,
)

read_task = PythonOperator(
    task_id='read_task',
    python_callable=read_from_mongodb_and_send_to_kafka,
    dag=dag,
)

submit_task = PythonOperator(
    task_id='submit_task',
    python_callable=submit_topology,
    dag=dag,
)

run_hdfsread_task = PythonOperator(
    task_id='run_hdfsread_task',
    python_callable=run_hdfsread,
    dag=dag,
)

decision_task >> [read_task, submit_task, run_hdfsread_task]

# Set up the email notification after the DAG completes
send_email_task = PythonOperator(
    task_id='send_email_task',
    python_callable=send_email,
    op_args=['officialark11@gmail.com', 'DAG Execution Report', 'The DAG execution has completed.'],
    dag=dag,
)

[read_task, submit_task, run_hdfsread_task] >> send_email_task













