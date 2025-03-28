# Web App (Localhost) Implementation

I tried hosting the website through github, but since it allows only only static websites, I couldn't do it. But Follow the steps below to run it on your localhost as a decent web app.

## Downloading prerequisites

Markovify, Flask and Requests Python module must be present in the system for proper execution of the Web Application. To download them on Kali Linux, follow these steps:

1. Activate virtual environment
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Download **Markovify** Python Module
   ```
   pip install markovify
   pip install flask
   pip install requests
   ```


## Downloading the Web App files

1. Clone into the **PassFort** repo using the command:
   ```
   git clone --depth 1 --filter=blob:none --sparse https://github.com/4n4gh4/PassFort.git
   ```

2. Move to **PassFort** directory and checkout only the **Web App** folder
   ```
   cd PassFort
   git sparse-checkout set "Web App"
   ```

3. Move to **'Web App'** and run **app.py**
   ```
   cd 'Web App'
   python app.py
   ```
