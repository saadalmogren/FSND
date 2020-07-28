


# Import the Python Library
import sys
get_ipython().system('{sys.executable} -m pip install bcrypt')
import bcrypt


# In[ ]:


password = b"studyhard"


# In[ ]:


# Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
hashed = bcrypt.hashpw(password, salt)
print(salt)
print(hashed)


# In[ ]:


# Check a plain text string against the salted, hashed digest
bcrypt.checkpw(password, hashed)


# In[ ]:




