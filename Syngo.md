Syngo [(official website)](http://www.medical.siemens.com/webapp/wcs/stores/servlet/LandingPage?storeId=10001&langId=-11&catalogId=-11&catTree=100010,1008631,1029622,1029618,200650&pageId=125332&_nc_showLayer=1) is a Siemens system that is used at [MIR](http://www.mir.wustl.edu/), where this software was initially developed, to store and retrieve billing data, among other things. Since this system contains useful information for QI work, we have built ways to integrate that Syngo data with DICOM-SR.

**The most important data** that we get from Syngo about each procedure that cannot be retrieved from DICOM-SR is:
  * The name of the physicians and Techs involved
  * the CPT codes of the procedure
  * in some cases--such as operator\_improvement.py and operator\_improvement\_surface.py-- we use the "Fluoro" value from the Syngo data (which actually represents total pedal time) if there is no SR data available.

If you see an inquiry that breaks down the analysis by physician or procedure type, chances are you need some Syngo data to allow that inquiry to run correctly.

# Faking SR Data #
Eventually we would like to support other supplementary data types. However, for now if you want to run some of the Inquiries that require Syngo data (or the code\_pairs utility), it is easy to massage to make it look enough like Syngo data that the program will run.

## Syngo Data Requirements ##
Some examples of the way we store SR data can be found as [test\_operator\_improvement.xls](http://dicom-sr-qi.googlecode.com/hg/test/data/test_operator_improvement.xls), as well as in the code\_pairs and extract\_cpts folders.

Important things to note:
  * the data must always be stored on the SECOND sheet of the .xls file. (You can tell which sheet is the second by looking at the tab ordering at the bottom of the page when you open the .xls file in Excel.)
  * All of the column headings that are found in the example files must be found in any Syngo file EXCEPT...
  * instead of having a bunch of separate columns for CPT codes, you can have one column for CPT codes, which has them all listed separated by commas

For most of the columns, you just need the heading. The program will tolerate missing values under most headings.

The **most important headings** are "MPI", which is the unique patient identifier number (equivalent to "Patient ID" in DICOM-SR data), and "DOS Start", which is the start date of the procedure. These are the most important because the program uses these criteria to match procedure records from Syngo data to procedure records from DICOM-SR data.

## Coercing Your Data ##

So to make your data look like syngo data:
  1. Copy the column headings from one of the example files into the SECOND sheet of a new .xls file.
  1. Fill in the columns that you'd like to use with your data.
  1. Make sure the MPI and DOS Start values match with your DICOM-SR data if you are planning on running an analysis that requires both types of data to be merged.
  1. Fill in the rest of the columns that are filled in in the examples with fake values.

That's it.