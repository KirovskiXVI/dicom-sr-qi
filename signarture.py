import my_utils
import numpy as np

procs = my_utils.get_procs('bjh')
clean_procs = [p for p in procs if p.is_real()]
clean_procs = [p for p in clean_procs if p.has_syngo()]
lookup = my_utils.organize(clean_procs, lambda x: ','.join(x.get_cpts()))
most_common_cpt = max([k for k in lookup.keys()], key=lambda x: len(lookup[x]))
common_procs = lookup[most_common_cpt]
import matplotlib.pyplot as plt
for i in range(4):
    durations = []
    for group in common_procs[i].get_event_groups(6):
        dur = 0
        for e in group:
            dur = dur + my_utils.total_seconds(e.get_duration())
        durations.append(dur)
    average_dur = sum(durations)/len(durations)
    average_durations = [dur/average_dur for dur in durations]
    plt.plot(average_durations) #np.linspace(0,1,len(durations))
        
plt.show()
