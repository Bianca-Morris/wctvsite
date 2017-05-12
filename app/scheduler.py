from apscheduler.schedulers.background import BackgroundScheduler
from app import app, apis, db, models

sched = BackgroundScheduler()

#@sched.scheduled_job('interval', minutes=1) #for testing
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def google_api_updater():
	"""Runs in the background of the application, and calls the Youtube APIs once every weekday at 5 pm. This will update the video data in the database, allowing the videos to update on the homepage."""
	vid_data = apis.getVids() #retrieves video data [[videoId, title, description, py-datetime, thumb_url], [videoId, title, description, py-datetime, thumb_url], etc.]
	if not vid_data:
		#if the weather api can't be reached logs to console
		app.logger.warning("Youtube API could not be reached; using fallback data. Will attempt again tomorrow.")
	else:
		#updates the data in the database with the new data
		ordered_vids = vid_data[:] #copies list
		ordered_vids.reverse() #reverses list, so it starts with the oldest video
		for video in ordered_vids: 
			#determines whether or not the videodata is in the database already
			exists = db.session.query(db.exists().where(models.Video.videoid==video[0])).scalar()		
			if (exists):
				app.logger.info("Video entitled '"+ video[1] +"' already in database.")
			else:
			#if it doesn't exist in the database, adds it.
				vid_db_entry = models.Video(videoid=video[0],title=video[1],description=video[2],published=video[3],thumbnail_url=video[4])
				db.session.add(vid_db_entry)
				db.session.commit()
				app.logger.info("Video entitled '"+ video[1] +"' added to database.")
