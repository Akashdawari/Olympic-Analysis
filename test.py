from datetime import datetime
import os
import logger


f= open("logs/test1.txt","w+")
obj = logger.App_Logger()

obj.log(f,"Fuck hard")