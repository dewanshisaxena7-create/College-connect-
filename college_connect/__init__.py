import pymysql

# This ensures Django's MySQL backend can use pure-python PyMySQL
pymysql.install_as_MySQLdb()
