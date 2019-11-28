Created a website with 3 subscription levels Level A, Level B, Level C. Users who subscribed to each level can only access a limited number of pages on the site. When a user tries to access a page that doesn't fall under his subscription level an appropriate message to be displayed and the content must not be shown to him. 

Doing the following things
1. Create multiple users with different subscription levels
2/ Create 100 pages with the pattern (http://127.0.0.1/a1/, http://127.0.0.1/a2/, http://127.0.0.1/a3/, http://127.0.0.1/a4/ etc)
3. Pages 1 to 20 can only be accessed by users with subscription Level A
4. Pages 20 to 50 can only be accessed by users with subscription Level B
5. Other pages can be accessed by users with subscription level C
6. Once the application is created the application admin must be able to change the subscription level of any page he desires

The following libraries are required:

  * pip install flask
  * pip install flask-sqlalchemy

