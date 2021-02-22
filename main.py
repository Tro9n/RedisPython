from Project import Project

# project1 = Project(client='Vakoms', pm='Any', assignees='Any1')
# project1.save()
# project2 = Project(client='Vakoms1', pm='Any2', assignees='Any3')
# project2.save()

p = Project.get(2)
p1 = {
            'id': p.id,
            'client': p.client,
            'pm': p.pm,
            'assignees': p.assignees
        }
print(p1)




