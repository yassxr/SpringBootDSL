from os import mkdir,makedirs
from os.path import exists, dirname, join
import jinja2
from app import get_metamodel
from app import this_folder

APP_DIRECTORY = '/Users/perso/SpringBootDSL/Spring_boot_app/'
POM_DIRECTORY = APP_DIRECTORY
PROPERTIES_DIRECTORY = APP_DIRECTORY

print(PROPERTIES_DIRECTORY)

this_fold = dirname(__file__)
print(this_fold)

def to_pascalcase(st):
    return st[0].upper() + st[1:]

def to_lowercase(st):
    return st[0].lower() + st[1:]

def convert(param):
    if(param):
        return 'true'
    if(not param):
        return 'false'

def main():

    mm = get_metamodel()

    model = mm.model_from_file('/Users/perso/SpringBootDSL/model/model.peep')

    def javatype(s):
        """
        Maps type names from PrimitiveType to Java.
        """
        return {
                'int': 'int',
                'String': 'String',
                'Long': 'Long',
                'boolean': 'boolean'
        }.get(s.name, s.name)

    # Create output folder
    #srcgen_folder = join(this_folder, APP_DIRECTORY)
    #print(srcgen_folder)
    #if not exists(srcgen_folder):
       # makedirs(srcgen_folder)
    main_class_folder = join(this_folder, APP_DIRECTORY)
    print(main_class_folder)
    if not exists(main_class_folder):
        makedirs(main_class_folder)
    model_folder=join(this_folder,APP_DIRECTORY + "model/")
    if not exists(model_folder):
        makedirs(model_folder)
    repository_folder = join(this_folder, APP_DIRECTORY + "repository/")
    if not exists(repository_folder):
        makedirs(repository_folder)
    service_folder = join(this_folder, APP_DIRECTORY + "service/")
    if not exists(service_folder):
        makedirs(service_folder)
    controller_folder = join(this_folder, APP_DIRECTORY + "controller/")
    if not exists(controller_folder):
        makedirs(controller_folder)
    resources_folder = join(this_folder, PROPERTIES_DIRECTORY + "resources/")
    print(resources_folder)
    if not exists(resources_folder):
        makedirs(resources_folder)
    

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filters 
    jinja_env.filters['javatype'] = javatype
    jinja_env.filters['to_pascalcase'] = to_pascalcase
    jinja_env.filters['to_lowercase'] = to_lowercase
    jinja_env.filters['convert'] = convert

    # Load Java templates
    main_class_template = jinja_env.get_template('template/main_class.template')
    model_template = jinja_env.get_template('template/model.template')
    repository_template = jinja_env.get_template('template/repository.template')
    service_template = jinja_env.get_template('template/service.template')
    controller_template = jinja_env.get_template('template/controller.template')
    pom_template = jinja_env.get_template('template/pom.template')
    properties_template = jinja_env.get_template('template/properties.template')

    for peep in model.peepModel.peeps:
        # For each entity generate java file
        #with open(join(srcgen_folder,
                       #"%s.java" % peep.name.capitalize()), 'w') as f:
           # f.write(model_template.render(peep=peep))
        with open(join(main_class_folder, "Application.java"), 'w') as file:
            file.write(main_class_template.render())
        with open(join(model_folder, "%s.java" % peep.name), 'w') as file:
            file.write(model_template.render(peep=peep))
        with open(join(repository_folder, "%sRepository.java" % peep.name), 'w') as file:
            file.write(repository_template.render(peep=peep))
        with open(join(service_folder, "%sService.java" % peep.name), 'w') as file:
            file.write(service_template.render(peep=peep))
        with open(join(controller_folder, "%sController.java" % peep.name), 'w') as file:
            file.write(controller_template.render(peep=peep))

    mainContent = model.pomFileModel.mainContent
    additionalContent = model.pomFileModel.additionalContent
    print(POM_DIRECTORY)

    with open(join(this_folder, POM_DIRECTORY, "pom.xml"), 'w') as file:       # making pom file
        file.write(pom_template.render(mainContent=mainContent,additionalContent=additionalContent))

    propertiesContent = model.databaseModel

    with open(join(resources_folder, "application.properties"), 'w') as file:   #making properties file
        file.write(properties_template.render(propertiesContent=propertiesContent))

if __name__ == "__main__":
    main()