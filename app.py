import streamlit as st
import requests


base_url = "https://jobs-predictions-api.p.rapidapi.com/jobs"

headers = {
	"X-RapidAPI-Key": "49e1a98ebfmshfad1b4f9f826aa0p14e4fdjsn1a0d78504b10",
	"X-RapidAPI-Host": "jobs-predictions-api.p.rapidapi.com"
}

response = requests.request("GET", base_url, headers=headers)

def get_data(url):
    resp = requests.get(url)
    return resp.json

def main():
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    st.title("DevDeeds -Search Jobs")
    
    if choice == "Home":
        st.subheader("Home")
        
        with st.form(key='searchform'):
            nav1,nav2,nav3 = st.columns([3,2,1])
            
            with nav1:
                search_term = st.text_input("Search Job")
            
            with nav2:
                location = st.text_input("Location")
            
            with nav3:
                st.text("Search ")
                submit_search = st.form_submit_button(label="Search")
        st.success("You searched for {} in {}".format(search_term,location))
        
        col1, col2 = st.columns([2,1])
        
        with col1:
            if submit_search:
                search_url = base_url.format(search_term, location)
                #st.write(search_url)
                data = get_data(search_url)
                st.write(data)
    
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()
