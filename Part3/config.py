########################################
######## GANGA CHALLENGE PART 3 ########
########################################

# Imports
import os

#--------------------------------------#

class Config(object):
    """ Contains configuration related to Flask """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "f3aa26f8b537acf6ee6305aafea0a10a"

#--------------------------------------#