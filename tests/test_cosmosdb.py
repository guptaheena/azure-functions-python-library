import unittest

import azure.functions as func
import azure.functions.cosmosdb as cdb
from azure.functions.meta import Datum

class TestCosmosdb(unittest.TestCase):
    def test_cosmosdb_convert_none(self):
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=None, trigger_metadata=None)
        self.assertIsNone(result)

    def test_cosmosdb_convert_string(self):
        datum: Datum = Datum("""
        {
            "id": "1",
            "name": "awesome_name"
        }
        """, "string")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'awesome_name')

    def test_cosmosdb_convert_bytes(self):
        datum: Datum = Datum("""
        {
            "id": "1",
            "name": "awesome_name"
        }
        """.encode(), "bytes")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'awesome_name')

    def test_cosmosdb_convert_json(self):
        datum: Datum = Datum("""
        {
            "id": "1",
            "name": "awesome_name"
        }
        """, "json")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'awesome_name')

    def test_cosmosdb_convert_json_name_is_null(self):
        datum: Datum = Datum("""
        {
            "id": "1",
            "name": null
        }
        """, "json")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], None)

    def test_cosmosdb_convert_json_multiple_entries(self):
        datum: Datum = Datum("""
        [
            {
                "id": "1",
                "name": "awesome_name"
            },
            {
                "id": "2",
                "name": "bossy_name"
            }
        ]
        """, "json")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'awesome_name')
        self.assertEqual(result[1]['name'], 'bossy_name')

    def test_cosmosdb_convert_json_multiple_nulls(self):
        datum: Datum = Datum("[null]", "json")
        result: func.DocumentList = cdb.CosmosDBConverter.decode(data=datum, trigger_metadata=None)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], None)
