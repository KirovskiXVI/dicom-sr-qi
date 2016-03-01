These are some scripts that we've written for other QI work that we've done outside of the "Inquiries" and outside of our work with DICOM-SR. You can find them in the `srqi/unported scripts` folder. (Nothing else in this folder is very useful right now.)

# Extract CPT #
A script for extracting procedure rows from a large excel spreadsheet according to the CPT codes in that procedure. This program can be found in [srqi/unported scripts/extract\_cpt](http://code.google.com/p/dicom-sr-qi/source/browse/#hg%2Funported%20scripts%2Fextract_cpt)

The full description of this program, along with instructions, can be found in its [README.txt file](http://dicom-sr-qi.googlecode.com/hg/unported%20scripts/extract_cpt/README.txt).

# Code Pairs #
This program was originally written to help us find catheter-associated bloodstream infections by detecting lines that had been removed early, and it will be described in those terms here for the sake of clarity, but there may be many other applications. From an input table describing a collection of procedures, tries to pair procedures according to their CPT codes (as in a "placement" and a "removal").

The script is run by putting files in the code\_pairs folder as described below and then double-clicking on "code\_pairs.py". This script does depend on having the rest of the srqi package [installed.](GettingStarted.md)

As above, a good way to start this description is to download the package and try running the example by simply double-clicking on "code\_pairs.py" and seeing what happens. One of the sheets of your output will look like the image below. (Notice the last two columns.)

<img src='http://dicom-sr-qi.googlecode.com/files/code_pairs%20output%20example.png' />

## Inputs ##

Before running the script, the code\_pairs folder should contain the following:

  * code\_pairs.py
  * code\_pairs.xls (contents described below)
  * reasons\_lookup.xls (contents described below)
  * any number of [Syngo](Syngo.md)-formatted data input files (see [Syngo](Syngo.md) for how to format the data in these files)

No other files should be in the folder. If there is a file called "output.xls", it will not cause any problems, but it will be overwritten when you run the script.

### code\_pairs.xls ###

It will be helpful to open the [version of code pairs](http://dicom-sr-qi.googlecode.com/hg/unported%20scripts/code_pairs/code_pairs.xls) that is included with the program to understand this description (image below).

Each sheet of code\_pairs.xls consists of 3 rows:
  * The first column of each has labels telling you what the line does (it is ignored by the program)
  * The 2nd and 3rd rows are labeled "code combination 1" and "code combination 2". In the context of looking for line placements and removals, "code combination 1" = a set of cpt codes representing a placement and "code combination 2" = a set of cpt codes representing a removal.
  * The first row allows to to specify the maximum time difference in days between procedures in a pair that we care about.

<img src='http://dicom-sr-qi.googlecode.com/files/code_pairs_xls%20example.png' height='100' />

In this example, a line placement is any CPT code combination that includes both "111" and "333"; a line removal is any CPT code combination that includes "222"; and since I'm looking for infections caused by bad sterile technique during the placement, I'm not interested in seeing any line removal that occurred more than 14 days after the placement, since those lines were most likely not infected.

A couple of things to note:
  * If you have multiple sheets in code\_pairs.xls, the program will run on each sheet independently and generate the results as different sheets of the output file.
  * If the last CPT code you list on any given row is "-99", that specifies that you would not like that combination to match if there are any other codes in the string. For example, if your combination is "222,333", that will match "222,333" and "222,333,111", but if you specify "222,333,-99", that will match "222,333" but NOT "222,333,111".
  * CPT code combinations are never sensitive to order.

### reasons\_lookup.xls ###

Again, you may want to open up the [example of this file](http://dicom-sr-qi.googlecode.com/hg/unported%20scripts/code_pairs/reasons_lookup.xls) that is included with the program (image included below).

You can leave this file entirely blank if you want if it doesn't sound like a useful feature for your workflow.

At our site, every time we find a pair of insertions/removals that could represent an infection that was caused by our IR team, we manually look up the reason for the removal that is listed in our EMR. Keeping track of what pairs we have already found and looked up can be a surprisingly hard task (see the "Caveats" section below), so we found that the simplest solution was to just keep a list of removals (identified by their procedure accession number) and the reasons for the removal. See the table below.

<img src='http://dicom-sr-qi.googlecode.com/files/reasons_lookup%20example.png' height='125' />

When you run code\_pairs.py, every time the program finds a "removal", it will check to see if you have the accession number for the procedure listed in reasons\_lookup.xls. If you do, it will pull the reason in to the results in a new column. (Update: In versions of dicom-sr-qi after 0.0.6, you can have as many "Reasons" columns as you want and they all will be pulled over into the output.)

If you have reasons listed for some and not others, the program will group all the reason-less pairs at the bottom of the output file to make it easy for you to identify them.

(Note: you can have multiple sheets in reasons\_lookup.xls, as long as they all have the same basic format as the first sheet and the program will treat them as if they are all just one big sheet.)

### Other input files ###

All other .xls files in the folder (other than output.xls) will be treated as [Syngo](Syngo.md)-formatted input files.

### output.xls ###

Once you run code\_pairs.py, the program will create (or overwrite) the file called output.xls.

As shown above, this is the same as the input files, except there are two columns added at the end: Line days, and removal reason. The CPT codes are also combined into a single column if they weren't already. Finally, procedures representing "placements" (code combination 1) are paired with procedures representing "removals" (code combination 2).

## Caveat(s) ##

The problem of pairing line-in/line-out procedures is harder than you might expect at first. It is complicated by the fact that:
  * A single patient can have multiple of the same line placed at once, rendering it impossible to figure out which line has been removed in a removal procedure.
  * A patient can have lines placed or removed at facilities for which we have no data.

Fortunately, the first scenario is relatively rare for the cases that we're interested in, so we simply ignore it. We then say that every removal corresponds to the last placement for which we have a record, and every removal for which we don't have a placement must correspond to a placement at an outside facility.

## Troubleshooting code\_pairs ##

Unfortunately, code\_pairs doesn't come with a graphical user interface, so there's no good way to get error messages to the user when it fails.

If you run code\_pairs.py and it doesn't create an output file, it means that the run failed. The most common causes of a failure are:
  1. Accidentally leaving the old output.xls file in the folder and having it open in Excel while code\_pairs runs. It can't over-write a file that you have open, so it fails. If this happens, just close Excel and try running code\_pairs again.
  1. There is some bad data in your spreadsheet (e.g. a non-number where a number is supposed to go.) Follow the instructions below to figure out where the bad data is.

In order to get more information about why code\_pairs failed...
  * right click on "code\_pairs.py" and select "Open with IDLE..." (assuming you have Enthought installed on your computer).
This will open up the source code of the program-- don't worry, you don't have to understand any of it.
  * Now press F5
This will run code\_pairs.py and open another window with some text in it. Ignore the text for now. Wait a couple of seconds while code\_pairs runs. If it runs successfully, you will just see another line of ">>>>" appear. If it fails again, you'll see a bunch of red text appear. Look at the last couple of lines of red text and see if it gives you any clues as to what went wrong. If it doesn't, contact one of the developers or file an Issue report on this site.