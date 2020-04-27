from tkinter import filedialog
from InvoiceData import InvoiceData
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
from statistics import mean

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler


from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import datetime

from PIL import Image, ImageTk
import inspect
from Calendar import *
from CompanyReport import CompanyReport



class BadDebt(ttk.Frame):
    
    # class variable to track direction of column
    # header sort
    SortDir = True     # descending
    BdSortDir = True
        
    def __init__(self, isapp=True, name='badDebt'):
        
        self.maindata = []
        self.data = []    
        self.badDebt = ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Bad Debt Report')
        self.isapp = isapp
        
        self.dFromTxt=StringVar()
        self.dToTxt=StringVar()
        self.fileNameTxt=StringVar()
        self.fileNameTxt.set('No file selected')
        self.selected = None        
        self.wopen=False
        self._create_demo_panel()
                
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)        
        self._create_treeview(demoPanel)
        self._load_data()
    
    def _create_treeview(self, parent):
        # Fixing a bug related to Tkinter style font colours not showing with Tkinter version 8.6.9 - https://bugs.python.org/issue36468
        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.
        
            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
        
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        # Python code bug fix ends here
        
        f = ttk.Frame(parent)
        f.pack(side=TOP, fill=BOTH, expand=Y)
        
        # create the tree and scrollbars
        self.dataCols = ('Lasku no.', 'Tosite no.', 'Asiakas nro', 'Asiakkaan nimi', 'Kategoria', 'Laskun päivä', 'Eräpäivä', 'Summa ilman ALVia', 'ALV', 'Yhteensä')        
        self.tree = ttk.Treeview(columns=self.dataCols, height=15, selectmode='browse', show = 'headings')
        self.tree.bind('<ButtonRelease-1>', self.checkSelection)
        
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set
                
        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=1, column=0, columnspan=8, padx=10, sticky=NSEW)
        ysb.grid(in_=f, row=1, column=8, sticky=NS)
        xsb.grid(in_=f, row=2, column=0, columnspan=8, sticky=EW)
        
        # add filename label
        filenameLabel = ttk.Label(textvariable=self.fileNameTxt)
        filenameLabel.grid(in_=f, row=0, column=0, columnspan=8, sticky=EW, padx=10, pady=10)
        
        # add separator and buttons
        sep = ttk.Separator(orient=HORIZONTAL)
        openBtn = ttk.Button(text='Open File', command=self.readData)
        summaryBtn = ttk.Button(text='Summary', command=self.summary)
        trendlineBtn = ttk.Button(text='Trendline', command=self.trendLine)
        agingBtn = ttk.Button(text='Aging Schedule', command=self.agingSchedule)
        baddebtBtn = ttk.Button(text='Bad Debt', command=self.badDebtReport)
        dismissBtn = ttk.Button(text='Close', command=self.winfo_toplevel().destroy)
        datefromLabel = ttk.Label(text='Date from:')
        datetoLabel = ttk.Label(text='Date to:')
                 
        
        self.dFromTxt.set("")
        self.dToTxt.set("")
        dFrom=ttk.Label(width=10, textvariable=self.dFromTxt, background='white', borderwidth=2, relief='groove')
        dTo=ttk.Label(width=10, textvariable=self.dToTxt, background='white', borderwidth=2, relief='groove')
        currMonth = ttk.Button(text='Current month', command=self.setCurrMonth)
        currYear = ttk.Button(text='Current year', command=self.setCurrYear)
        clrDate = ttk.Button(text='Clear date selection', command=self.clearDate)
        aboutBtn = ttk.Button(text='About', command=self.about)
        
        #Create Select From Date -button
        im = Image.open('images//calendar_blank.png')
        imh1 = ImageTk.PhotoImage(im)
        selFromBtn = ttk.Button(image=imh1, command=self.selDateFrom)
        selFromBtn.image = imh1
        
        #Create Select From Date -button
        imh2 = ImageTk.PhotoImage(im)
        selToBtn = ttk.Button(image=imh2, command=self.selDateTo)
        selToBtn.image = imh2
        
        #Create frame for date controls 
        f2 = ttk.Frame(parent)
        datefromLabel.grid(in_=f2, row=0, column=0, sticky=W)
        datetoLabel.grid(in_=f2, row=1, column=0, sticky=W)
        dFrom.grid(in_=f2, row=0, column=1, padx=5)
        dTo.grid(in_=f2, row=1, column=1, padx=5)
        currMonth.grid(in_=f2, row=0, column=3, sticky=EW, padx=5)
        currYear.grid(in_=f2, row=1, column=3, sticky=EW, padx=5)
        clrDate.grid(in_=f2, row=0, column=4, sticky=EW, padx=5)
        selFromBtn.grid(in_=f2, row=0, column=2)
        selToBtn.grid(in_=f2, row=1, column=2)
        
        
        # add separator and buttons to the frame, including date controls frame
        sep.grid(in_=f, row=3, column=0, columnspan=9, sticky=EW, pady=5)
        f2.grid(in_=f, row=4, column=2, columnspan=6, sticky=EW, pady=5)
        openBtn.grid(in_=f, row=5, column=2, sticky=EW, pady=5)
        summaryBtn.grid(in_=f, row=5, column=3, sticky=EW, pady=5)
        trendlineBtn.grid(in_=f, row=5, column=4, sticky=EW, pady=5)
        agingBtn.grid(in_=f, row=5, column=5, sticky=EW, pady=5)
        baddebtBtn.grid(in_=f, row=5, column=6, sticky=EW, pady=5)
        dismissBtn.grid(in_=f, row=5, column=7, sticky=EW, pady=5)
        aboutBtn.grid(in_=f, row=6, column=2, sticky=EW, pady=5)
        
        # set frame resize priorities
        f.rowconfigure(1, weight=1)
        f.columnconfigure(0, weight=1)

    
    def _load_data(self):
        
        # configure column headings
        for c in self.dataCols:
            self.tree.heading(c, text=c,
                              command=lambda c=c: self._column_sort(c, BadDebt.SortDir))            
            self.tree.column(c, anchor='w', width=Font().measure(c))
            
             
        # define tags for Treeview row colors - black for positive and red for negative values 
        self.tree.tag_configure('debit', foreground='black')
        self.tree.tag_configure('credit', foreground='red')
        
        # add data to the tree 
        for item in self.maindata:
            arr = (item.ino, item.rno, item.cno, item.cname, item.cat, item.idate.strftime("%d-%m-%Y"), item.ddate.strftime("%d-%m-%Y"), self.comsep(item.sevat), self.comsep(item.vat), self.comsep(item.s))
            if item.s >= 0:
                self.tree.insert('', 'end', values=arr, tags=('debit',))
            else:
                self.tree.insert('', 'end', values=arr, tags=('credit',))
                
            # and adjust column widths if necessary
            for idx, val in enumerate(arr):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width = iwidth)

        
    def _column_sort(self, col, descending=False):
        
        # grab values to sort as a list of tuples (column value, column id)
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)   # item[1] = item Identifier
        
        # reverse sort direction for next sort operation
        BadDebt.SortDir = not descending
    
    def checkSelection(self, a):
        # remove selection if pressed again, otherwise allocate selection to self.selected 
        curItem = self.tree.focus()
                
        if curItem == self.selected and self.selected is not None:
            for item in self.tree.selection():
                self.tree.selection_remove(item)
            self.selected = None
        else:    
            self.selected = curItem
        
    
    def setCurrMonth(self):
        #Find last day of the month
        dtoday = datetime.date.today()
        next_month = dtoday.replace(day=28) + datetime.timedelta(days=4)
        last_day_of_month = next_month - datetime.timedelta(days=next_month.day)
            
            
        #Set dates for the first and last of the month
        self.dFromTxt.set(datetime.date.today().replace(day=1).strftime('%d-%m-%Y'))
        self.dToTxt.set(datetime.date.today().replace(day=(last_day_of_month.day)).strftime('%d-%m-%Y'))
    
    def setCurrYear(self):
        self.dFromTxt.set(datetime.date.today().replace(day=1, month=1).strftime('%d-%m-%Y'))
        self.dToTxt.set(datetime.date.today().replace(day=31, month=12).strftime('%d-%m-%Y'))
            
    
    def clearDate(self):
        self.dFromTxt.set("")
        self.dToTxt.set("")
    
        
    def selDateFrom(self):
        root2=Toplevel()
        root2.title("Select date")
        ttkcal=Calendar(master=root2, selection_callback=self.get_selectionFrom, firstweekday=calendar.MONDAY)
        ttkcal.pack(expand=1, fill='both')
        root2.update()
        root2.minsize(root2.winfo_reqwidth(), root2.winfo_reqheight())
        root2.mainloop()
        
        
    def get_selectionFrom(self, selection):
        self.dFromTxt.set(selection.strftime('%d-%m-%Y'))
        
    
    def selDateTo(self):
        root2=Toplevel()
        root2.title("Select date")
        ttkcal=Calendar(master=root2, selection_callback=self.get_selectionTo, firstweekday=calendar.MONDAY)
        ttkcal.pack(expand=1, fill='both')
        root2.update()
        root2.minsize(root2.winfo_reqwidth(), root2.winfo_reqheight())
        root2.mainloop()
        
        
    def get_selectionTo(self, selection):
        self.dToTxt.set(selection.strftime('%d-%m-%Y'))
    
    
    def test(self):
        # This method checks whether data has been loaded before attempting to run analysis
        if len(self.maindata) == 0: 
            messagebox.showinfo(title="No data selected", message="Please open and select a CSV file before running analysis.")
            return False
        
        if len(self.data) == 0:
            messagebox.showinfo(title="No invoices in period", message="There are no invoices with invoice dates within the selected period.\n\nPlease select different from and to dates and try again.")
            return False
        
        return True
    
    def about(self):
        # Brings up information on program
        messagebox.showinfo(title="About", message="Bad Debt Analysis Tool\nVersion 1.0\n\nCompiled as part of TUAS Software Development Course, spring 2020.\n© 2020 Mikko Wiseman")
    
    def filterData(self):
        # Check if user has selected a customer number in TreeView
        customerNumber = None
        if self.selected is not None:
            vals = self.tree.item(self.selected).get('values')
            customerNumber = vals[2]
        
        self.data.clear()
        for item in self.maindata:
            # Filter only selected customers to data, ignore if no customer is selected
            if customerNumber is not None:
                if customerNumber is not item.cno:
                    continue
            
            # Check if invoice date range matches with user selected date range, ignore if no date selection
            if (self.dFromTxt.get() == "" or item.idate >= datetime.datetime.strptime(self.dFromTxt.get(), '%d-%m-%Y').date()) and (self.dToTxt.get() == "" or item.idate <= datetime.datetime.strptime(self.dToTxt.get(), '%d-%m-%Y').date()):
                self.data.append(item)
        
        
    def readData(self):
    
        #Trying to open file
        try:
            
            filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
            
            # if no filename selected, throw an error
            if filename == None:
                raise OSError
            
            with open(filename, mode='r', encoding='utf-8') as f:
                #Delete existing data from self.maindata
                self.maindata.clear()
                
                #Reading data
                for line in f:
                    entries = line.split(";")
                    
                    #If data is valid, creating a new InvoiceData object and adding it to a list
                    try:
                        self.maindata.append(InvoiceData(entries[0], entries[1], entries[2], entries[3], entries[4], entries[5], entries[6], entries[7], entries[8], entries[9]))
                    except:
                        # Can add additional read error handling mechanisms here - currently just ignoring and not entering data if corrupted
                        continue
                    
                total = 0.0
                for line in self.maindata:
                    total += line.s
                
                
                self.fileNameTxt.set("File: " + filename.replace('/','\\'))
                # Display data
                self._load_data()
                    
                # Display success message
                msg = str(len(self.maindata)) + " lines with a total value of " + str(self.comsep(round(total, 2))) + " read from file."
                messagebox.showinfo(title="Success!", message=msg )
                      
        except ValueError: # Catching an error related to data 
            messagebox.showinfo(title="Data corrupted or not valid CSV data file!", message="Unable to use file data")
            f.close()
        except OSError: # Catching an IO-exception
            messagebox.showinfo(title="File read error", message="No file selected or error reading file!")
        
    
    
    def comsep(self, num):
        # Returns a value with thousands separated with commas
        return "{:,}".format(num)
    
    def summary(self):
        self.filterData()
        
        # Testing whether data has been loaded before attempting to run analysis - if not, terminating the method run by null return
        if self.test() == False:
            return
        sumroot = Tk()
        sumroot.title("Summary")
        sumframe = Frame(sumroot)
        sumframe.pack(side=TOP, fill=BOTH, expand=Y)
        
        total = 0
        debit = 0
        credit = 0
        itemno = len(self.data)
        
        for line in self.data:
            total += line.s
            if line.s < 0:
                credit += line.s
            else:
                debit += line.s
            
        if self.selected == None:
            selectedlabel = ttk.Label(sumframe, text='All entries', font=('Helvetica', 16, 'bold'))
        else:
            dataline = self.tree.item(self.selected).get('values')
            companyname = dataline[3]
            
            selectedlabel = ttk.Label(sumframe, text=companyname, font=('Helvetica', 16, 'bold'))
            
        totallabel = ttk.Label(sumframe, text='Invoices total: ')
        totalsum = ttk.Label(sumframe, text=str(self.comsep(round(total, 2))))
        debitlabel = ttk.Label(sumframe, text='Debit notes: ')
        debitsum = ttk.Label(sumframe, text=str(self.comsep(round(debit, 2))))
        creditlabel = ttk.Label(sumframe, text='Credit notes: ')
        creditsum = ttk.Label(sumframe, text=str(self.comsep(round(credit, 2))))
        itemnolabel = ttk.Label(sumframe, text='Number of items: ')
        itemnosum = ttk.Label(sumframe, text=str(self.comsep(itemno)))
        
        selectedlabel.grid(in_=sumframe, row=0, column=0, columnspan=2, sticky=EW, padx=10, pady=20)
        itemnolabel.grid(in_=sumframe, row=1, column=0, sticky=W, padx=10, pady=5)
        itemnosum.grid(in_=sumframe, row=1, column=1, sticky=W, padx=10, pady=5)
        totallabel.grid(in_=sumframe, row=2, column=0, sticky=W, padx=10, pady=5)
        totalsum.grid(in_=sumframe, row=2, column=1, sticky=W, padx=10, pady=5)
        debitlabel.grid(in_=sumframe, row=3, column=0, sticky=W, padx=10, pady=5)
        debitsum.grid(in_=sumframe, row=3, column=1, sticky=W, padx=10, pady=5)
        creditlabel.grid(in_=sumframe, row=4, column=0, sticky=W, padx=10, pady=5)
        creditsum.grid(in_=sumframe, row=4, column=1, sticky=W, padx=10, pady=5)
        
        lateframe = ttk.Frame(sumroot)
        lateframe.pack(side=BOTTOM, fill=BOTH, expand=Y)
        
        # create the tree and scrollbars
        self.lateDataCols = ('Lasku no.', 'Tosite no.', 'Asiakas nro', 'Asiakkaan nimi', 'Kategoria', 'Laskun päivä', 'Eräpäivä', 'Summa ilman ALVia', 'ALV', 'Yhteensä')        
        self.latetree = ttk.Treeview(lateframe, columns=self.dataCols, height=10, selectmode='browse', show = 'headings')
        
        lateysb = ttk.Scrollbar(lateframe, orient=VERTICAL, command= self.latetree.yview)
        latexsb = ttk.Scrollbar(lateframe, orient=HORIZONTAL, command= self.latetree.xview)
        self.latetree['yscroll'] = lateysb.set
        self.latetree['xscroll'] = latexsb.set
        sep = ttk.Separator(lateframe, orient=HORIZONTAL)
        closeBtn = ttk.Button(lateframe, text='Close', command=sumroot.destroy)
        latelabel = ttk.Label(lateframe, text='Late invoices:', foreground='red', font=('Helvetica', 16, 'bold'))
        
        # add tree and scrollbars to frame
        sep.grid(in_=lateframe, row=0, column=0, columnspan=3, sticky=EW, pady=10)
        latelabel.grid(in_=lateframe, row=1, column=0, sticky=W, padx=10, pady=10)
        self.latetree.grid(in_=lateframe, row=2, column=0, columnspan=2, padx=10, sticky=NSEW)
        lateysb.grid(in_=lateframe, row=2, column=3, sticky=NS)
        latexsb.grid(in_=lateframe, row=3, column=0, columnspan=2, sticky=EW)
        closeBtn.grid(in_=lateframe, row=4, column=1, sticky=W, pady=10)
        
        # configure column headings
        for c in self.lateDataCols:
            self.latetree.heading(c, text=c)            
            self.latetree.column(c, anchor='w', width=Font().measure(c))
            
        # add data to the tree 
        for item in self.data:
            
            if item.ddate < datetime.date.today():
                arr = (item.ino, item.rno, item.cno, item.cname, item.cat, item.idate.strftime("%d-%m-%Y"), item.ddate.strftime("%d-%m-%Y"), self.comsep(item.sevat), self.comsep(item.vat), self.comsep(item.s))
                if item.s >= 0:
                    self.latetree.insert('', 'end', values=arr)
                
                    
                # and adjust column widths if necessary
                for idx, val in enumerate(arr):
                    iwidth = Font().measure(val)
                    if self.latetree.column(self.lateDataCols[idx], 'width') < iwidth:
                        self.latetree.column(self.lateDataCols[idx], width = iwidth)
    
    def badDebtReport(self):
        
        # Testing whether data has been loaded before attempting to run analysis - if not, terminating the method run by null return
        if len(self.maindata) == 0: 
            messagebox.showinfo(title="No data selected", message="Please open and select a CSV file before running analysis.")
            return
        
        bdroot = Tk()
        bdroot.title("Bad Debt Report")
        bdcomframe = Frame(bdroot)
        bdcomframe.pack(side=TOP, fill=BOTH, expand=Y)
        
        # Creating a dictionary for company data and adding items from maindata to sumnmarise
        complist = {}
        
        for item in self.maindata:
            if item.cno in complist.keys():
                x = complist[item.cno]
            else:
                x = CompanyReport(item.cno, item.cname)
                
            ovd = (datetime.date.today()- item.ddate).days
            
            if ovd <= 0:    
                x.addCur(item.s)
            else:
                x.addOvd(item.s)
            
            x.addOvdd(ovd)
            complist[item.cno] = x
        
        # create the tree and scrollbars
        self.bdDataCols = ('Asiakas nro', 'Asiakkaan nimi', 'Laskuja ajoissa', 'Laskuja myöhässä', 'Myöhässä %', 'Keskim. myöhässä vrk', 'Max myöhässä vrk')        
        self.bdtree = ttk.Treeview(bdcomframe, columns=self.bdDataCols, height=10, selectmode='browse', show = 'headings')
        
        bdysb = ttk.Scrollbar(bdcomframe, orient=VERTICAL, command= self.bdtree.yview)
        bdxsb = ttk.Scrollbar(bdcomframe, orient=HORIZONTAL, command= self.bdtree.xview)
        self.bdtree['yscroll'] = bdysb.set
        self.bdtree['xscroll'] = bdxsb.set
        sep = ttk.Separator(orient=HORIZONTAL)
        
        # add tree and scrollbars to frame
        self.bdtree.grid(in_=bdcomframe, row=0, column=0, columnspan=2, padx=10, pady=5, sticky=NSEW)
        bdysb.grid(in_=bdcomframe, row=0, column=3, sticky=NS)
        bdxsb.grid(in_=bdcomframe, row=1, column=0, columnspan=2, sticky=EW)
        #sep.grid(in_=bdcomframe, row=2, column=0, columnspan=3, sticky=EW, pady=5)
        
        # set frame resize priorities
        bdcomframe.rowconfigure(0, weight=1)
        bdcomframe.columnconfigure(0, weight=1)

        
        # configure column headings
        for c in self.bdDataCols:
            self.bdtree.heading(c, text=c,
                              command=lambda c=c: self.BdColumnSort(c, BadDebt.BdSortDir))            
            self.bdtree.column(c, anchor='w', width=Font().measure(c))
        
        
        fig = Figure(figsize=(3, 4), dpi=100, constrained_layout=True)
        fig.patch.set_facecolor('#F0F0F0')
        fig.patch.set_alpha(0.7)
        bdchart = fig.add_subplot(111)
        
        bdchart.title.set_text("Current vs. late")
        bdchart.set_xticks(np.arange(len(complist.keys())))
        
        xlegend = []
        for item in complist.values():
            xlegend.append(item.cname)
        
        bdchart.set_xticklabels(xlegend, rotation=45, fontsize=8)
        
        
        canvas = FigureCanvasTkAgg(fig, master=bdroot)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, bdroot)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #Close button functionality
        def _quit():
            bdroot.quit()     # stops mainloop
            bdroot.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=bdroot, text="Close", command=_quit)
        button.pack(side=BOTTOM)
        
        # add data to the tree
        pos = 0
        for item in complist.values():
            arr = (item.cno, item.cname, self.comsep(round(item.currs, 2)), self.comsep(round(item.ovds, 2)), int(round((item.ovds/(item.currs+item.ovds)*100), 0)), int(round(mean(item.ovdd), 0)), max(item.ovdd)) 
            self.bdtree.insert('', 'end', values=arr)
                    
            # and adjust column widths if necessary
            for idx, val in enumerate(arr):
                iwidth = Font().measure(val)
                if self.bdtree.column(self.bdDataCols[idx], 'width') < iwidth:
                    self.bdtree.column(self.bdDataCols[idx], width = iwidth)
            # add bar charts
            bdchart.bar(pos, item.currs, align='center', color='blue')
            bdchart.bar(pos, -item.ovds, align='center', color='red')
            
            pos += 1
            
        mainloop()        
        
    def BdColumnSort(self, col, descending=False):
        
        # grab values to sort as a list of tuples (column value, column id)
        data = [(self.bdtree.set(child, col), child) for child in self.bdtree.get_children('')]
        
        # reorder data
        # tkinter looks after moving other items in
        # the same row
        data.sort(reverse=descending)
        for indx, item in enumerate(data):
            self.bdtree.move(item[1], '', indx)   # item[1] = item Identifier
        
        # reverse sort direction for next sort operation
        BadDebt.BdSortDir = not descending
        
            
    def agingSchedule(self):
        self.filterData()
        
        # Testing whether data has been loaded before attempting to run analysis - if not, terminating the method run by null return
        if self.test() == False:
            return
        
        curr=0.0 # Value of invoices not due
        cat1=0.0 # Value of invoices 0-30 days old
        cat2=0.0 # Value of invoices 31-60 days old
        cat3=0.0 # Value of invoices over 61 days old
        
        tod = datetime.date.today()
        
        for line in self.data:
            
            if (tod - line.ddate).days < 0:
                curr += line.s
            elif (tod - line.ddate).days < 30:
                cat1 += line.s
            elif (tod - line.ddate).days <= 60:
                cat2 += line.s
            elif (tod - line.ddate).days > 60:
                cat3 += line.s
        
        cats = ['Current\n' + str(round(curr, 2)), '0-30:\n' + str(round(cat1, 2)), '31-60\n'+ str(round(cat2, 2)), '61+\n' + str(round(cat3, 2))]
        
        res = [curr, cat1, cat2, cat3]
        
        root = Tk()
        root.wm_title("Aging invoice report")
        y_pos = np.arange(len(cats))
        fig = Figure(figsize=(9, 6), dpi=100, constrained_layout=True)
        fig.patch.set_facecolor('#F0F0F0')
        ai = fig.add_subplot(111)
        
        ai.bar(y_pos, res, align='center', color=['green','blue','orange', 'red'])
        
        ai.title.set_text("Aging invoice report")
        
        ai.set_xticks(y_pos)
        ai.set_xticklabels(cats)
        ai.set_ylabel('Value')
        
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #Close button functionality
        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=root, text="Close", command=_quit)
        button.pack(side=BOTTOM)
        
        mainloop()
    
    def trendLine(self):
        
        self.filterData()
        
        # Testing whether data has been loaded before attempting to run analysis - if not, terminating the method run by null return
        if self.test() == False:
            return
        
        dates = []
        
        
        for line in self.data:
            dates.append(line.ddate)
        
        if self.dFromTxt.get() == "" or min(dates) > datetime.datetime.strptime(self.dFromTxt.get(), '%d-%m-%Y').date():
            mindate = min(dates)
        else:
            mindate = datetime.datetime.strptime(self.dFromTxt.get(), '%d-%m-%Y').date()
            
        if self.dToTxt.get() == "" or max(dates) < datetime.datetime.strptime(self.dToTxt.get(), '%d-%m-%Y').date():
            maxdate = max(dates)
        else:
            maxdate = datetime.datetime.strptime(self.dToTxt.get(), '%d-%m-%Y').date()
               
        # Adding values to dictionary
        vals = {}
        for line in self.data:
            if line.ddate.toordinal() in vals.keys():
                vals[line.ddate.toordinal()] = line.s+vals[line.ddate.toordinal()]
            else:
                vals[line.ddate.toordinal()] = line.s
        
        # Creating a dictionary for due date - cumulative value of expected payments pairs
        cumu = {}
        total = 0.0
        
        for x in range(mindate.toordinal()-1, maxdate.toordinal()+1):
            if x in vals.keys():
                total += vals[x]
                cumu[x] = total
            else:
                cumu[x] = total
        
        datevals = []
        
        for x in cumu.keys():
            y = datetime.date.fromordinal(x)
            z = y.strftime("%d-%m-%y")
            if z[0:2] == "01" or int(z[0:2]) % 5 == 0:
                datevals.append(z)
            else:
                datevals.append("")
                
        cumvals = list(cumu.values())
        
        # Opens a new window and draws graphs
        root = Tk()
        root.wm_title("Trend line analysis")
        
        fig = Figure(figsize=(9, 6), dpi=100, constrained_layout=True)
        fig.patch.set_facecolor('#F0F0F0')
        tl = fig.add_subplot(111)
        
        tl.plot(cumvals)
        pltitle = "Trend line analysis %s - %s" %(mindate.strftime("%d-%m-%y"), maxdate.strftime("%d-%m-%y"))
        tl.title.set_text(pltitle)
        y_pos = np.arange(len(cumvals))
        tl.set_xticks(y_pos)
        tl.set_xticklabels(datevals, rotation=90, fontsize=8)
        tl.set_ylabel('Cumulative value')
        
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        #Close button functionality
        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(master=root, text="Close", command=_quit)
        button.pack(side=BOTTOM)
        
        mainloop()        
        

    
if __name__ == '__main__':
    BadDebt().mainloop()