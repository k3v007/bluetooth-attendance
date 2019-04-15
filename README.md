# Bluetooth Attendance System
**Linux System is a MUST!!**

## Installation 
1. Install mysql and complete it's configuration 
``` sudo apt update
    sudo apt install mysql-server
    sudo mysql_secure_installation```
2. Install redis-server
``` sudo apt install redis-server
    # By default refis-server is running on 6379 port```
3. Create a virtual environment (using conda etc.) 
``` conda create -n env python=3.7.1     # use any python >= 3.5
    conda acitvate env ```
4. Move to project directory
5. Install the requirements
``` pip install -r requirements.txt ``` 
6. To deactivate the conda environment
``` conda deactivate ```


## Usage
1. Set app settings and environment variables - rename .env.example to .env and set the values as directed in the file 
2. Open terminal in current project directory
3. Run the following commands to set migrations: 
``` python python manage.py db init 
    python manage.py db migrate -m "Inital commit"
    python manage.py db upgrade ```
4. Run Flask-RQ2 worker
``` flask rq worker```
5. Finally run the flask app (on a different terminal than that of rq worker in same project directory) 
``` python python run.py ```