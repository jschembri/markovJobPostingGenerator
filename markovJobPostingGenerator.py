# -*- coding: utf-8 -*-


import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc

import readJobs
import markovgen
import codecs
import random

try:
    from settings import postgresPasswordLocal, SECRET_KEY 
    HEROKU = False
except ImportError:
    SECRET_KEY = os.environ['SECRET_KEY']
    HEROKU = True


SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True
TESTING = True
#HEROKU = True


#Create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
if HEROKU:
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
  app.config['SQLALCHEMY_DATABASE_URI'] =  postgresPasswordLocal

db = SQLAlchemy(app)



class JobSearches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobtitle = db.Column(db.String(200))
    searches = db.Column(db.Integer)
    def __init__(self, jobtitle):
        self.jobtitle = jobtitle
        self.searches = 1
    def __str__(self):
       return '<Job: %r>' % self.jobtitle
    def __repr__(self):
       return '<Job: %r>' % self.jobtitle
    def add_searches(self):
       self.searches += 1       


def addInDatabase(jobtitle):
  jobtitle = jobtitle.title()
  job = JobSearches.query.filter_by(jobtitle=jobtitle).first()
  if job is None:
    newJob = JobSearches(jobtitle)
    db.session.add(newJob)
    db.session.commit()
  else:
    job.add_searches()
    db.session.commit()





#
@app.route('/')
def show_entries():
   entries = []
   return render_template('funny_jobs.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
   #g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
   #g.db.commit()

   #spacedJobTitle = request.form['jobtitle']
   jobTitle = request.form['jobtitle'].title()
   #jobTitle = request.form['jobtitle'].replace(" ", "+")
   scraping = False
   try:
      newJob, jobtitleFilename, jobbulletFilename = readJobs.existingJob(jobTitle, scraping)
      if newJob:
         readJobs.mainReadJobs(jobTitle, jobtitleFilename, jobbulletFilename, 5)
      #creating the opening and closing 
      jobfile = codecs.open(jobtitleFilename, encoding='utf-8')
      markov = markovgen.Markov(jobfile)

      sentences = random.randint(2, 3)
      theOpening = markov.generate_markov_text(sentences)
      flash(theOpening,'theOpening' )

      sentences = random.randint(2, 3)
      theClosing = markov.generate_markov_text(sentences)
      flash(theClosing,'theClosing')

      if( os.path.isfile(jobbulletFilename) ):
         bulletHeader = [ 'Key Responsibilities', 'Duties', 'Key Duties and Responsibilities', 'Objectives', 'Qualifications', 'Main Responsibilities']
         flash(random.choice(bulletHeader),'bulletHeader')
         #creating in the bullet points
         file = codecs.open(jobbulletFilename, encoding='utf-8')
         markovBullets = markovgen.MarkovBullets(file)
      flash(jobTitle,'jobtitleMsg' )
      sentences = random.randint(5, 7)
      theBullets = markovBullets.generate_markov_text(sentences)
      flash(theBullets,'bullets' )
      addInDatabase(jobTitle)
   except:
      flash("There was an error in your request....Try Again",'error')  
   return redirect(url_for('show_entries'))

# Simple tracking to find out most common search  
@app.route('/top')
def show_top_jobs():
   #entries = JobSearches.query.limit(100).all().order_by(searches)
   entries = JobSearches.query.order_by(desc(JobSearches.searches)).limit(100)
   return render_template('topJobs.html', entries=entries)


if __name__ == '__main__':
   app.run()

