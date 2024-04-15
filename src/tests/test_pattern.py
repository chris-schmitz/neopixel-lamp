# import unittest
from dataclasses import dataclass

import pytest
from unittest.mock import MagicMock

from src.lib.patternrunner import PatternRunner
from src.lib.pattern import Pattern


class TestSuite:
    def test_pattern_iteration(self):
        pattern = Pattern(
            "test",
            [
                [(1, 1, 1), (2, 2, 2), (3, 3, 3)],
                [(4, 4, 4), (5, 5, 5), (6, 6, 6)],
            ],
        )

        assert [(1, 1, 1), (2, 2, 2), (3, 3, 3)] == pattern.get_next_frame()
        assert [(4, 4, 4), (5, 5, 5), (6, 6, 6)] == pattern.get_next_frame()
        assert [(1, 1, 1), (2, 2, 2), (3, 3, 3)] == pattern.get_next_frame()
        assert [(4, 4, 4), (5, 5, 5), (6, 6, 6)] == pattern.get_next_frame()
