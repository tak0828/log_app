# PyMySQLをMySQLdbとして使用
import pymysql

# Django 6.0のバージョンチェックに対応
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

