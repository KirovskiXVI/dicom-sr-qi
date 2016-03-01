# Audience #

This guide is intended for Python programmers who would like to create their own inquiries.

# Installation #

The first thing you want to do is grab a copy of the source code. You can do this by downloading the most recent demo from the [Downloads](Downloads.md) section. However, if you have experience with [Mercurial](http://mercurial.selenic.com/), it might be better to grab the source from our repository. Instructions on how to get the code with Mercurial can be found [here](http://code.google.com/p/dicom-sr-qi/source/checkout).

You should also try everything out from a user's perspective by going through the GettingStarted tutorial, if you haven't already.

# Creating Our First Inquiry #

In this tutorial, we will be creating our own inquiry. The inquiry will simply read in DICOM-SR data from an xml file and print out the total number of frames used in each procedure.

Start by creating a file called "frame\_count.py" in the "active\_inquiries" directory. (You can see a completed version of the same file in the "inquiries" directory.)

Start by adding the following lines:
```
from srqi.core import inquiry
import datetime

#The name of the class must be the same as the file name, except
#with the first letter of each word capitalized.
class Frame_Count(inquiry.Inquiry): #all inquiries inherit from inquiry.Inquiry
    # "NAME" and "description" are standard class variables that are used to
    # provide information to the user. If you don't specify them, they will
    # be replaced by reaonable defaults.
    NAME = "Frame Counter" 
    description = """Counts the number of frames in each procedure

    Data required:
        DICOM-SR xml

    Parameters:
        START_DATE - limit the procedures analyzed to those after this date
    """
    # Define a parameter called START_DATE that is to be specified by the user.
    # The first argument of the Inquiry_Parameter constructor is a default value
    # and the second is an optional human-readable name for the parameter.
    START_DATE = inquiry.Inquiry_Parameter(datetime.date.today(), "Start Date")
    
```

You can add other class variables, module-level variables, functions, etc if you want. The core modules and gui look for certain functions and variables, but it's happy to ignore any other stuff you've included in your class or module.

## Starting and Understanding the `Run` Method ##

Next we have to define what our inquiry is going to do with the input data. We do this by overriding the `run` method of inquiry.Inquiry. Start by just writing the method signature:

```
    def run(self, sr_procs, context, extra_procs):
```

This method will be called by the GUI when the user presses the "Run" button. The full (and most up to date) documentation for how these parameters will be filled in can be found in [core/inquiry.py](http://code.google.com/p/dicom-sr-qi/source/browse/core/inquiry.py#37). The whole method is reproduced here:

```
    def run(self, sr_procs, context, extra_procs):
        """Do all the necessary work with the data
        and save the stuff you need for the other methods

        Parameters:
            sr_procs - a list of ReadXML.Procedure objects representing sr
                reports for single procedures.
            context - a Context object. doesn't currently do anything, but
                is a placeholder for when we will need to pass context
                information from a broader database without giving it all the
                data from all the individual procedures in the national database
            extra_procs - a list of other types of objects (e.g.
                Syngo_Procedures) representing procedures that could not be
                associated with any of the sr procedures.
        """
        raise NotImplementedError("Inquiry.run must be overridden in implementing class")

```

So when the user presses "Run", the GUI looks at all of the data files that the user has specified and passes them to the function `get_procs_from_files` in `my_utils.py`. This function takes some guesses at what kinds of data is stored in each file and creates Python objects for each procedure record in each file. For example, if one of the input files is a DICOM-SR xml file, the objects that will be created will be of the type `srdata.Procedure`. If they are spreadsheets that have been exported from Syngo, the billing data system that is currently used at the Mallinckrodt Institute of Radiology, `Parse_Syngo.Syngo` objects will be created.

Next, since dicom-sr-qi is centered around DICOM-SR data, the program attempts to pair every non `srdata.Procedure` object with a `srdata.Procedure` object. If it is successful, it assigns that procedure object to the Procedure object using a method like `srdata.Procedure.set_syngo`. If it is unsuccessful--i.e. if it can't find a srdata.Procedure object that looks like it corresponds to the non-SR procedure object-- it will just save the non-SR procedure object in a big heterogenous collection of unmatched non-SR procedure objects. As you may have guessed, this will be passed in to `run` in the `extra_procs` parameter. All `srdata.Procedure` objects are then passed to `run` as an iterable in the `sr_procs` variable.


## Accessing the Data ##

Now that we've figured out how to get the procedure objects, we need to figure out how to access the data in them. Fill in the following methods in your Frame\_Count class:
```
    def run(self, sr_procs, context, extra_procs):
        self.sr_proc = sr_procs[1]

    def get_text(self):
        return '\n'.join(dir(self.sr_proc))
```

The whole purpose of the `run` method is essentially to process the data in whatever way we want and then save some information as variables like `self.some_information`. Then, when the GUI calls certain pre-determined methods like `get_text`, `get_tables`, and `get_figures` later, you will use the `self.some_information` variables to build tables and create figures with the data, which will be passed back to the GUI and rendered as the html output.

Go ahead and run the program with the Frame\_Count inquiry enabled as described in the GettingStarted tutorial using any SR xml file as an input. (I suggest using sample\_anon.xml from the latest demo zip in our Downloads section.) Now open the output. You should see that a `srdata.Procedure` object has a lot of attributes, including

```
Gender
PatientID
Performing_Physician
Scope_of_Accumulation
SeriesDate
SeriesDescription
SeriesInstanceUID
StudyDate
StudyDescription
StudyInstanceUID
```

Obviously these are data about the procedure from the SR file. You will also notice that it has a `get_events` method. Try modifying count\_frames.py so the `get_text` method reads

```
    def get_text(self):
        return '\n'.join(dir(self.sr_proc.get_events()[1]))
```

This should give you some insight on how to access the data from each irradiation event in each procedure.

It may be helpful to look at the source files for `srdata` to get more information about the `Procedure` and `Event` objects. You can also open a python interpreter, load in some SR data, and play around with the objects as follows: (assuming you've started the interpreter from inside the directory containing the srqi folder)

```
>>> from srqi.core import my_utils
>>> procs, extra_procs = my_utils.get_procs_from_files(["C:\Users\SOME_PATH\srqi\Data\sample.xml"])
>>>
```

## Writing Output ##

Now let's change `run` and `get_text` a bit and add the `get_figures` and `get_tables` methods that I alluded to earlier so we're actually displaying something useful.

```
    def run(self, sr_procs, context, extra_procs):
        # do some trivial "analysis" of the procedures by calling some
        # convenience methods proceded by the srdata.Procedure objects
        self.frame_counts = []
        self.start_times = []
        for proc in sr_procs:
            if not len(proc.get_events()) ==0 \
               and proc.get_start_time().date() > self.START_DATE.value: #note the .value part of this
                self.frame_counts.append(proc.get_number_of_pulses())
                self.start_times.append(proc.get_start_time())


    def get_text(self):
        # Return a string to be shown to the user as part of the output
        return "There are a total of " + str(len(self.frame_counts)) + " procedures in the input file"

    def get_figures(self):
        # return a list of matplotlib figure objects that will be
        # saved and rendered
        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.scatter(self.start_times, self.frame_counts)
        plt.title("Frame counts over time.")
        plt.xlabel("Start Time of Procedure")
        plt.ylabel("Number of Frames")
        return [fig]

    def get_tables(self):
        # make a demo_table demonstrating the basic idea of making a table
        # out of an iterable of iterables (in this case, a list of tuples)
        demo_table = [("Row0 Col0", "Row0 Col1"), ("Row1 Col0", "Row1 Col1")]
        assert(demo_table[0][1] == "Row0 Col1")
        assert(demo_table[1][1] == "Row1 Col1")
        # make a more useful table
        # the function call `zip(self.start_times, self.frame_counts)`
        # creates a list of tuples that looks like
        # [ (start_time1, frame_count1),
        #   (start_time2, frame_count2),
        #   (start_time3, frame_count3),...]
        table1 = zip(self.start_times, self.frame_counts)
        heading = [("Start Times", "Frame Counts")]
        table1 = heading  + table1
        return [demo_table, table1]
                
```

Now try opening up the GUI, selecting some sample data, and running the Frame Counter inquiry. (**Remember to set your Start Date back early enough!**) If it runs, congratulations! Look at the output and see if you can correlate it to what is going on in the commented code. If it gives you an error message, don't worry! It does for me too. Just check out our CommonErrors section and we'll have it fixed in no time.