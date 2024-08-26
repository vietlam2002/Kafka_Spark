from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

cluster = Cluster(['cassandra'])
session = cluster.connect()
rows = session.execute('SELECT * FROM system_schema.columns limit 3;')
for row in rows:
    print(row.keyspace_name + ", " + row.table_name + ", " + row.column_name)
cluster.shutdown()
