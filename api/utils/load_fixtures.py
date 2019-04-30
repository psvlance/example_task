import sys
import os

import psycopg2


def gen_collection_name(filename: str):
    rst = filename.split('/')[-1]
    rst = rst.split('.')[0]
    return rst


def get_db_connector():
    try:
        connection = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
    except psycopg2.OperationalError:
        connection = None
    return connection

def type_of(str):
    # TODO: hack beause of we know structure
    TYPES = {
        'date': 'date',
        'channel': 'varchar(255)',
        'country': 'varchar(255)',
        'os': 'varchar(255)',
        'impressions': 'int',
        'clicks': 'int',
        'installs': 'int',
        'spend': 'decimal(12,2)',
        'revenue': 'decimal(12,2)',
    }

    return TYPES[str]


def main(filename: str):
    connection = get_db_connector()
    if not connection:
        sys.exit(1)

    print(f'Handle {filename}')
    print(connection.get_dsn_parameters())

    with open(filename) as f:
        titles = []
        cur = None
        for line in f:
            variables = [f'{x.strip()}' for x in line.split(',')]

            if not cur:
                cur = connection.cursor()

            if not titles:
                titles = variables
                vars_block = ','.join([f'{x} {type_of(x)}' for x in titles])
                script = f'CREATE TABLE test (id serial PRIMARY KEY, {vars_block});'

                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                for result in cur.fetchall():
                    if 'test' in result:
                        script = ''
                        continue

            else:
                titles_block = ','.join(titles)
                variables[0] = '/'.join(reversed(variables[0].split('.')))
                for i in (0,1,2,3):
                    variables[i] = f"'{variables[i]}'"
                vars_block = ','.join(variables)
                script = f'INSERT INTO test({titles_block}) VALUES({vars_block});'

            if script:
                print(script)
                # cur.execute(script)
                # connection.commit()
        cur.close()
    connection.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
