# Big Design Issues #

Right now when you right an inquiry, you have to decide _a priori_ how to group procedures for comparison. For example, the Physician\_FPS inquiry looks at how the average FPS of each physician changes over time. Thus we are explicitly comparing physicians. However, we could easily want to compare across:
  * Divisions
  * Hospitals
  * Rooms
  * Procedure types (e.g. how does FPS on TIPS compare to FPS on IVC filters)
  * Individual procedures
  * X-ray machines (does one machine always default back to a higher FPS?)
  * Date ranges (somewhat of a special case)
  * Fellows/residents (RAD2's)

And of course you can want to compare across pairs of these things: how do the team of Attending A and Fellow B do vs. Attending A and Fellow C?

This calls out for some kind of orthogonality between the analysis and the groups of procedures over which the data runs.

This also seems like it would be a very common problem in data analysis: filtering data and comparing across different groups. We're basically describing SQL queries here, so there should be a solution that already exists for providing a gui to allow users to build these kinds of queries and feed them into other things for analysis.

Possible solutions:
  * 3rd party data mining software (e.g. RapidMiner) may have already implemented this.
  * Write one inquiry and use drop-down options to allow the user to make a choice, then handle all the options in whatever way is easiest in the inquiry itself. (Possibly even write a special Inquiry\_Parameter subclass)

# Dose Mapping #

Several groups are working on how to map where dose is incident upon the patient's body. A simple-ish first approximation would be to ignore patient position and essentially look at dose incident upon the under side of the table.

Currently blocked on figuring out specific geometry of the x-ray projection of our generators.

# Beam Angles #

Separately from dose-mapping, it may be useful to look at beam-angles of high-dose cases, since some high dosages may be explained by inappropriate imaging through thick or dense body parts, or imaging at oblique angles that unnecessarily increase the radiation dose.

# Procedure Metrics #
Given a procedure CPT code combination, look at distributions of:
  * Number of frames of fluoro and DSA used
  * Total Dose/DAP
  * Fluoro time
  * Procedure duration

Option to give either total distribution or change over time?