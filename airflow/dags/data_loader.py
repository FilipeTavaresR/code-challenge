from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),  
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_loader',  
    default_args=default_args,
    description='Pipeline para extrair dados de arquivos CSV e carregar em tabelas de banco de dados postgres',
    schedule_interval='00 17 * * *',  
    catchup=False,  
)

# Função para obter o valor de testedata das variáveis do airflow
def get_testedata(**kwargs):
    testedata = Variable.get("testedata", default_var=None)
    
    # Se não estiver definida, usa a data atual
    if not testedata:
        testedata = kwargs['ds'] 
    
    return testedata

# Tarefa para executar a função de recuperar testdata
get_testedata_task = PythonOperator(
    task_id='get_testedata',
    python_callable=get_testedata,
    provide_context=True,  
    dag=dag,
)

# Tarefa para rodar o Meltano
run_meltano = BashOperator(
    task_id='data_loader',
    bash_command='cd ~/meus_projetos/dbloader/ && LOAD_DATE={{ ti.xcom_pull(task_ids="get_testedata") }} meltano run all',
    dag=dag,
)

# Defina a ordem das tarefas
get_testedata_task >> run_meltano