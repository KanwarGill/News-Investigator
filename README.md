Team Chihuahuas (16) CSCC01 Project
===================================

Phase 3
-------
_All items are located under the master branch._

**Report Location**: Course Related Items/Reports/Phase 3 Report.pdf

**Contents of Report**: The report contains 

- the state of the project
- the iteration plans

**Burndown Chart**: The Burndown charts are located in the excel file located in `Project Management/Iteration Planning/Burndown_Charts.xslx`

Please note that the excel file contains six worksheets each of which contains the burndown chart for that week. The ideal burndown is shown with the blue line and the actual burndown is shown with the red line.

**Release Plan & Task Board**: These are contained in our team trello account. The access to this account has already been given to you.

**Code Inspection Video**: Video location at `Project Management/Code Review/Code_Review.mov`

Build and Run Instructions:
---------------------------
_For simplicity, please following these instruction while on mathlab._

1. Clone the repo from the master branch
2. Open 3 terminals and change their directories to `Website/flaskVersion/app`
3. In the first terminal run the server using `python views.py`
4. In the second terminal run the task processing queue using `celery -A views.celery worker`
5. In the third terminal run firefox (or a browser of your choice). Make sure the browser is running from mathlab.
6. In the browser head the the spcified address `localhost:5000`. The website will be running.

**Current Functionality**:
  
- Add/Delete/Show/Hide sources
- Add/Delete/Show/Hide keywords
- Show results
- Start web crawl

Code Reviews
-----------------------
All the code reviews are located in `Project Management/Code Review`. The reviews follow the format mentioned in the handout.
- Kanwar looked at Samson's backend code
- Samson looked at Kanwar's code for pipeline for the database
- Carlos looked Kenny's code for the login page and Twitter handles
- Kenny looked at Vinicius' code for index.html and main.js files
- Vinicius looked at Carlos' code for encrypting the password on signup and login pages

Unit Test Instructions:
-----------------------
Unit tests are done from the `flask` branch.

1. On terminal, install the Python library `mock`. The easiest way this can be done is `pip install mock`.
2. Change directory to `Website/flaskVersion/app`
3. Run the tests using `python tests.py`
