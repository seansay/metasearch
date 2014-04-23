import duckduckgo

from .base import EngineBase, ResultItemBase


class DuckgoEngine(EngineBase):

    name = "duckduckgo"
    url = "http://www.duckduckgo.com/"
    weight = 0.5

    TYPES = {
        'ANSWER': u'answer',
        'DISAMBIGUATION': u'disambiguation'
    }

    def _send_request(self, query, **kwargs):
        return duckduckgo.query(query)

    def _clean_raw_data(self, raw_data):
        results = []

        if raw_data.type == self.TYPES['ANSWER']:
            results =  raw_data.results
        elif raw_data.type == self.TYPES['DISAMBIGUATION']:
            results = raw_data.related
        else:
            return []

        results  = [DuckGoResultItem.new(item) for item in results]
        return filter(lambda x: x.is_result, results)


class DuckGoResultItem(ResultItemBase):

    source = DuckgoEngine

    def __init__(self, data):
        # test if the element is  an actual result
        if hasattr(data, 'text') and hasattr(data, 'url'):
            self.url = data.url
            self.title = data.text
            self.description = None
            try:
                self.image = data.icon.url
            except Exception as e:
                self.image = None
            # mark the result flag
            self.is_result = True
        else:
            self.is_result = False
