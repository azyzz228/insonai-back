INSOIN.AI backend repository. 

Installation Guide:
1. Install python on your device
2. copy this repository to your device using git clone "repo_url" or download zip file
3. In project directory open terminal and type "python3 -m venv venv"
4. Proceed to install requirements by typing "pip install -r requirements.txt"
5. Create .env file in your directory
6. 
Copy this data to your env
DEBUG=1
SECRET_KEY=mvkvmfkdvmfkdmvkfdvmkfdmvkfdmvkfdmkvfmdk
DATABASE=postgres
SQL_HOST=localhost
SQL_PORT=5432
SQL_DB=inson_ai_db
SQL_USER=postgres
SQL_PASSWORD=1234567
7. Create postgres db with name inson_ai_db, postgres must be installed on your device
8. Proceed to creating migration, this will create necessary tables in db, type "python3 manage.py migrate"
10. Search for meta-lama-3 LLM module and pass together key TOGETHER_KEY to .env with key
11. Congratulations! Now you can run project by typing "python3 manage.py runserver"


FILE STRUCTURE
- main directory serves to hold all functionality of a project, 
  -- ai directory serves to hold AI related functionalities, LLM, STT and TTS
  -- models.py file serves to hold all db tables
  -- serializers.py file serves to serialize objects data
  -- urls.py file consist of information about routes of a project
  -- views.py file consist of endpoints which is being triggered by client
