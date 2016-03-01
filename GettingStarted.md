This document will walk you through downloading the project and running a few sample analyses. Here we assume that you already are familiar with what a DICOM-SR report is and have an idea of how you might go about collecting them, even if you don't actually have any data in hand right now.

You will note that all of the analyses we do here use DICOM-SR reports that have been converted from native .SR files to .xml files using the CARE Analytics software, which was developed mostly by Siemens and is freely available from our Downloads page.


**Table of Contents**


# Installation #

There are two steps to installing the program:
  * Installing the dependencies
  * Downloading the program and unzipping it

If you have access to the Enthought Python distribution, this should be extremely easy: 20 minutes max, most of which will be spent waiting for Enthought to install.

## Step 1: Install Dependencies ##

### The Easy Way ###

The dicom-sr-qi program depends on packages in the [Enthought Python Distribution](http://www.enthought.com/products/epd.php) which provides an easy way to install a large collection of fantastic tools for scientific computing on any platform with just a few clicks. So the first step to use dicom-sr-qi is to download and install Enthought. (Only a few of these tools are stand-alone applications, however, so you don't need to worry about adding a bunch of new programs to your start menu/applications mentu/desktop/etc.)

Enthought is [free for academic institutions](http://www.enthought.com/products/edudownload.php) and [relatively cheap](http://www.enthought.com/products/getepd.php) for non-academic institutions. (srqi was written and tested on version 7.0-2 32bit.) See "the hard way" below if you do not have an academic email address and want to avoid spending money.


### The Hard Way ###

The specific packages that dicom-sr-qi relies on are:
  * the base Python 2.7 installation
  * Matplotlib
  * numpy
  * xlrd and xlwt
  * Jinja2
  * wxPython
  * (this list may be incomplete)

all of which are completely free and open source, so it is very possible to download and install all of them independently without buying anything.

The best way to get these is to download Enthought's [EPD Free](http://www.enthought.com/products/epd_free.php), which will automatically install all of the packages except for Jinja2, xlrd, and xlwt. Though I haven't tested it and it seems too good to be true, it looks like Enthought might also provide a tool (enpkg, see the EPD free link above) to download the rest of the packages for free as well, but you may have to install them individually from their websites.

## Step 2: Get the package ##

Go to our [downloads](http://code.google.com/p/dicom-sr-qi/downloads/list) page, download the most recent demo package (called something like Demo0.0.3), and unzip it wherever you want.

# Running the Demo #

## Start the Program ##
Once you unzip the file, you should have a folder called something like "dicom-sr-qi0.0.3" and another folder inside that called "mrqi".
  * Open the "srqi" folder and double click on the file called "main.py".
Two windows should open.

One window should be all black. We won't use this for anything. Just ignore it. If it doesn't close when you close the main window later, go ahead and close it, but don't close it while the main window is running.

The other window should look like this

<img src='http://dicom-sr-qi.googlecode.com/files/demo0.0.1-1.PNG' height='300' />

We will use the top panel to load data into the program and the bottom panel to specify how we want to analyze it.

## Add Some Data ##
Let's start by analyzing a very small sample.
  * Click the "Add Data Source Button" and navigate to the same folder where you found the "main.py" file.
  * Then click on the "sample data" folder and select "sample\_anon.xml".
This is a xml file that is very similar to the xml files produced by Care Analytics to store DICOM-SR data.

Now that that data file has been selected, it should appear in the white box at the top of the window.
  * Check the box next to it.
  * Also go ahead and click on the button labeled "Missing\_Data\_Inquiry >>".
Your window should now look like this:

<img src='http://dicom-sr-qi.googlecode.com/files/demo0.0.2-2.PNG' height='300' />


## Run Your First Analysis ##
  * If you want, you can read the description by clicking on the "Description" link.
  * Otherwise, just go ahead and check the "Enabled" box, set the "Start Date" back to anything before September 2009, and then click "Run" at the bottom of the window.
A progress bar should pop up for a second (don't worry if you don't actually see the bar move) and then go away to indicate that the analysis is complete.

  * Now go back to the folder where you found "main.py". You might notice that a new folder has been created called "output". Open it up and double click on the file called "output.html" inside.

The figure isn't particularly helpful, but the table underneath should make some more sense. All this analysis does is show the number of procedures per day in the xml file you loaded in. This is helpful in finding periods of time where we might have lost some data from some of the procedures.

## Try a Bigger Data Set ##
Let's try that again with a bigger data set.
  * Go back to the main window,
  * uncheck the box next to the "sample\_anon.xml" file path,
  * click on "Add data source",
  * select "bjh\_anon.xml" from the same folder as "sample\_anon.xml",
  * and check the box next to it once it appears in the white box.
  * Make sure the box next to "Enabled" is still checked and
  * click "Run" again.
(This analysis should take significantly longer, mostly because it takes a long time to read in the large xml file.)
  * Now open "output.html" again (or simply refresh the page if you still have it open in your browser) to see the results of the analysis run on the larger data set.

The figure should make a little more sense now. (Notice how points representing weekends are red, which helps because we might expect to have fewer procedures then even if we aren't missing data.) However, you shouldn't notice anything very interesting: we changed the dates a little when we anonymized the data so that we could distribute it with this demo.

## Try some other analyses ##

  * Go ahead and close both program windows.

  * Go back to the "srqi" folder and look in the "active\_inquiries" folder.
In there, you should see one file that we're interested in: `missing_data_inquiry.py`. (You'll see a lot of files called `__init__.py` and a lot of "Compiled Python" files, which end in ".pyc". You can safely ignore all of them.)  "missing\_data\_inquiry.py" is a very simple program, written in Python, which tells the larger program how to do the analysis that we just did and how the results should be displayed. We generally call a single analysis an "Inquiry".

  * Now go back to "srqi" again and open up the "inquries" folder.
This is a library of other inquiries, just like `missing_data_inquiry.py`, which we are working on. Each one looks at the data and analyzes it and displays it in a different way. Some of them even combine the SR data with other kinds of data (e.g. billing data) to get richer analyses.

However, not everyone has every kind of data and not everyone wants to routinely use every inquiry, so we don't load them into the program by default.
  * Copy and paste `average_fps.py` and `room_usage.py` from the "inquiries" folder into the "active\_inquiries" folder.
  * Then run `main.py` again.
  * Add the "bjh\_anon.xml" data source as you did before and expand all of the inquiry windows by clicking their respective buttons.

Your window should now look like this:

<img src='http://dicom-sr-qi.googlecode.com/files/demo0.0.1-3.PNG' height='300' />

Again, feel free to read the descriptions if you want. Notice how these two new inquiries have parameter values that can be changed, but come pre-loaded with a reasonable default.

  * Check all 3 of the "Enabled" boxes and then click "Run".
  * After the analysis finishes, open up "output.html" again.
Examples of the output graphs are below:

<img src='http://dicom-sr-qi.googlecode.com/files/demo0.0.1-Average_Fps0.png' height='250' />
<img src='http://dicom-sr-qi.googlecode.com/files/demo0.0.1-Room_Usage0.png' height='250' />


The results from all 3 inquiries have been combined into a single html document. See if you can make sense of what is going on by browsing around and reading the inquiry descriptions. (Keep in mind, though, that the "room\_usage" analysis is going to make less sense because the times and dates of the procedures have been randomized in the anonymized data set.) Try changing the parameters on the main screen or only "enabling" a subset of the inquiries and then rerunning the analysis.

You should notice that the program runs _much_ more quickly the second time you click "Run", even on the larger data set. That is because it takes a very long time to read the DICOM-SR .xml files, but the analyses themselves are run very quickly. If you don't change the data set between runs, the program avoids re-reading the xml file.