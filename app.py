from __future__ import unicode_literals
import os
from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export


this_folder = dirname(__file__)
#print(this_folder)

class SimpleType(object):
    
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name

def get_metamodel():
    
    simple_types = {
            'int': SimpleType(None, 'int'),
            'String': SimpleType(None, 'String'),
            'Long': SimpleType(None, 'Long'),
            'boolean': SimpleType(None, 'boolean')
    }
    metamodel = metamodel_from_file('meta-model/peep.tx',
                                    classes=[SimpleType],
                                    builtins=simple_types)

    return metamodel


def main():

    mm = get_metamodel()

    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)
    metamodel_export(mm, join(dot_folder,'peep.dot'))

    model = mm.model_from_file('model/model.peep')
    model_export(model, join(dot_folder, 'model.dot'))


if __name__ == "__main__":
    main()
