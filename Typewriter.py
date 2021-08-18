#--importing the modules--
from tkinter.ttk import *
from tkinter import *
from words_list import words
import time as t
import json as j
import random as r
#-main window-
main=Tk()
main.resizable(False, False)
main.geometry('700x500')
main.title('Typewriter')
Label(text='Typewriter', bg = 'light grey', width = 40, font = 'arial 20').pack()
#--setting up the variables--
start,time_var,correct,mistakes,s,test_time=0,0,0,0,False,0
#----updates the window every 0.1 seconds----
def update():
    global s,start,time_var,correct,mistakes,test_time
    w=word_box.get(1.0, END).split()
    word_box.configure(state='normal')
    word_box.tag_add(start,word_box.search(w[start],'1.0',END),f"{word_box.search(w[start], '1.0', END)}+{len(w[start])}c")
    if not entry.get().strip() in [w[start][0:a]for a in range(len(w[start])+1)]:
        word_box.tag_config(start, background='red')
    elif entry.get()==w[start]:
        word_box.tag_config(start, background='white')
    else:
        word_box.tag_config(start, background='light grey')
    if entry.get()!="" or start!=0:
        if not(s):
            test_time=time_var
            print(test_time)
        s=True
    if mode.get()==1 and s:
        time_var-=0.1
        mins,secs=divmod(time_var,60)
        time_label.configure(text=f'{int(mins):02}:{int(secs):02}')
        if int(time_var)==0:
            tabs.select(1)
            with open("typewriter_data.json","r") as f:
                contents=j.load(f)
            contents['data'].append({'test_no':len(contents['data'])+1,'WPM':round((correct/test_time)*100),'ACC':round((correct/(correct+mistakes))*100),'Date':t.strftime('%m-%d-%Y')})
            v=contents['data'][-1]
            results_label.configure(
            text=f"""   WPM - {v['WPM']}
    ACC - {v['ACC']}
    Test Number - {v['test_no']}
    Date - {v['Date']}
        """
            )
            contents=j.dumps(contents,indent=4)
            results_table.insert(parent='',index='end',iid=len(results_table.get_children())+1,values=(v['test_no'],v['WPM'],v['ACC'],v['Date']))
            with open("typewriter_data.json","w") as f:
                f.write(contents)
            reset()
    if tabs.index(tabs.select()) == 0:
        entry.configure(state='normal')
    else:
        entry.configure(state='disabled')
    word_box.configure(state='disabled')
    main.after(100, update)
#--when the user presses the space key--
def space_enter(event):
    global start,correct,mistakes
    if tabs.index(tabs.select()) == 0:
        entry.configure(state='normal')
        word_box.configure(state='normal')
        w=word_box.get(1.0, END).split()
        if start==len(w)-1:
            gen_word()
            start=0
            for l in word_box.tag_names():
                word_box.tag_delete(l)
        else:
            word_box.tag_add(start,word_box.search(w[start], '1.0', END),f"{word_box.search(w[start], '1.0', END)}+{len(w[start])}c")
            if entry.get().strip()==w[start]:
                correct+=1
                correct_label.config(text=f'Correct: {correct}')
                word_box.tag_config(start, foreground='green', background='white')
            else:
                mistakes+=1
                mistakes_label.config(text=f'Mistakes: {mistakes}')
                word_box.tag_config(start, foreground='red',background='white')
            start+=1
    entry.delete(0, END)
    word_box.configure(state='disabled')
#--reseting the wordbox--
def gen_word():
    global tw
    word_box.configure(state='normal')
    word_box.delete(1.0,END)
    tw=[];r.shuffle(words);tw=words[0:100]
    for i in tw:
        word_box.insert(END, f'{i} ')
    word_box.configure(state='disabled')
#-changing the mode(practice/timed)-
def mode_change(value):
    global time_var
    reset()
    if value=='normal':
        if timed.get()==0:
            time_var=15
            time_label.configure(text="00:15")
        elif timed.get()==1:
            time_var=30
            time_label.configure(text="00:30")
        elif timed.get()==2:
            time_var=60
            time_label.configure(text="01:00")
    else:
        time_change('00:00')
    for i in(time_15,time_30,time_60):
        i.configure(state=value)
#--resets everything, and changes the text of time_label--
def time_change(value):
    reset()
    time_label.configure(text=value)
#---resets all the variables,word_box,entry box, and time---
def reset():
    global s,start,time_var,time_var,correct,mistakes
    gen_word()
    s,start,time_var,correct,mistakes=False,0,0,0,0
    entry.delete(0,END)
    correct_label.config(text='Correct: 0')
    mistakes_label.config(text='Mistakes: 0')
    if timed.get()==0:
        time_var=15
        time_label.configure(text="00:15")
    elif timed.get()==1:
        time_var=30
        time_label.configure(text="00:30")
    elif timed.get()==2:
        time_var=60
        time_label.configure(text="01:00")
    for l in word_box.tag_names():
        word_box.tag_delete(l)
    practice_b.configure(state='normal')
    timed_b.configure(state='normal')
    if mode.get()==1:
        for i in(time_15,time_30,time_60):
            i.configure(state='normal')
    else:
        for i in(time_15,time_30,time_60):
            i.configure(state='disabled')
