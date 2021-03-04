from models.model_redis import connection


def first_migration():
    connection.set('project-latest-id', 0)
    connection.set('vkpn-latest-id', 0)


first_migration()
