# Program freezes during a "run" #

Windows tends to report that the program is "Not Responding" when it is busy crunching through data. The "Cancel" button on the progress bar doesn't actually work except to cut off the very last few seconds of the run, which doesn't help.

Chances are you've just put in a very large data set. Wait and the program will eventually get through it, even if Windows (or whatever OS you're using) is calling it non-responsive. True freezes should be very very rare.

# Big Scary Error Messages #

If you get a big, scary error message during a "Run", there are a couple of things you should do.

First, look at the last line (or couple of lines) of the message and see if there is anything you can understand. Well-written inquiries will put error messages down here that can give you very good hints as to what went wrong and how to fix it.

Second, look at the "Add data source" panel. Did you forget to check any of the boxes? Did you accidentally include any unsupported file types (e.g. ".xlsx"?)

Finally, there should be lots of things that look like file names/paths in the error message . Look through those and see if there is anything that looks like an inquiry file name, e.g. "C:\path\to\srqi\active\_inquiries\my\_inquiry.py". If you see one, disable that inquiry and try running the program again. Repeat until the program stops giving you errors. If you only have to disable one inquiry to stop the program from giving you an error, there is probably just a bug in that inquiry: open an "Issue" on this website, leave a comment somewhere in the Wiki, or contact one of the developers directly for help. The more inquiries you have to disable, the more likely it is that the problem is with your data. Try running the same inquiries on different data sets and see if you can figure out what is going on. If you can't, feel free to try contacting us via the methods listed above.