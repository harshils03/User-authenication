import pymysql as pm
import hashlib
import random
import smtplib
from email.mime.text import MIMEText



conn = pm.connect(host='localhost',user='root',database='pass_verify',password='root')
cur = conn.cursor()


def create_hash(input):
    hash33 = hashlib.new("SHA256")
    hash33.update(input.encode())
    hashed_input = hash33.hexdigest()
    return hashed_input

def forgot_pass():
    print("--------------------------------")
    print("--------------------------------")
    print("Forget Password? No worries")
    def create_otp():
        g_otp = random.randint(1000,9999)
        sg_otp = str(g_otp)
        return sg_otp
    
    otp = create_otp()


    user_mail = input("You will recieve an otp... Enter your email address: ")

    msg = MIMEText("Forgot the password? No problem.Your otp is "+otp+", enter this and reset your password.")
    msg['Subject'] = "You have recieved an OTP"
    msg['From'] = "harshil.s1403@gmail.com"
    msg['To'] = ', '.join(user_mail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login("harshil.s1403@gmail.com", "tizi bopt xiwr grjw")
        smtp_server.sendmail("harshil.s1403@gmail.com", user_mail, msg.as_string())
    print("OTP sent, Check your MAIL!!")

    
    def verify():
        while True:
            print("-----------------------------")
            enterotp = int(input("Enter your otp: "))
            if enterotp == int(otp):
                print("Correct!! You are verified.")
                new_pass = input("Enter your new password: ")
                
                print("-----------------------------")
                break
            else:
                print("Not correct, Enter again!!.")
                continue
            print("-----------------------------")
        return new_pass
            
        
    input_pass = verify()

    new_pass11 = create_hash(input_pass)
    

    query = "UPDATE users SET password = '"+new_pass11+"' WHERE email = '"+user_mail+"';"
    cur.execute(query)
    conn.commit()
    print("Password changed!!")


    



def add_data():
    while True:
            
        print("--------------------------------")
        print("--------------------------------")
        print("Welcome!! Enter your details one by one")
        f_name = input("Enter your first name: ")
        l_name = input("Enter your last name: ")
        age = int(input("Enter your age: "))
        email = input("Enter your email: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if age <= 16:
            print("--------------------------------")
            print(f"OOPS, You are {age}. User must be 16 or more")
            print("--------------------------------")
            main()
            break
        else:
            hashed_pass = create_hash(password)  

            query = "insert into users (First_Name,Last_Name,Age,user_name,password,email) values (%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (f_name,l_name,age,username,hashed_pass,email))
            conn.commit()
            print("Information added")
            print("--------------------------------")
            print("--------------------------------")
            main()




def verify_login():
    while True:
        print("--------------------------------")
        print("--------------------------------")
        user_name = input("Enter your username: ")
        password = input("Enter your password: ")

        query22 = "SELECT user_name FROM users"
        cur.execute(query22)
        conn.commit()


        fetched_users = []

        yy = cur.fetchall()
        for i in yy:
            fetched_users.append(i[0])


        if user_name in fetched_users:
            print("------")
        else:
            print("User not found")
            pp = int(input("Want to register? Press 1. Want to exit? Press2-->> "))
            if pp == 1:
                add_data()
                break
            elif pp == 2:
                verify_login()
                break
            else:
                print("Enter valid option")

        

        query = "SELECT password,user_name,email FROM users WHERE user_name ='"+user_name+"';"
        cur.execute(query)
        conn.commit()

        xx = cur.fetchall()

        



        for i in xx:
            fetched_pass = i[0]
        hashed_pass = create_hash(password)
        

        if fetched_pass == hashed_pass:
            print("verified")
            print("--------------------------------")
            print("--------------------------------")
            break
        
        else:
            cc = int(input("Wrong Pass! Press 1 to retry. Press 2 to reset your pass-->> "))
            if cc == 1:
                continue
            elif cc == 2:
                forgot_pass()
        break






def main():
    xx = int(input('''Press 1 to register,
Press 2 to login
-->> '''))
    if xx == 1:
        add_data()
    elif xx == 2:
        verify_login()
    else:
        print("Enter valid")





# main()
forgot_pass()
# verify_login()  
# add_data()




