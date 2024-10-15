
import streamlit as st
import json
from streamlit_lottie import st_lottie
import sqlite3
import pandas as pd

# Function to create a SQLite database and a table
def create_db():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            job_link TEXT,
            company TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def check_job(email,job_link):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('SELECT job_link FROM jobs WHERE email = ?', (email,))
    job_links = c.fetchall()
    conn.commit()
    conn.close()
    job_list = list(map(lambda x: x[0], job_links))
    if job_link in job_list:
        return False
    return True
# Function to add a new job to the database
def add_job(email, job_link, company, status):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO jobs (email, job_link, company, status) VALUES (?, ?, ?, ?)
    ''', (email, job_link, company, status))
    conn.commit()
    conn.close()

# Function to update the status of a job in the database
def update_status(email, application_id, status):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''UPDATE jobs SET status = ? WHERE email = ? AND application_id = ?''', (status, email, application_id))
    conn.commit()
    conn.close()

# Function to retrieve all jobs from the database
def get_jobs(email):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('SELECT application_id, job_link, company, status FROM jobs WHERE email = ?', (email,))
    jobs = c.fetchall()
    conn.close()
    return jobs

# Function to display the form to add a new job
def add_job_form():
    st.markdown("<h3 style='text-align: center;'>Add a New Job</h3>", unsafe_allow_html=True)
    with st.form(key='add_job'):
        job_link = st.text_input("Job Link")
        company = st.text_input("Company")
        status = st.selectbox("Status", ["applied", "testlink_received", "interviewed", "offered", "rejected", "accepted"])
        submit_button = st.form_submit_button(label='Save')
        if submit_button:
            if check_job(st.session_state['user'],job_link):
                add_job(st.session_state['user'], job_link, company, status)
                st.success("Job added successfully!")
                st.rerun()
            else:
                st.info("You have already applied for this job") 

# Function to display the form to update a job's status
def update_status_form():
    st.markdown("<h3 style='text-align: center;'>Update Job Status</h3>", unsafe_allow_html=True)
    with st.form(key='update_status'):
        application_id = st.number_input("Application ID", min_value=1, step=1)
        status = st.selectbox("New Status", ["applied", "testlink_received", "interviewed", "offered", "rejected", "accepted"])
        submit_button = st.form_submit_button(label='Update')
        if submit_button:
            update_status(st.session_state['user'], application_id, status)
            st.success("Job status updated successfully!")
            st.rerun()

# Main app function
def main():
    st.write("<h1><center>Application Tracker</center></h1>", unsafe_allow_html=True)
    st.write("<center>Organize, Track, and Succeed</center>", unsafe_allow_html=True)
    with open('src/job_tracker.json', encoding='utf-8') as anim_source:
        animation = json.load(anim_source)
    st_lottie(animation, height=200, key="job_tracker_anim")

    if 'is_logged' not in st.session_state:
        st.session_state['is_logged'] = False

    if st.session_state['is_logged']:
        create_db()

        # Display existing jobs in a table
        st.markdown("<h3 style='text-align: center;'>Job Listings</h3>", unsafe_allow_html=True)
        jobs = get_jobs(st.session_state['user'])
        df = pd.DataFrame(jobs, columns=["Unique Application ID", "Job Link", "Company", "Status"])
        st.dataframe(df, width=1500,hide_index=True)

        add_job_form()
        update_status_form()

        if st.button("Logout"):
            st.session_state['is_logged'] = False
            del st.session_state['user']
            st.rerun()
    else:
        st.markdown("<h3 style='text-align: center; color: red;'>You are not Logged In</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
