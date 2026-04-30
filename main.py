from db.sqlitedb import SqliteDB

sql = SqliteDB("projecttracker.db")
sql.CreateTable()
insert_query = '''
SELECT * FROM PROJECTS
'''
rows = sql.SelectQuery(insert_query)
for row in rows:
    print(row)



