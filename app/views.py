from flask import render_template, request
from app import app, apis, db, models
from .forms import ContactForm
from flask_mail import Mail, Message

@app.context_processor
def api_processor():
	"""Creates a forecast dictionary that is accessible from all pages."""
	#Needs testing; may need to be updated with a scheduler so that it updates itself every few minutes...
	forecast = apis.getWeather()
	return dict(forecast=forecast)

@app.route('/')
@app.route('/index')
def index():
	"""Retrieves video data from the sqlite database, processes it, and passes it to the template."""
	#queries database for data on last 5 videos
	last_five_q = models.Video.query.order_by('id').limit(5) #Retrieves the last 5 entries in the database
	video_bank = []
	for vid in last_five_q:
		video_data = [] 
		#splits title into two parts: the title and the Season/Episode number (NOTE: VIDEO TITLES MUST BE FORMATTED THIS WAY OR ELSE ERRORS WILL HAPPEN; I haven't yet written handlers for those, so they will crash all of the things.)
		updated_title = vid.title.split('[')
		video_data.append(updated_title[0])
		video_data.append(vid.description)
		video_data.append(vid.thumbnail_url)
		video_data.append(vid.videoid)
		video_data.append(vid.published.strftime("%B, %A %d, %Y"))
		video_data.append('[' + updated_title[1])
		video_data.append(vid.published.strftime("%m.%d.%Y"))
		video_bank.append(video_data)
	video_bank.reverse() #Reverses the videos in the data bank, so that they show up in the right order on the page; I'm sure there's a better way to do this using jinja2... will look into it.
	return render_template("index.html", 
							title="WCTV - Home",
							videos = video_bank)

@app.route('/about')
def about():
	"""Renders the About US page of the WCTV website, using base.html as a base and about.html for the content."""
	return render_template("about.html", 
							title="WCTV - About Us")

@app.route('/castcrew')
def castcrew():
	"""Renders the Cast & Crew page of the WCTV website, using base.html as a base and castcrew.html for the content."""
	return render_template("castcrew.html", 
							title="WCTV - Cast & Crew")

mail = Mail(app)	#Initializes mail for the contact page

@app.route('/contact', methods=["GET","POST"])
def contact():
	"""Renders the appropriate form, handles validation errors, and processes the messages so that they can be emailed to the appropriate WCTV member."""
	#initializes an instance of the contact form
	form = ContactForm()
	
	#If the user is submitting data to the server through the form, and it all validates properly (includes the right amount of characters, is formatted in 'name@provider.com' format, etc.)
	if request.method == "POST" and form.validate():
	
		#Sets up the email message, sends it off, and returns the success page.
		msg = Message(("RE: WCTV Website Visitor, " + form.name.data), 
						sender = "wellesleycollege.boobtube@gmail.com", #account mail is sent from
						recipients = ["bmorris@wellesley.edu"]) #list of admins notified on submission
		msg.body = form.message.data
		mail.send(msg)
		return render_template("contact.html", title="WCTV - Form Sent!", success=True)	
	
	#If the user attempts to submit data that doesn't validate,
	elif request.method == "POST" and not form.validate():
		#Re-renders the template, which will now be updated with appropriate error messages
		return render_template('contact.html', title="WCTV - Contact Us", form=form)
	
	#If the user attempts to retrieve data form the website (usually upon first load of the page), renders the form
	elif request.method == "GET":
		return render_template('contact.html', title="WCTV - Contact Us", form=form)

@app.route('/terms') 
def terms():
	"""Renders the Terms & Privacy Policy page of the WCTV website, using base.html as a base and terms.html for the content."""
	return render_template('terms.html', title="WCTV - Terms of Service & Privacy Policy")

@app.errorhandler(500)
@app.errorhandler(503)
@app.errorhandler(504)
@app.errorhandler(Exception)
def exception_handler(e):
	"""Renders a custom error page in the case of a Flask exception or common server-side error. Ensures Flask exception pages (and their useful info!) still show up while in debugging mode."""
	
	if app.debug == False: #allows error pages to show up on debug mode
		app.logger.error('Server Error: %s', (e))
		return render_template('exception.html', title="WCTV - Something went wrong...")

@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(403)
def error_handler(e):
	"""Renders a custom error page in the case of common client-side errors. Allows default error pages to show up while in debugging mode."""
	if app.debug == False:
		app.logger.error('Client Error: %s', (e))
		return render_template('exception.html', title="WCTV - Oh noes!", error=True)
		
@app.route('/error')
def error():
	#Generates a server error for the purpose of testing out the logs. Remove this or comment out when in production.
	return 1/0