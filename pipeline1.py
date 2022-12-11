from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import requests as r 
import json
import mysql.connector
import pendulum
# Pega o cambio e guarda num ficheiro JSON na pasta onde os algoritimos estão a rodar
def getCambioEuroSendByEmail():
    euro_to_any = r.get ("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/eur.json").json()
    UMeuroToAOA = euro_to_any['eur']['aoa']    
    servername = "db4free.net"
    dbname = "conferencia"
    username = "jchilela"
    password = "admin@2022"
   
    
    mydb = mysql.connector.connect(
      host=servername,
      user=username,
      password=password,
      database=dbname
    )
    
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO cambiosConf (valor) VALUES ( '" + str(UMeuroToAOA) +  "')"
    
    mycursor.execute(sql)
    
    mydb.commit()


def enviarEmail():
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText
    
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    msg={}
    me ='geral@'
    you ='juliochilela@gmail.com'
    msg['Subject'] = 'The contents of '
    msg['From'] = 'geral@'
    msg['To'] = 'juliochilela@gmail.com'
    
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    print("email enviado")


dag = DAG('insereCambio', description='Insere cambio no mysql',
          schedule_interval='0 * * * *',
          start_date=datetime(2022, 12, 8), catchup=False)

tarefa1 = PythonOperator(task_id='tarefa1', python_callable=getCambioEuroSendByEmail, dag=dag)

tarefa2 = PythonOperator(task_id='tarefa2', python_callable=enviarEmail, dag=dag)

tarefa1 >> tarefa2