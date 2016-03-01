# Introduction #

There are some common patterns in inquiry development that srqi provides some special mechanisms for handling.

# Standard Parameters #

It is very common to want to allow users to limit their analyses to procedures that took place in a given date range. To do this, add the class attributes `DATE_RANGE_START` and `DATE_RANGE_END` to your inquiry class as follows:

```
DATE_RANGE_START = inquiry.get_standard_parameter("DATE_RANGE_START")
DATE_RANGE_END = inquiry.get_standard_parameter("DATE_RANGE_END")
```

With these set (you can use one or both), that's all you need to do. The interface and the filtering of procedures is done for you.

# "Organizing" Objects #

We frequently want to group procedures in different ways. For example, we want might want to calculate the mean DAP for events of different Irradiation Event Types. To do this easily, use `srqi.core.my_utils.organize`. For example:
```
#get a bunch of dicom-sr Event objects saved as a list called 'events'
from srqi.core import my_utils
event_dict = my_utils.organize(events, key = lambda e:e.Irradiation_Event_Type
# event_dict['Fluoroscopy'] = a list of all Events in `events` with irradiation type "Fluoroscopy
```
