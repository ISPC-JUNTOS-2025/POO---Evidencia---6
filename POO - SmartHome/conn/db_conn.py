import mysql.connector
from mysql.connector import errorcode
import configparser
import pathlib


class DBConn:
    def __init__(self, config_file="config.ini"):
        self.conn = None
        self.cursor = None
        self.db_params = {} 
        
        if config_file:
            config_parser = configparser.ConfigParser()
            try:
                config_path = pathlib.Path(__file__).parent.parent / config_file 
                config_parser.read(config_path)
                self.db_params = {
                    'user': config_parser['database']['user'],
                    'password': config_parser['database']['password'],
                    'host': config_parser['database']['host'],
                    'port': int(config_parser['database']['port']), 
                    'database': config_parser['database']['database']
                }
            except KeyError as e:
                raise ValueError(f"Falta la sección 'database' o una clave en config.ini: {e}")
            except FileNotFoundError:
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_file}")


    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.db_params)
            return self.conn  
        except mysql.connector.Error as err:
            raise err
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            
        if self.conn:
            self.conn.close()