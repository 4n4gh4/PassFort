# Web App (Localhost) Implementation

I tried hosting the website through github, but since it allows only only static websites, I couldn't do it. But Follow the steps below to run it on your localhost as a decent web app.

1. Clone into the **PassFort** repo using the command:
   `git clone --depth 1 --filter=blob:none --sparse https://github.com/4n4gh4/PassFort.git`

2. Move to **PassFort** directory and checkout only the **Web App** folder
   `cd PassFort`
   `git sparse-checkout set "Web App"`

3. Run the **app.py**

