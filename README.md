Team Chihuahuas (16) CSCC01 Project
===================================
**Imporant**: The host for our database has been going offline very recently. If it does, the website will not start and the unittests cannot run. A quick observation shows that our database is operational during the morning and late in the evening, but encounters a internal server error in the afternoon.

Phase 4
-------
_All items are located under the master branch._

**Report Location**: Our report is located in `Course Related Items/Reports/Phase 4 Report.pdf`.

**Burndown Chart**: The Burndown charts are located in the excel file located in `Project Management/Iteration Planning/Burndown_Charts.xslx`

Please note that the excel file contains eight worksheets each of which contains the burndown chart for that week except the last week. The ideal burndown is shown with the blue line and the actual burndown is shown with the red line.

**Release Plan & Task Board**: These are contained in our team trello account. The access to this account has already been given to you.

Improvement from Phase 3
------------------------
Please see the improved unittests for `GetResultsTestCase`, located in `Website/flaskVersion/app/tests.py`

Build and Run Instructions
---------------------------
_For simplicity, please follow these instructions while on mathlab._

1. Clone the repo from the master branch
2. Open 3 terminals and change their directories to `Website/flaskVersion/app`
3. In the first terminal run the server using `python views.py`
4. In the second terminal run the task processing queue using `celery -A views.celery worker`
5. In the third terminal run firefox (or a browser of your choice). Make sure the browser is running from mathlab.
6. In the browser go to the specified address `localhost:5000`. The website will be running.

**Current Functionality**:
  
- Keyword management
- Feed Crawl and Article Crawl
  * View the results of the crawl
- Twitter Crawl
  * View the results of the crawl

Code Reviews
------------
All the code reviews are located in `Project Management/Code Review`. New code reviews are as follows:

- `Carlos' table_graph.txt` - Samson reviewed Carlos' graph functionality for tweets.
- `Kenny's get_tweets.txt` - Kanwar reviewed Kenny's view tweets table functionality.
- `Samson_review.txt` - Vinicius reviewed Samson's save documents to database functionality.
- `Kanwar's Twitter Table.txt` - Kenny reviewed Kanwar's view tweets table functionality (frontend).
- `Vinicius' signup fix.txt` - Carlos reviewed Vinicius' login functionality.

**Code Inspection Video**: Video location at `Project Management/Code Review/Code_Inspection_Phase_IV.mov`

Unit Test Instructions
-----------------------

1. Change directory to `Website/flaskVersion/app`
2. Run the tests using `python tests.py`

Automation Tests Instructions
------------------------------
_Automation tests are run from the flask branch._

Note: They only work in the Firefox browser because it has support for the Selenium IDE.

1. Open the website in Firefox.
2. Open the Selenium IDE (You may have to install this plugin if you don't have it).
3. Load the file "New_full_testing" into the Selenium IDE under "Open Test Suite"
4. Slow down the Selenium testing speed, otherwise the tests will fail for clicking too fast
5. Run the the full test suite
