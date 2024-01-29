# Social Networking App Backend with Django REST Framework

**A robust REST API for powering user authentication, friend connections, and social interactions.**

## Features

- **Secure User Authentication:** JWT authentication with password hashing.
- **Friend Requests and Connections:** Manage friend requests, accept/reject connections, and view a user's friend list.
- **Social Interactions:** Post status updates, view friends' feeds, and interact with posts (like, comment).

## Technologies Used

- Python 3.12.1
- Django 5.0.1
- Django REST Framework 3.14.0
- MySQL (or your preferred database)

## Installation and Setup

1. Clone the repository:

  ```bash
    git clone https://github.com/tejas-21sept/social_network_backend.git

  ```
   
2. Create a virtual environment and activate it:

    i.Open a terminal:

      - Windows: Open `Command Prompt` or `PowerShell`.
      - macOS/Linux: Open a terminal window.

    
    ii. Navigate to the project directory:

      ```python
        cd social_network_backend
    
      ```


    iii. Create the virtual environment:

      ```python
        python -m venv venv

      ```

    iv. Activate the virtual environment:


      ```python

        source venv/bin/activate  # Linux/macOS

        venv\Scripts\activate.bat  # Windows 

      ```


3. Install dependencies:

  ```pip
    pip install -r requirements.txt

  ```

4. Create a database.
  - MySQL-specific instructions: The following commands are specific to MySQL databases. If you're using a different database, please refer to its documentation for the appropriate commands.

  * Open the MySQL command line client: Access your MySQL client using your preferred method (e.g., through a terminal or GUI tool).

  * Create the database: Execute the following command to create a new database, replacing DATABASE_NAME with your desired name:

  ```mysql
    CREATE DATABASE_NAME ;

  ```

5. Create a .env file:

  - Create a file named .env in the root directory of the project.
  - Copy the contents of the ``.env-example`` file into .env.
  - Fill in the appropriate values for your environment variables, such as API keys, database credentials, and any other sensitive information.

6. Apply database migrations
   
  ```python 
    python manage.py makemigrations
    python manage.py migrate

  ```

7. Run the development server:

  ```python
    python manage.py runserver

  ```

## Note:- After running local server, in postman use `base_url` as `http://127.0.0.1:8000`.

## Resources

1. Project Link
  **Project Repository:** [Social Network Backend](https://github.com/tejas-21sept/social_network_backend)

2. Postman Collection
   
  > Copy below URL in browser 
  
  `https://api.postman.com/collections/27274140-d5634f89-705a-46fd-84ba-4d7a980e5fea?access_key=PMAT-01HN9NNNNJB7MBS5SHXG4B34WY`

  > Open postman webapp/app and go to the existing collections. Click on import and above link there and import the collection.
