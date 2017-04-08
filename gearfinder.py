#!pypy
# this is a program that takes the machine information,
# i.e. the gear teeth information and saves it as a python list.
# Then iterates over the list to get all the possible gear ratios
# within specified tolerance using the given data. this data is
# then sorted with respect to the deviation from absolute ratio
# provided by user.

from Tkinter import *
import tkMessageBox as msg
import pickle
import itertools
from datetime import datetime


def update_file(gear_dict):
    file_obj = open('gear_config', 'wb')
    pickle.dump(gear_dict, file_obj)
    file_obj.close()


def update_log(info):
    file_obj = open('log.txt', 'a')
    file_obj.write(info)
    file_obj.close()


def read_file():
    try:
        file_obj = open('gear_config', 'rb')
        data = pickle.load(file_obj)
        file_obj.close()
        return data

    except:
        return {}


class Application:
    def __init__(self, master):
        master.title('Gear Finder')

        # 3 primary frames
        top_frame = Frame(master)  # contains the results
        mid_frame = Frame(master)  # contains the inputs req
        bottom_frame = Frame(master)  # contains about and machine config

        top_frame.pack(pady=10, padx=10)
        mid_frame.pack(pady=10)
        bottom_frame.pack(pady=5)

        # Listbox and scroll for the top frame
        self.scroll = Scrollbar(top_frame, orient=VERTICAL)
        self.result_lb = Listbox(top_frame, width=55, height=30, yscrollcommand=self.scroll.set, font="TkFixedFont")
        self.scroll.config(command=self.result_lb.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.result_lb.pack()

        self.result_lb.insert(0, '     Gear setup            Ratio           Deviation  ')
        self.result_lb.insert(END, ' ')

        # medium frame
        option_menu_label = Label(mid_frame, text='Gearset:').pack(side=LEFT)

        # first making a option menu
        self.option = StringVar(master)
        self.option_menu = OptionMenu(mid_frame, self.option, ' ')
        self.option_menu.pack(side=LEFT)
        self.update_options(read_file())

        ratio_label = Label(mid_frame, text='    Ratio :')
        tol_label = Label(mid_frame, text='    Tolerance :')

        ratio_entry = Entry(mid_frame, width=10)
        tol_entry = Entry(mid_frame, width=10)

        ratio_label.pack(side=LEFT)
        ratio_entry.pack(side=LEFT)
        tol_label.pack(side=LEFT)
        tol_entry.pack(side=LEFT)

        ratio_entry.insert(0, ' ')  # default values
        tol_entry.insert(0, '0.000051')

        find_button = Button(mid_frame, text='Find', command=lambda: self.compute(ratio_entry.get(), tol_entry.get()))
        find_button.pack(side=LEFT)

        # bottom frame
        machine_button = Button(bottom_frame, text='Configure gearset', command=self.open_machine_config)
        about_button = Button(bottom_frame, text='About', command=self.open_help)

        machine_button.pack(side=LEFT, padx=20)
        about_button.pack(side=LEFT, padx=25)

        self.result_var = StringVar()
        self.result_label = Label(bottom_frame, textvariable=self.result_var).pack(side=LEFT, padx=20)
        self.result_var.set('    ')

    # machine config window
    def open_machine_config(self):
        self.entry_window = Toplevel(root)
        self.entry_window.grab_set()
        self.entry_window.title('Machine Configuration')
        # DEFINING FRAMES
        config_window_top_frame = Frame(self.entry_window)
        config_window_mid_frame = Frame(self.entry_window)
        config_window_entry_frame = Frame(config_window_mid_frame)
        config_window_name_frame = Frame(config_window_mid_frame)
        config_bottom_frame = Frame(self.entry_window)

        config_window_top_frame.pack(pady=5)
        config_window_mid_frame.pack(fill=X, expand=1)
        config_window_name_frame.pack(side=LEFT)
        config_window_entry_frame.pack(side=RIGHT, fill=X, expand=1)
        config_bottom_frame.pack(pady=5)

        Label(config_window_top_frame, text='\'Plese enter the all gearset seprated by a space\'').pack(side=TOP,
                                                                                                        pady=10)

        # all them macine names

        machine_name_1 = Entry(config_window_name_frame, width=25)
        machine_name_1.pack(pady=10, padx=5)
        machine_name_2 = Entry(config_window_name_frame, width=25)
        machine_name_2.pack(pady=10, padx=5)
        machine_name_3 = Entry(config_window_name_frame, width=25)
        machine_name_3.pack(pady=10, padx=5)
        machine_name_4 = Entry(config_window_name_frame, width=25)
        machine_name_4.pack(pady=10, padx=5)
        machine_name_5 = Entry(config_window_name_frame, width=25)
        machine_name_5.pack(pady=10, padx=5)
        machine_name_6 = Entry(config_window_name_frame, width=25)
        machine_name_6.pack(pady=10, padx=5)
        machine_name_7 = Entry(config_window_name_frame, width=25)
        machine_name_7.pack(pady=10, padx=5)
        machine_name_8 = Entry(config_window_name_frame, width=25)
        machine_name_8.pack(pady=10, padx=5)
        machine_name_9 = Entry(config_window_name_frame, width=25)
        machine_name_9.pack(pady=10, padx=5)
        machine_name_10 = Entry(config_window_name_frame, width=25)
        machine_name_10.pack(pady=10, padx=5)

        # all them entries...

        machine_entry_1 = Entry(config_window_entry_frame, width=90)
        machine_entry_1.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_2 = Entry(config_window_entry_frame, width=90)
        machine_entry_2.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_3 = Entry(config_window_entry_frame, width=90)
        machine_entry_3.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_4 = Entry(config_window_entry_frame, width=90)
        machine_entry_4.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_5 = Entry(config_window_entry_frame, width=90)
        machine_entry_5.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_6 = Entry(config_window_entry_frame, width=90)
        machine_entry_6.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_7 = Entry(config_window_entry_frame, width=90)
        machine_entry_7.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_8 = Entry(config_window_entry_frame, width=90)
        machine_entry_8.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_9 = Entry(config_window_entry_frame, width=90)
        machine_entry_9.pack(pady=10, padx=5, fill=X, expand=1)
        machine_entry_10 = Entry(config_window_entry_frame, width=90)
        machine_entry_10.pack(pady=10, padx=5, fill=X, expand=1)

        # putting default value by reading from file after converting to string
        try:
            info_dict = read_file()
            count = 1
            for foo in info_dict.keys():
                if type(info_dict[foo]) == list and len(info_dict[foo]) != 0:
                    info_string = ' '.join(str(i) for i in info_dict[foo])
                    placeholder1 = 'machine_entry_' + str(count) + '.insert(0,info_string)'
                    placeholder2 = 'machine_name_' + str(count) + '.insert(0,foo)'
                    exec (placeholder1) in globals(), locals()
                    exec (placeholder2) in globals(), locals()
                    count += 1
        except:
            pass

        save_button = Button(config_bottom_frame, text=' Save Preferences ',
                             command=lambda: self.save_config(machine_entry_1.get(), machine_entry_2.get(),
                                                              machine_entry_3.get(), machine_entry_4.get(),
                                                              machine_entry_5.get(), machine_entry_6.get(),
                                                              machine_entry_7.get(), machine_entry_8.get(),
                                                              machine_entry_9.get(), machine_entry_10.get(),
                                                              machine_name_1.get(), machine_name_2.get(),
                                                              machine_name_3.get(), machine_name_4.get(),
                                                              machine_name_5.get(), machine_name_6.get(),
                                                              machine_name_7.get(), machine_name_8.get(),
                                                              machine_name_9.get(), machine_name_10.get()))
        save_button.pack()

    def compute_button(self, ratio, tol):
        top = Toplevel()
        top.transient()
        top.grab_set()
        Label(top, text="Computing, please wait...").pack()
        import time
        time.sleep(2)
        self.compute(ratio, tol)

    def save_config(self, machine_entry_1, machine_entry_2, machine_entry_3, machine_entry_4, machine_entry_5,
                    machine_entry_6, machine_entry_7, machine_entry_8, machine_entry_9, machine_entry_10,
                    machine_name_1, machine_name_2, machine_name_3, machine_name_4, machine_name_5, machine_name_6,
                    machine_name_7, machine_name_8, machine_name_9, machine_name_10):

        # putting provided input inside a dict
        name_list = [machine_name_1, machine_name_2, machine_name_3, machine_name_4, machine_name_5, machine_name_6,
                     machine_name_7, machine_name_8, machine_name_9, machine_name_10]
        entry_list = [machine_entry_1, machine_entry_2, machine_entry_3, machine_entry_4, machine_entry_5,
                      machine_entry_6, machine_entry_7, machine_entry_8, machine_entry_9, machine_entry_10]
        pass_dict = {}

        for foo in range(0, 10):
            if len(name_list[foo]) != 0 and len(entry_list[foo]) != 0:  # check for empty entries

                try:  # to check if the user has entered a  valid integer only.
                    pass_dict[name_list[foo]] = map(int, entry_list[foo].split())

                except:
                    msg.showwarning('Alert!', 'Please provide valid input \n     (decimal point integers ONLY) ')
        # updating the file
        update_file(pass_dict)
        self.entry_window.grab_release()
        self.entry_window.destroy()

        # changing values in option selector
        self.update_options(read_file())

    def update_options(self, pass_dict):
        if len(pass_dict) != 0:
            self.option.set(pass_dict.keys()[0])  # default value
            self.option_menu.children['menu'].delete(0, 'end')
            for foobar in pass_dict.keys():
                self.option_menu.children['menu'].add_command(label=foobar, command=lambda z=foobar: self.option.set(z))
        else:
            self.option.set('')
            self.option_menu.children['menu'].delete(0, 'end')

    def open_help(self):
        msg.showinfo('About', '   Developed by Dev Aggarwal \n Agnee Transmissions pvt. ltd.')

    # the main computing operation
    def compute(self, ratio, tol):

        # update the log
        now = datetime.now()
        update_log('\n' + "----------------- " + str(now.date().strftime('%d/%m/%Y')) + ' --- ' + str(
            now.time().strftime('%I:%M %p')) + " -----------------------------------------" + '\n')
        update_log('Required ratio= ' + str(ratio) + '  Tolerance= ' + str(tol) + '   Chosen Set= ' + str(
            self.option.get()) + '\n')
        update_log(' Gear setup            Ratio           Deviation  ' + '\n')
        # clearing last output
        self.result_lb.delete(2, END)

        try:  # to check for valid integer input
            self.tolerance = float(tol)
            self.ratio = float(ratio)

            m = 0  # for counting the number of reults
            save_list = []  # for saving result

            try:  # just in case the file was tempered and a non int ended up in there.
                self.machine = read_file()[self.option.get()]
                self.machine = map(float, self.machine)

                # computing result
                for i in itertools.permutations(self.machine, 4):
                    predicted_ratio = i[0] / i[1] * i[2] / i[3]
                    compare = abs(predicted_ratio - self.ratio)
                    if compare <= self.tolerance:
                        config_result = str(int(i[0])) + '/' + str(int(i[1])) + ' x ' + str(int(i[2])) + '/' + str(
                            int(i[3]))
                        save_list.append([config_result, round(predicted_ratio, 10), round(compare, 10)])
                        m = m + 1

            except:
                msg.showwarning('Alert!',
                                'Please check the gearset for valid entries \n     (decimal point integers ONLY) ')

            # updating the result
            self.result_var.set(str(str(m)) + '  ')
            save_list = sorted(save_list, key=lambda x: x[2])
            for foo in save_list:
                entry = str('  ' + str(foo[0]) + ' ' * (23 - len(str(foo[0]))) + str(foo[1]) + ' ' * (
                15 - len(str(foo[1]))) + str(foo[2]))  # create a readable output
                update_log(entry + '\n')  # save output to log
                self.result_lb.insert(END, entry)  # print output
                self.result_lb.insert(END, ' ')

        except ValueError:
            msg.showwarning('Alert!',
                            'Please enter a valid value of ratio and tolerance \n      (decimal point intgers ONLY)')


root = Tk()
app = Application(root)
root.mainloop()
