import wx
from srqi.core import my_utils
from srqi.gui import report_writer
import datetime
import numbers
import traceback
import numbers


class Inquiry_Parameter_Panel(wx.Panel):

    def __init__(self, *args, **kwargs):
        self.param = kwargs['parameter']
        del kwargs['parameter']
        wx.Panel.__init__(self,*args, **kwargs)
        # add stuff
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, 1, self.param.label))
        if isinstance(self.param.value, datetime.date):
            self.ctrl = wx.DatePickerCtrl(self, style=wx.DP_DROPDOWN)
            wx_date = my_utils.python_date_to_wx_date(self.param.value)
            self.ctrl.SetValue(wx_date)
            sizer.Add(self.ctrl)
        elif isinstance(self.param.value, bool):
            #important that we do this check first, since apparently True can be seen as an int
            self.ctrl = wx.CheckBox(self)
            sizer.Add(self.ctrl)
        elif isinstance(self.param.value, numbers.Real):
            self.ctrl = wx.SpinCtrl(self)
            self.ctrl.SetRange(0,1000000)
            self.ctrl.SetValue(self.param.value)
            sizer.Add(self.ctrl)
        else:
            raise NotImplementedError("Inquiry has parameter that cannot be displayed in the gui.")
        self.SetSizer(sizer)
            
    def get_value(self):
        value = self.ctrl.GetValue()
        if isinstance(value, wx.DateTime):
            value = my_utils.wx_date_to_python_date(value)
        return value
        

class Inquiry_Panel(wx.CollapsiblePane):
    def __init__(self, *args, **kwargs):
        self._inquiry_class = kwargs['inquiry_class']
        del kwargs['inquiry_class']
        kwargs['label'] = self._inquiry_class.get_name()
        wx.CollapsiblePane.__init__(self,*args, **kwargs)
        # add stuff
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.enabled_box = wx.CheckBox(self.GetPane(),label = "Enabled")
        self.description_link = wx.HyperlinkCtrl(self.GetPane(),wx.ID_ANY,
                                                 "Description", 'inquiry.get_description')
        sizer.Add(self.enabled_box)
        sizer.Add(self.description_link)
        self.Bind(wx.EVT_HYPERLINK, self.show_description, self.description_link)
        param_names = self._inquiry_class.get_parameter_names()
        self.param_panels = {}
        params = [getattr(self._inquiry_class, param_name) for param_name in param_names]
        for param_name, param in zip(param_names,params):
            param_panel = Inquiry_Parameter_Panel(self.GetPane(), parameter=param)
            self.param_panels[param_name] = param_panel
        #add the panels in the right order
        for panel in sorted(self.param_panels.values(), key= lambda x:x.param.weight):
            sizer.Add(panel)
        self.GetPane().SetSizer(sizer) # see http://xoomer.virgilio.it/infinity77/wxPython/Widgets/wx.CollapsiblePane.html for why GetPane is used here
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.on_change)

    def is_enabled(self):
        return self.enabled_box.GetValue()

    def show_description(self, event):
        dlg = wx.MessageDialog(self.GetPane(),
                                       message = self._inquiry_class.get_description(),
                                       style=wx.OK)
        dlg.ShowModal()
    
    def get_inquiry_class(self):
        for param_name in self._inquiry_class.get_parameter_names():
            new_value = self.param_panels[param_name].get_value()
            getattr(self._inquiry_class, param_name).set_value(new_value)
        return self._inquiry_class

    def on_change(self, event):
        self.GetParent().Layout()

class Inquiry_Selection_Panel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.inq_panels = []
        for inq in my_utils.get_inquiry_classes():
            inq_panel = Inquiry_Panel(self, inquiry_class=inq)
            self.inq_panels.append(inq_panel)
            sizer.Add(inq_panel,0)
        self.SetSizer(sizer)
        
    def get_inquiry_classes(self):
        out = []
        for p in self.inq_panels:
            if p.is_enabled():
                out.append(p.get_inquiry_class())
        return out
        



class Main_Frame(wx.Frame):

    def __init__(self, *args, **kwargs):
        import data_panel
        wx.Frame.__init__(self, *args, **kwargs)
        self.main_panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.data_panel = data_panel.Data_Panel(self.main_panel, style=wx.RAISED_BORDER)
        self.inq_selection_panel = Inquiry_Selection_Panel(self.main_panel, style=wx.RAISED_BORDER)
        sizer.Add(self.data_panel,1,wx.EXPAND)
        sizer.Add(self.inq_selection_panel,2,wx.EXPAND)
        run_button = wx.Button(self.main_panel, label = "Run")
        self.Bind(wx.EVT_BUTTON, self.run, run_button)
        sizer.Add(run_button,0,wx.ALIGN_CENTER)
        self.main_panel.SetSizer(sizer)
        self._report_writer = None

    def show_exception(self, e):
        dlg = wx.MessageDialog(self.main_panel,
                                       message = "An error occured while attempting to write the report."\
                                       "\n Error message is: \n" +traceback.format_exc()\
                                       +'\n'+ str(e),
                                       style=wx.CANCEL|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        

    def run(self, event):
        inq_classes = self.inq_selection_panel.get_inquiry_classes()
        prog_dlg = wx.ProgressDialog(title = "Running inquiries",
                                     message = "Reading and processing data files",
                                     maximum = 2,
                                     parent = self.main_panel,
                                     style = wx.PD_AUTO_HIDE|wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME)
        data_paths = self.data_panel.get_file_names()
        try:
            if not self._report_writer:
                self._report_writer = report_writer.Report_Writer(data_paths,inq_classes)
            else:
                self._report_writer.update(data_paths, inq_classes)
            cont, _ = prog_dlg.Update(1, "Writing report.")
            if cont:
                self._report_writer.write()
        except Exception as e:
            self.show_exception(e)
            prog_dlg.Update(2, "Done")
        prog_dlg.Update(2, "Done")


class MirqiApp(wx.App):
    def OnInit(self):
        frame = Main_Frame(None, title = "MIR Quality Improvement")
        frame.Show(True)
        frame.Centre()
        return True

def main():
    app = MirqiApp(0)
    app.MainLoop()

if __name__ == "__main__":
    main()
    



