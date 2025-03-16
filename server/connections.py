from sqlalchemy import create_engine
from sqlalchemy import Engine, Connection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from server.settings import Settings

class Database:
    engine: Engine
    connection: Connection
    
    def __init__(self, settings: Settings):
        self.engine = create_engine(url=settings.database.uri)
        
    def setup(self):
        self.connection = self.engine.connect()
        self.sessionmaker = sessionmaker(bind=self.connection)

    def teardown(self):
        self.connection.close()
        self.engine.dispose()
        

class Connections:
    sql: Session

    def __init__(self, database: Database,):
        self.database = database
    
    def __enter__(self):
        self.sql = self.database.sessionmaker()

        self.sql.begin()
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            self.sql.rollback()
        else:
            self.sql.commit()
        self.sql.close()