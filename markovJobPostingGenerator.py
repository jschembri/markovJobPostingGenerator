# -*- coding: utf-8 -*-


import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.sqlalchemy import SQLAlchemy

import readJobs
import markovgen
import codecs
import random

try:
    from settings import postgresPasswordLocal, SECRET_KEY 
except ImportError:
    SECRET_KEY = os.environ['SECRET_KEY']


SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True
TESTING = True
HEROKU = True


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
    def __init__(self, jobtitle):
        self.jobtitle = jobtitle
    def __repr__(self):
        return '<Job: %r>' % self.jobtitle




#
@app.route('/')
def show_entries():
   cur = JobSearches.query.all()
   entries = []
   return render_template('funny_jobs.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
   #g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
   #g.db.commit()
   jobTitle = request.form['jobtitle'].replace(" ", "+")
   try:
     readJobs.mainReadJobs(jobTitle)

     #creating the opening and closing 
     jobfile = codecs.open('markovJobs.txt', encoding='utf-8')
     markov = markovgen.Markov(jobfile)

     sentences = random.randint(2, 3)
     theOpening = markov.generate_markov_text(sentences)
     flash(theOpening,'theOpening' )

     sentences = random.randint(2, 3)
     theClosing = markov.generate_markov_text(sentences)
     flash(theClosing,'theClosing')


     bulletHeader = [ 'Key Responsibilities', 'Duties', 'Key Duties and Responsibilities', 'Objectives', 'Qualifications', 'Main Responsibilities']
     flash(random.choice(bulletHeader),'bulletHeader')

     #creating in the bullet points
     file = codecs.open('bulletmarkovJobs.txt', encoding='utf-8')
     markovBullets = markovgen.MarkovBullets(file)
     flash(request.form['jobtitle'],'jobtitleMsg' )
     sentences = random.randint(5, 7)
     theBullets = markovBullets.generate_markov_text(sentences)
     flash(theBullets,'bullets' )
   except:
      flash("There was an error in your request....Try Again",'error')  
   return redirect(url_for('show_entries'))



if __name__ == '__main__':
   app.run()

