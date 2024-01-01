**Instructions**
Using Terminal, do the following:

    $ python app.py

This programm will instantiate meta-model from the grammar peep.tx. A model.peep is then parsed and instantiated by the meta-model and both meta-model and model are exported to .dot files in the folder dotexport. This command will generate dot files in dotexport folder. We can convert those files to PNG format. Note: It is important to have GraphViz installed!!!

To convert the files to PNG format do the following :

    dot -Tpng -O dotexport/peep.dot
   
    dot -Tpng -O dotexport/model.dot

Run code generation:

    $ python codegen.py
  
This will produce in Spring_boot_app folder which contains generated layers (model,controller,repository,service) for each term instance as well as the pom.xml file and application.properties file.

Meta-model can be checked or visualized by textX command line tool. To check and visualize meta-model you can use command :

    $ textx generate meta-model/peep.tx --target dot
