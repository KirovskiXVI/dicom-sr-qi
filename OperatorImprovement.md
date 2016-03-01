This metric attempts to comment on the amount of fluoro time`***` that an operator uses during procedures relative to his peers. It does this by grouping procedures by their CPT codes, looking at the median fluoro time for each group, and comparing the procedures done by the physician in a given "window" of time to these medians.

The end result is a plot like the one shown below which shows how a physician's metric compares to that of his peers over time:

<img src='http://dicom-sr-qi.googlecode.com/files/blended attendings simulation.png' height='300' />

Here we can see a group of 3 physicians, each using significantly different amounts of fluoro during procedures and each seeming to improve at least somewhat over time.

It's options menu in the graphical user interface looks like this:

<img src='http://dicom-sr-qi.googlecode.com/files/operator_improvement%20options.png' height='125' />

# Data Requirements #

Syngo data possibly supplemented with DICOM-SR data. This inquiry relies on Syngo data to separate procedures by CPT codes and which physicians performed them. If DICOM-SR data is available, the inquiry will use fluoro times from the DICOM-SR data instead of the Syngo data, as DICOM-SR data is taken to be the gold standard of accuracy for fluoro time recording.

# Detailed Description of Metric #
It is calculated as follows:

  * First, we exclude all “uncommon” procedures. We define an uncommon procedure as any cpt code combination for which we have fewer than "Minimum Procedure Count" examples in the data set.
  * Then we calculate the median fluoro time for every remaining procedure type.
  * Then, for each procedure performed by an operator we calculate a fluoro time "excess".
    * We define this to be the (fluoro time for that procedure - the median fluoro time for that procedure type) / the median fluoro time for that procedure type`*`.
    * For example, if a physician does a procedure with cpt code combination "36556, 77001" (insertion of a non-tunneled cath under fluoro guidance), and uses 3 minutes of fluoro, we would compare that number 3 to the median number of minutes of fluoro in our data set for all non-tunneled cath placements. If that median was 2 minutes, we would say that the physician's "excess" would be (3-2)/2 = .5, meaning that he used 50% more fluoro for this procedure than might be expected.
    * We set the maximum "excess" to be 2`**` to avoid over-penalizing a physician for encountering a single very difficult instance of a very common procedure.
  * We then take a sliding window of different sizes (400 procedures by default), average the excesses over all the procedures in the window, and plot.

`*` If "Normalize excesses" is turned off, then we don't divide by the median fluoro time, but this should almost always be left on. Leaving it off can make the metric much more sensitive to case mix, as cases with longer median fluoro times also tend to have larger variations in fluoro times. We found that in at least one case, a phyiscian who was actually improving according the "normalized" metric appeared to be getting worse according to the non-normalized metric, presumably because he was beginning to do longer procedures. However, disabling "normalize excess" can give you an idea of how many extra minutes of fluoro are being used by a physician, since the units of the y axis will be in minutes instead of as a percent of expected.

`**` This can be turned on and off with the "Limit Excess" option.

`***` On this page we use "fluoro time" to mean "pedal time".

# Validation #

We have qualitatively validated this metric in several ways:

Looking at data from our own physicians, there is significant iter-physician variation. There are some striking examples of differences in fluoro usage that can be easily explained by years of experience. There are also at least 2 examples of significant reductions in fluoro usage made by a physician over the course of the time frame for which we have data.

We also generated some simulated data sets and plotted their results when run through the Operator Improvement inquiry algorithm. (Results shown below.)

## Lognormal Simulation ##
The first image shows a simulation in which we took the procedure dates from a real physician, but changed all the CPT codes so that all procedures appeared to be of a single type. We then changed all the fluoro times, drawing new times randomly from a lognormal distribution. Finally, we multiplied every time by an improvement factor which ranged from 1.0 at the beginning of the time frame to .8 at the end to simulate a 20% improvement. The window used was 400 procedures wide. The graph clearly demonstrates that the improvement is visible through the noise of the distribution (mean and stddev of underlying normal distribution were log(5) and .5 respectively) and through the smoothing inherent in the windowing.

<img src='http://dicom-sr-qi.googlecode.com/files/lognormal simulation.png' height='300' />

The code for this simulation can be found in simulate\_data2.py

The same graph simulant, but with a window size of 50 instead of 400.

<img src='http://dicom-sr-qi.googlecode.com/files/simulated%20improvement%20w50.png' height='300' />

## Blended Attendings ##

Next we performed an experiment to simulate improvement with the minimum number of modifications of the data set possible. We began by selecting 3 physicians, a "basis", "most", and "least". The "most" and "least" were chosen for using the most fluoro time and least fluoro time respectively (from visualization of their Operator Improvement plots). The "basis" attending essentially provided a list of cpt codes and dates to which we assigned fluoro times as follows. For each procedure, we looked at the set of procedures with the same cpt code combination that were performed by either the "most" attending or the "least" attending. We then randomly chose a fluoro time from either the "most" attending's procedures or the "least" attendings procedures in such a way that the probability of choosing from the "most" attending's procedures moved linearly from 100% to 0% from the beginning of the time frame to the end. (See the image below, which shows the algorithm run on "most", "least", and "simulated.) This allowed us to create a set of simulated procedures with an extremely realistic case mix and distribution of fluoro times while making very few assumptions about the data. Again, the evidence of improvement is clear.

<img src='http://dicom-sr-qi.googlecode.com/files/blended attendings simulation.png' height='300' />



## Lognormal July Effect ##

Another pattern we anticipate seeing in some of the data is the "July Effect", which predicts that the amount of fluoro use will go up starting July 1st when new fellows arrive and decrease slowly over the year after that.

To see how this might appear in our plots, we used the procedure described in "Lognormal Simulation" above, except instead of applying a transformation to simulate improvement, we applied the transformation new\_fluoro\_time = old\_fluoro\_time `*` (1.x - .x`*`# of days since july first/(# of days from july first to january 1st)), where `x` is the percent increase in fluoro usage we expect from the July effect.

Some plots of different window sizes and values of X are below.

### Window 400 procedures, July Effect = 20% ###
<img src='http://dicom-sr-qi.googlecode.com/files/simulated july window 400 20 percent.png' height='300' />

### Window 50 procedures, July Effect = 20% ###
<img src='http://dicom-sr-qi.googlecode.com/files/simulated july window 50 20percent.png' height='300' />

### Window 400 procedures, July Effect = 50% ###
<img src='http://dicom-sr-qi.googlecode.com/files/simulated%20july%20window400%2050percent.png' height='300' />


### Window 50 procedures, July Effect = 50% ###
<img src='http://dicom-sr-qi.googlecode.com/files/simulated july window 50 50percent.png' height='300' />