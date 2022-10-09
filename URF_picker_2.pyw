# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 10:43:58 2022

@author: Ben-Gaming
"""
import pickle
import os
import random
import urllib.request

console_bool = False
try:
    import tkinter as tk
except ImportError:
    console_bool = True

version = float(2.01)

path = '\\'.join(os.path.realpath(__file__).split('\\')[:-1]) + '\\'
champions_path = path + "Champions"
modules_path = path + "Modules"
git_url = 'https://raw.githubusercontent.com/bepalmet/URF-picker-2/main'


choices = {
     '1': "Select champion",
     '2': "Unplayed champions",
     '3': 'Played champions'
     }


def get_champlist():
    #with open('{}\\champlist.txt'.format(path)) as file:
    #    text = file.read()
    #    return text.split('\n')
    response = urllib.request.urlopen(git_url + '/champlist').read().decode('utf-8')
    return response.split('\n')
    
def update_program():
    
    if not os.path.exists(path + 'updater.py'):
        try:
            updater_text = ''.join(urllib.request.urlopen(git_url + '/updater.py').read().decode('utf-8'))
            with open(path + 'updater.py', 'w') as updater_file:
                updater_file.write(updater_text)
        except urllib.error.HTTPError as e:
            error_window = tk.Tk()
            error_window.title("Update Error")
            label = tk.Label(
                error_window, 
                text= "There was an error while trying to update:\
                    \n{}\nYou might be offline".format(e)
                                )
            label.pack()
            error_window.wait_window()
    
    max_version = float(''.join(urllib.request.urlopen(git_url + '/version').read().decode('utf-8')))
    global version
    if version < max_version:
        os.system('python updater.py')
        raise SystemExit

class champion():
    
    def __init__(self, name, played= False, icon_link= None):
        self.name = name
        self.icon_link = icon_link
        self.played = played
        
    def __getitem__(self, i):
        return [self.name, self.played, self.icon_link][i]
    
    def __str__(self):
        return str([self.name, self.played])
    
last_changed = champion("None")


def update_folders():
    
    champ_array = get_champlist()
        
    try:
        os.mkdir(champions_path)
    except FileExistsError:
        None
    
    for champ_name in champ_array:
        current_champ_path = "{}\\{}".format(champions_path, champ_name)
        files_path = '{}\\{}'.format(current_champ_path, champ_name)
        try:
            os.mkdir(current_champ_path)
            with open('{}.dat'.format(files_path), 'wb') as champ_file:
                champ = champion(champ_name, False, "{}.png".format(files_path))
                pickle.dump(champ, champ_file) 
        except FileExistsError:
            None


def get_cache():
    
    cache = []
    
    for root, dirs, files in os.walk(champions_path):
        for folder in dirs:
            try:
                with open('{}\\{}\\{}.dat'.format(champions_path, folder, folder), 'rb') as f:    
                    cache.append(pickle.load(f))
            except FileNotFoundError:
                with open('{}\\{}\\{}.dat'.format(champions_path,folder, folder), 'wb') as f:    
                    champ = champion(folder, False, '{}\\{}\\{}.bmp'.format(champions_path, folder, folder))
                    pickle.dump(champ, f)
                    cache.append(champ)
    return cache

def get_champ_from_cache(name, cache):
    for item in cache:
        if name == item.name:
            return item

def select_random(cache):
    while True:
        champ = random.choice(list(cache))
        if not champ[1]:
            return champ


def change_mark(champ, cache, mark=None):
    if mark is None:
        if cache[cache.index(champ)].played:
            cache[cache.index(champ)].played = False
            champ.played = False
        else:
            cache[cache.index(champ)].played = True
            champ.played = True
    else:
        cache[cache.index(champ)].played = mark
        champ.played = mark
    try:
        with open('{}\\{}\\{}.dat'.format(champions_path, \
                                          champ.name, champ.name), 'r+b') as f:    
            pickle.dump(champ, f)
    except FileNotFoundError:
        None
    global last_changed
    last_changed = champ
  
    
def get_list(cache, mark):
    array = []
    for i in cache:
        if i.played == mark:
            array.append(i)
    return array

 
def create_output_frame(action_value, main_frame, cache):
    
    relief = "flat"
        
    random_label = tk.Label(
        master= main_frame, 
        fg= "black",
        bg= "white",
        justify= "center",
        relief= relief
        )
    unplayed_list = tk.Listbox(master= main_frame, relief= relief, selectmode= 'extended')
    played_list = tk.Listbox(master= main_frame, relief= relief, selectmode= 'extended')


    def output_random():
            
        
        random_label.grid(row= 1, column= 0, columnspan= 2, sticky= "nsew", padx= 2, pady= 2)
        
        champ = select_random(cache)

        text = "Your chosen Champion:\n\n{}\n\nMark as played?"\
            .format(champ.name)
        random_label["text"] = text   
        
    
        def yes_func(champ=champ, cache=cache, mark=True):
            change_mark(champ, cache, True)
            create_output_frame(-1, main_frame, cache)
            
        yes_button = tk.Button(
            master= main_frame, 
            text= "Yes",
            command= yes_func,
            padx= 10,
            pady= 10,
            borderwidth= 0,
            fg= "black",
            bg= "lightgrey",
            font= ('calibri', 12, 'bold'),
            relief= tk.SOLID
            )
        yes_button.grid(row= 2, column= 0, sticky= "nsew", padx= 2, pady= 2)
        
        def no_func():
            output_random()
            
            
        no_button = tk.Button(
            master= main_frame, 
            text= "No",
            command= no_func,
            padx= 10,
            pady= 10,
            borderwidth= 0,
            fg= "black",
            bg= "lightgrey",
            font= ('calibri', 12, 'bold'),
            relief= tk.SOLID
            )
        no_button.grid(row= 2, column= 1, sticky= "nsew", padx= 2, pady= 2)
    
    
    def output_unplayed(unplayed):
        
        def mark_played():
            sel_index = unplayed_list.curselection()
            for i in sel_index:
                if sel_index != ():
                    sel = unplayed_list.get(i)
                    c = get_champ_from_cache(sel, cache)
                    change_mark(c , cache, True)
                    create_output_frame(0, main_frame, cache)
                else:
                    None
        
        
        i = 1
        for champ in unplayed:
            unplayed_list.insert(i, champ.name)
            i += 1
        unplayed_list.grid(row= 1, column= 2, columnspan= 2, sticky= "nsew", padx= 2, pady= 2)
        
        scroll = tk.Scrollbar(main_frame, orient="vertical")
        scroll.grid(row= 1, column= 2, columnspan= 2, sticky= "nse", padx= 2, pady= 2)
        
        scroll.config(command=unplayed_list.yview)
        unplayed_list.config(yscrollcommand= scroll.set)
        
        played_button = tk.Button(
            master= main_frame, 
            text= "Move to played",
            command= mark_played,
            padx= 10,
            pady= 10,
            borderwidth= 0,
            fg= "black",
            bg= "lightgrey",
            font= ('calibri', 12, 'bold'),
            relief= tk.SOLID
            )
        played_button.grid(row= 2, column= 2, columnspan= 2, sticky= "nsew", padx= 2, pady= 2)
        
        if last_changed in unplayed:
            index = unplayed.index(last_changed)
            unplayed_list.selection_set(index)
            unplayed_list.see(index)
            
    
    def output_played(played):
        
        def mark_unplayed():
            sel_index = played_list.curselection()
            for i in sel_index:
                if sel_index != ():
                    sel = played_list.get(i)
                    c = get_champ_from_cache(sel, cache)
                    change_mark(c , cache, False)
                    create_output_frame(0, main_frame, cache)
                else:
                    None
        
        i = 1
        for champ in played:
            played_list.insert(i, champ.name)
            i += 1
        played_list.grid(row= 1, column= 4, columnspan= 2, sticky= "nsew", padx= 2, pady= 2)
        
        scroll = tk.Scrollbar(main_frame, orient="vertical")
        scroll.grid(row= 1, column= 4, columnspan= 2, sticky= "nse", padx= 2, pady= 2)
        
        scroll.config(command=played_list.yview)
        played_list.config(yscrollcommand= scroll.set)
        
        
        unplayed_button = tk.Button(
            master= main_frame, 
            text= "Delete from played",
            command= mark_unplayed,
            padx= 10,
            pady= 10,
            borderwidth= 0,
            fg= "black",
            bg= "lightgrey",
            font= ('calibri', 12, 'bold'),
            relief= tk.SOLID
            )
        unplayed_button.grid(row= 2, column= 4, columnspan= 2, sticky= "nsew", padx= 2, pady= 2)
        
        
        if last_changed in played:
            index = played.index(last_changed)
            played_list.selection_set(index)
            played_list.see(index)
         
    unplayed = get_list(cache, False)
    played = get_list(cache, True)    
         
    def create_button_panel():
        i = 0
        for k in list(choices.keys()):
            def func(a=k):
                len_unplayed, len_played = create_output_frame(a, main_frame, cache)
                
            new_button = tk.Button(
                master= main_frame, 
                text= choices[k], 
                command= func,
                padx= 20,
                pady= 10,
                borderwidth= 0,
                fg= "black",
                bg= "lightgrey",
                font= ('calibri', 12, 'bold'),
                relief= tk.SOLID
                )
            if k == '2':
                new_button['text'] += " ({})".format(len(unplayed))
            elif k == '3':
                new_button['text'] += " ({})".format(len(played))
            new_button.grid(padx= 2, pady= 2, row= 0, column= i, columnspan= 2)
            i += 2
        

        
    if action_value == -1:
        output_random()
        output_unplayed(unplayed)
        output_played(played)
        create_button_panel()
    elif action_value == 0:
        output_unplayed(unplayed)
        output_played(played)
        create_button_panel()
    elif action_value == '1': 
        output_random()
    elif action_value == '2': 
        output_unplayed(unplayed)
    elif action_value == '3': 
        output_played(played)
        
    return (len(unplayed), len(played))
    """
    elif action_value == '4': 
        return change_mark(cache, played=True)
    elif action_value == '5': 
        return change_mark(cache, played=False)
    elif action_value == '0': 
        return update_champion_list()
    """
  

def create_window(cache):
    
        

    
    window = tk.Tk()
    window.title("URF picker 2")
    window.resizable(width=False, height=False)
    window.configure(bg= "black")
    
    main_frame = tk.Frame(
        master= window
        )
    main_frame.grid(row= 0, column= 0, padx= 5, pady= 5)
    
    len_unplayed, len_played = create_output_frame(-1, main_frame, cache)
    
    gridsize = [3, len(list(choices.keys()))*2]
    for i in range(gridsize[0]):
        main_frame.rowconfigure(i, weight= 1)
    for i in range(gridsize[1]):
        main_frame.columnconfigure(i, weight= 1)
        
    
    
    
    
    
    def set_background_color(color="black", widget=window):
        for child in widget.winfo_children():
            if child.cget('bg') == "SystemButtonFace":
                child.configure(bg= "black")
            set_background_color(widget=child)   
    
    set_background_color()
    window.mainloop()

def main():
    update_program()
    update_folders()
    create_window(get_cache())
    
main()