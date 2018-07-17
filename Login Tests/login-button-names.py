# Websites' button information is stored in a dictionary of dictionaries below.
# Following this format makes it easy for any user to modify which server they wish to test without looking at the login-test.py code

buttons = {} # dictionary name - do not change

# add a site you wish to test
careercenter-staff = {}
careercenter-staff["username_button"] = "logon"
careercenter-staff["password_button"] = "pass"
careercenter-staff["submit_button"] = "pass"
careercenter-staff["text_to_find"] = "Work-study Information"

# follow this format
careercenter-student = {}
careercenter-student["username_button"] = "SID"
careercenter-student["password_button"] = "birthdate"
careercenter-staff["submit_button"] = "birthdate"
careercenter-staff["text_to_find"] = ""

eop-admin = {}
eop-admin["username_button"] = "username"
eop-admin["password_button"] = "password"
eop-admin["submit_button"] = "signinform"
eop-admin["text_to_find"] = "System lockout options"

eop-msi = {}
eop-msi["username_button"] = "SID"
eop-msi["password_button"] = HAS THREE
eop-msi["submit_button"] = "Submit"
eop-msi["text_to_find"] = "Account Options"

eop-staff = {}
eop-staff["username_button"] = "username"
eop-staff["password_button"] = "password"
eop-staff"submit_button"] = "Submit"
eop-staff["text_to_find"] = "UCSC Learning Support Services On-line Tutor Signup System"

eop-student = {}
eop-student["username_button"] = "SID"
eop-student["password_button"] = HAS THREE
eop-student["submit_button"] = "signinform"
eop-student["text_to_find"] = "registration"

eop-tutor = {}
eop-tutor["username_button"] = "SID"
eop-tutor["password_button"] = HAS THREE
eop-tutor["submit_button"] = "LOGIN"
eop-tutor["text_to_find"] = "closed"

fixit = {}
fixit["username_button"] = "enteremail"
fixit["password_button"] = "enterpassword"
fixit["submit_button"] = "//img[@alt='Student']"
fixit["text_to_find"] = "Location of Problem"


# add your site dictionary to the overall "buttons" dictionary
buttons["careercenter-staff"] = careercenter-staff
buttons["careercenter-student"] = careercenter-student
buttons["eop-admin"] = eop-admin
buttons["eop-msi"] = eop-msi
buttons["eop-staff"] = eop-staff
buttons["eop-student"] = eop-student
buttons["eop-tutor"] = eop-tutor
buttons["fixit"] = fixit
