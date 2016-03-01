# Introduction #

There are lots of common tasks that require automation when working with DICOM-SR files. Documented here are our solutions to these problems.

# Anonymizing Care Analytics DICOM-SR Files #

This documents the process we used to create the anonymized .xml file that we distribute with our demo releases.

After installing srqi, run python in interactive mode from the directory containing the srqi folder. Then do the following:

```
>>>#in_path = path to the xml file to be anonymized. for example "C:\\Users\\mcstrother\\my_data\\sample.xml"
>>>#out_path = path to the desired output file. e.g. "C:\\Users\\mcstrother\\my_data\\smaple_anon.xml"
>>>from srqi.core.anonymize import anonymize_sr
>>>anonymize_sr(in_path, out_path)
```

The `anonymize_sr` function attempts to fully anonymize the data while preserving as much of the meaningful information within it as possible. There are some trade-offs involved, so the current implementation errs on the side of destroying too much information and making absolutely sure that the data is fully anonymized. If this becomes a commonly used feature, we will fine tune the algorithm over time and we may even add the ability to customize what information is or is not removed.