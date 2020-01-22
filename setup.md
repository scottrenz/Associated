rm -rf env
virtualenv env
pip3 install virtualenv
virtualenv env
source env/bin/activate
pip3 install flask flask-sqlalchemy
pip freeze > requirements.txt

pip3 install -U textblob
python3  -m textblob.download_corpora lite
# if "unable to import flask" then:

<!-- Simple solution :

Go to command palette Type-- Python:Select Interpreter

Select your virtual environment that you created

answered specifically for vscode -->
