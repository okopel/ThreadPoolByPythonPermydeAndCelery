import os.path
from threading import Lock

from sqlalchemy import select, create_engine, MetaData, Table, Column, String, Integer

import config as settings

mutex = Lock()


# DB class, singleton
class DbManager:
    __instance = None

    @staticmethod
    def getInstance():
        if DbManager.__instance is None:
            DbManager()
        return DbManager.__instance

    # Virtually private constructor
    def __init__(self):

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

    # execute task to the db engine
    def executeEngine(self, msg):
        ans = None
        mutex.acquire()  # mutex to avoid race condition
        try:
            ans = self.engine.execute(msg)
        except Exception as e:
            print(e)
            ans = None
        finally:
            mutex.release()
            return ans

    # insert the id  & raw data to the db
    # result will be "wait" flag until calculating
    # return 0 if success, 1 for an error
    def insertEx(self, r_id, raw_d):
        msg = self.table.insert().values(id=r_id, raw_data=raw_d, result=settings.tmp_var_name)
        ans = self.executeEngine(msg)
        if ans is None:  # exception case
            return 1
        else:
            return 0

    # get the result from the DB by ID
    def getResById(self, r_id):
        msg = select([self.table.c.result]).where(self.table.c.id == r_id)
        ans = self.executeEngine(msg)
        if ans == settings.tmp_var_name:  # The result doest ready yet
            return ans
        elif ans is not None:
            return ans.scalar()
        else:  # None case->exception
            return None

    # save the result in the db
    def uploadResById(self, r_id, ans):
        msg = self.table.update().values(result=str(ans)).where(self.table.columns.id == r_id)
        self.executeEngine(msg)
