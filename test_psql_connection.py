import psycopg2
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://daniellee@127.0.0.1/eiademand')

# conn = psycopg2.connect(
#     host="localhost",
#     database="macrosignals",
#     user="daniellee")

# cur = conn.cursor()
# cur.execute("SELECT * FROM Temp;")
# print(cur.fetchone())

# df_temp = pd.DataFrame({'col1': [4], 'col2': [5]})
# df_temp.to_sql('temp2', engine, if_exists='replace')

data = [
	{"index": 1, "col1": 2, "col2": 3},
	{"index": 2, "col1": 2, "col2": 3},
	{"index": 3, "col1": 2, "col2": 3},
]

query = ("INSERT INTO temp2 (index, col1, col2)"
			"VALUES (%(index)s, %(col1)s, %(col2)s)") 

# print(engine.execute("SELECT * FROM temp2;").fetchone())
engine.execute(query, data)





# import psycopg2

    
# data = [
#         {"name": "samplename", "group": "samplegroup", "timestamp": sampletimestamp,
#             "totaltime": sampletotaltime, "errorcode": sampleerrorcode},
#         {"name": "samplename", "group": "samplegroup", "timestamp": sampletimestamp,
#             "totaltime": sampletotaltime, "errorcode": sampleerrorcode},
#         {"name": "samplename", "group": "samplegroup", "timestamp": sampletimestamp,
#             "totaltime": sampletotaltime, "errorcode": sampleerrorcode},
#         {"name": "samplename", "group": "samplegroup", "timestamp": sampletimestamp,
#             "totaltime": sampletotaltime, "errorcode": sampleerrorcode}
# ]


# db = psycopg2.connect("dbname='my_database' user='user' password='password'")   
# cursor = db.cursor() 
# cursor.executemany(
#     'INSERT INTO mytable (name, group, timestamp, totaltime, errorcode) '
#     'VALUES (%(name)s, %(group)s, %(timestamp)s, %(totaltime)s, %(errorcode)s)',
#     data
# )