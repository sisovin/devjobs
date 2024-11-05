import streamlit as st
import streamlit.components.v1 as stc
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "http://localhost:3500/results"

# Set page configuration
st.set_page_config("Search Dev Jobs App")

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize the Logger instance
logger = Logger(log_file=os.path.join(log_dir, 'logfile.log'), level=Logger.LEVEL_INFO)

# Function to Retrieve Data
def get_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        logger.info(f"Response Status Code: {response.status_code}")
        return response.json()
    except ConnectionError:
        logger.error("Connection error occurred.")
        st.error("Connection error occurred. Please check your internet connection.")
    except Timeout:
        logger.error("Request timed out.")
        st.error("Request timed out. Please try again later.")
    except RequestException as e:
        logger.error(f"An error occurred: {e}")
        st.error(f"An error occurred: {e}")
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON response.")
        st.error("Failed to decode JSON response.")

# Function to Filter Data
def filter_data(data, search_term, location):
    filtered_data = []
    for job in data:
        title = job.get('title', '').lower()
        job_location = job.get('location', '').lower()
        logger.info(f"Checking job: {title} in {job_location}")
        if search_term.lower() in title and location.lower() in job_location:
            filtered_data.append(job)
    return filtered_data

JOB_HTML_TEMPLATE = """
<div style="width:100%;height:100%; margin:1px; padding:5px;position:relative;border-radius:5px;border:1px solid;box-shadow:0 0 1px #eee; background-color: #31333F;border-left: 5px solid #6c6c6c; color:white;">
<br/>
<h3>{title}</h3>
<h4>{company}</h4>
<h5>{location}</h5>
<h6>{datePosted}</h6>
</div>
"""
JOB_DESC_HTML_TEMPLATE = """
<div style="color:#fff">
{description}
</div>
"""
JOB_HOWTOAPPLY_HTML_TEMPLATE = """
<div style="color:#fff">
{how_to_apply}
</div>
"""

def main():
    st.sidebar.title("Menu:")
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)        
    
    st.title("Niewin: Search Dev Jobs")
    st.markdown("<hr style='border: solid 1px;'>", unsafe_allow_html=True)  # Add a solid line
        
    if choice == "Home":
        st.subheader("Home")
        # Nav Search Form
        with st.form(key='searchform'):
            nav1, nav2, nav3 = st.columns([3,2,1])
            
            with nav1:
                search_term = st.text_input("Search Job")
            with nav2:              
                location = st.text_input("Location")
            with nav3:
                st.text("Search")
                submit_search = st.form_submit_button(label='Search')
              
        st.success("You searched for {} in {}".format(search_term, location))
        logger.info("You searched for {} in {}".format(search_term, location))  
        
        # Results
        col1, col2 = st.columns([2,1])
        
        with col1:
            if submit_search:
              # Fetch all data
              data = get_data(base_url)
              if data:
                  logger.info(f"API Response: {json.dumps(data, indent=4)}")  # Log the entire API response
                  num_of_results = len(data)
                  st.subheader("Showing: {} jobs".format(num_of_results))
                  # Filter data based on search term and location
                  filtered_data = filter_data(data, search_term, location)
                  if filtered_data:
                      for i in filtered_data:
                          job_howtoapply = i.get('application_url', 'No application URL provided')                                                                               
                          st.markdown(JOB_HTML_TEMPLATE.format(
                            title=i['title'],
                            company=i['company'].get('name'),
                            location=i['location'],
                            datePosted=i['published'],                              
                          ), unsafe_allow_html=True)
                          # Description
                          with st.expander("Description"):
                              stc.html(JOB_DESC_HTML_TEMPLATE.format(description=i['description']), scrolling=True)
                          
                          # How to Apply
                          with st.expander("How To Apply"):
                              stc.html(JOB_HOWTOAPPLY_HTML_TEMPLATE.format(how_to_apply=job_howtoapply), scrolling=True)
                          
                      logger.info(f"Filtered Search Results: {json.dumps(filtered_data, indent=4)}")
                  else:
                      st.write("No matching jobs found.")
                      logger.info("No matching jobs found.")
              else:
                  st.write("No data returned from the API.")
                  logger.info("No data returned from the API.")    
        with col2:
          with st.form(key='email_form'):
            st.write("Be the first to get new jobs information")
            email = st.text_input("Enter your email")
              
            submit_email = st.form_submit_button(label='Subscribe')
            
            if submit_email:
              st.success("A message was sent to {}".format(email))
              logger.info("A message was sent to {}".format(email))
                         
        
    else:
        st.subheader("About")
    
if __name__ == '__main__':
    main()