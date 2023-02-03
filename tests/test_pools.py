from unittest import TestCase

from module.pools import get_factories_file, Factories, dump_factories_file


class TestPools(TestCase):

    def test_update_factories(self):
        model = {
            'test': 'test.txt',
            'test2': 'test2.txt',
            'test3': 'test3.txt'
        }
        factories: dict = get_factories_file()
        factories.update(model)
        dump_factories_file(factories)
        factories_updated = get_factories_file()
        print(factories_updated)
        print(factories)

    def test_get_factories_file(self):
        factories = get_factories_file()
        print(factories)

    def test_factories_items(self):
        factories = Factories()
        return_value = {key: item.info() for key, item in factories.items()}
        print(return_value)

    def test_dump_factories(self):
        values = {
            "parsed": "parsed.txt",
            "west": "west.txt",
            "checked": "non_checked_west.txt",
        }
        dump_factories_file(values)
