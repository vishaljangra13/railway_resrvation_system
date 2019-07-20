import pymysql
from tkinter import *
import tkinter.messagebox as box
import random
conn = pymysql.connect(host='localhost', user='vishal', passwd='vishal', db='train') 
cur = conn.cursor()

window=Tk()
flag=0
source=''
destination=''
date=''
passenger=0
clas=''
window.title("login page")
frame=Frame(window)
#frame1=Frame1(window)
entry1=Entry(window)
entry2=Entry(window,show="*")
label6=Label(window,text="login id")
label7=Label(window,text="password")
def train():
    global source
    global destination
    global date
    global passenger
    global clas
    window1=Tk()
    window1.title("Reservation Page")
    frame1=Frame(window1)
    img=PhotoImage(file="300px-IRCTC_Logo.svg.png")
    label=Label(window1,image=img,bg="Black").grid(row=1,column=10)
    label1=Label(window1,text="Enter Source").grid(row=3)

    m1=StringVar(window1)
    m1.set('chandigarh')
    e1=OptionMenu(window1,m1,'sonepat','delhi','chandigarh')

    e1.grid(row=3,column=10)
    #print(m1.get())
    label2=Label(window1,text="Enter Destination").grid(row=5)
    label3=Label(window1,text="Enter date in format dd/mm/yyyy").grid(row=7)
    label4=Label(window1,text="Enter class in which you want to travel").grid(row=9)
    label5=Label(window1,text="Enter number of passengers").grid(row=11)
    m2=StringVar(window1)
    m2.set('sonepat')
    e2=OptionMenu(window1,m2,'sonepat','delhi','chandigarh')
    m3=StringVar(window1)
    e3=Entry(window1,textvariable=m3)
    m4=StringVar(window1)
    m4.set('AC')
    e4=OptionMenu(window1,m4,'AC','sleeper')
    m5=StringVar(window1)
    e5=Entry(window1,textvariable=m5)
    
    e2.grid(row=5,column=10)
    e3.grid(row=7,column=10)
    e4.grid(row=9,column=10)
    e5.grid(row=11,column=10)    
    btn3=Button(window1,text="Show Trains",command=lambda:display(window1,m1.get(),m2.get(),m3.get(),m4.get(),m5.get()))
    btn3.place(x=200,y=600)
    window1.mainloop()
def display(window1,source,destination,date,clas,passengers) :
    #print("select name from route where source='{}' and destination='{}'and date='{}'and {}>={}".format(source,destination,date,clas,passengers))
    cur.execute("select name from route where source='{}' and destination='{}'and date='{}'and {}>={}".format(source,destination,date,clas,passengers))
    result2=cur.fetchall()
    c=list()
    for i in range(len(result2)) :
        for j in range(len(result2[i])) :
            c.append(result2[i][j])
    t=tuple(c)
    if len(t)==0 :
        box.showinfo("greetings","No Trains Available")
    else :
        m8=StringVar(window1)
        m8.set('train')
        e6=OptionMenu(window1,m8,*t).grid(row=3,column=19)
        btn4=Button(window1,text="Book Train",command=lambda:trainbooking(window1,m8.get(),clas,source,destination,date,passengers))
        btn4.place(x=600,y=430)
def trainbooking(window1,trainname,clas,source,destination,date,passengers) :
    cur.execute("select {} from route where source='{}' and destination='{}'and date='{}' and name='{}'".format(clas,source,destination,date,trainname))
    a=cur.fetchall()
    seat=int(int(a[0][0])-int(passengers))
    cur.execute("update route set {}={} where source='{}' and destination='{}'and date='{}' and name='{}'".format(clas,seat,source,destination,date,trainname))
    conn.commit()
    label5=Label(window1,text="Enter credit card").grid(row=13,column=19)
    m9=StringVar()
    e9=Entry(window1,textvariable=m9)
    e9.grid(row=15,column=19)
    btn5=Button(window1,text="pay",command=lambda:payment(window1,m9.get()))
    btn5.grid(row=17,column=19)
def payment(window1,cardnumber) :
    r=random.randint(100000000000,999999999999)
    ra=int(r)
    if len(cardnumber)==19 :
        box.showinfo("greetings","ticket booked\nticket PNR no={}".format(ra))
        window1.quit()
        window1.destroy()
    else :
        box.showinfo("greetings","Payment cancelled 404 error")
def quitwindow() :
    global window
    window.quit()
    window.destroy()
def dialog():
    global flag
    cur.execute("SELECT id from user")
    result1=cur.fetchall()
    cur.execute("select pass from user")
    result2=cur.fetchall()
    for i in range(len(result1)) :
        for j in range(len(result1[i])) :
            a=result1[i][j]
            b=result2[i][j]
            if(a==entry1.get() and b==entry2.get()):
                box.showinfo("greetings","welcome"+" "+entry1.get())
                quitwindow()
                train()
                flag=1
    if(flag!=1) :
        box.showinfo("greetings","not registered")
def dialog1() :
    global flag
    a=entry1.get()
    b=entry2.get()
    cur.execute("SELECT id from user")
    result1=cur.fetchall()
    for i in range(len(result1)) :
        for j in range(len(result1[i])) :
            c=result1[i][j]
            if(c==a):
                box.showinfo("greetings","User already Registered")
                flag=1
                break;
    if(flag!=1) :
        cur.execute("insert into user values('{}','{}')".format(a,b))
        conn.commit()
        #conn.close()
btn1=Button(window,text="login",command=dialog)
btn2=Button(window,text="Register",command=dialog1)
label6.grid(row=1,column=1)
label7.grid(row=3,column=1)
entry1.grid(row=1,column=3)
entry2.grid(row=3,column=3)
btn1.grid(row=5,column=2)
btn2.grid(row=7,column=2)
frame.place(x=40,y=200)
window.mainloop()