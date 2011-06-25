import my_utils


class Report(object):
    def __init__(self, inquiries):
        self.inqs = inquiries


class Inquiry(object):
    def __init__(self, procs, context = None):
        self.run(procs, context)

    def run(self, procs, context):
        """Do all the necessary work with the data
        and save the stuff you need for the other methods
        """
        raise NotImplementedError()

    def get_table(self):
        """Return a list of lists which, when output as a table would
        be sufficient to allow someone to remake the figure returned
        by get_figure

        Ideally, this should be formatted so someone would be able
        to remake the figure almost instantly in excel
        """
        raise NotImplementedError()

    def get_figure(self):
        """Return a matplotlib figure

        """
        raise NotImplementedError()

    def get_name(self):
        """ Return a name as a unicode object
        """
        raise NotImplementedError()

import numpy as np
import matplotlib.pyplot as plt
class Physician_FPS(Inquiry):

    def run(self, procs, context):
        DAYS_PER_PERIOD = 14
        procs = [p for p in procs if p.is_valid() and p.is_real() and p.has_syngo()]
        procs_by_attending = my_utils.organize(procs, lambda x: x.get_syngo().rad1.replace(',',''))

        first_time = min(procs, key = lambda x: x.get_start_time()).get_start_time()
        last_start_time = max(procs, key = lambda x: x.get_start_time()).get_start_time()
        self.num_periods = int((last_start_time - first_time).days/DAYS_PER_PERIOD)

        out = {}
        for attending, procs in procs_by_attending.iteritems():
            events = [p.get_events() for p in procs]
            events = sum(events, [])# flatten from list of lists to list of events
            events = [e for e in events if e.Irradiation_Event_Type == "Fluoroscopy"]
            events_by_period = my_utils.organize(events,
                                                 lambda e: int((e.get_start_time() - first_time).days/DAYS_PER_PERIOD))
            out[attending] = events_by_period            

        self.lookup = out #lookup[attending][period_number] --> event


    def get_table(self):
        attending_list = sorted(self.lookup.keys())
        dimension = (self.num_periods ,len(attending_list))
        average_table =np.zeros(dimension).tolist()
        count_table = np.zeros(dimension).tolist()
        for a, attending in enumerate(attending_list):
            for period in range(self.num_periods):
                if period in self.lookup[attending]:
                    events = self.lookup[attending][period]
                    count = len(events)
                    average = my_utils.average_fps(events)
                    count_table[period][a] = count
                    average_table[period][a] = average
                else:
                    count_table[period][a] = 0
                    average_table[period][a] = ''
        out = [[''] + attending_list + [''] + attending_list] #heading of table
        print out
        for r in range(len(average_table)):
            row = [r] + average_table[r] + [''] + count_table[r]
            out.append(row)
        return out

    def get_figure(self):
        num_attendings = len(self.lookup.keys())
        fig = plt.figure(1)
        for a, attending in enumerate(sorted(self.lookup.keys())):
            plt.subplot(num_attendings, 1,a)
            plt.axis([0,self.num_periods,5,15])
            plt.xlabel('Period Number')
            plt.ylabel('Average FPS')
            plt.title(attending)
            x = []
            y = []
            s = []
            for period, events in self.lookup[attending].iteritems():
                x.append(period)
                y.append(my_utils.average_fps(events))
                s.append(len(events))
            plt.scatter(x,y,s=s,label=attending)
            plt.plot(x,y,color='red')
        return fig

    def get_name(self):
        return u'Physician FPS'

import jinja2

if __name__ == '__main__':
    procs = my_utils.get_procs('slch')
    procs = [p for p in procs if p.is_pure()]
    inq = Physician_FPS(procs)
    inq.get_figure()
    #env = jinja2.Environment(autoescape=lambda x: True,
    #    loader=jinja2.PackageLoader('core','templates'))
    #template = env.get_template('report.html')
    with open('./templates/report.html','r') as f:
        temp_string = f.read()
    template = jinja2.Template(temp_string)
    with open('output.html','w') as out_f:
        out_f.write(template.render(inquiries = [inq]))
    
            
        


    
        
        
