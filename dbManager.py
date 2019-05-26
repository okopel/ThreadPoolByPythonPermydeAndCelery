import os.path
from threading import Lock

from sqlalchemy import select, create_engine, MetaData, Table, Column, String, Integer

import config as settings

mutex = Lock()


class DbManager:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DbManager.__instance is None:
            DbManager()
        return DbManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DbManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DbManager.__instance = self

        self.engine = create_engine('sqlite:///' + settings.client_data_path)
        metadata_client_data = MetaData(self.engine)
        self.table = Table(settings.client_data_name, metadata_client_data,
                           Column('id', Integer, primary_key=True),
                           Column('raw_data', String),
                           Column('result', String), autoload=True)
        # create the DB just if It does not exist
        if not os.path.exists(settings.client_data_path):
            self.table.create()

    def executeEngine(self, msg):
        mutex.acquire()
        ans = self.engine.execute(msg)
        mutex.release()
        return ans

    def insertEx(self, r_id, raw_d):
        msg = self.table.insert().values(id=r_id, raw_data=raw_d, result=settings.tmp_var_name)
        try:
            self.executeEngine(msg)
            return 0
        except:
            return 1

    def getById(self, r_id):
        msg = select([self.table.c.result]).where(self.table.c.id == r_id)
        ans = self.executeEngine(msg)
        return ans.scalar()

    def uploadResById(self, r_id, ans):
        msg = self.table.update().values(result=str(ans)).where(self.table.columns.id == r_id)
        self.executeEngine(msg)