#--tabs--
tabs=Notebook(main,height=410,width=650)
typing_tab=Frame(main,height=410,width=650,bg='grey97')
results_tab=Frame(main,height=410,width=650,bg='grey97')
tabs.add(typing_tab,text="   Typing   ")
tabs.add(results_tab,text="   Results  ")
tabs.place(x=25,y=50)
#--Results Section--
scroll = Scrollbar(results_tab)
scroll.place(x = 622, y = 30, width = 20, height = 350)
results_table = Treeview(results_tab, yscrollcommand= scroll.set,height=16)
scroll.config(command = results_table.yview)
results_table['columns'] = ("Test_num", "WPM","Accuracy", "Date")
results_table.column("#0", width = 0, minwidth = 0)
results_table.column("Test_num", anchor = "w", width = 70, minwidth = 10)
results_table.column("WPM", anchor = "center", width = 90, minwidth = 30)
results_table.column("Accuracy", anchor = "center", width = 90, minwidth = 30)
results_table.column("Date", anchor = "center", width = 120, minwidth = 60)
results_table.heading("#0", text = "Label")
results_table.heading("Test_num", text = "Test no.")
results_table.heading("WPM", text = "WPM")
results_table.heading("Accuracy", text = "ACC")
results_table.heading("Date", text = "Date")
results_table.place(x = 250, y = 30)
results_label=Label(results_tab, text="     No Data",font='arial 10',justify='center',width=15,bg='grey97')
results_label.place(x=62,y=60)
Label(results_tab, text="Results:\n(Latest test)",font='arial 10',bg='grey97').place(x=95,y=20)
Label(results_tab, text="Recent tests",font='arial 9',bg='grey97').place(x=400,y=5)
#-the widgets-
word_box = Text(typing_tab, height = 12 , width = 75, wrap='word')
word_box.place(x=20,y=80)
gen_word()
word_box.configure(state='disabled')
entry = Entry(typing_tab, width = 50);entry.place(x=160,y=300)
time_label=Label(typing_tab, text='00:00', font='arial 10',bg='grey97');time_label.place(x=20,y=55)
correct_label=Label(typing_tab,text='Correct: 0',font='arial 10',bg='grey97');correct_label.place(x=110,y=55)
mistakes_label=Label(typing_tab,text='Mistakes: 0',font='arial 10',bg='grey97');mistakes_label.place(x=210,y=55)
reset_button=Button(typing_tab, text='reset', font='arial 15',bg='grey97',command=reset);reset_button.place(x=480,y=300)
Label(typing_tab,text='time').place()
timed=IntVar()
mode=IntVar()
practice_b=Radiobutton(typing_tab,text="Practice",variable=mode,value=0,bg='grey97',command=lambda:mode_change('disabled'))
practice_b.place(x=350,y=55)
timed_b=Radiobutton(typing_tab,text="Timed",variable=mode,value=1,bg='grey97',command=lambda:mode_change('normal'))
timed_b.place(x=420,y=55)
time_15=Radiobutton(typing_tab,text="15",variable=timed,value=0,state='disabled',bg='grey97',command=lambda:time_change("00:15"))
time_15.place(x=500,y=55)
time_30=Radiobutton(typing_tab,text="30",variable=timed,value=1,state='disabled',bg='grey97',command=lambda:time_change("00:30"))
time_30.place(x=540,y=55)
time_60=Radiobutton(typing_tab,text="60",variable=timed,value=2,state='disabled',bg='grey97',command=lambda:time_change("01:00"))
time_60.place(x=580,y=55)
#--checks creates a new file if the the save file doesn't exists--
try:
    with open("typewriter_data.json","r") as f:
        contents=j.load(f)
    if len(contents['data'])>0:
        latest_data=contents['data'][-1]
        results_label.configure(
            text=f"""    WPM - {latest_data['WPM']}
    ACC - {latest_data['ACC']}
    Test Number - {latest_data['test_no']}
    Date - {latest_data['Date']}
            """
        )
    for i in contents['data']:
        results_table.insert(parent='',index='end',iid=len(results_table.get_children())+1,values=(i['test_no'],i['WPM'],i['ACC'],i['Date']))
except FileNotFoundError:
    with open("typewriter_data.json","w+") as f:
        pass
    data = j.dumps({'data':[]},indent=4)
    with open("typewriter_data.json","w") as f:
        f.write(data)
#--key binds--
main.bind('<space>',space_enter)
#--after function(update)--
main.after(100, update)
#---mainloop--
main.mainloop()
#Started on July 18,2021 and finished on August 18 2021
#made by AGCAL