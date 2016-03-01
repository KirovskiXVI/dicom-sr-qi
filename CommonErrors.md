# Tutorial Pitfalls #

## Dealing With Missing Data ##

Since we're working with real-life data here, we're bound to run into some unexpected input. For example, if you used sample\_anon.xml as your test data set, you probably got an error like this:

```
An error occured while attempting to write the report.
 Error message is: 
Traceback (most recent call last):
  File "C:\Users\mcstrother\Documents\srqi\gui\main.py", line 173, in run
    self._report_writer.update(data_paths, inq_classes)
  File "C:\Users\mcstrother\Documents\srqi\gui\report_writer.py", line 66, in update
    self._update_inquiry_objects(inquiry_classes, data_changed)
  File "C:\Users\mcstrother\Documents\srqi\gui\report_writer.py", line 62, in _update_inquiry_objects
    self.inqs = [cls(self.procs, extra_procs = self.extra_procs) for cls in inquiry_classes]
  File "C:\Users\mcstrother\Documents\srqi\core\inquiry.py", line 23, in __init__
    self.run(sr_procs, context, extra_procs)
  File "C:\Users\mcstrother\Documents\srqi\active_inquiries\frame_count.py", line 31, in run
    if proc.get_start_time() > self.START_DATE.value: #note the .value part of this
  File "C:\Users\mcstrother\Documents\srqi\core\ReadXML.py", line 195, in get_start_time
    raise my_exceptions.DataMissingError("Procedure has no radiation events.")
DataMissingError: Procedure has no radiation events.

Procedure has no radiation events.
```

Obviously, there must be some SR reports that are generated for procedures where the operator never used any radiation. Since get\_start\_time defined the start of the procedure as the beginning of the first irradiation event, it throws a DataMissingError. Two ways around this are:

  1. Catch the DataMissingError with a `try: except:` block.
  1. Check for the presence of irradiation events before trying to get the start time using the convenience method using `not len(proc.get_events()) == 0`.

So a valid implementation of `run` from the tutorial might looks like:

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
```

## No Procedures In Date Range ##

If you forget to set your Start Date back when you run the inquiry from the gui, you will get a long, fairly unhelpful error ending with: `zero-size array to ufunc.reduce without identity`.

Looking at the traceback, at least you can tell that the error is coming from `plt.scatter` in `get_figures` when you try to pass it two empty lists. It's totally up to you how you want to handle this exception. One way to do it might be to just add a check like:
```
if len(self.frame_counts) ==0:
        return None
```
to `get_figures` and then add something like
```
if len(self.frame_counts) == 0:
    return "WARNING: No procedures found in specified date range."
```
to `get_text`