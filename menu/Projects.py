import streamlit as st
import requests
from bs4 import BeautifulSoup

def main():
    st.markdown("<h1 style='text-align: center; color: black;'>Projects</h1>", unsafe_allow_html=True)
    
    st.write("Get your project idea here:")
    
    # Create a dropdown box for project type selection
    project_types = ["Project", "Research Paper"]
    selected_project_type = st.selectbox("Select your project type:", project_types)
    
    if selected_project_type == "Project":
        # Create a dropdown box for domain selection
        domains = ["Electrical Engineering", "Software Engineering", "Mechanical Engineering", "Civil Engineering", "Computer Science", "Other"]
        selected_domain = st.selectbox("Select your domain:", domains)
        
        # Display project ideas based on the selected domain
        if selected_domain == "Electrical Engineering":
            project_ideas = [
                "Design a smart home automation system",
                "Develop a renewable energy harvesting system",
                "Create a wireless communication system for IoT devices",
                "Build a robotic arm for industrial automation"
            ]
        elif selected_domain == "Software Engineering":
            project_ideas = [
                "Develop a chatbot for customer service",
                "Create a mobile app for tracking personal expenses",
                "Design a web application for online learning",
                "Build a game using machine learning algorithms"
            ]
        elif selected_domain == "Mechanical Engineering":
            project_ideas = [
                "Design a 3D printed prosthetic limb",
                "Develop a sustainable transportation system",
                "Create a robotic system for search and rescue operations",
                "Build a wind turbine for renewable energy generation"
            ]
        elif selected_domain == "Civil Engineering":
            project_ideas = [
                "Design a sustainable building using green architecture",
                "Develop a water management system for urban areas",
                "Create a bridge design using advanced materials",
                "Build a smart traffic management system"
            ]
        elif selected_domain == "Computer Science":
            project_ideas = [
                "Develop a natural language processing system",
                "Create a computer vision system for object detection",
                "Design a cybersecurity system for network protection",
                "Build a recommender system for e-commerce"
            ]
        else:
            project_ideas = ["No project ideas available for this domain"]
        
        st.write("Project ideas for **" + selected_domain + "**:")
        for idea in project_ideas:
            st.write("- " + idea)
    else:
        st.write("Research paper ideas will be displayed here.")
        
        # Create a text box for user input
        user_input = st.text_input("Enter your research paper prompt:", placeholder="Type your research paper prompt here")
        
        if user_input:
            # Fetch details from Google Scholar and ACM Library
            scholar_url = "https://scholar.google.com/scholar?q=" + user_input.replace(" ", "+")
            
            st.write("### Research Papers:")
            response = requests.get(scholar_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('div', class_='gs_r')
            if results:
                for result in results:
                    title_element = result.find('h3', class_='gs_rt')
                    if title_element:
                        title = title_element.text
                        link = title_element.find('a')['href']
                        st.markdown(f"- **{title}** ([{link}])")
            else:
                st.write("No results found for this search.")

if __name__ == "__main__":
    main()