from unittest import TestCase

from source.dsl.symbol_table.SymbolTable import SymbolTable
from source.dsl.symbol_table.SymbolType import SymbolType


class TestSymbolTable(TestCase):
    def test_add(self):
        symbol_table = SymbolTable()
        symbol_table.add("svm1", SymbolType.ML_METHOD, {})
        with self.assertWarns(Warning):
            symbol_table.add("svm1", SymbolType.ML_METHOD, {})
