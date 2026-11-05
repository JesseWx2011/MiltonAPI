from ftplib import FTP
import os

host = os.environ.get('FTP_SERVER')
user = os.environ.get('FTP_USERNAME')
code = os.environ.get('FTP_PASSWORD')

file = open("./radar_anim.gif", "rb")

if not all([host, user, code]):
  raise ValueError("Uh oh! Looks like one of the variables is either missing, or a typo was made in one of them.")

ftp = FTP(host)
ftp.connect(host)
ftp.login(user, code)
ftp.cwd("./images/")
ftp.storbinary('STOR radar_anim.gif', file)
print("Uploading radar images")

ftp.quit()
ftp.close()
