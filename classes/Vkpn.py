from models.model_redis import Model


class Vkpn(Model):
    def __init__(self, pk=None, title=None, body=None, types=None, project=None):
        if pk is not None:
            pk = int(pk)
        self.pk = pk
        self.title = title
        self.body = body
        self.types = types
        self.project = project

    def __str__(self):
        return str({
            'id': self.pk,
            'title': self.title,
            'body': self.body,
            'type': self.types,
            'project': self.project,
        })
