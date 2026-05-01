from DataFields.DataField import IntegerType,PositiveInteger,StringField,DateField,ProjectStatus
from db.sqlitedb import SqliteDB
from DataFields.generic_values import GenericValue

class InstallationModule:
    db = SqliteDB(GenericValue.project_tracker_db)
    def __init__(self):
        self.db.CreateTable()