The inquiry simply computes the average frames/pulses per second used during Fluoro imaging over all of the procedures in a DICOM-SR .xml file.

The graph below shows the output of this inquiry when run on some actual data from one of the sites in Saint Louis.

<img src='http://dicom-sr-qi.googlecode.com/files/Average_Fps0.png' height='300' />

Dot sizes indicate the number of irradiation events that occurred during the period. (Each period was 7 days long in this case.) Obviously, there is some data missing from some of the periods.

## Detailed Description ##

To calculate the "Average" the irradiation events are weighted by their duration, so an event where the pedal was depressed for 60 seconds will be weighted 60 times more than an event where the pedal was depressed by 1 second.

## Effect of FPS on Radiation Dosage ##

Fluoro machines raise radiation dose per frame/pulse in order to preserve image quality when FPS is lowered, so cutting the frame rate in half does not necessarily cut the dose per procedure in half. However, the evidence so far suggests that there is the potential for very significant dose savings by reducing frame rate. Further discussion/evidence is collected below.

A discussion of effect of FPS on image perception: Aufrichtig R, Xue P, Thomas CW, Gilmore GC, Wilson DL. Perceptual comparison of pulsed and continuous fluoroscopy. Med Phys 1994; 21:245-256.

[A paper](http://www.ncbi.nlm.nih.gov/pubmed/11452079) on general radiation exposure issues in Fluoroscopy. Figure 6 (taken from above) shows the effect of reducing FPS on radiation exposure. 15 fps, 10 fps, and 7.5 fps had 88%, 62%, and 51% of the exposure of 30 fps respectively when attempts were made to adjust the dose per frame to give images comparable to the 30 fps sampling, but it remains to be seen how this works in practice with our machines.

The same paper, however, also alludes to some systems "opening the television camera aperture" to compensate for lower fps without increasing frame-rate.