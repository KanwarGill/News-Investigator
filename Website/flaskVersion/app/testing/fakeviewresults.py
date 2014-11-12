class FakeViewResults(object):
    '''A replicated couchdb.client.ViewResults object.'''
    def __init__(self, id, key, value):
        self.id = id
        self.key = key
        self.value = value