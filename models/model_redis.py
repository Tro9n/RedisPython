import redis
import ast


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
        connection.lpush(list_key, self.pk)

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
        self.pk = self.latest_instance_id() + 1
        connection.hmset(key, ast.literal_eval(self.__str__()))
        self.increment_latest_instance_id()
        self.add_to_list()
        return self

    @classmethod
    def get(cls, pk):
        key = cls.cache_key(pk)
        result = connection.hgetall(key)
        return result

    @classmethod
    def to_list(cls):
        list_key = cls.list_key()
        instances = []
        for instance_id in connection.lrange(list_key, 0, -1):
            instance = cls.get(instance_id)
            instances.append(instance)
        return instances
