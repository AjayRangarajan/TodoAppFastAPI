# TODO APP using FastAPI
A Simple TODO application with all CRUD operations and User Authentication created with FastAPI

## Runnig the app
I have used `uvicorn` as asgi server for this application. To run this application run the following command in the command line.

```bash
uvicorn main:app --reload
```

For running it on specific port, run the following command with PORT number
```bash
uvicorn main:app --reload --port <PORT>
```
Here, the `<PORT>` is a number of the custom port. By default uvicorn will run on  *PORT 8000*

### Requirements

All the required packages were added to `requirements.txt` file.

### Environment variables
All the required *Environment variables* were added to `env.sample` file.

### API endpoints

#### user endpoints
    
    * signup
    * login

#### todo endpoints

    * tasks
    * create_task
    * get_task
    * update_task
    * delete_task

### Authentication used

OAuth2 with Password (and hashing), Bearer with JWT tokens

### Database

Any Relational database can be used by adding the **DATABASE_URI** in the `.env` file