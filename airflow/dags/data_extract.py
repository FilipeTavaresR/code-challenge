from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_extractor',  
    default_args=default_args,
    description='Pipeline para extração dos dados de arquivos CSV e tabelas de banco de dados postgres e gravar em um repositório local',
    schedule_interval='45 16 * * *',  
    catchup=False,  
)

run_meltano = BashOperator(
    task_id='data_extractor',
    bash_command='cd ~/meus_projetos/databaseextractor/ && meltano run all', 
    dag=dag,
)

run_meltano