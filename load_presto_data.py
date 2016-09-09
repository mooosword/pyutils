import os

from pyhive import presto
from ..utils import logger
from ..utils import usage

LEVEL = 1


class PrestoClient:

    def __init__(self, host, port, catalog, schema):
        self.cursor = presto.connect(host=host, port=port, catalog=catalog, schema=schema).cursor()
        logger.info("Initialized presto client..", LEVEL)

    def query(self, operation):
        self.cursor.execute(operation)
        res = self.cursor.fetchall()
        header = PrestoClient.get_header(self.cursor.description)
        return res, header

    @staticmethod
    def get_header(description):
        return [t[0] for t in description]


