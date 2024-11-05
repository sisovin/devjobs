# Dev Jobs Search App

This application allows users to search for developer jobs using a Streamlit interface. The app fetches job data from a local JSON server and displays the results based on the user's search criteria.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/devjobs.git
   cd devjobs
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv devjobs-env
   source devjobs-env/bin/activate  # On Windows use `devjobs-env\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the JSON server:

   ```sh
   npx json-server@latest -p 3500 -w data/jobs/positions.json
   ```

   This will start the JSON server on port 3500 and watch for changes in the `positions.json` file.

2. Run the Streamlit app:

   ```sh
   streamlit run streamlit_app.py
   ```

   This will start the Streamlit app, and you can access it in your browser at `http://localhost:8501`.

## Troubleshooting

### Network Issues

If you encounter network issues preventing the connection to the GitHub Jobs API, follow these steps:

1. **Check Network Connection**: Ensure that your internet connection is stable and working.
2. **Check API Endpoint**: Verify that the API endpoint `https://jobs.github.com/positions.json` is accessible from your browser or using a tool like `curl`.
3. **Handle Connection Errors in Code**: Add error handling in your code to manage connection errors gracefully.

### Common Errors

#### No such command 'streamlit_app.py'

Ensure you are using the correct command to run the Streamlit app:

```sh
streamlit run streamlit_app.py
```

#### Cannot load Streamlit frontend code

This can happen when you update Streamlit while a Streamlit app is running. To fix this, simply reload the app by pressing F5, Ctrl+R, or Cmd+R. If the error persists, try force-clearing your browser's cache.

## Code Overview

### Streamlit App

The main Streamlit app is defined in 

streamlit_app.py

. It includes functions to retrieve and filter job data, and display the results in a user-friendly format.

### Error Handling

The `get_data` function includes error handling for connection errors, timeouts, and other request exceptions. It logs the errors and displays appropriate messages to the user.

### Example Code

Here's an example of how the `get_data` function handles errors:

```python
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
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```

This `README.md` provides a comprehensive guide to setting up and running the Dev Jobs Search App, along with troubleshooting tips and an overview of the code.This `README.md` provides a comprehensive guide to setting up and running the Dev Jobs Search App, along with troubleshooting tips and an overview of the code.

Here's how you can modify your [`get_data`] function to handle connection errors:

```python
import streamlit as st
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "https://jobs.github.com/positions.json?description={}&location={}"

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

def main():
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
                # Create search query
                search_url = base_url.format(search_term, location)
                # st.write(search_url)
                data = get_data(search_url)
                if data:
                    st.write(data)
                    logger.info(f"Search Results: {data}")
        
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()
```

This code adds error handling for connection errors, timeouts, and other request exceptions. It logs the errors and displays appropriate messages to the user.

Network issue:
Cannot load Streamlit frontend code. This can happen when you update Streamlit while a Streamlit app is running.
To fix this, simply reload this app by pressing F5, Ctrl+R, or Cmd+R.
If the error persists, try force-clearing your browser's cache as described here

The issue lies in the [`if __name__ == '__name__':`] statement. It should be [`if __name__ == '__main__':`]. This is a common mistake and prevents the [`main()`] function from being executed when the script is run.

Here's the corrected code:

```python
import streamlit as st
import requests

def main():
    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    st.title("Niewin: Search Dev Jobs")
    
    if choice == "Home":
        st.subheader("Home")
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()
```

The log entries indicate that the search for "software engineer" in "new york" returned no matching jobs, while the search for "software engineer" in "san francisco" returned a matching job. This suggests that the filtering logic is working correctly, but there are no jobs matching the search criteria for "new york".

To ensure that the filtering logic is robust and to provide better feedback to the user, let's add some additional logging and display messages to help debug and understand the results.

Here's the updated code with enhanced logging and user feedback:

```python
import streamlit as st
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "http://localhost:3500/jobs"

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
        if search_term.lower() in job['title'].lower() and location.lower() in job['location'].lower():
            filtered_data.append(job)
    return filtered_data

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
                    logger.info(f"Total jobs fetched: {len(data)}")
                    # Filter data based on search term and location
                    filtered_data = filter_data(data, search_term, location)
                    if filtered_data:
                        st.write("Filtered Data:", filtered_data)  # Display filtered data
                        st.write(json.dumps(filtered_data, indent=4))
                        logger.info(f"Filtered Search Results: {json.dumps(filtered_data, indent=4)}")
                    else:
                        st.write("No matching jobs found.")
                        logger.info("No matching jobs found.")
                else:
                    st.write("No data returned from the API.")
                    logger.info("No data returned from the API.")
        
    else:
        st.subheader("About")
    
if __name__ == '__main__':
    main()
```

