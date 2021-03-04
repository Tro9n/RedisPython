from classes.project import Project
from flask import Flask

# project1 = Project(client='Vakoms', pm='Any', assignees='Any1')
# project1.save()
# project2 = Project(client='Vakoms1', pm='Any2', assignees='Any3')
# project2.save()
# project3 = Project(client='Vakoms12', pm='Any22', assignees='Any32')
# project3.save()
#
p = Project.get(1)
c = Project.to_list()
print(p)
print(len(c))

app = Flask(__name__)


@app.route('/')
def hello():
    test_dict = Project.get(3)
    test_list = str(Project.to_list())
    return test_dict


if __name__ == "__main__":
    app.run()
