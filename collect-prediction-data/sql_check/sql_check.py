from sqlalchemy import create_engine
from sqlalchemy.sql import text

pgusername = "<postgres-username>"
pgpassword = "<postgres-password>"
pgendpoints = "<postgres-service-endpoints>"

engine = create_engine(
    'postgresql://{}:{}@{}'.format(pgusername, pgpassword, pgendpoints), echo=True)

with engine.connect() as con:
    statement = text("""SELECT * FROM prediction;""")
    rs = con.execute(statement)

    for row in rs:
        print(row)