In this updated code:

1. **Enhanced Logging**: Added logging to display the total number of jobs fetched from the API.
2. **User Feedback**: Added messages to inform the user if no matching jobs are found or if no data is returned from the API.

This should help you better understand the results and provide more informative feedback to the user. If there are no jobs matching the search criteria for "new york", it will be clearly indicated in the logs and the user interface.

The `KeyError: 'how_to_apply'` indicates that the key `'how_to_apply'` does not exist in one of the job dictionaries. To handle this gracefully, you can use the `get` method of dictionaries, which returns `None` (or a default value) if the key is not found.

Here's how you can update the code to handle this:

```python
job_howtoapply = i.get('how_to_apply', 'No application instructions provided')
```

This will set [`job_howtoapply`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fd%3A%2FlearnPython%2Fdevjobs%2Fstreamlit_app.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A109%2C%22character%22%3A22%7D%7D%5D%2C%222289532e-29a7-41d1-bd09-5991e008fed8%22%5D "Go to definition") to `'No application instructions provided'` if the key `'how_to_apply'` is not found in the dictionary.

Here's the updated context of your code:

```python
import streamlit as st
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "http://localhost:3500/jobs"

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
        if search_term.lower() in job['title'].lower() and location.lower() in job['location'].lower():
            filtered_data.append(job)
    return filtered_data

JOB_HTML_TEMPLATE = """
<div>

</div>
<h2>{title}</h2>
<h4>{company}</h4>
<p><strong>Location:</strong> {location}</p>
<p><strong>Date Posted:</strong> {datePosted}</p>
<p><strong>Description:</strong> {description}</p>
<p><strong>How to Apply:</strong> {how_to_apply}</p>
<a href="{company_url}" target="_blank">Company Website</a>
<hr>
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
                st.text("Search ")
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
                    logger.info(f"Total jobs fetched: {len(data)}")
                    # Filter data based on search term and location
                    filtered_data = filter_data(data, search_term, location)
                    if filtered_data:
                        for i in filtered_data:
                            job_howtoapply = i.get('how_to_apply', 'No application instructions provided')
                            st.write(JOB_HTML_TEMPLATE.format(
                                title=i['title'],
                                company=i['company'],
                                location=i['location'],
                                datePosted=i['datePosted'],
                                description=i['description'],
                                how_to_apply=job_howtoapply,
                                company_url=i['company_url']
                            ), unsafe_allow_html=True)
                        logger.info(f"Filtered Search Results: {json.dumps(filtered_data, indent=4)}")
                    else:
                        st.write("No matching jobs found.")
                        logger.info("No matching jobs found.")
                else:
                    st.write("No data returned from the API.")
                    logger.info("No data returned from the API.")
        
    else:
        st.subheader("About")
    
if __name__ == '__main__':
    main()
```

This update ensures that the code handles the case where the `'how_to_apply'` key is missing in the job dictionary, preventing the `KeyError` and providing a default message instead.

The log entries indicate that the search for "software engineer" in "new york" returned no matching jobs, while the search for "software engineer" in "san francisco" returned a matching job. This suggests that the filtering logic is working correctly, but there are no jobs matching the search criteria for "new york".

To ensure that the filtering logic is robust and to provide better feedback to the user, let's add some additional logging and display messages to help debug and understand the results.

Here's the updated code with enhanced logging and user feedback:

```python
import streamlit as st
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "http://localhost:3500/jobs"

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
        if search_term.lower() in job['title'].lower() and location.lower() in job['location'].lower():
            filtered_data.append(job)
    return filtered_data

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
                    logger.info(f"Total jobs fetched: {len(data)}")
                    # Filter data based on search term and location
                    filtered_data = filter_data(data, search_term, location)
                    if filtered_data:
                        st.write("Filtered Data:", filtered_data)  # Display filtered data
                        st.write(json.dumps(filtered_data, indent=4))
                        logger.info(f"Filtered Search Results: {json.dumps(filtered_data, indent=4)}")
                    else:
                        st.write("No matching jobs found.")
                        logger.info("No matching jobs found.")
                else:
                    st.write("No data returned from the API.")
                    logger.info("No data returned from the API.")
        
    else:
        st.subheader("About")
    
if __name__ == '__main__':
    main()
```

In this updated code:

1. **Enhanced Logging**: Added logging to display the total number of jobs fetched from the API.
2. **User Feedback**: Added messages to inform the user if no matching jobs are found or if no data is returned from the API.

This should help you better understand the results and provide more informative feedback to the user. If there are no jobs matching the search criteria for "new york", it will be clearly indicated in the logs and the user interface.

