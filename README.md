# DSCI551_ChatDB
This GitHub is a collection of files created for our final class project for DSCI 551.
It was created and is maintained by Jacob Graber and Myles Molnar.

## Prerequisites
Users must have MySQL Server installed and running on their local machine. See 'requirements.txt' for all necessary libraries and packages.

## Architectural Overview
Below is a summary of the various directories in this repository.

### Data
Data is a directory that contains sample data which the user can use to upload to either MySQL or MongoDB. Should the user want to upload their own data to ChatDB, we would recommend placing the file(s) in this directory for easy access when providing ChatDB with the filepath(s).

### Scripts
There are seven key files in the scripts directory. Six of these operate on the backend of ChatDB's functionality, while the file named 'chatdb.py' is effecitvely the fronted and the core functionality file. No contents of these files should be modified, other than the login info in the ChatDB file, which is addressed in the configuration section.
#### Archived
The directory called 'archived' exists purely for those users looking to investigate how this application was created. It contains a series of old testing files that were used during the development process of ChatDB. Its contents do not necessarily need to be looked at, our team simply thought it prudent to include in our final submission.

## Configuration
In order to use ChatDB, users must first provide the login information for their local MySQL connection in the 'chatdb.py' file. The user should NOT modify any of the login information for the MongoDB connection information, as this is run on a cloud server that our team maintains. Please ensure that your MySQL server is running before trying to use ChatDB, and that there exists a database with the name that is provided in the login info dictionary.

## Usability
After launching ChatDB, the core functionality of the application should become pretty apparent to the user, but should there be any confusion, here are some tips for usage.

**Uploading Datasets:**
- Prompt ChatDB to upload a dataset, then provide the filepath as needed.
- For SQL, the following filetypes are acceptable for upload: .sql (preferred), .csv
- For MongoDB, the following filetypes are acceptable for upload: .json
- Ex: upload sql ../data/restbase_sql/restbase_location.sql
- Ex: upload mongo ../data/UW_JSON_DATA/UW_std_course.json

**Exploring Datasets:**
- Prompt ChatDB to explore datasets, then specify either MongoDB or SQL.
- Metadata and sample data from the relevant dataset will be displayed.

**Example Queries:**
- Prompt ChatDB to generate example queries for either SQL or MongoDB data.
- Five queries will be generated at a time, and the user can select one to run and its results will be displayed.
- Ex: 'Show me some example sql queries.'

**Example Queries with Keywords:**
- Prompt ChatDB to generate example queries with specific keywords for either SQL or MongoDB data.
- Five queries will be generated at a time, and the user can select one to run and its results will be displayed.
- Ex: 'Show me some example sql queries with count and group by.'
- Ex: 'Show me some example mongodb queries with aggregate and match.'

**User-Inputted Queries:**
- Prompt ChatDB to generate and execute a specific SQL or MongoDB query using natural language.
- Below is a list of user inputs that will work on the pre-provided sample data stored in ChatDB.

*SQL*
* Show me all columns where food_type matches burgers from generalinfo
* Show me all columns where food_type is burgers and city is alameda from generalinfo
* How many restaurants have each review from generalinfo
* Show me the biggest 5 food types by average review of restaurants from each food_type in generalinfo rank them by AVG(review)
* Show me the street_num from location table, filter to where city is san francisco
* Show me the 5 biggest street_num, filter to where city is san francisco and use the location table

*MongoDB*
* Show me all of the columns and only 5 rows where hasPosition is equal to Faculty from UW_std_person
* show me average p_id, maximum p_id, minimum p_id, and count of all rows from UW_std_person grouped by hasPosition
* Show me all of the columns and only 5 rows where hasPosition is equal to Faculty_eme from UW_std_person
* Show me all columns from UW_std_person where inPhase equals Post_Generals
* Show me all of the columns and top 5 rows where yearsInProgram equals Year_4 from UW_std_person sorted by p_id
* Show all course_id from UW_std_course where courseLevel is equal to Level_500

**Exiting the Program:** 
- To end the ChatDB session, type 'exit'.
