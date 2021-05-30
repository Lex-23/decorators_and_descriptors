import json
import datetime
from urllib.parse import urlparse


class BaseField:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        issues = instance.parse()
        val = instance.metadata[self.value]
        return issues[str(val)]


class IntField(BaseField):
    def __get__(self, instance, owner):
        val = super().__get__(instance, owner)
        return int(val)


class StrField(BaseField):
    def __get__(self, instance, owner):
        val = super().__get__(instance, owner)
        return str(val)


class DateField(BaseField):
    def __get__(self, instance, owner):
        val = super().__get__(instance, owner)
        return datetime.datetime.strptime(val, "%Y-%M-%d")


class UrlField(BaseField):
    def __get__(self, instance, owner):
        val = super().__get__(instance, owner)
        return urlparse(val)


class Record:
    id = IntField('id')
    username = StrField('username')
    created_at = DateField('created_at')
    profile_url = UrlField('profile_url')

    def __init__(self, row, metadata):
        self.row = row
        self.metadata = metadata

    def parse(self):
        data = self.row
        data_list = data.split(',')
        data_dict = {i.split(':')[0]: i.split(':', maxsplit=1)[1] for i in data_list}
        return data_dict


with open('metadata.json') as f_in:
    metadata = json.load(f_in)

with open('issues.csv') as f_in:
    records = [
        Record(row.strip(), metadata=metadata)
        for row in f_in
    ]

print(type(records[0].id), records[0].id)
print(type(records[0].username), records[0].username)
print(type(records[0].created_at), records[0].created_at)
print(type(records[0].profile_url), records[0].profile_url)
