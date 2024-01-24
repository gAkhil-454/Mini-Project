import smtplib
import os
sender_email = "drstrange5940@gmail.com"
receiver_email = "scrapmail454@gmail.com"
password = input(str("Please enter your password: "))
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(sender_email, password)
print("login success")

# message to be sent
message = "Hammaya..mothaaaniki ochindi ra"

# sending the mail
s.sendmail(sender_email,receiver_email, message)
print("email has been sent to " , receiver_email)
# terminating the session
s.quit()