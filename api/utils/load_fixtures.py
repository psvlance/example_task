import sys
import os
import json

import psycopg2

def gen_collection_name(filename: str):
    rst = filename.split('/')[-1]
    rst = rst.split('.')[0]
    return rst


def get_db_connector():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
    except psycopg2.OperationalError:
        connection = None
    return connection

def type_of(str):
    # TODO: hack
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

    if connection:
        with open(filename) as f:
            titles = []
            cur = connection.cursor()
            for line in f:
                variables = [x.strip() for x in line.split(',')]
                if not titles:
                    titles = variables
                    vars_block = ','.join([f'{x} {type_of(x)}' for x in titles])
                    cur.execute(f'CREATE TABLE test (id serial PRIMARY KEY, {vars_block});')
                else:
                    titles_block = ','.join(titles)
                    vars_block = ','.join(variables)
                    cur.execute(f'INSERT INTO test ({titles_block}) VALUES ({vars_block});')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
