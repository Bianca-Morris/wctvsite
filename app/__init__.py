from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

#configurations for the mail server, port, etc. are stored in either config.py or config.cfg)
app.config.from_object('config') #update this with your own api keys, etc.
app.config.from_pyfile('config.cfg', silent=True) #instance/config.cfg not included in version control

db = SQLAlchemy(app) #initializes database

from app import apis, views, models, scheduler

ADMINS = ["wellesleycollege.boobtube@gmail.com, bmorris@wellesley.edu"] #add email addresses of people to recieve emails if/when app produces an exception, so that they can troubleshoot it

#initializes & configures error log handlers	
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler, SMTPHandler
	from logging import getLogger, Formatter
	
	#Extends SMTPHandler so that it can use TLS and Gmail will work
	#Code is from: https://mail.python.org/pipermail/python-list/2009-December/560415.html
	"""
	class TlsSMTPHandler(logging.handlers.SMTPHandler):
		def emit(self, record):
	"""
	"""
			Emit a record.

			Format the record and send it to the specified addressees.
	"""
	"""
			try:
				import smtplib
				import string # for tls add this line
				try:
					from email.utils import formatdate
				except ImportError:
					formatdate = self.date_time
				port = self.mailport
				if not port:
					port = smtplib.SMTP_PORT
				smtp = smtplib.SMTP(self.mailhost, port)
				msg = self.format(record)
				if self.username:
					smtp.ehlo() # for tls add this line
					smtp.starttls() # for tls add this line
					smtp.ehlo() # for tls add this line
					smtp.login(self.username, self.password)
				smtp.sendmail(self.fromaddr, self.toaddrs, msg)
				smtp.quit()
			except (KeyboardInterrupt, SystemExit):
				raise
			except:
				self.handleError(record)
	"""		
	#creates a handler to log errors to file
	logHandler = RotatingFileHandler('info.log')
	logHandler.setLevel(logging.WARNING) #logs any warnings or errors
	
	"""
	#creates a handler to send email with error logs to admins
	mailHandler = TlsSMTPHandler(
		mailhost = (app.config.get('MAIL_SERVER'), app.config.get('MAIL_PORT')),
		fromaddr = 'Bug Reporter at wellesleycollege.boobtube@gmail.com', 
		toaddrs = ADMINS, 
		subject = 'URGENT: WCTV Site Exception! Troubleshoot ASAP',
		credentials = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD')))
	mailHandler.setLevel(logging.ERROR) #only sends emails for errors, not warnings or info
	
	def mail_formatter(handler):
	"""
	"""Formats the email to be sent by the mailHandler in the event of an error."""
	"""	
		handler.setFormatter(Formatter('''
		Message type:       %(levelname)s
		Location:           %(pathname)s:%(lineno)d
		Module:             %(module)s
		Function:           %(funcName)s
		Time:               %(asctime)s

		Message:

		%(message)s
		'''))
	"""
	
	def log_formatter(handler):
		"""Formats the log entry that will be stored in info.log"""
		handler.setFormatter(Formatter(
		'%(asctime)s %(levelname)s: %(message)s '
		'[in %(pathname)s:%(lineno)d]'
		))	
	
	#adds handlers for the Flask app itself and sqlalchemy database and formats them
	for logger in [app.logger, getLogger('sqlalchemy'), getLogger('werkzeug')]:
		#logger.addHandler(mailHandler)
		logger.addHandler(logHandler)
		#mail_formatter(mailHandler)
		log_formatter(logHandler)

#schedules daily update of the google api
scheduler.google_api_updater()
scheduler.sched.start() #starts the timer to call the apis periodically, and update their databases