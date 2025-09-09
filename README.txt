Step by Step guide to install and run.

1. extract folder
2. open folder in Visual code studio
3. CTRL + Shift + ` open terminal
4. Python 3.11 provided, issues may arise if python is installed already
5. enter this line to create virtal env -  py -3.11 -m venv .venv
6. then   -   .\.venv\Scripts\Activate.ps1
Optional - Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Fixes permissions error
7. Download psql (file in download)
8. 
CREATE ROLE candidate_user WITH LOGIN PASSWORD 'supersecret';
CREATE DATABASE candidate_intake OWNER candidate_user;
GRANT ALL PRIVILEGES ON DATABASE candidate_intake TO candidate_user;

9. To run the server - uvicorn app.main:app --reload
