
# Social Network API

This project is a Django-based API for a social network. It includes Docker configuration for streamlined setup and deployment.


## Prerequisites
```bash
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.8 or higher.
- You have Docker installed on your machine.
- You have basic knowledge of Docker and Python.

```
## Installation Instructions
### Clone the Repository
To get started, clone this repository to your local machine:
```bash
Follow these steps to get your development environment set up:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-network.git
   cd social-network

```

## Setup Environment


```bash
 python -m venv env
# Activate the virtual environment
# On Windows
env\Scripts\activate
# On MacOS/Linux
source env/bin/activate


```
## 
Make sure to fill in all necessary variables like database configurations and secret keys.

## Install Dependencies
The project dependencies are listed in the requirements.txt file located at the root of the project directory. These dependencies will be automatically installed when building the Docker container. However, if you need to install them manually for any reason, you can run:

```bash
  pip install -r requirements.txt

```
## Configuration
Create a .env file in the root directory of the project and add the necessary environment variables

```bash
DEBUG=on
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME


```
## Running the Application
You can run the application using Docker Compose or the Django development server:
## Using Docker Compose
Execute the following command to build and start all required services:
```bash

  docker-compose up --build

```
This command builds the Docker images and starts the containers specified in the 'docker-compose.yml' file.

## Using the Django Development Server
 Apply the migrations:

 ```bash
  python manage.py migrate
```
## Start the development server
 ```bash
  python manage.py runserver
```
## API Usage
Once the application is running, you can use the provided Postman collection (api.postman_collection.json) to interact with the API.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
 ```bash
 
### Notes:
- Replace `https://github.com/yourusername/social-network.git` with your actual GitHub repository URL.
- Ensure you include any specific environment variables needed for your Django settings in the `.env` file example.
- You might want to provide more specific API usage details or expand the sections based on your project’s features or requirements.

This README provides a structured way to guide users through setting up and using your project, enhancing the overall accessibility and usability of your repository.

```


## Documentation

[Documentation] 

```bash
## API Endpoints

This section provides detailed examples of requests for each API endpoint using Postman. Import the provided collection into Postman to interact with the API directly.

### Importing the Collection
1. Open Postman.
2. Click on 'Import' at the top left of the application.
3. Choose 'Link' and paste the URL of the collection.
4. Click 'Continue' and then 'Import' to add the collection to your workspace.

### Available Endpoints

#### User Registration
- **Method:** POST
- **Endpoint:** 'http://127.0.0.1:8000/api/signup/'
- **Body:**
  ```json
  {
    "email": "aws@gmail.com",
    "name": "aws",
    "password": "aws@password"
  }

```
Description: Registers a new user with email, name, and password

#### User Login

##### . Method : POST
####  . Endpoint: http://127.0.0.1:8000/api/login/
####  . Body

```bash
  {
  "email": "aws@gmail.com",
  "password": "aws@password"
  }

```

### Send Friend Request
#### Method: POST
#### Endpoint: http://127.0.0.1:8000/api/friend-request/
#### Header: Authorization: Bearer {token}
#### Body:

```bash
#### Send Friend Request

- **GET Method:**
  - **Endpoint:** `http://127.0.0.1:8000/api/friend-request/`
  - **Header:** Authorization: Bearer {token}
  - **Description:** Retrieves a list of all users. This can be used to display potential friends to send requests to.

- **POST Method:**
  - **Endpoint:** `http://127.0.0.1:8000/api/friend-request/`
  - **Header:** Authorization: Bearer {token}
  - **Body:**
    ```json
    {
      "receiver": 16
    }
    ```
  - **Description:** Sends a friend request to another user by specifying the receiver's user ID.

### Usage Tips
- For the GET method, ensure you are authorized (using the token) to fetch the list of users.
- For the POST method, replace `"receiver": 16` with the actual user ID of the person you wish to send a friend request to.
- Check the response status and data for each request to understand how the API processes it.

This setup allows users to first find potential friends using the GET method and then initiate friend requests using the POST method.

```

###### This format clarifies the distinction between the two methods under the same endpoint, making it easier for users to understand how to use each method effectively.

### Search Users
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/api/search/?search=user
#### Header: Authorization: Bearer {token}
#### Description: Searches for users based on the provided query parameter.

### List of Accepted Friends
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/api/friends/
#### Header: Authorization: Bearer {token}
#### Description: Retrieves a list of friends that have accepted the user's friend requests.

### Pending Friend Requests
#### Method: GET
#### Endpoint: http://127.0.0.1:8000/api/pending-requests/
#### Header: Authorization: Bearer {token}
#### Description: Lists all pending friend requests received by the user.

### Accept or Reject Friend Request
#### Method: PUT
#### Endpoint: http://127.0.0.1:8000/api/update-request/9/
#### Header: Authorization: Bearer {token}
#### Body

```bash
{
  "action": "accept"
}

```
#### Description: Allows the user to accept or reject a friend request by specifying the action ('accept or reject').

### Testing Tips

#### @ Ensure that you have replaced {token} with the actual token received after logging in.
#### @ Check the response status and data for each request to understand the API behavior.

For further details or issues, please consult the API documentation linked here or contact our support team.

```bash

This section will make your README comprehensive and very helpful for users who wish to interact with your API effectively.


```
