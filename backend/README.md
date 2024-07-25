
## Setup

  

#### To set up the backend, follow these steps:
  

1. Ensure you have Python 3 installed on your system.

2. Navigate to the project directory in the terminal.

3. Run the `build.py` script to install dependencies, initialize the database, and start the server.

  
```bash

# if using a UNIX based system
python3 build.py

# or, if using a Windows based system
python build.py

```


4. Once the server is running, you can access the API endpoints to manage household profiles.

5. You can test user endpoints with when you are in test directory:

```bash

pytest

```

  
## API Endpoints

  
The backend exposes the following API endpoints:

  
### User oriented endpoints
- `GET /api/v1/users/`: Retrieve a list of all household profiles.
- `GET /api/v1/users/{user_id}`: Retrieve a specific household profile by User ID.
- `POST /api/v1/users/`: Create a new household profile.
- `PUT /api/v1/users/{user_id}`: Update an existing household profile by User ID.
- `DELETE /api/v1/users/{user_id}`: Delete a household profile by User ID.
- `POST /api/v1/web3login`: Returns a JWT-based token upon succesful login via the Web3Login adapter for registered Users.


### Request oriented endpoints
- `GET /api/v1/requests/`: Retrieve a list of all requests.
- `GET /api/v1/users/{user_id}/requests`: Retrieve a specific request by User ID.
- `GET /api/v1/agents/{agent_id}/requests`: Retrieve a list of requests by Agent ID.
- `GET /api/v1/users/requests/{request_id}`: Retrieve a specific request's detail by Request ID.
- `GET /api/v1/agent/requests/{request_id}`: Retrieve a specific request's detail by Request ID.
- `GET /api/v1/users/requests/{request_id}`: Retrieve a specific request's detail by Request ID.
- `POST /api/v1/requests/`: Create a new request.
- `PUT /api/v1/requests/{request_id}`: Update an existing request.
- `PATCH /api/v1/requests/{request_id}`: Update the approval status of a request by Request ID.
- `DELETE /api/v1/requests/{request_id}`: Delete a request by Request ID.
- `POST /api/v1/login`: Returns a JWT-based token upon succesful login using stored Agent credentials.
