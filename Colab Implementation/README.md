# PassFort Colab Implementation

## Pre Requisites

The `markovify` model is being used, so that has to be installed, along with `rockyou.txt`. To satisfy the prerequisites, run the following in colab before `code.py`: 

```
!pip install markovify
!wget https://github.com/danielmiessler/SecLists/raw/master/Passwords/Leaked-Databases/rockyou.txt.tar.gz
!tar -xvzf rockyou.txt.tar.gz
!mv rockyou.txt /content/
!ls /content/
```

Now, <b>PassFort</b> will work with [code.py](code.py) 
