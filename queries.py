import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

global connection_string
connection_string = os.getenv('CONNECTION_STRING')

def insert_allert_to_db(allert,allert_datetime):
    try:
        # Conexão com o banco de dados
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Inserts na tabela de Avisos
        cursor.execute("""
            INSERT INTO Avisos (Aviso, DtCriacao, StatusID,DtAviso)
                VALUES (?, GETDATE(), 1,?);
        """,allert,allert_datetime)
        cursor.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while inserting the allert: {e}")

def select_allerts_from_db():
    try:
        # Conexão com o banco de dados
        conn = pyodbc.connect(
            connection_string)
        cursor = conn.cursor()

        # Select dos avisos pendentes e finalizados
        cursor.execute("""
            SELECT AvisoID Código, Aviso, DtCriacao Data_Criação, DtFinalizado Data_Finalização, DtAviso Data_Aviso, StatusID Status FROM Avisos
                WHERE StatusID IN (1,2);
        """)
        # Armazenar os resultados em um DataFrame do Pandas
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        conn.close()
        return df
    except Exception as e:
        print(f"An error occurred while inserting the allert: {e}")

def select_allerts_from_db_by_id(allert_id):
    try:
        # Conexão com o banco de dados
        conn = pyodbc.connect(
            connection_string)
        cursor = conn.cursor()

        # Select dos avisos pendentes e finalizados
        cursor.execute("""
            SELECT AvisoID Código, Aviso, DtCriacao Data_Criação, DtFinalizado Data_Finalização, DtAviso Data_Aviso, StatusID Status FROM Avisos
                WHERE AvisoID = ?;
        """,allert_id)
        # Armazenar os resultados em um DataFrame do Pandas
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        conn.close()
        return df
    except Exception as e:
        print(f"An error occurred while inserting the allert: {e}")

def select_canceled_allerts_from_db():
    try:
        conn = pyodbc.connect(
            connection_string)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AvisoID Código, Aviso, DtCriacao Data_Criação, DtFinalizado Data_Finalização, DtAviso Data_Aviso, StatusID Status FROM Avisos
                WHERE StatusID = 3;
        """)

        df = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
        conn.close()
        return df
    except Exception as e:
        print(f"An error occurred while inserting the allert: {e}")

def update_allert_status_in_db(allert,statusID):
    try:
        # Conexão com o banco de dados
        conn = pyodbc.connect(
            connection_string)
        cursor = conn.cursor()

        # Update na tabela de Avisos
        cursor.execute("""
            UPDATE AVisos SET StatusId = ?, DtFinalizado = GETDATE() WHERE AvisoID = ?;
        """,statusID,allert)
        cursor.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while inserting the allert: {e}")

def select_pending_allerts_from_db():
    try:
        conn = pyodbc.connect(
            connection_string)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AvisoID Código, Aviso, StatusID Status, DtAviso Data_Aviso From Avisos
                WHERE StatusID = 1;
        """)

        df = pd.DataFrame.from_records(cursor.fetchall(),columns=[desc[0] for desc in cursor.description])
        conn.close()
        return df
    except Exception as e:
        print(f"An error occurred while selecting the allert: {e}")
        return pd.DataFrame()
