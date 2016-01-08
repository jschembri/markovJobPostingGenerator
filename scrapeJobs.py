#scrape jobs

import readJobs


#list of jobs that need to scrape...we can add more later and only the new Jobs get scraped

scrapedJobs = [
'Mechanical Engineer',
'Electrical Engineer',
'Biomedical Engineer',
'Engineer',
'Writer',
'Technical Writer',
'Lawyer',
'Manager',
'Web Developer',
'Sofware Engineer',
'Casher',
'Sales representative',
'Supervisor',
'Labourer',
'Project Engineer',
'Junior Engineer',
'Intermediate Engineer',
'Senior Engineer',
'QA Engineer',
'Designer',
'Design Engineer',
'Drafter',
'Manufacturing Engineer',
'Web Administrator',
'Web Designer',
'Freelance Writer',
'Mechatronics Engineer',
]


scraping = True

print "Starting to Scrape jobs"
for jobTitle in scrapedJobs:
	newJob, jobtitleFilename, jobbulletFilename = readJobs.existingJob(jobTitle, scraping)
	if newJob:
		readJobs.mainReadJobs(jobTitle, jobtitleFilename, jobbulletFilename, 200)
		print "Finished Scraping %s" % jobTitle