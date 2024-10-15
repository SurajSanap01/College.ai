import streamlit as st
import sqlite3
from streamlit_authenticator.utilities.hasher import Hasher
import bcrypt
import re

salt = bcrypt.gensalt(rounds=12)

user_conn = sqlite3.connect('users.db',check_same_thread=False)
user_cursor = user_conn.cursor()
user_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT
    )
''')
user_conn.commit()


if 'is_logged' not in st.session_state: 
    st.session_state['is_logged'] = False

def main():
    st.write("<h1><center>Account</center></h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "SignUp"])

    def get_user_emails():
        user_cursor.execute('SELECT email FROM users')
        email_list=[]
        em=user_cursor.fetchall()
        for row in em:
            email_list.append(row[0])
        user_conn.commit()
        return email_list
    
    


    def login():
        with st.form(key='login', clear_on_submit=True):
            st.subheader(':green[Login]')
            email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
            password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            btn1, bt2, btn3, btn4, btn5 = st.columns(5)
            btn3=st.form_submit_button('Login')
            
            if btn3:
                email_lst=get_user_emails()
                if email in email_lst:
                    user_cursor.execute('SELECT email,password FROM users WHERE email=?',(email,))
                    records = user_cursor.fetchall()
                    # print("Printing ID ", records)
                    saved_pass=eval(records[0][1])
                    password=str.encode(password1)
                    if bcrypt.checkpw(password, saved_pass):
                        st.success("Logged In")
                        st.session_state['is_logged'] = True
                        st.session_state['user']=email
                    else:
                        st.warning("Wrong Password")                
                    
                else:
                    st.warning('Email is not correct')

    def sign_up():
        user_conn = sqlite3.connect('users.db')
        user_cursor = user_conn.cursor()
        user_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')
        user_conn.commit()

        def validate_email(email):
            """
            Check Email Validity
            :param email:
            :return True if email is valid else False:
            """
            pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$" #tesQQ12@gmail.com

            if re.match(pattern, email):
                return True
            return False

        

        with st.form(key='signup', clear_on_submit=True):
            st.subheader(':green[Sign Up]')
            email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
            password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
            password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
            btn1, bt2, btn3, btn4, btn5 = st.columns(5)
            btn3=st.form_submit_button('Sign Up')
            if btn3:
                if email:
                    if validate_email(email):
                        if email not in get_user_emails():
                            if len(password1) >= 6:
                                if password1 == password2:
                                    # Add User to DB
                                    password=str.encode(password2)
                                    hashed_password = bcrypt.hashpw(password, salt)

                                    user_cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, str(hashed_password)))
                                    user_conn.commit()
                                    get_user_emails()
                                    st.success('Account created successfully!! Great Now You Can login with registered email')
                                    return True
                                else:
                                    st.warning('Passwords Do Not Match')
                            else:
                                st.warning('Password is too Short')
                        else:
                            st.warning('Email Already exists!!')
                    else:
                        st.warning('Invalid Email')

    with tab1:
        login()
    with tab2:
        sign_up()
if __name__=="__main__":
    main()


