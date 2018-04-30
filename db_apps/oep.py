
import os
from configobj import ConfigObj
import requests
import logging
from collections import namedtuple

try:
    config = ConfigObj(os.environ['CONFIG_PATH'])
    token = config['OEP']['TOKEN']
except KeyError:
    token = None


oep_url = 'http://oep.iks.cs.ovgu.de'


Case = namedtuple('Case', ['success_code', 'success_msg', 'error_msg'])
cases = {
    'create': Case(
        201,
        'Table "{schema}.{table}" generated successfully.',
        'Could not create table "{schema}.{table}".'
    ),
    'select': Case(
        200,
        None,
        'Could not select data from table "{schema}.{table}".'
    ),
    'insert': Case(
        201,
        'Added data to table "{schema}.{table}".',
        'Could not insert data into table "{schema}.{table}".'
    ),
    'delete': Case(
        200,
        'Rows in "{schema}.{table}" deleted successfully.',
        'Could not delete rows from "{schema}.{table}".'
    ),
    'delete_table': Case(
        200,
        'Table "{schema}.{table}" deleted successfully.',
        'Could not delete table "{schema}.{table}".'
    )
}


class OEPTable(object):
    schema = None
    table = None
    structure = None

    @classmethod
    def select(cls, where=None):
        select_url = cls.__set_meta(
            '{oep_url}/api/v0/schema/{schema}/tables/{table}/rows/')

        if where is not None:
            where_clause = '?where='
            if isinstance(where, list):
                where_clause += '&'.join(where)
            elif isinstance(where, str):
                where_clause += where
            else:
                raise TypeError(
                    'Unknown where type - must be list of str or str')
            select_url += where_clause

        result = requests.get(select_url)
        cls.__check_response('select', result)
        return result.json()

    @classmethod
    def insert(cls, data):
        insert_url = cls.__set_meta(
            '{oep_url}/api/v0/schema/{schema}/tables/{table}/rows/new')
        response = requests.post(
            insert_url,
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token %s' % token
            }
        )
        cls.__check_response('insert', response)

    @classmethod
    def delete(cls, data):
        # Not working yet!
        insert_url = cls.__set_meta(
            '{oep_url}/api/v0/schema/{schema}/tables/{table}/rows/')
        response = requests.delete(
            insert_url,
            json={'query': data},
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token %s' % token
            }
        )
        cls.__check_response('delete', response)

    @classmethod
    def create_table(cls):
        if token is None:
            raise RuntimeError('No OEP token given in DB config')

        if None in (cls.schema, cls.table, cls.structure):
            raise ValueError('Table is not set correctly')

        create_url = cls.__set_meta(
            '{oep_url}/api/v0/schema/{schema}/tables/{table}/')
        response = requests.put(
            create_url,
            json=cls.structure,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Token %s' % token}
        )
        cls.__check_response('create', response)

    @classmethod
    def delete_table(cls):
        if token is None:
            raise RuntimeError('No OEP token given in DB config')

        if None in (cls.schema, cls.table):
            raise ValueError('Table is not set correctly')

        delete_url = cls.__set_meta(
            '{oep_url}/api/v0/schema/{schema}/tables/{table}')
        response = requests.delete(
            delete_url,
            headers={'Authorization': 'Token %s' % token}
        )
        cls.__check_response('delete_table', response)

    @classmethod
    def __set_meta(cls, entry):
        return entry.format(
            oep_url=oep_url,
            schema=cls.schema,
            table=cls.table
        )

    @classmethod
    def __check_response(cls, case, response):
        if case not in cases:
            raise KeyError('Response-case not found')

        if response.status_code == cases[case].success_code:
            if cases[case].success_msg is not None:
                logging.info(
                    cases[case].success_msg.format(
                        schema=cls.schema,
                        table=cls.table
                    )
                )
        else:
            try:
                reason = response.json()['reason']
            except (KeyError, AttributeError):
                reason = response.text
            logging.warning(
                cases[case].error_msg.format(
                    schema=cls.schema,
                    table=cls.table
                ) +
                'Reason: {reason}'.format(reason=reason)
            )
