import mysql.connector as ms
from random import randint
import datetime as dt
import calendar as c
from tabulate import tabulate
import webbrowser

#-----------DATA VALIDITY SECTION STARTS HERE-----------

#TO CHECK THE VALIDITY OF GIVEN CONTACT NUMBER

def phnocheck(ph):
     if len(str(ph))!=10 or ph<0:
   print("!!!!!!!Enter a valid contact number!!!!!!!")
   return True
     if ph>2147483647:
   print("!!!!!!!sql error: Enter a contact number 
         smaller than 2147483647!!!!!!!")
   return True
     return False

#TO CHECK THE VALIDITY OF GIVEN EMAIL

def emailcheck(em):
     if not (em.split(".")[-1].isalpha()) or em.count("@")!=1:
   print("!!!!!!!Invalid email!!!!!!!")
   return True
     if len(em)>30:
   print("!!!!!!!Email is too long!!!!!!!")
   return True
     for i in em:
   if not(i.isalnum() or i=="@" or i=="."):
      print("!!!!!!!Invalid email!!!!!!!")
      return True
     return False

#TO CHECK THE VALIDITY OF GIVEN DATE

def datecheck(date):
     l=date.split("-")
     if len(l)!=3 or len(date)!=10 or len(l[0])!=4 or 
     len(l[1])!=2 or len(l[2])!=2 :
    print("!!!!!!!Please enter date in the format yyyy-
          mm-dd!!!!!!!")
    return True
     if not(l[0].isdigit()) or not(l[1].isdigit()) or 
     not(l[2].isdigit()):
    print("!!!!!!!Please enter a valid date in the format 
          yyyy-mm-dd!!!!!!!")
    return True
     if (int(l[1]) in [1,3,5,7,8,10,12] and int(l[2])>31) or 
        (int(l[1]) in [4,6,9,11] and int(l[2])>30):
    print("!!!!!!!Please enter a valid date!!!!!!!")
    return True
     elif int(l[1])==2:
    if ((int(l[0])%4==0 and int(l[0])%100!=0) or 
       (int(l[0])%400==0)):
 if int(l[2])>29:
    print("!!!!!!!Please enter a valid
          date!!!!!!!")
    return True
    elif int(l[2])>28:
 print("!!!!!!!Please enter a valid date!!!!!!!")
 return True
     return False

#-----------DATA VALIDITY SECTION ENDS HERE-----------

#-------------LOGIN INTERFACE STARTS HERE-------------

def interface():
print("*******WELCOME TO BANK MANAGEMENT SYSTEM*******")
ut=input("Enter login type(admin or customer) or (exit):")
if ut=="admin":
adminlogin()
elif ut=="customer":
customerlogin()
elif ut=="exit":
print("-----------------------------------------------
       -")
print("*******...THANK YOU,PLEASE VISIT 
      AGAIN...*******")
print("-----------------------------------------------
      -")
else:
print("!!!!!!!Enter admin or customer or exit 
      only!!!!!!!")
interface()

#----------LOGIN INTERFACE ENDS HERE-----------

#--------CUSTOMER INTERFACE STARTS HERE--------

def customerlogin():
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
cb=db.cursor()
cb.execute("select id,password from interface where 
            type='{}'".format("user"))
u=cb.fetchall()
print("*******WELCOME TO USER INTERFACE*******")
id=input("Enter login id:")
pd=input("Enter your password:")
for i in u:
if i[0]==id and i[1]==pd:
cb.execute("select Account_number from 
            acc_details where id='{}'"
              .format(id))
  u=cb.fetchone()
ac=u[0]
print("~~~~~~~LOGIN SUCCESSFUL~~~~~~~")
cust_home(ac)
break
else:
print("!!!!!!!INVALID CREDENTIALS!!!!!!!")
print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
print("#######ACCESS DENIED#######")

#TO DISPLAY CUSTOMER PANEL

def cust_home(ac):
print("_______CUSTOMER PANEL_______")
print("Enter mp to modify id and password")
print("Enter a for account details")
print("Enter ab to check available balance")
print("Enter l for locker details")
print("Enter p to create or modify pin")
print("Enter t for transaction panel")
print("Enter th to see transaction history")
print("Enter r for review")
print("Enter lo to log out")
ch=input("Enter your choice:")
if ch=="mp":
   modifypassword()
elif ch=="a":
   acc(ac)
elif ch=="ab":
   balance(ac)
elif ch=="l":
   locker(ac)
elif ch=="p":
   transpin(ac)
elif ch=="t":
   transac(ac)
elif ch=="th":
   transhis(ac)
elif ch=="r":
   review(ac)
elif ch=="lo":
   interface()
else:
   print("!!!!!!!Enter mp or a or ab or l or p or t or th 
          or r or lo only!!!!!!!")
   cust_home(ac)

#TO MODIFY LOGIN PASSWORD

def modifypassword():
db=ms.connect(host="localhost",user="root",password=admin, 
              database="bms")
cb=db.cursor()
print("_______MODIFY PASSWORD PANEL_______")
cb.execute("select * from interface where
           Type={}".format("user"))
u=cb.fetchall()
op=input("Enter old password:")
if(len(op))<8:
     print("!!!!!!!Entered value is too short!!!!!!!")
     modifypassword()
     return
elif (len(op))>8:
   	  print("!!!!!!!Entered value is too long!!!!!!!")
     modifypassword()
     return
for i in u:
    if op==i[1]:
       np=input("Enter new password:")
       if(len(np))<8:
         print("!!!!!!!Entered value is too 
               short!!!!!!!")
          modifypassword()
         return
   elif (len(np))>8:
         print("!!!!!!!Entered value is too 
               long!!!!!!!")
        modifypassword()
        return
else:
  cb.execute("update interface set password={} where 
             password={}".format(np,op))
   db.commit()
   print("~~~~~~~PASSWORD MODIFIED 
         SUCCESSFULLY~~~~~~~")
    leave("customer")
else:
print("!!!!!!!INVALID PASSWORD!!!!!!!")
print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
print("#######ACCESS DENIED#######")

#TO DISPLAY ACCOUNT DETAILS OF THE CUSTOMER IN TABULAR FORM

def acc(ac):
db=ms.connect(host="localhost",user="root",password=admin, 
              database="bms")
cb=db.cursor()
cb.execute("select
Account_number,Account_holder,Nominee_name,Father_name,Date_of_birth,Gender,Marital_status,Contact_number,E_mail,Address,Account_type,Account_category from acc_details where Account_number={}".format(ac))
u=cb.fetchone()
if u:
print("_______ACCOUNT DETAILS_______")
acc=tabulate([u],headers=["Account_number","Account_holder","Nominee_name","Father_name","Date_of_birth","Gender","Marital_status","Contact_number","E_mail","Address","Account_type","Account_category"],tablefmt="grid")
print(acc)
cust_home(ac)

#TO DISPLAY BALANCE OF THE CUSTOMER IN TABULAR FORM

def balance(ac):
db=ms.connect(host="localhost",user="root",password=admin, 
              database="bms")
cb=db.cursor()
try:
pin=int(input("Enter your pin:"))
if (len(str(pin)))<4:
print("!!!!!!!Entered value is too short!!!!!!!")
print("!!!!!!!Enter pin of 4 digits!!!!!!!")
balance(ac)
elif(len(str(pin)))>4:
print("!!!!!!!Entered value is too long!!!!!!!")
print("!!!!!!!Enter pin of 4 digits!!!!!!!")
balance(ac)
except ValueError:
print("!!!!!!!Enter integer only!!!!!!!")
balance(ac)
cb.execute("select Pin from acc_details where 
            Account_number={}".format(ac))
ucb=cb.fetchone()
if ucb[0]==pin:
cb.execute("select * from acc_details natural join 
            avail_balance")
u=cb.fetchone()
print("_______AVAILABLE BALANCE_______")
bl=[]
if u[12]<2000:
print("!!!!!!!LOW BALANCE!!!!!!!")
else:
       bl.append([u[0],u[1],int(u[14])])
balance=tabulate(bl,headers=["Account_number","Account_holder","Available_balance"],tablefmt="grid")
print(balance)
else:
print("!!!!!!!INVALID PIN!!!!!!!")
print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
print("#######ACCESS DENIED#######")
cust_home(ac)

  #TO DISPLAY LOCKER PANEL

def locker(ac):
   print("_______LOCKER PANEL_______")
   print("Enter mdl for more details about locker")
   print("Enter la for your locker access")
   print("Enter b to go back")
ch=input("Enter your choice:")
if ch=="mdl":
about_locker(ac)
elif ch=="la":
locker_access(ac)
elif ch=="b":
cust_home(ac)
else:
print("!!!!!!!Enter mdl or la or b only!!!!!!!")
locker(ac)

#TO DISPLAY MORE DETAILS ABOUT LOCKER

def about_locker(ac):
db=ms.connect(host="localhost",user="root",password=admin, 
              database="bms")
cb=db.cursor()
cb.execute("select Size,Registration_fee,Annual_rent from  
            locker")
u=cb.fetchall()
al=[]
for i in u:
al.append(i)
tal=tabulate(al,headers=["Size","Registration_fee","Annual_ 
                         rent"],tablefmt="grid")
print("_______MORE DETAILS ABOUT LOCKER_______")
print(tal)
print("***Note: Locker Visit Charges(All Sizes): 12 visits 
      free. Thereafter: Rs.100/- per visit.")
locker(ac)

#TO DISPLAY LOCKER DETAILS OF THE CUSTOMER IN TABULAR FORM

def locker_access(ac):
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
cb=db.cursor()
print("_______LOCKER ACCESS PANEL_______")
id=input("Enter your locker ID:")
if(len(id))<5:
print("!!!!!!!Entered value is too short!!!!!!!")
locker_access(ac)
elif (len(id))>5:
print("!!!!!!!Entered value is too long!!!!!!!")
locker_access(ac)
try:
lpin=int(input("Enter your pin:"))
if (len(str(lpin)))<4:
print("!!!!!!!Entered value is too 
      short!!!!!!!")
print("!!!!!!!Enter pin of 4 digits!!!!!!!")
locker_access(ac)
elif(len(str(lpin)))>4:
print("!!!!!!!Entered value is too long!!!!!!!")
print("!!!!!!!Enter pin of 4 digits!!!!!!!")
locker_access(ac)
except ValueError:
print("!!!!!!!Enter integer only!!!!!!!")
locker_access(ac)
cb.execute("select Locker_ID,Locker_Pin from locker where 
           Status='{}'".format("Rented"))
u=cb.fetchall()
c=0   
for i in u:
if i[0]=="id" and i[1]=="lpin":
c=c+1
timestamp=dt.datetime.now().strftime("%Y-%m-%d
                                      %H:%M:%S")
if c>12:
cb.execute("select Available_balance from 
            avail_balance where 
            Account_number={}".format(ac))
uu=cb.fetchone()
if uu[0]>=(100+2000):
cb.execute("update avail_balance set 
                                 Available_balance=Available_
                                 balance-{} where 
                                 Account_number={}"
                                .format(100,ac))
cb.execute("select Nominee_name,Details 
           from locker where Locker_ID='{}' 
           and Locker_Pin={}".
           format(id,lpin))
uc=cb.fetchone()
if uc:
lk=[]
for i in uc:
lk.append(i)
                     lkt=tablate(lk,headers=["Nominee_name",
                                             "Details"],
                                 tablefmt="grid")
print("_______LOCKER DETAILS_______")
print(lkt)
cb.execute("update locker set Access 
           log='{}' where Locker_ID='{}'"
           .format(timestamp,id))
db.commit()
locker(ac)
else:
print("!!!!!!!YOU DON'T HAVE ENOUGH 
      BALANCE!!!!!!!")
print("#######ACCESS DENIED#######")
else:
cb.execute("select Nominee_name,Details from
           locker where Locker_ID='{}' and 
           Locker_Pin={}".format(id,lpin))
uc=cb.fetchone()
if uc:
lk=[]
for i in uc:
lk.append(i)
lkt=tablate(lk,headers=["Nominee_name","
                        Details"],
             tablefmt="grid")
print("_______LOCKER DETAILS_______")
print(lkt)
cb.execute("update locker set Access 
           log='{}' where Locker_ID='{}'".
           format(timestamp,id))
db.commit()
locker(ac)
else:
print("!!!!!!!INVALID CREDENTIALS!!!!!!!")
print("!!!!!!!AUTHENTICATION 
       UNSUCCESSFUL!!!!!!!")
              print("#######ACCESS DENIED#######")
#TO CREATE AND MODIFY TRANSACTION PIN OF THE CUSTOMER 
def transpin(ac): 
   db=ms.connect(host="localhost",user="root",password=admin,da 
              tabase="bms")
    cb=db.cursor()
    print("Enter cp to create pin")
    print("Enter mp to modify pin")
    print("Enter b to go back")
    ch=input("Enter your choice:")
    if ch=="cp":
        try:
            np=int(input("Enter new pin:"))
            if (len(str(np)))<4:
                print("!!!!!!!Pin is too short!!!!!!!")
                transpin(ac)
            elif (len(str(np)))>4:
                print("!!!!!!!Pin is too long!!!!!!!")
                transpin(ac)
            cb.execute("select Pin from acc_details")
            u=cb.fetchall()
            for i in u:
                if np==i[0]:
                    break
            else:
               cb.execute("update acc_details set Pin={} where
                           Account_number={}".format(np,ac))
                db.commit()
                print("~~~~~~~PIN CREATED SUCCESSFULLY~~~~~~~")
                leave("customer")
        except ValueError:
            print("!!!!!!!Enter integers only!!!!!!!")
            transpin(ac)
    elif ch=="mp":
        try:
            op=int(input("Enter your old pin:"))
            if (len(str(op)))<4:
                print("!!!!!!!Pin is too short!!!!!!!")
                transpin(ac)
            elif (len(str(op)))>4:
                print("!!!!!!!Pin is too long!!!!!!!")
                transpin(ac)
        except ValueError:
            print("!!!!!!!Enter integers only!!!!!!!")
            transpin(ac)
        cb.execute("select Pin from acc_details where
                    Account_number={}".format(ac))
        u=cb.fetchone()
        if u[1]==op:
            try:
                np=int(input("Enter new pin:"))
                if (len(str(np)))<4:
                    print("!!!!!!!Pin is too short!!!!!!!")
                    transpin(ac)
                elif (len(str(np)))>4:
                    print("!!!!!!!Pin is too long!!!!!!!")
                    transpin(ac)
                for i in u:
                    if np==i[1]:
                        break
                else:
                    cb.execute("update acc_details set Pin={}
                               where Account_number={}"
                               .format(np,ac))
                    db.commit()
                    print("~~~~~~~PIN MODIFIED 
                          SUCCESSFULLY~~~~~~~")
                    leave("customer")
            except ValueError:
                print("!!!!!!!Enter integers only!!!!!!!")
                transpin(ac)
        else:
            print("!!!!!!!INVALID PIN!!!!!!!")
            print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
            print("#######ACCESS DENIED#######")
    elif ch=="b":
        cust_home(ac)
    else:
        print("!!!!!!!Enter cp or mp or b only!!!!!!!")
        transpin(ac)

#TO DISPLAY TRANSACTION PANEL
        
def transac(ac):
print("_______TRANSACTION PANEL_______")
     print("Enter d to debit money")
     print("Enter c to credit money")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="d":
debit(ac)
     elif ch=="c":
          credit(ac)
     elif ch=="b":
          cust_home(ac)
     else:
     print("!!!!!!!Enter d or c or b only!!!!!!!")
          transac(ac)

#TO DEBIT MONEY FROM THE CUSTOMER'S ACCOUNT

def debit(ac):  
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
cb=db.cursor()
date=dt.date.today()
day=date.strftime("%A")
cb.execute("select * from acc_details natural join 
            avail_balance where Account_number={}".
            format(ac))
    u=cb.fetchone()
     try:
     ad=float(input("Amount to be debited:"))
     except ValueError:
          print("!!!!!!!Enter integer or float value 
                only!!!!!!!")
          debit(ac)
     try:
     pin=int(input("Enter your pin:"))
          if (len(str(pin)))<4:
          print("!!!!!!!Entered value is too short!!!!!!!")
               print("!!!!!!!Enter pin of 4 digits!!!!!!!")
               debit(ac)
          elif(len(str(pin)))>4:
               print("!!!!!!!Entered value is too long!!!!!!!")
               print("!!!!!!!Enter pin of 4 digits!!!!!!!")
               debit(ac)
     except ValueError:
          print("!!!!!!!Enter integer only!!!!!!!")
          debit(ac)
     cb.execute("select Pin from acc_details where 
                Account_number={}".format(ac))
     ucb=cb.fetchone()
     if ucb[1]==pin:
         cb.execute("select Available_balance from avail_balance 
                    where Account_number={}".format(ac))
         uu=cb.fetchone()
         if uu[0]>=(ad+2000):
    cb.execute("update avail_balance set
                         Available_balance=Available_balance-{} 
                         where Account_number={}".format(ad,ac))
     cb.execute("insert into transac_his   
                values({},'{}',{},'{}','{}','{}','{}')"
               .format(ac,u[1],ad,"Withdrawl","Online",
                str(date),day))
               db.commit()
               print("~~~~~~~TRANSACTION SUCCESSFUL~~~~~~~")
               print("YOUR CURRENT BALANCE IS",u[14]-ad)
               leave("customer")
         else:
         print("!!!!!!!YOU DON'T HAVE ENOUGH 
               BALANCE!!!!!!!")
         print("!!!!!!!TRANSACTION UNSUCCESSFUL!!!!!!!")
     else:
     print("!!!!!!!INVALID PIN!!!!!!!")
          print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
          print("#######TRANSACTION DENIED#######")

#TO CREDIT MONEY FROM THE CUSTOMER'S ACCOUNT
        
def credit(ac):
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
cb=db.cursor()
date=dt.date.today()
day=date.strftime("%A")
cb.execute("select * from acc_details natural join 
           avail_balance where Account_number={}"
           .format(ac))
u=cb.fetchone()
     try:
         cd=float(input("Amount to be credited:"))
     except ValueError:
         print("!!!!!!!Enter integer or float value 
               only!!!!!!!")
         credit(ac)
     try:
         pin=int(input("Enter your pin:"))
         if (len(str(pin)))<4:
         print("!!!!!!!Entered value is too short!!!!!!!")
              print("!!!!!!!Enter pin of 4 digits!!!!!!!")
              credit(ac)
         elif(len(str(pin)))>4:
         print("!!!!!!!Entered value is too long!!!!!!!")
              print("!!!!!!!Enter pin of 4 digits!!!!!!!")
              credit(ac)
     except ValueError:
         print("!!!!!!!Enter integer only!!!!!!!")
         credit(ac)
     cb.execute("select Pin from acc_details where 
                 Account_number={}".format(ac))
     ucb=cb.fetchone()
     if ucb[1]==pin:
         cb.execute("select Available_balance from avail_balance 
                    where Account_number={}".format(ac))
         uu=cb.fetchone()
         if uu[0]>=(cd+2000):
             cb.execute("update avail_balance set 
                        Available_balance=Available_balance+{} 
                        where Account_number={}".format(cd,ac))
             cb.execute("insert into transac_his 
values({},'{}',{},'{}','{}','{}','{}')".format(ac,u[1],cd,"Deposit","Online",str(date),day))
             db.commit()
             print("~~~~~~~TRANSACTION SUCCESSFUL~~~~~~~")
             print("YOUR CURRENT BALANCE IS",u[14]+cd)
             leave("customer")
         else:
             print("!!!!!!!YOU DON'T HAVE ENOUGH 
                   BALANCE!!!!!!!")
             print("!!!!!!!TRANSACTION UNSUCCESSFUL!!!!!!!")
     else:
         print("!!!!!!!INVALID PIN!!!!!!!")
         print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
         print("#######TRANSACTION DENIED#######")

#TO DISPLAY TRANSACTION HISTORY PANEL

def transhis(ac):
print("_______TRANSACTION HISTORY PANEL_______")
     print("Enter 5t to see details of last 5 transactions")
     print("Enter mt to see details of last month trasactions")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="5t":
     last5t(ac)
     elif ch=="mt":
          lastmontht(ac)
     elif ch=="b":
          cust_home(ac)
     else:
          print("!!!!!!!Enter 5t or mt or b only!!!!!!!")
          transhis(ac)

#TO DISPLAY LAST 5 TRANSACTIONS OF THE CUSTOMER IN A TABULAR 
 FORM
        
def last5t(ac):
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     cb.execute("select * from transac_his where 
                Account_number={}".format(ac))
     u=cb.fetchall()
     print("_______LAST 5 TRANSACTIONS_______")
     if u:
     ct5l=0
          t5l=[]
          for i in u[-1:-6:-1]:
          ct5l=ct5l+1
               t5l.append((ct5l,)+i)
his5t=tabulate(t5l,headers=["S.No.","Account_number",
                            "Account_holder","Amount",
                           "Type","Mode","Date","Day"]
                ,tablefmt="grid")
          print(his5t)
     else:
          print("~~~~~~~NO TRANSACTION HISTORY FOUND~~~~~~~")
     transhis(ac)

#TO DISPLAY LAST MONTH TRANSACTIONS OF THE CUSTOMER IN A TABULAR 
 FORM
    
def lastmontht(ac):
date=dt.date.today()
     ds=str(date)
     d=int(ds[-2:])
     m=int(ds[-5:-3])
     y=int(ds[0:4])
     for i in range(30):
     d=d-1
          if d==0:
          m=m-1
               if m in [1,3,5,7,8,10,12]:
               d=31
               elif m in [4,6,9,11]:
                    d=30
               elif m==2:
               if c.isleap(int(ds[0:4])):
                    d=29
                    else:
                         d=28
               elif m==0:
                d=31
                m=12
                y=y-1
     ds=str(dt.date(y,m,d))
    db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     cb.execute("select * from transac_his where 
                Account_number={} and Date>={}".format(ac,ds))
     u=cb.fetchall()
     print("_______LAST MONTH TRANSACTIONS_______")
     if u:
     cmtl=0
          mtl=[]
          for i in u[-1:-6:-1]:
          cmtl=cmtl+1
         mtl.append((cmtl,)+i) 
          hism=tabulate(mtl,headers=["S.No.","Account_number",
                                     "Account_holder","Amount",
                                     "Type","Mode","Date","Day"]
                  ,tablefmt="grid")
          print(hism)
     else:
     print("~~~~~~~NO TRANSACTION HISTORY FOUND~~~~~~~")
     transhis(ac)

#TO TAKE REVIEW OF THE CUSTOMER
    
def review(ac=0):
print("*******PLEASE LEAVE US YOUR VALUABLE 
       FEEDBACK*******")
     ch=input("Enter (now or later):")
     ch=ch.lower()
     if ch=="now":
     webbrowser.open("https://forms.gle/oXcP7cKUauHneVCk9")
          leave("customer")
     elif ch=="later":
          leave("customer")
     else:
          print("!!!!!!!Enter now or later only!!!!!!!")
          review(ac)

#--------CUSTOMER INTERFACE ENDS HERE-------

#--------OWNER INTERFACE STARTS HERE--------

def adminlogin(): 
db=ms.connect(host="localhost",user="root",password=admin,
                   database="bms")
     cb=db.cursor()
     cb.execute("select id,password from interface where
                type='{}'".format("admin"))
     u=cb.fetchall()
     print("*******WELCOME TO BANK INTERFACE*******")
     id=input("Enter login id:")
     pd=input("Enter your password:")
     for i in u:
     if i[0]==id and i[1]==pd:
          print("~~~~~~~LOGIN SUCCESSFUL~~~~~~~")
               adm_home()
               break
     else:
          print("!!!!!!!INVALID CREDENTIALS!!!!!!!")
          print("!!!!!!!AUTHENTICATION UNSUCCESSFUL!!!!!!!")
          print("#######ACCESS DENIED#######")

#TO DISPLAY ADMIN PANEL
        
def adm_home():
print("_______ADMIN PANEL_______")
     print("Enter a for account details")
     print("Enter ca to create an account")
     print("Enter cip to create id and password")
     print("Enter ea to modify account details")
     print("Enter da to delete an account")
     print("Enter l for locker details")
     print("Enter s for searching")
     print("Enter r for review panel")
     print("Enter lo to log out")
     ch=input("Enter your choice:")
     if ch=="a":
     acc_()
     elif ch=="ca":
     cacc()
     elif ch=="cip":
          cip()
     elif ch=="ea":
          macc()
     elif ch=="da":
          dacc()
     elif ch=="l":
          locker_()
     elif ch=="s":
          search()
     elif ch=="r":
          sreview()
     elif ch=="lo":
          interface()
     else:
          print("!!!!!!!Enter a or ca or cip or ea or da or l or 
                s or r or lo only!!!!!!!")
          adm_home()

#TO DISPLAY ACCOUNTS IN A TABULAR FORM
        
def acc_():
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     print("_______ACCOUNT DETAILS PANEL_______")
     print("Enter aa to show all accounts")
     print("Enter a to show individual's account")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="aa":
     cb.execute("select 
Account_number,Account_holder,Nominee_name,Father_name,Date_of_birth,Gender,Marital_status,Contact_number,E_mail,Address,Account_type,Account_category from acc_details")
     u=cb.fetchall()
          if u:
          caal=0
               aal=[]
               for i in u:
               caal=caal+1
             aal.append((caal,)+i)            aac=tabulate(aal,headers=["S.No.","Account_number",
"Account_holder","Nominee_name","Father_name","Date_of_birth","Gender","Marital_status","Contact_number","E_mail","Address","Account_type","Account_category"],
tablefmt="grid")
         print("_______ACCOUNT DETAILS_______")
         print(aac)
         acc_()
elif ch=="a":
try:
          ac=int(input("Enter account number:"))
               if (len(str(ac)))<8:
               print("!!!!!!!Entered value is too 
                     short!!!!!!!")
                    print("!!!!!!!Enter account number of 8 
                          digits!!!!!!!")
                    acc_()
               elif(len(str(ac)))>8:
               print("!!!!!!!Entered value is too 
                      long!!!!!!!")
                    print("!!!!!!!Enter account number of 8
                           digits!!!!!!!")
                    acc_()
     except ValueError:
     print("!!!!!!!Enter integer only!!!!!!!")
               acc_()
cb.execute("select
Account_number,Account_holder,Nominee_name,Father_name,Date_of_birth,Gender,Marital_status,Contact_number,E_mail,Address,Account_type,Account_category from acc_details where Account_number={}".format(ac))
          u=cb.fetchone()
          if u:             
          anc=tabulate([u],headers=["Account_number",
"Account_holder","Nominee_name","Father_name","Date_of_birth","Gender","Marital_status","Contact_number","E_mail","Address","Account_type","Account_category"],
tablefmt="grid")
 print("_______ACCOUNT DETAILS_______")
                print(anc)
                acc_()
          else:
               print("~~~~~~~NO SUCH ACCOUNT FOUND~~~~~~~")
               print("~~~~~~~TRY AGAIN~~~~~~~")
               acc_()
    elif ch=="b":
        adm_home()
    else:
        print("!!!!!!!Enter aa or a or b only!!!!!!!")
        acc_()

#TO DISPLAY CREATE A NEW ACCOUNT PANEL 

def cacc():
date=str(dt.date.today())
     print("_______NEW ACCOUNT PANEL_______")
     ac=input("Enter (major or minor) account category:")
     if ac=="major":
     cmacc(ac,date)
     elif ac=="minor":
          c_macc(ac,date)
     else:
          print("!!!!!!!Enter major or minor only!!!!!!!")
          cacc()

#TO CREATE A MAJOR ACCOUNT

def cmacc(ac,date):
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     cb.execute("select Account_number from acc_details")
     u=cb.fetchall()
     p=randint(0,99999999)
     for i in u:
     if p==i[0]:
          break
     else:
     an=p
     n=input("Enter your full name:")
     if n.isspace():
     print("!!!!!!!Enter a valid name!!!!!!!")
     cmacc(ac,date)
          return
     elif len(n)>30:
          print("!!!!!!!Name is too long!!!!!!!")
          cmacc(ac,date)
          return
     elif len(n)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          cmacc(ac,date)
          return
     nn=input("Enter nominee's name:")
     if nn.isspace():
          print("!!!!!!!Enter a valid name!!!!!!!")
          cmacc(ac,date)
          return
     elif len(nn)>30:
          print("!!!!!!!Name is too long!!!!!!!")
          cmacc(ac,date)
          return
     elif len(nn)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          cmacc(ac,date)
          return
     fn=input("Enter father's name:")
     if fn.isspace():
          print("!!!!!!!Enter a valid name!!!!!!!")
          cmacc(ac,date)
          return
     elif len(fn)>30:
          print("!!!!!!!Name is too long!!!!!!!")
          cmacc(ac,date)
          return
     elif len(fn)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          cmacc(ac,date)
          return
     db=input("Enter your date of birth:")
     f=datecheck(db)
     if f:
          cmacc(ac,date)
          return
     if db>date:
          print("!!!!!!!Enter a valid date!!!!!!!")
          cmacc(ac,date)
          return
     g=input("Enter gender:")
     if g.lower() not in ["male","female","transgender"]:
          print("!!!!!!!Invalid gender!!!!!!!")
          print("!!!!!!!Enter male or female or transgender 
                only!!!!!!!")
          cmacc(ac,date)
          return
     mls=input("Enter marital status:")
     if mls.lower() not in ["married","unmarried"]:
          print("!!!!!!!Invalid marital status!!!!!!!")
          print("!!!!!!!Enter married or unmarried only!!!!!!!")
          cmacc(ac,date)
          return
     cn=int(input("Enter contact number:"))
     f=phnocheck(cn)
     if f:
          cmacc(ac,date)
          return
     e=input("Enter your E-mail:")
     f=emailcheck(e)
     if f:
          cmacc(ac,date)
          return
     a=input("Enter your address:")
     if a.isspace():
          print("!!!!!!!Enter a valid address!!!!!!!")
          cmacc(ac,date)
          return
     elif len(a)>100:
          print("!!!!!!!Address is too long!!!!!!!")
          cmacc(ac,date)
          return
     elif len(a)<1:
          print("!!!!!!!Address is too short!!!!!!!")
          cmacc(ac,date)
          return
     at=input("Enter account type:")
     if at.lower() not in ["savings","current","bussiness"]:
          print("!!!!!!!Invalid account type!!!!!!!")
          print("!!!!!!!Enter savings or current or 
                bussiness!!!!!!!")
          cmacc(ac,date)
          return
     uc=input("Enter (now or later) to create id and password 
              for login:")
     uc=uc.lower()
     if uc=="now":
          cb.execute("select * from interface where 
                      Type={}".format("user"))
          c=cb.fetchall()
          id=input("Enter id:")
          if(len(id))<8:
              print("!!!!!!!Entered value is too short!!!!!!!")
              cmacc(ac,date)
              return
          elif (len(id))>20:
              print("!!!!!!!Entered value is too long!!!!!!!")
              cmacc(ac,date)
              return
          p=input("Enter password:")
          if(len(p))<8:
              print("!!!!!!!Entered value is too short!!!!!!!")
              cmacc(ac,date)
              return
          elif (len(p))>8:
              print("!!!!!!!Entered value is too long!!!!!!!")
              cmacc(ac,date)
              return
          for i in c:
          if id==i[0] or p==i[1]:
               break
          else:
          cb.execute("inset into interface values 
                     ('{}','{}','{}')".format(id,p,"user"))
               cb.execute("insert into 
                           acc_details(Account_number,
                         Account_holder,Nominee_name,Father_name
                          ,Date_of_birth,Gender,Marital_status,
                           Contact_number,E_mail,Address,
  Account_type,Account_category,id)
                         values({},'{}','{}','{}','{}',
'{}','{}',{},'{}','{}','{}','{}','{}')".format(an,n,nn,fn,db,g,ms,cn,e,a,at,ac))
               db.commit()
               print("~~~~~~~ACCOUNT CREATED  
                     SUCCESSFULLY~~~~~~~")                 
               leave("admin")
      elif uc=="later":
      cb.execute("insert into 
                 acc_details(Account_number,Account_holder,
                 Nominee_name,Father_name,Date_of_birth,
                 Gender,Marital_status,Contact_number,
              E_mail,Address,Account_type,Account_category) 
                values({},'{}','{}','{}','{}','{}','{}',{},
                       '{}','{}','{}','{}')"
                 .format(an,n,nn,fn,db,g,ms,cn,e,a,at,ac))
           db.commit()
           print("~~~~~~~ACCOUNT CREATED SUCCESSFULLY~~~~~~~")
           leave("admin")
      else:
           print("!!!!!!!Enter now or later only!!!!!!!")
           cmacc(ac,date)
           return

#TO CREATE A MINOR ACCOUNT
    
def c_macc(ac,date):  
db=ms.connect(host="localhost",user="root",password=admin,
                   database="bms")
     cb=db.cursor()
     cb.execute("select Account_number from acc_details")
     u=cb.fetchall()
     p=randint(0,99999999)
     for i in u:
     if p==i[0]:
          break
     else:
     an=p
     n=input("Enter your full name:")
     if n.isspace():
     print("!!!!!!!Enter a valid name!!!!!!!")
          c_macc(ac,date)
          return
     elif len(n)>30:
          print("!!!!!!!Name is too long!!!!!!!")
          c_macc(ac,date)
          return
     elif len(n)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          c_macc(ac,date)
          return
     nn=input("Enter nominee's name:")
     if nn.isspace():
     print("!!!!!!!Enter a valid name!!!!!!!")
          c_macc(ac,date)
          return
     elif len(nn)>30:
     print("!!!!!!!Name is too long!!!!!!!")
          c_macc(ac,date)
          return
     elif len(nn)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          c_macc(ac,date)
          return
     fn=input("Enter father's name:")
     if fn.isspace():
          print("!!!!!!!Enter a valid name!!!!!!!")
          c_macc(ac,date)
          return
     elif len(fn)>30:
          print("!!!!!!!Name is too long!!!!!!!")
          c_macc(ac,date)
          return
     elif len(fn)<1:
          print("!!!!!!!Name is too short!!!!!!!")
          c_macc(ac,date)
          return
     db=input("Enter your date of birth:")
     f=datecheck(db)
     if f:
          c_macc(ac,date)
          return
     if db>date:
          print("!!!!!!!Enter a valid date!!!!!!!")
          c_macc(ac,date)
          return
     g=input("Enter gender:")
     if g.lower() not in ["male","female","transgender"]:
          print("!!!!!!!Invalid gender!!!!!!!")
          print("!!!!!!!Enter male or female or transgender 
                 only!!!!!!!")
          c_macc(ac,date)
          return
     mls=input("Enter marital status:")
     if mls.lower() not in ["married","unmarried"]:
     print("!!!!!!!Invalid marital status!!!!!!!")
          print("!!!!!!!Enter married or unmarried only!!!!!!!")
          c_macc(ac,date)
          return
     cn=int(input("Enter contact number:"))
     f=phnocheck(cn)
     if f:
     c_macc(ac,date)
          return
     e=input("Enter your E-mail:")
     f=emailcheck(e)
     if f:
     c_macc(ac,date)
          return
     a=input("Enter your address:")
     if a.isspace():
          print("!!!!!!!Enter a valid address!!!!!!!")
          c_macc(ac,date)
          return
     elif len(a)>100:
          print("!!!!!!!Address is too long!!!!!!!")
          c_macc(ac,date)
          return
     elif len(a)<1:
          print("!!!!!!!Address is too short!!!!!!!")
          c_macc(ac,date)
          return
     at=input("Enter account type:")
     if at.lower() not in ["savings","current","bussiness"]:
          print("!!!!!!!Invalid account type!!!!!!!")
          print("!!!!!!!Enter savings or current or 
                bussiness!!!!!!!")
          c_macc(ac,date)
          return
     uc=input("Enter (now or later) to create id and password
              for login:")
     uc=uc.lower()
if uc=="now":
     cb.execute("select * from interface where
                 Type={}".format("user"))
          c=cb.fetchall()
          id=input("Enter id:")
          if(len(id))<8:
          print("!!!!!!!Entered value is too short!!!!!!!")
              c_macc(ac,date)
              return
          elif (len(id))>20:
              print("!!!!!!!Entered value is too long!!!!!!!")
              c_macc(ac,date)
              return
          p=input("Enter password:")
          if(len(p))<8:
              print("!!!!!!!Entered value is too short!!!!!!!")
              c_macc(ac,date)
              return
          elif (len(p))>8:
              print("!!!!!!!Entered value is too long!!!!!!!")
              c_macc(ac,date)
              return
          for i in c:
          if id==i[0] or p==i[1]:
               break
          else:
               cb.execute("inset into interface values 
                          ('{}','{}','{}')"
                          .format(id,p,"user"))
               cb.execute("insert into 
                      acc_details(Account_number,Account_holder,
                         Nominee_name,Father_name,Date_of_birth,
                           Gender,Marital_status,Contact_number,
                           E_mail,Address,Account_type,
                           Account_category,id) 
                        values({},'{}','{}','{}','{}','{}','{}',
                           {},'{}','{}','{}','{}','{}')"
                       .format(an,n,nn,fn,db,g,ms,cn,e,a,at,ac))
               db.commit()
               print("~~~~~~~ACCOUNT CREATED 
                     SUCCESSFULLY~~~~~~~")
               leave("admin")
elif uc=="later":
     cb.execute("insert into 
 acc_details(Account_number,Account_holder,
                Nominee_name,Father_name,Date_of_birth,
                Gender,Marital_status,Contact_number,
              E_mail,Address,Account_type,Account_category) 
                values({},'{}','{}','{}','{}','{}','{}',
                {},'{}','{}','{}','{}')"
                .format(an,n,nn,fn,db,g,ms,cn,e,a,at,ac))
          db.commit()
          print("~~~~~~~ACCOUNT CREATED SUCCESSFULLY~~~~~~~")
          leave("admin")
     else:
          print("!!!!!!!Enter now or later only!!!!!!!")
          c_macc(ac,date)
          return

#TO CREATE ID AND PASSWORD OF CUSTOMER FOR LOGIN
    
def cip():
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     print("_______NEW ID AND PASSWORD PANEL_______")
     cb.execute("select * from interface where
                 Type={}".format("user"))
     u=cb.fetchall()
     id=input("Enter id:")
     if(len(id))<8:
     print("!!!!!!!Entered value is too short!!!!!!!")
          cip()
          return
     elif (len(id))>20:
          print("!!!!!!!Entered value is too long!!!!!!!")
          cip()
          return
     p=input("Enter password:")
     if(len(p))<8:
          print("!!!!!!!Entered value is too short!!!!!!!")
          cip()
          return
     elif (len(p))>8:
     print("!!!!!!!Entered value is too long!!!!!!!")
          cip()
          return
     for i in u:
     if id==i[0] or p==i[1]:
          break
          else:
          cb.execute("inset into interface values 
                     ('{}','{}','{}')".format(id,p,"user"))
               db.commit()
               print("~~~~~~~ID AND PASSWORD CREATED
                     SUCCESSFULLY~~~~~~~")
               leave("admin")
        
#TO MODIFY THE CUSTOMER'S ACCOUNT DETAILS
        
def macc():
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     date=dt.date.today()
     try:
     ac=int(input("Enter account number:"))
if (len(str(ac)))<8:
          print("!!!!!!!Entered value is too short!!!!!!!")
               print("Enter account number of 8 digits")
               macc()
          elif(len(str(ac)))>8:
               print("!!!!!!!Entered value is too long!!!!!!!")
               print("Enter account number of 8 digits")
               macc()
     except ValueError:
     print("!!!!!!!Enter integer only!!!!!!!")
          macc()
     print("_______MODIFY ACCOUNT DETAILS_______")
     print("Enter nm to modify name")
     print("Enter nn to modify nominee's name")
     print("Enter fn to modify father's name")
     print("Enter db to modify date of birth")
     print("Enter g to modify gender")
     print("Enter ms to modify marital status")
     print("Enter cn to modify contact number")
     print("Enter e to modify e-mail")
     print("Enter a to modify address")
     print("Enter at to modify account type")
     print("Enter c to modify account category:")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="nm":
     nnm=input("Enter new name:")
          if nnm.isspace():
          print("!!!!!!!Enter a valid name!!!!!!!")
               macc()
               return
          elif len(nnm)>30:
               print("!!!!!!!Name is too long!!!!!!!")
               macc()
               return
          elif len(nnm)<1:
               print("!!!!!!!Name is too short!!!!!!!")
               macc()
               return
          cb.execute("update acc_details set 
                      Account_holder='{}'".format(nm))
     elif ch=="nn":
     nnn=input("Enter nominee's new name:")
          if nnn.isspace():
               print("!!!!!!!Enter a valid name!!!!!!!")
               macc()
               return
          elif len(nnn)>30:
               print("!!!!!!!Name is too long!!!!!!!")
               macc()
               return
          elif len(nnn)<1:
               print("!!!!!!!Name is too short!!!!!!!")
               macc()
               return
          cb.execute("update acc_details set  
                      Nominee_name='{}'".format(nnn))
     elif ch=="fn":
          nfn=input("Enter father's new name:")
          if nfn.isspace():
          print("!!!!!!!Enter a valid name!!!!!!!")
               macc()
               return
          elif len(nfn)>30:
               print("!!!!!!!Name is too long!!!!!!!")
               macc()
               return
          elif len(nfn)<1:
               print("!!!!!!!Name is too short!!!!!!!")
               macc()
               return
          cb.execute("update acc_details set
                      Father_name='{}'".format(nfn))
     elif ch=="db":
         ndb=input("Enter new date of birth:")
         f=datecheck(ndb)
         if f:
              macc()
              return
         if ndb>date:
              print("!!!!!!!Enter a valid date!!!!!!!")
              macc()
         cb.execute("update acc_details set 
                     Date_of_birth='{}'".format(ndb))
     elif ch=="g":
         ng=input("Enter new gender:")
         if ng.lower() not in ["male","female","transgender"]:
         print("!!!!!!!Invalid gender!!!!!!!")
              print("!!!!!!!Enter male or female or transgender 
                    only!!!!!!!")
              macc()
              return
         cb.execute("update acc_details set 
                     Gender='{}'".format(ng))
     elif ch=="ms":
         ems=input("Enter new marital status:")
         if ems.lower() not in ["married","unmarried"]:
              print("!!!!!!!Invalid marital status!!!!!!!")
              print("!!!!!!!Enter married or unmarried 
                    only!!!!!!!")
              macc()
              return
         cb.execute("update acc_details set Marital 
                     status='{}'".format(ems))
     elif ch=="cn":
         ncn=int(input("Enter new contact number:"))
         f=phnocheck(ncn)
         if f:
              macc()
              return
         cb.execute("update acc_details set 
                     Contact_number={}".format(ncn))
     elif ch=="e":
         ne=input("Enter new E-mail:")
         f=emailcheck(ne)
         if f:
              macc()
              return
         cb.execute("update acc_details set 
                     E_mail='{}'".format(ne))
     elif ch=="a":
         na=input("Enter new address:")
         if na.isspace():
              print("!!!!!!!Enter a valid address!!!!!!!")
              macc()
              return
         elif len(na)>100:
              print("!!!!!!!Address is too long!!!!!!!")
              macc()
              return
         elif len(na)<1:
              print("!!!!!!!Address is too short!!!!!!!")
              macc()
              return
         cb.execute("update acc_details set
                     Address='{}'".format(na))
     elif ch=="at":
         eat=input("Enter new account type:")
         if eat.lower() not in  
         ["savings","current","bussiness"]:
         print("!!!!!!!Invalid account type!!!!!!!")
              print("!!!!!!!Enter savings or current or 
                    bussiness!!!!!!!")
              macc()
              return
         cb.execute("update acc_details set 
                     Account_type='{}'".format(eat))
     elif ch=="c":
         nc=input("Enter new account category:")
         if nc.lower() not in ["minor","major"]:
              print("!!!!!!!Invalid account category!!!!!!!")
              print("!!!!!!!Enter major or minor!!!!!!!")
              macc()
              return
         cb.execute("update acc_details set new 
                     Account_category='{}'".format(nc))
     elif ch=="b":
     adm_home()
     else:
     print("!!!!!!!Enter nm or nn or fn or db or g or ms or 
           cn or e or a or c or b only!!!!!!!")
          macc()
          db.commit()
          leave("admin")

#TO DELETE THE CUSTOMER'S ACCOUNT
    
def dacc(): 
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     try:
     ac=int(input("Enter account number:"))
          if (len(str(ac)))<8:
          print("!!!!!!!Entered value is too short!!!!!!!")
               print("Enter account number of 8 digits")
               dacc()
          elif(len(str(ac)))>8:
               print("!!!!!!!Entered value is too long!!!!!!!")
               print("Enter account number of 8 digits")
               dacc()
     except ValueError:
          print("!!!!!!!Enter integer only!!!!!!!")
          dacc()
     ch=input("Do you want to delete permanently ???(yes or 
              no):")
     ch=ch.lower()
     if ch=="yes":
     cb.execute("select 
 Account_number,Account_holder,Nominee_name,
 Father_name,Date_of_birth,Gender,
 Marital_status,Contact_number,E_mail,
 Address,Account_type,Account_category,id
                     from acc_details where Account_number={}"
                     .format(ac))
          u=cb.fetchone()
          cb.execute("select Available_balance from 
                     avail_balance where  
                     Account_number={}".format(ac))
          uc=cb.fetchone()
          cb.execute("insert into dacc_details 
                     values({},'{}','{}','{}','{}','{}','{}',{},
                    '{}','{}','{}','{}',{})".format(u[0],u[1],
                     u[2],u[3],u[4],u[5],u[6],u[7],u[8],
                     u[9],u[10],u[11],uc[1]))
          cb.execute("delete from avail_balance where 
                      Account_number={}".format(ac))
          cb.execute("delete from acc_details where 
                      Account_number={}".format(ac))
          cb.execute("delete from interface where 
                     id={}".format(u[12]))
          db.commit()
          print("~~~~~~~ACCOUNT DELETED SUCCESSFULLY~~~~~~~")
          leave("admin")
     elif ch=="no":
          adm_home()
     else:
          print("!!!!!!!Enter yes or no only!!!!!!!")
          dacc()
        
#TO DISPLAY LOCKER PANEL
        
def locker_():
print("_______LOCKER PANEL_______")
     print("Enter lr for locker registration and rental")
     print("Enter re for locker return")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="lr":
     locker_registration()
     elif ch=="re":
          locker_return()
     elif ch=="b":
          adm_home()
     else:
          print("!!!!!!!Enter lr or re or b only!!!!!!!")
          locker_()

#TO REGISTER AND RENT A LOCKER TO THE CUSTOMER
        
def locker_registration():
print("_______LOCKER REGISTRATION AND RENTAL PANEL_______")
     s=input("Enter size of locker you want:")
s=s.title()
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     cb.execute("select Locker_ID,Registration_fee,Annual_rent 
                from locker where Size='{}' and Status='{}'"
                .format(s,"Available"))
     u=cb.fetchall()
     if u:
     lr=0
          lk=[]
          lid=[]
          for i in u:
          lr=lr+1
               lid.append(i[0])
               lk.appeend((lk,)+i)
          lkt=tabulate(lk,headers=["Locker_ID",  
                                   "Registration_fee",
"Annual_rent"],
                       tablefmt="grid")
          print("_______LOCKERS AVAILABLE_______")
          print(lkt)
          if lr==0:
          print("~~~~~~~NO LOCKERS AVAILABLE~~~~~~~")
          elif lr==1:
               print("~~~~~~~",lr,"LOCKER AVAILABLE~~~~~~~")
          else:
               print("~~~~~~~",lr,"LOCKERS AVAILABLE~~~~~~~")
         id=input("Enter locker ID:")
         if(len(id))<5:
              print("!!!!!!!Entered value is too short!!!!!!!")
              locker_registration()
         elif (len(id))>5:
              print("!!!!!!!Entered value is too long!!!!!!!")
              locker_registration()
         if id not in lid:
              print("!!!!!!!Enter a Locker ID from the table 
                    shown above only!!!!!!!")
              locker_registration()
              return
         n=input("Enter customer's name:")
         if n.isspace():
              print("!!!!!!!Enter a valid name!!!!!!!")
              locker_registration()
              return
         elif len(n)>30:
              print("!!!!!!!Name is too long!!!!!!!")
              locker_registration()
              return
         elif len(n)<1:
              print("!!!!!!!Name is too short!!!!!!!")
              locker_registration()
              return
         nn=input("Enter nominee's name:")
         if nn.isspace():
              print("!!!!!!!Enter a valid name!!!!!!!")
              locker_registration()
              return
         elif len(nn)>30:
              print("!!!!!!!Name is too long!!!!!!!")
              locker_registration()
              return
         elif len(nn)<1:
              print("!!!!!!!Name is too short!!!!!!!")
              locker_registration()
              return
        t=int(input("Enter tenure(years):"))
        try:
        t=int(input("Enter tenure(years):"))
             if (len(str(t)))<1:
             print("!!!!!!!Tenure is too short!!!!!!!")
                  locker_registration()
             elif (len(str(t)))>2:
                  print("!!!!!!!Tenure is too long!!!!!!!")
                  locker_registration()
        except ValueError:
        print("!!!!!!!Enter integers only!!!!!!!")
             locker_registration()
        d=input("Enter details of deposits:")
        if d.isspace():
        print("!!!!!!!Enter valid details !!!!!!!")
             locker_registration()
             return
        elif len(d)>100:
             print("!!!!!!!Details are too long!!!!!!!")
             locker_registration()
             return
        elif len(d)<1:
             print("!!!!!!!Details are too short!!!!!!!")
             locker_registration()
             return
        try:
             p=int(input("Enter new pin:"))
             if (len(str(p)))<4:
             print("!!!!!!!Pin is too short!!!!!!!")
                  locker_registration()
             elif (len(str(p)))>4:
                  print("!!!!!!!Pin is too long!!!!!!!")
                  locker_registration()
        except ValueError:
             print("!!!!!!!Enter integers only!!!!!!!")
             locker_registration()
        try:
             cp=int(input("Enter new pin:"))
             if (len(str(cp)))<4:
                  print("!!!!!!!Pin is too short!!!!!!!")
                  locker_registration()
             elif (len(str(cp)))>4:
                  print("!!!!!!!Pin is too long!!!!!!!")
                  locker_registration()
        except ValueError:
             print("!!!!!!!Enter integers only!!!!!!!")
             locker_registration()
        if cp==p:
             cb.execute("update locker set Account_holder='{}'
                         where Locker_ID='{}'".format(n,id))
             cb.execute("update locker set Nominee_name='{}' 
                         where Locker_ID='{}'".format(nn,id))
             cb.execute("update locker set Locker_pin={} where 
                         Locker_ID='{}'".format(cp,id))
             cb.execute("update locker set Tenure={} where 
                         Locker_ID='{}'".format(t,id))
             cb.execute("update locker set Details='{}' where 
                         Locker_ID='{}'".format(d,id))
             cb.execute("update locker set Status={} where 
                         Locker_ID='{}'".format("Rented",id))
             db.commit()
        else:
             print("!!!!!!!Pin does not match!!!!!!!")
             locker_registration()
    else:
         print("~~~~~~~SORRY NO",s,"LOCKER AVAILABE NOW~~~~~~~")
         print("~~~~~~~TRY WITH A DIFFERENT SIZE~~~~~~~")
         locker_registration()
    cb.execute("select Registration_fee,Annual_rent,Tenure from 
                locker where Locker_ID='{}'".format(id))
    c=cb.fetchone()
    a=c[0]+c[1]*c[2]
    try:
    ac=int(input("Enter account number:"))
         if (len(str(ac)))<8:
         print("!!!!!!!Entered value is too short!!!!!!!")
              print("Enter account number of 8 digits")
              locker_registration()
         elif(len(str(ac)))>8:
              print("!!!!!!!Entered value is too long!!!!!!!")
              print("Enter account number of 8 digits")
              locker_registration()
    except ValueError:
         print("!!!!!!!Enter integer only!!!!!!!")
         locker_registration()
    cb.execute("select Available_balance from avail_balance 
                where Account_number={}".format(ac))
    uc=cb.fetchone()
    if uc[0]>=(a+2000):
    cb.execute("update avail_balance set 
                Available_balance=Available_balance-{}  
                where Account_number={}".format(a,ac))
         db.commit()
         print("~~~~~~~PAYMENT SUCCESSFUL~~~~~~~")
         print("~~~~~~~LOCKER RESGISTRATION AND RENTAL 
               SUCCESSFUL~~~~~~~")
         locker_()
    else:
         print("!!!!!!!PAYMENT UNSUCCESSFUL!!!!!!!")
         print("!!!!!!!YOU DON'T HAVE ENOUGH BALANCE!!!!!!!")
         print("!!!!!!!LOCKER RESGISTRATION AND RENTAL 
               UNSUCCESSFUL!!!!!!!")
         locker_()

#TO RETURN THE LOCKER REGISTERED AND RENTED BY CUSTOMER
             
def locker_return(): 
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     id=input("Enter locker id:")
     if(len(id))<5:
     print("!!!!!!!Entered value is too short!!!!!!!")
          locker_return()
     elif (len(id))>5:
          print("!!!!!!!Entered value is too long!!!!!!!")
          locker_return()
     try:
          p=int(input("Enter master pin:"))
          if (len(str(p)))<4:
          print("!!!!!!!Pin is too short!!!!!!!")
              locker_return()
          elif (len(str(p)))>4:
              print("!!!!!!!Pin is too long!!!!!!!")
              locker_return()
     except ValueError:
          print("!!!!!!!Enter integers only!!!!!!!")
          locker_return()
     cb.execute("select * from locker where Locker_ID='{}'
                and Master_pin={}".format(id,p))
     u=cb.fetchone()
     if u:
     cb.execute("update locker set Account_holder=Null 
                 where Locker_ID='{}'".format(id))
          cb.execute("update locker set Nominee_name=Null where 
                      Locker_ID='{}'".format(id))
          cb.execute("update locker set Locker_pin=Null where 
                      Locker_ID='{}'".format(id))
          cb.execute("update locker set Tenure=Null where
                      Locker_ID='{}'".format(id))
          cb.execute("update locker set Details=Null where 
                      Locker_ID='{}'".format(id))
          cb.execute("update locker set Status={} where
                      Locker_ID='{}'".format("Available",id))
          cb.execute("update locker set Access_log=Null where 
                      Locker_ID='{}'".format(id))
          db.commit()
          print("~~~~~~~LOCKER RETURN SUCCESSFUL~~~~~~~")
          locker()
     else:
          print("!!!!!!!LOCKER RETURN UNSUCCESSFUL!!!!!!!")
          locker()

#TO DISPLAY SEARCH PANEL
        
def search():
print("_______SEARCH PANEL_______") 
     print("Enter a to search on the basis of age")
     print("Enter g to search on the basis of gender")
     print("Enter ms to search on the basis of marital status")
     print("Enter s to search on the basis of surnames")
     print("Enter l to search on the basis of locality")
     print("Enter c to search on the basis of category of 
           account")
     print("Enter t to search on the basis of type of account")
     print("Enter ba to search on the basis of balance")
     print("Enter b to go back")
     ch=input("Enter your choice:")
     if ch=="a":
     search_age()
     elif ch=="g":
          search_gender()
     elif ch=="ms":
          search_marital_status()
     elif ch=="s":
          search_surname()
     elif ch=="l":
          search_locality()
     elif ch=="c":
          search_category()
     elif ch=="t":
          search_type()
     elif ch=="ba":
          search_balance()
     elif ch=="b":
          adm_home()
     else:
          print("!!!!!!!Enter a or g or ms or s or l or c or t 
          or ba or b only!!!!!!!")
          search()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF AGE
        
def search_age():  
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     print("Enter m for minor account holders")
     print("Enter ma for adult account holders")
     print("Enter sc for senior citizen account holders")
     uc=input("Enter category to search:")
     cb.execute("select Account_number,Account_holder,
                 Date_of_birth from acc_details")
     u=cb.fetchall()
     days_in_year = 365.2425
     cm=0
     ca=0
     csc=0
     al=[]
     if uc=="m":
     print("_______MINOR ACCOUNT HOLDERS_______")
          for i in u:
          age = int((dt.date.today() - i[2]).days /
                     days_in_year)
          if age<=18:
               cm=cm+1
                    al.append([cm,i[0],i[1]])
          mah=tabulate(al,headers=["S.No.","Account_number",
                                   "Account_holder"],
                        tablefmt="grid")
          print(mah)
          if cm==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
          elif cm==1:
               print("There is",cm,"minor account
                      holder~~~~~~~")
         else:
              print("~~~~~~~There are",cm,"minor account
                     holders~~~~~~~")
         search()
     elif uc=="ma":
     print("_______MAJOR ACCOUNT HOLDERS_______")
          for i in u:
          age = int((dt.date.today() - i[2]).days /
                     days_in_year)
               if 60>age>=18:
               ca=ca+1
                    al.append([ca,i[0],i[1]])
          maah=tabulate(al,headers=["S.No.","Account_number",
                                    "Account_holder"],
                        tablefmt="grid")
          print(maah)
          if ca==0:
              print("~~~~~~~There are no such account
                     holders~~~~~~~")
          elif ca==1:
              print("~~~~~~~There is",ca,"major account 
                     holder~~~~~~~")
          else:
              print("~~~~~~~There are",ca,"major account 
                     holders~~~~~~~")
          search()
     elif uc=="sc":
          print("_______SENIOR CITIZEN ACCOUNT HOLDERS_______")
          for i in u:
          age = int((dt.date.today() - i[2]).days / 
                     days_in_year)
               if age>=60:
               csc=csc+1
                    al.append([csc,i[0],i[1]])
          csah=tabulate(al,headers=["S.No.","Account_number",
                                     "Account_holder"],
          tablefmt="grid")
          print(csah)
          if csc==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
          elif csc==1:
               print("~~~~~~~There is",csc,"senior citizen 
                      account holder~~~~~~~")
          else:
               print("~~~~~~~There are",csc,"senior citizen 
                      account holders~~~~~~~")
          search()
     else:
          print("!!!!!!!Enter m or ma or sc only!!!!!!!")
          search_age()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF GENDER
        
def search_gender(): 
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     cb.execute("select Account_number,Account_holder,Gender 
                 from acc_details")
     u=cb.fetchall()
     uc=input("Enter gender to search:")
     uc=uc.lower()
     if uc in ["male","female","transgender"]:
     print("_______",uc.upper(),"ACCOUNT HOLDERS_______")
          gc=0
          gl=[]
          for i in u:
          if (i[2].lower())==uc:
               gc=gc+1
                    gl.append([gc,i[0],i[1]])
          gah=tabulate(gl,headers=["S.No.","Account_number",
                                    "Account_holder"],
          tablefmt="grid")
          print(gah)
          if gc==0:
               print("~~~~~~~There are no such account 
                      holders~~~~~~~")
          elif gc==1:
               print("~~~~~~~There is",gc,uc,"account
                      holder~~~~~~~")
          else:
               print("~~~~~~~There are",gc,uc,"account 
                      holders~~~~~~~")
          search()
     else:
          print("!!!!!!!Enter male or female or
                 transgender!!!!!!!")
          search_gender()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF MARITAL STATUS
        
def search_marital_status():  
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     cb.execute("select Account_number,Account_holder,
                 Marital_status from acc_details")
     u=cb.fetchall()
     uc=input("Enter marital status to search:")
     uc=uc.lower()
     if uc in ["married","unmarried"]:
     print("_______",uc.upper(),"ACCOUNT HOLDERS_______")
          mc=0
          ml=[]
          for i in u:
          if (i[2].lower())==uc:
               mc=mc+1
                    ml.append([mc,i[0],i[1]])
          msah=tabulate(ml,headers=["S.No.","Account_number",
                                     "Account_holder"],
          tablefmt="grid")
          print(msah)
          if mc==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
          elif gc==1:
               print("~~~~~~~There is",mc,uc,"account 
                      holder~~~~~~~")
          else:
               print("~~~~~~~There are",mc,uc,"account 
                      holders~~~~~~~")
          search()
     else:
          print("!!!!!!!Enter married or unmarried only!!!!!!!")
          search_marital_status()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF SURNAME
        
def search_surname():
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     cb.execute("select Account_number,Account_holder from 
                 acc_details")
     u=cb.fetchall()
     uc=input("Enter surname to search:")
     uc=uc.lower()
     print("_______ACCOUNT HOLDERS HAVING SURNAME",
           uc.upper(),"_______")
     cn=0
     sl=[]
     for i in u:
     if (i[1].split()[-1].lower())==uc:
          cn=cn+1
               sl.append([cn,i[0],i[1]])
     sah=tabulate(sl,headers=["S.No.","Account_number",
                              "Account_holder"],
     tablefmt="grid")
     print(sah)
     if cn==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
     elif cn==1:
          print("~~~~~~~There is",cn,"account holder having 
                 surname",uc,"~~~~~~~")
     else:
          print("~~~~~~~There are",cn,"account holders having
                 surname",uc,"~~~~~~~")
     search()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF LOCALITY
    
def search_locality():
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     uc=input("Enter locality to search:")
     cu=0
     ll=[]
     cb.execute("select Account_number,Account_holder from 
                 acc_details where Address like '{}'"
                 .format("%"+uc+"%"))
     u=cb.fetchall()
     print("_______ACCOUNT HOLDERS BELONGING TO",
            uc.upper(),"LOCALITY_______")
     for i in u:
     cu=cu+1
          ll.append([cu,i[0],i[1]])
     lah=tabulate(ll,headers=["S.No.","Account_number",
                               "Account_holder"],
     tablefmt="grid")
     print(lah)
     if cu==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
     elif cu==1:
          print("~~~~~~~There is",cu,"account holder belonging 
                 to",uc,"locality~~~~~~~")
     else:
          print("~~~~~~~There are",cu,"account holders belonging 
                 to",uc,"locality~~~~~~~")
     search()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF CATEGORY
    
def search_category(): 
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     cb.execute("select Account_number,Account_holder,
                 Account_category from acc_details")
     u=cb.fetchall()
     uc=input("Enter category of account to search:")
     uc=uc.lower()
     if uc in ["major","minor"]:
          print("_______ACCOUNT HOLDERS HAVING",
                 uc.upper(),"ACCOUNTS_______")
          cc=0
          cl=[]
          for i in u:
          if (i[2].lower())==uc:
               cc=cc+1
                    cl.append([cc,i[0],i[1]])
          cah=tabulate(cl,headers=["S.No.","Account_number",
                                    "Account_holder"],
          tablefmt="grid")
          print(cah)
          if cc==0:
              print("~~~~~~~There are no such account 
                     holders~~~~~~~")
          elif cc==1:
              print("~~~~~~~There is",cc,"account holder
                     having",uc,"account~~~~~~~")
          else:
              print("~~~~~~~There are",cc,"account holders
                     having",uc,"accounts~~~~~~~")
          search()
     else:
          print("!!!!!!!Enter major or minor only!!!!!!!")
          search_category()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF TYPE
        
def search_type():  
db=ms.connect(host="localhost",user="root",password=admin,
              database="bms")
     cb=db.cursor()
     cb.execute("select Account_number,Account_holder,
                 Account_type from acc_details")
     u=cb.fetchall()
     uc=input("Enter type of account to search:")
     uc=uc.lower()
     if uc in ["savings","current","business"]:
          print("_______ACCOUNT HOLDERS HAVING",
                uc.upper(),"ACCOUNTS_______")
     ct=0
          tl=[]
          for i in u:
          if (i[2].lower())==uc:
                  ct=ct+1
                  tl.append([ct,i[0],i[1]])
          tah=tabulate(tl,headers=["S.No.","Account_number",
                                   "Account_holder"],
                       tablefmt="grid")
          print(tah)
          if ct==0:
              print("~~~~~~~There are no such account 
                     holders~~~~~~~")
          elif ct==1:
              print("~~~~~~~There is",ct,"account holder 
                     having",uc,"account~~~~~~~")
          else:
              print("~~~~~~~There are",ct,"account holders 
                     having",uc,"accounts~~~~~~~")
          search()
     else:
          print("!!!!!!!Enter savings or current or business 
                 only!!!!!!!")
          search_type()

#TO SEARCH AND DISPLAY ACCOUNTS ON THE BASIS OF BALANCE
        
def search_balance():  
db=ms.connect(host="localhost",user="root",password=admin,
               database="bms")
     cb=db.cursor()
     cb.execute("select a.Account_number,Account_holder,
                 Available_balance from acc_details a,
                 avail_balance ab where 
                 a.Account_number=ab.Account_number")
     u=cb.fetchall()
     try:
     sp=float(input("Enter starting point:"))
          ep=float(input("Enter ending point:"))
     except ValueError:
          print("!!!!!!!Enter integer or float value 
                 only!!!!!!!")
          search_balance()   
     print("_______ACCOUNT HOLDERS HAVING BALANCE BETWEEN",
           sp,"AND",ep,"_______")
     cp=0
     bl=[]
     for i in u:
     if sp<=i[2]<=ep:
              cp=cp+1
              bl.append([cp,i[0],i[1]])
     bah=tabulate(bl,headers=["S.No.","Account_number",
                              "Account_holder"],
     tablefmt="grid")
     print(bah)
     if cp==0:
          print("~~~~~~~There are no such account 
                 holders~~~~~~~")
     elif cp==1:
          print("~~~~~~~There is",cp,"account holder having 
                 balance between",sp,"and",ep,"~~~~~~~")
     else:
          print("~~~~~~~There are",cp,"account holders having 
                 balance between",sp,"and",ep,"~~~~~~~")
     search()

#TO DISPLAY REVIEWS OF THE CUSTOMERS
    
def sreview():
print("_______REVIEW PANEL_______")
webbrowser.open("https://docs.google.com/spreadsheets/d/1MM
                      Z0xnam28eqXhwl_30vfYnYyEgPIaBwGHWQHMc1MHc/
                      edit?usp=drivesdk")
 leave("admin")

def leave(s,ac=0):
print("h for home")
     print("i for interface")
     print("e to exit")
     ch=input("Enter your choice:")
     if ch=="h":
     if s=="admin":
          adm_home()
          elif s=="customer":
     cust_home(ac)
     elif ch=="i":
     interface()
     elif ch=="e":
print("----------------------------------------------- 
        -")
          print("*******...THANK YOU,PLEASE VISIT AGAIN...
                 *******")
                            print("-----------------------------------------------
                  -")
     else:
          print("!!!!!!!Enter h or i or e only!!!!!!!")
          leave(s,ac)
  interface()



 

 





















