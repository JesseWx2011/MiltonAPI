from ftplib import FTP
import os

host = os.environ.get('FTP_SERVER')
user = os.environ.get('FTP_USERNAME')
code = os.environ.get('FTP_PASSWORD')

file = open("./radar_anim.gif", "rb")

ftp = FTP(host)
ftp.connect(host)
ftp.login(user, code)
ftp.cwd("./images/")
ftp.storbinary('STOR radar_anim.gif', file)
print("Uploading radar images")

ftp.quit()
ftp.close()