```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Software Engineer",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "San Francisco, CA",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["JavaScript", "React", "Node.js", "MongoDB"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 2,
      "title": "Product Manager",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "New York, NY",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Product Management", "Agile", "Scrum", "Jira"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 3,
      "title": "Data Scientist",
      "description": "We are looking for a data scientist to join our team.",
      "location": "Seattle, WA",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Python", "Machine Learning", "Data Analysis", "SQL"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 4,
      "title": "UX Designer",
      "description": "We are looking for a UX designer to join our team.",
      "location": "Austin, TX",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["UX Design", "Wireframing", "Prototyping", "Figma"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 5,
      "title": "DevOps Engineer",
      "description": "We are looking for a DevOps engineer to join our team.",
      "location": "Boston, MA",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["AWS", "Docker", "Kubernetes", "CI/CD"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 6,
      "title": "QA Engineer",
      "description": "We are looking for a QA engineer to join our team.",
      "location": "Denver, CO",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Testing", "Automation", "Selenium", "Jenkins"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 7,
      "title": "Backend Developer",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "Chicago, IL",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Java", "Spring Boot", "Microservices", "SQL"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 8,
      "title": "Frontend Developer",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "Los Angeles, CA",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["HTML", "CSS", "JavaScript", "Vue.js"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 9,
      "title": "Mobile Developer",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "Miami, FL",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Swift", "iOS", "Android", "React Native"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 10,
      "title": "Cloud Architect",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "San Diego, CA",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Azure", "Cloud Computing", "Infrastructure", "Networking"],
      "datePosted": "2021-01-01"
    },
    {
      "id": 11,
      "title": "Security Analyst",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "Houston, TX",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": [
        "Cybersecurity",
        "Risk Assessment",
        "Penetration Testing",
        "SIEM"
      ],
      "datePosted": "2021-01-01"
    },
    {
      "id": 12,
      "title": "System Administrator",
      "description": "We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.We are looking for a mobile developer to join our team.",
      "location": "Phoenix, AZ",
      "company": "Microsoft Inc",
      "company_url": "https://www.microsoft.com",
      "type": "Full-time",
      "experience": "Mid-level",
      "skills": ["Linux", "Windows Server", "Networking", "Scripting"],
      "datePosted": "2021-01-01"
    }
  ]
}



```
import streamlit as st
import streamlit.components.v1 as stc
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
from functions.logger import Logger
import json

base_url = "http://localhost:3500/jobs"

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
        if search_term.lower() in job['title'].lower() and location.lower() in job['location'].lower():
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
                st.text("Search ")
                submit_search = st.form_submit_button(label='Search')
              
        st.success("You searched for {} in {}".format(search_term, location))
        logger.info("You searched for {} in {}".format(search_term, location))  
        
        # Results
        col1, col2 = st.columns([2,1])
        
        with col1:
            if submit_search:
                # Fetch all data
                search_url = base_url.format(search_term, location)
                data = get_data(search_url)
                if data:
                    num_of_results = len(data)
                    logger.info(f"Total jobs fetched: {len(data)}")
                    # Filter data based on search term and location
                    st.subheader("Showing: {} jobs".format(num_of_results))
                    
                    # for i in data:
                    #  job_title = i['title'],
                    #  job_location = i['location'],
                    #  company = i['company'],
                    #  company_url = i['company_url'],
                    #  job_post_date = i['datePosted'],
                    #  job_desc = i['description'],
                    #  job_howtoapply = i.get('how_to_apply', 'No application instructions provided')
                    #  st.markdown(JOB_HTML_TEMPLATE.format(
                    #    title=job_title, 
                    #    location=job_location, 
                    #    company=company, 
                    #    company_url=company_url, 
                    #    datePosted=job_post_date, 
                    #    description=job_desc, 
                    #    how_to_apply=job_howtoapply), unsafe_allow_html=True)
                    # Filter data based on search term and location
                    filtered_data = filter_data(data, search_term, location)
                    if filtered_data:
                        for i in filtered_data:
                            job_howtoapply = i.get('how_to_apply', 'No application instructions provided')
                                                        
                            
                            company_url=i['company_url']
                            st.markdown(JOB_HTML_TEMPLATE.format(
                              title=i['title'],
                              company=i['company'],
                              location=i['location'],
                              datePosted=i['datePosted'],                              
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
                    
                    
        
    else:
        st.subheader("About")
    
if __name__ == '__main__':
    main()

### Conclusion

The Dev Jobs Search App provides a user-friendly interface for searching developer jobs using Streamlit. By following the installation and running instructions, you can quickly set up the application and start searching for jobs based on your criteria. The app includes robust error handling to manage network issues and other exceptions gracefully, ensuring a smooth user experience. With the ability to filter job data and display detailed job descriptions and application instructions, this app is a valuable tool for job seekers in the tech industry.
