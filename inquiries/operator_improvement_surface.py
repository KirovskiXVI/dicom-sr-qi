from mirqi.core import inquiry
from mirqi.inquiries.operator_improvement import get_procedures_helper, sort_by_rads_helper
import collections
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

class Operator_Improvement_Surface(inquiry.Inquiry):
    MIN_REPS = inquiry.Inquiry_Parameter(50, "Minimum procedure count",
                                         "The minimum number of times a procedure with the same CPT codes must occur to be considered to have a reasonable distribution")
    PROCS_PER_WINDOW = inquiry.Inquiry_Parameter(100, "Procedures Per Window",
                                                 "Number of procedures that should be considered in the sliding window calculation of the operators performance metric.")
    STEP_SIZE = inquiry.Inquiry_Parameter(50, "Step size",
                                          "Number of procedures between the beginnings of each window. ")
    
    def run(self, procs, context, extra_procs):
        cpt_to_procs = get_procedures_helper(procs, extra_procs, self.MIN_REPS.value)
        self.rad1_to_procs = sort_by_rads_helper(sum(cpt_to_procs.values(),[]), self.PROCS_PER_WINDOW.value)
                                          

    def get_figures2(self):
        
        ys = [(1.0/self.PROCS_PER_WINDOW.value)*(i+1) for i in range(self.PROCS_PER_WINDOW.value)]
        figs= []
        for rad1, procs in self.rad1_to_procs.iteritems():
            max_x = 0
            verts = []
            for i in range(0, len(procs), self.STEP_SIZE.value):
                if i+self.PROCS_PER_WINDOW.value < len(procs):
                    xs = sorted([proc.fluoro for proc in procs[i:i+self.PROCS_PER_WINDOW.value]])
                    if xs[-1]>max_x:
                        max_x = xs[-1]
                    verts.append(zip(xs,ys))
                    verts[-1].append((xs[-1],0))#adds a point to the polygon directly below the last point to draw the baseline correctly
            zs = range(len(verts))
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_title(rad1)
            facecolors = [colorConverter.to_rgba('g', alpha=.6) for _ in range(len(verts))]
            poly = PolyCollection(verts,
                              facecolors = facecolors )
            poly.set_alpha(0.7)
            ax.add_collection3d(poly, zs=zs, zdir='y')
            ax.set_xlabel("Fluoro time")
            ax.set_xlim3d(0,10)
            ax.set_zlabel("% of Procedures This Fluoro Time or Below")
            ax.set_ylabel("Time")
            ax.set_ylim3d(0,len(verts))
            plt.show()
            figs.append(fig)
        return figs

    def get_figures2(self):
        all_xs = []
        all_ys = []
        all_zs = []
        ys = [(1.0/self.PROCS_PER_WINDOW.value)*(i+1) for i in range(self.PROCS_PER_WINDOW.value)]
        for rad1, procs in self.rad1_to_procs.iteritems():
            for i in range(0, len(procs), self.STEP_SIZE.value):
                if i+self.PROCS_PER_WINDOW.value < len(procs):
                    xs = sorted([proc.fluoro for proc in procs[i:i+self.PROCS_PER_WINDOW.value]])
                    all_xs += xs
                    all_ys += ys
                    all_zs += [i]*len(xs)
            fig = plt.figure()
            ax = plt.gca(projection='3d')
            surf = ax.plot_surface(np.array(all_xs), np.array(all_ys), np.array(all_zs))
            plt.show()

    def get_figures(self):
        from matplotlib.collections import LineCollection
        ys = [(1.0/self.PROCS_PER_WINDOW.value)*(i+1) for i in range(self.PROCS_PER_WINDOW.value)]
        all_xs = []
        for rad1, procs in self.rad1_to_procs.iteritems():
            for i in range(0, len(procs), self.STEP_SIZE.value):
                if i+self.PROCS_PER_WINDOW.value < len(procs):
                    xs = sorted([proc.fluoro for proc in procs[i:i+self.PROCS_PER_WINDOW.value]])
                    all_xs.append(xs)
            fig = plt.figure()
            ax = plt.gca()
            ax.set_xlim(0,10)
            ax.set_ylim(0,1)
            line_segments= LineCollection([zip(xs,ys) for xs in all_xs])
            line_segments.set_array(range(len(all_xs)))
            ax.add_collection(line_segments)
            plt.show()
        

if __name__ == '__main__':
    inquiry.inquiry_main(Operator_Improvement_Surface, 'bjh')
