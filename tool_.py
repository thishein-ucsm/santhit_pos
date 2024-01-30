import datetime
from tkinter import *
import json
from tkcalendar import Calendar


def isStatusOK(checklist):
        for x in checklist:
            if x=='' or x=='Select': return False
        return True
def isMatch(s1,s2):
    if s1==s2: return True
    else: return False
def loadConfig():
    with open('c:\\santhit\\config.json',"r") as file_:
        data=file_.read()
    d_=json.loads(data)
    return d_
def updateConfig(key_,value_):
    from database import connect_db

    raw=loadConfig()
    raw[key_]=value_
    file_path="c:\\santhit\config.json"
    d_=json.dumps(raw)
    with open(file_path, 'w') as file:
        file.write(d_)

def openCalendar(root,txt,btn):
    cal_win=root
    cal_win.title("Calendar")
    x=btn.winfo_rootx()
    y=btn.winfo_rooty()
    # cal_win.iconphoto(False,iconimg)

    cal_win.geometry(f"200x220+{x+20}+{y-50}")
    cal_win.resizable(0,0)
    year_ = int(datetime.datetime.now().strftime('%Y'))
    month_ = int(datetime.datetime.now().strftime('%m'))
    day_ = int(datetime.datetime.now().strftime('%d'))

    cal = Calendar(cal_win, date_pattern="dd/MM/yyyy",selectmode = 'day',year = year_, month = month_,day = day_)
    cal.pack(side=TOP,fill=X)
    ok = Button(cal_win,command=lambda: setDate(cal_win,txt,cal),text="OK",bg="orange",fg="blue")
    ok.pack(side=BOTTOM,padx=5)

def setDate(a,txt,cal):
    txt.set(cal.get_date())
    a.destroy()

def clear(entrys,cmb):
    for i in entrys:
        i.set("")
    if cmb==None:
        pass
    else:
        for i in cmb:
            i.set("Select")


def update_combo(table,column,cmb):
    from database import connect_db
    namelist=[]

    con=connect_db()
    mycur=con.cursor()
    sql=f"SELECT {column} from {table}"
    mycur.execute(sql)

    rows=mycur.fetchall()
    namelist.clear()
    for row in rows:
        namelist.append(row[0])
    if mycur.rowcount>0:
        cmb.config(values=namelist)
    else:
        cmb.config(values="Empty")
    # print(rows)
    con.close()

def update_entry(table,check_id,value,column,var_ent):
    from database import connect_db
    con=connect_db()
    mycur=con.cursor()
    sql=f"select {column} from {table} where {check_id}={value}"
    mycur.execute(sql)
    a=mycur.fetchone()
    var_ent.set(a[0])
    con.close()

def check_digit(checklist):
    a=[]
    for i in checklist:
        a.append(i.isdigit())
    if False in a:
        return False
    else:
        return True

def generate_id(table,idname):
    from database import connect_db
    con=connect_db()
    mycur= con.cursor()
    sql=f"select {idname} from {table} order by id desc limit 1"
    mycur.execute(sql)
    row=mycur.fetchone()
    if row==None:
        cur_id=idname+"-"+"0000"
    else:
        cur_id=row[0]
    a=cur_id.split("-")
    b=int(a[1])
    c=str(b+1)

    if len(c)<4:
        temp=a[0]+"-"+("0"*(4-len(c))+c)
    else:
        temp=a[0]+"-"+c
    con.close()
    return temp
  
def save_to_wallet(id,dep,wit,date):
    from database import connect_db
    des=id
    deposit=dep
    withdraw=wit
    date_=date
    walid=generate_id("wallet","walid")
    con=connect_db()
    mycur= con.cursor()
    sql=f"select balance from wallet order by id desc limit 1"
    mycur.execute(sql)
    row=mycur.fetchone()
    if row==None:
        balance=0+int(deposit)-int(withdraw)
    else:
        balance=int(row[0])+int(deposit)-int(withdraw)
    sql="insert into wallet(walid,description,deposit,withdraw,balance,date) values (%s,%s,%s,%s,%s,%s)"
    val=(walid,des,deposit,withdraw,balance,date_)
    mycur.execute(sql,val)
    con.commit()
    con.close()
def update_wallet(id,dep,wit,date,dep_dif,wit_dif):
    from database import connect_db
    des=id
    deposit=dep
    withdraw=wit
    date_=date
    dep_dif_=dep_dif
    wit_dif_=wit_dif
    con=connect_db()
    mycur=con.cursor()
    sql="update wallet set deposit=%s,withdraw=%s,date=%s where description=%s"
    val=(deposit,withdraw,date_,des)
    mycur.execute(sql,val)
    con.commit()
    con.close()
    update_balance(des,dep_dif_,wit_dif_)
def delete_wallet(id,dep_dif,wit_dif):
    from database import connect_db

    des=id
    con=connect_db()
    mycur=con.cursor()
    update_balance(des,dep_dif,wit_dif)
    sql="delete from wallet where description=%s"
    val=(des,)
    mycur.execute(sql,val)
    con.commit()
    con.close()
def set_balance():
    from database import connect_db

    con=connect_db()
    mycur=con.cursor()
    sql="select balance from wallet order by id desc limit 1"
    mycur.execute(sql)
    a=mycur.fetchone()
    if a==None:
        return 0
    return a[0]
def update_balance(id,dep,wit):
    from database import connect_db

    des=id
    deposit=dep
    withdraw=wit
    con=connect_db()
    mycur=con.cursor()
    sql="select id from wallet where description=%s"
    val=(des,)
    mycur.execute(sql,val)
    cur_id=mycur.fetchone()
    sql="select id,balance from wallet where id>=%s"
    val=(cur_id[0],)
    mycur.execute(sql,val)
    a=mycur.fetchall()
    for i in a:
        cur_walid=i[0]
        cur_bal=i[1]
        new_bal=int(cur_bal)-int(deposit)+int(withdraw)
        sql="update wallet set balance=%s where id=%s"
        val=(new_bal,cur_walid)
        mycur.execute(sql,val)
        con.commit()
        
    con.close()
        

