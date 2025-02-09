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
This section describes how to use colibri in detail.
- [XML-input file overview](#xml-input-file-overview)
  - [SaveTable](#savetable)
  - [LoadTable](#loadtable)
  - [ROIMeans](#roimeans
- [Named Object Container](#named-object-container)

### XML-input file overview
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
Example xml-files for specific tasks can be found in the ```test/xml_input``` folder, which can be used as templates.
The following sections describe each task and the XML-structure that should be used.

#### SaveTable
Saves a table (data that has been calculated from another task) from the [Named Object Container](#named-object-container) to a file.
The XML-structure required is:
```
<task name="SaveTable">
  <name>...</name>    <!-- The table name in the Named Object container -->
  <file>...</file>    <!-- The file where the table will be saved -->
</task>
```

#### LoadTable
Loads a table previously saved with the [SaveTable](#savetable) task from a file to the [Named Object Container](#named-object-container).
The XML-structure required is:
```
<task name="LoadTable">
  <file>...</file>    <!-- The file where the table has been saved -->
  <name>...</name>    <!-- The desired name of the table in the Named Object container -->
</task>
```

#### ROIMeans
Loads a 
```
<task name="ROIMeans">
  <img_path>...</img_path>    <!-- Path to the directory of the image files -->
  <roi_path>...</roi_path>    <!-- Path to the file containing the ROIs -->
  <labels>...</labels>        <!-- Labels for the ROIs (OPTIONAL) -->
  <ignore>...</ignore>        <!-- Do not compute means for these ROIs (OPTIONAL) -->
  <resample>...</resample>    <!-- Resample either images or ROI (OPTIONAL) -->
  <frame_dur>...</frame_dur>  <!-- Also calculate frame duration (OPTIONAL) -->
  <res_name>...</res_name>    <!-- The result will be stored a a table in the Named Object Container under this name -->
</task>
```

### Named Object container

