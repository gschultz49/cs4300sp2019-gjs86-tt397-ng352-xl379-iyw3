import os

APP_ROOT = os.path.dirname(os.path.abspath( __file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

print ("SETTINGS")
print (APP_ROOT)
print (APP_STATIC)
