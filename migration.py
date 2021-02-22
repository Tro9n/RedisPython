from Project import connection


def first_migration():
    connection.set('project-latest-id', 0)


first_migration()
