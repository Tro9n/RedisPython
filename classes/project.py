from models.model_redis import Model


class Project(Model):

    def __init__(self, pk=None, client=None, pm=None, assignees=None):
        if pk is not None:
            pk = int(pk)
        self.pk = pk
        self.client = client
        self.pm = pm
        self.assignees = assignees

    def __str__(self):
        return str({
            'id': self.pk,
            'client': self.client,
            'pm': self.pm,
            'assignees': self.assignees
        })



