from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

#since the airflow.cfg document define dags_folder = '/Users/shuting/airflow/dags' locally,
#the dag.py need to be put in the user defined dag folder to successfully run the code.

# Define DAG parameters
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 2),
    'retries': 1,
}

# Create DAG
dag = DAG(
    dag_id='heroku_dash_dag',
    default_args=default_args,
    description='A simple DAG to trigger Heroku Dash App',
    schedule_interval='* * * * *',  # Run every minute
    catchup=False,  # Don't catch up on missed runs
)

# Define tasks
trigger_heroku_dash = HttpOperator(
    task_id='trigger_heroku_dash',
    method='GET',
    http_conn_id='heroku_dash_app',
    endpoint='/', # Replace with the relative path of your Heroku app, or '/' if it is the root path
    dag=dag,
)

def print_message():
    print("Dashboard Page2 has been opened.")

python_task = PythonOperator(
    task_id="print_message",
    python_callable=print_message,
    dag=dag,
)

# Add tasks to the DAG
trigger_heroku_dash >> python_task
