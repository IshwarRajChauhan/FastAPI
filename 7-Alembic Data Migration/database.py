from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#---------------------------------------------------------
#For sqlite3

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

#---------------------------------------------------------
#For PostgreSQL

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@localhost/TodoApplicationDatabase'  
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

#---------------------------------------------------------
#For MySQL
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Admin123!@127.0.0.1:3306/todoapplicationdatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)







SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()










