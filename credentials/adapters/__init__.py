from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from credentials.settings import Settings

class Database:
    def __init__(self, settings: Settings):
        self.engine = create_engine(url=settings.database.uri)
        
    def setup(self):
        self.connection = self.engine.connect()
        self.sessionmaker = sessionmaker(bind=self.connection)

    def teardown(self):
        self.connection.close()
        self.engine.dispose()