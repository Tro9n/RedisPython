import redis
import json

connection = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


class Model(object):

    @classmethod
    def latest_instance_id_key(cls):

        class_name = cls.__name__.lower()
        return '%s-latest-id' % (class_name,)

    @classmethod
    def list_key(cls):

        class_name = cls.__name__.lower()
        return '%ss' % (class_name,)

    def add_to_list(self):

        list_key = self.list_key()
        connection.lpush(list_key, self.id)

    @classmethod
    def latest_instance_id(cls):

        return int(connection.get(cls.latest_instance_id_key()))

    def increment_latest_instance_id(self):

        connection.incr(self.latest_instance_id_key())

    @classmethod
    def cache_key(cls, identifier=None):

        if identifier is None:
            identifier = cls.latest_instance_id() + 1
        class_name = cls.__name__.lower()
        return '%s-%d' % (class_name, int(identifier))

    def save(self):

        key = self.cache_key()
        self.id = self.latest_instance_id() + 1
        connection.hmset(key, self.repr())
        self.increment_latest_instance_id()
        self.add_to_list()
        return self

    @classmethod
    def get(cls, id):
        key = cls.cache_key(id)
        d = connection.hgetall(key)
        return cls(**d)

    # TODO: Use redis pipeline here
    @classmethod
    def list(cls):
        list_key = cls.list_key()
        instances = []
        for instance_id in connection.lrange(list_key, 0, -1):
            instance = cls.get(instance_id)
            instances.append(instance)
        return instances


class Project(Model):

    def __init__(self, id=None, client=None, pm=None, assignees=None):
        if id is not None:
            id = int(id)
        self.id = id
        self.client = client
        self.pm = pm
        self.assignees = assignees

    def repr(self):
        return {
            'id': self.id,
            'client': self.client,
            'pm': self.pm,
            'assignees': self.assignees
        }

    # @staticmethod
    # def write_to_json(data):
    #     with open('data.json', 'w', encoding='utf-8') as f:
    #         json.dump(data, f, ensure_ascii=False, indent=4)
