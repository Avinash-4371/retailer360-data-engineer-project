from airflow.decorators import dag, task
from pendulum import datetime

@dag(
    dag_id="simple_print_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example"],
)
def simple_dag_builder():
    
    @task
    def print_message():
        message = "Simple!"
        print(message)
        return message
    
    print_message()


simple_dag_builder()