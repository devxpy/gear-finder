from tkinter import *
from tkinter import messagebox, ttk
import pickle
from itertools import permutations
from datetime import datetime
from time import time
from threading import Thread


def update_file(gear_dict):
    file_obj = open('gear_config', 'wb')
    pickle.dump(gear_dict, file_obj)
    file_obj.close()

def read_file():
    try:
        file_obj = open('gear_config', 'rb')
        data = pickle.load(file_obj)
        file_obj.close()
        return data
    except:
        return {}

def update_log(info):
    file_obj = open('log.txt', 'a')
    file_obj.write(info)
    file_obj.close()

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master=master
        self.master.title('Gear Finder')
        self.master.minsize(width=500, height=700)

        # Insert a menu bar on the main window
        m=Menu(self.master, tearoff=False)
        self.master.config(menu=m)

        # Create a menu button that brings up a menu
        o=Menu(m, tearoff=False)
        m.add_cascade(label="Options", menu=o)

        o.add_command(label="Modify Gearset", command=self.open_machine_config)
        o.add_command(label="About", command=self.open_about)

        # 3 primary frames
        results_frame = Frame(self.master)  # contains the results
        entry_frame = Frame(self.master)  # contains the inputs req
        self.status_frame = Frame(self.master)  # contains about and machine config
        results_frame.pack(pady=10, padx=10, fill=BOTH, expand=1)
        entry_frame.pack(pady=10)
        self.status_frame.pack(pady=5)

        # Listbox and scroll for the top frame
        scroll = Scrollbar(results_frame, orient=VERTICAL)
        self.result_lb = Listbox(results_frame, yscrollcommand=scroll.set, font="TkFixedFont")
        scroll.config(command=self.result_lb.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.result_lb.pack(fill=BOTH, expand=1)
        self.result_lb.insert(0, '     Gear setup            Ratio           Deviation  ')
        self.result_lb.insert(END, ' ')

        # medium frame
        Label(entry_frame, text='Gearset:').pack(side=LEFT)

        self.option = StringVar(master)
        self.option_menu = OptionMenu(entry_frame, self.option, ' ')
        self.option_menu.pack(side=LEFT)
        self.update_options(read_file())

        ratio_label = Label(entry_frame, text='    Ratio :')
        tol_label = Label(entry_frame, text='    Tolerance :')
        ratio_entry = Entry(entry_frame, width=10)
        tol_entry = Entry(entry_frame, width=10)
        ratio_label.pack(side=LEFT)
        ratio_entry.pack(side=LEFT)
        tol_label.pack(side=LEFT)
        tol_entry.pack(side=LEFT)
        ratio_entry.insert(0, ' ')  # default values
        tol_entry.insert(0, '0.000051')
        find_button = Button(entry_frame, text='Find', command=lambda: self.initiate_computation(ratio_entry.get(), tol_entry.get()))
        find_button.pack(side=LEFT)

        # bottom frame
        Label(self.status_frame, text='Ready').pack()

    def open_machine_config(self):
        config_window_entries ={}

        #inititalize the gui
        config_window = Toplevel(self.master)
        config_window.grab_set()
        config_window.title('Machine Configuration')
        title_frame = Frame(config_window)
        in_frame = Frame(config_window )
        button_frame = Frame(config_window)
        title_frame.grid(row=0, column=0)
        in_frame.grid(row=1, sticky=N+E+S+W, column=0)
        button_frame.grid(row=2, column=0)
        Label(title_frame, text='Please enter the all gear-sets separated by a space').grid(pady=10)

        config_window.columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(in_frame, orient=HORIZONTAL, bd=0, relief='flat')
        xscrollbar.grid(row=1, column=0, sticky=E+W)

        in_canvas = Canvas(in_frame,width='20c', height='10c', background='#181818', scrollregion=(0, 0, 6200, 0), xscrollcommand=xscrollbar.set)
        in_canvas.grid(row=0, column=0, sticky=N+S+E+W)
        input_frame = Frame(in_canvas)
        in_canvas.create_window(0,0, window=input_frame, anchor='nw')

        xscrollbar.config(command=in_canvas.xview)

        in_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

        for i in range(10):
            entry_id = 'entry_num_' + str(i)
            config_window_entries[entry_id] = [Entry(input_frame, width=25,text=''), Entry(input_frame, width=1000,text='')]
            config_window_entries[entry_id][0].grid(row=i, column=0, pady=10, padx=5)
            config_window_entries[entry_id][1].grid(row=i, column=1, sticky=N+E+S+W, pady=10, padx=5)

        #try to get the saved machine info from the file
        try:
            count=0
            info_dict = read_file()
            if info_dict != {}:
                for foo in info_dict:
                    if type(info_dict[foo]) == list and len(info_dict[foo]) != 0:
                        entry_id = 'entry_num_' + str(count)
                        config_window_entries[entry_id][0].insert(0, str(foo))
                        config_window_entries[entry_id][1].insert(0,' '.join(list(map(str, info_dict[foo]))))
                        count += 1
        except:
            pass

        #make the save button
        Button(button_frame, text=' Save Preferences ', command=lambda: self.save_config(config_window_entries, config_window)).grid(row=0, column=1)

    def save_config(self, e, config_window):
        pass_dict = {}

        for i in range(10):
            entry_id = 'entry_num_' + str(i)

            if len(e[entry_id][0].get().split())!= 0 and len(e[entry_id][1].get().split())!= 0: # check for empty entries
                try:  # to check if the user has entered a  valid integer only.
                    pass_dict[e[entry_id][0].get()] = list(map(int, e[entry_id][1].get().split()))
                except:
                    messagebox.showwarning('Alert!', 'Please provide valid input \n     (decimal point integers ONLY) ')

        update_file(pass_dict)
        self.update_options(read_file())
        config_window.grab_release()
        config_window.destroy()

    def update_options(self, pass_dict):
        if len(pass_dict) != 0:
            self.option.set('Select')
            self.option_menu.children['menu'].delete(0, 'end')
            for foobar in pass_dict.keys():
                self.option_menu.children['menu'].add_command(label=foobar, command=lambda z=foobar: self.option.set(z))
        else:
            self.option.set('')
            self.option_menu.children['menu'].delete(0, 'end')

    def open_about(self):
        messagebox.showinfo('About', '   Made by Dev Aggarwal \n Agnee Transmissions pvt. ltd.')

    def initiate_computation(self, ratio, tol):

        try:  # to check for valid integer input
            tol = float(tol)
        except ValueError:
            messagebox.showwarning('Alert!', 'Please enter a valid Tolerance')
            return None
        try:
            ratio = float(ratio)
        except ValueError:
            messagebox.showwarning('Alert!', 'Please enter a valid Ratio')
            return None

        try: #if user forgets to select an option
            gear_set = read_file()[self.option.get()]
        except:
            messagebox.showwarning('Alert!', 'Please select a gearset from dropdown')
            return None

        try:  # just in case the file was tampered and a non int ended up in there.
            gear_set = list(map(int, gear_set))
        except:
            messagebox.showwarning('Alert!', 'Please check the gearset for correct values')
            return None

        # update the log
        now = datetime.now()
        update_log('\n' + "------------------------ " + str(now.date().strftime('%d/%m/%Y')) + ' --- ' + str(
            now.time().strftime('%I:%M %p')) + " ---------------------------------------------------------------------" + '\n')
        update_log('Required ratio= ' + str(ratio) + '  Tolerance= ' + str(tol) + '   Chosen Set= ' + str(self.option.get()) + '\n')
        update_log(' Gear setup            Ratio           Deviation  ' + '\n')

        # clearing last output
        self.result_lb.delete(2, END)

        #update the status bar
        self.status_frame.destroy()
        self.status_frame = Frame(self.master)
        self.status_frame.pack(pady=5)
        Label(self.status_frame, text=' Please Wait For Calculation !   ').pack(side='left')
        progbar=ttk.Progressbar(self.status_frame, length=100, mode='indeterminate')
        progbar.pack(side='left')
        progbar.start()

        #start a new thread to compute result
        Thread(target=self.compute, args=(ratio, tol, gear_set, progbar)).start()


    # the main computing operation
    def compute(self, ratio, tol, gear_set, progbar):
        results = 0  # for counting the number of reults
        total_iterations=len(gear_set)*(len(gear_set)-1)*(len(gear_set)-2)*(len(gear_set)-3)
        save_list = []  # for saving result
        start=time()
        # computing result
        for i in permutations(gear_set, 4):
            predicted_ratio = i[0] / i[1] * i[2] / i[3]
            compare = abs(predicted_ratio - ratio)
            if compare <= tol:
                config_result = str(i[0]) + '/' + str(i[1]) + ' x ' + str(i[2]) + '/' + str(i[3])
                save_list.append([config_result, round(predicted_ratio, 10), round(compare, 10)])
                results = results + 1
        end=time()
        # updating the results
        save_list = sorted(save_list, key=lambda x: x[2])
        for foo in save_list:
            entry = str('  ' + str(foo[0]) + ' ' * (23 - len(str(foo[0]))) + str(foo[1]) + ' ' * (
            15 - len(str(foo[1]))) + str('{0:.12f}'.format(foo[2])))  # create a readable output
            update_log(entry + '\n')  # save output to log
            self.result_lb.insert(END, entry)  # print output
            self.result_lb.insert(END, ' ')
        progbar.stop()
        #updating the status bar
        self.status_frame.destroy()
        self.status_frame = Frame(self.master)
        self.status_frame.pack(pady=5)
        Label(self.status_frame, text='Found '+ str(results) + ' results, after ' + str(total_iterations) + ' iterations in ' + str(round(end-start,2)) + ' sec' ).pack()

if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    app.mainloop()
