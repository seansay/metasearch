import os
import pytest
from engines import FarooEngine

@pytest.fixture(scope="module")
def engine():
    engine = FarooEngine(api_key=os.environ["FAROO_API_KEY"])
    return engine

@pytest.fixture(scope="module")
def results(engine):
    return engine.search("python")


def test_result_item(results):
    item = results[0]
    assert hasattr(item, "title")
    assert hasattr(item, "url")
    assert hasattr(item, "description")
    assert item.source.name == 'faroo'

def test_result_priority(results):
    item = results[1]
    assert item.priority == 1

def test_count(engine):
    results = engine.search("python", limit=5)
    assert len(results) == 5