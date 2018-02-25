import mysql.connector
from mysql.connector import errorcode
from Database import config
from Database import DATABASE

class ConnectionFactory(object):

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**config)
            self.connection.database = DATABASE
        except mysql.connector.Error as e:
            print e.msg        

    def getConnection(self):
        return self.connection
