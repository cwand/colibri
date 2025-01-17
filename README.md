# colibri
Python code for analysing PET and SPECT images with a particular focus on dynamic acquisitions. Light-weight and easy to use. Code can be run from an XML input file.

## Getting colibri
Clone the repository to your computer using git:
```
> git clone https://github.com/cwand/colibri
```

Enter the directory.
Make sure you are on the main branch:
```
> git checkout main
```

Create a new virtual python environment:
```
> python -m venv my_venv
```

Activate the virtual environment. Commands vary according to OS and shell (see [the venv documentation](https://docs.python.org/3/library/venv.html)), but in a Windows PowerShell:
```
> my_venv\Scripts\Activate.ps1
```

Install colibri and required dependencies
```
> pip install .
```

If everything has gone right, you should be able to run colibri
```
> python -m colibri
Starting COLIBRI 1.0.1

Missing command line argument: path to an XML file. Exiting!
```

## Using colibri
To run colibri, the main program has to be supplied to the path of an XML-file. This file contains the tasks that colibri should perform and any information required.
The XML-file should have the following structure:
```
<colibri>
  <task name="ExampleTask1">
    <tag1>INFO_HERE</tag1>
    <tag2>INFO_HERE</tag2>
  </task>
  <task name="ExampleTask2">
    <tag1>INFO_HERE</tag1>
    <tag2>INFO_HERE</tag2>
  </task>
</colibri>
```
Example xml-files for specific tasks can be found in the ```test/xml_input``` folder.
To pass data from one task to the other, a "Named Object" container is available. For example, to compute ROI-means and then apply a correction to one of the means:
```
<colibri>
  <task name="ROIMeans">
    <img_path>...</img_path>
    <roi_path>...</roi_path>
    <res_name>tac</res_name> <!-- Data will be saved in Named Object container under this name -->
  </task>
  <task name="Correction">
    <table_name>tac</table_name> <!-- Here we tell colibri to use the correct object from the Named Object container -->
    ...
  </task>
</colibri>
```

When the XML-file is done, colibri can be run using
```
> python -m colibri path/to/XML/file.xml
Starting COLIBRI 1.0.1

...
```
