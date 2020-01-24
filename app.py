from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy import insert

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
engine = create_engine('sqlite:///test.db')
metadata = MetaData()
metadata.create_all(engine)

# class LookupDatabase { 
#      abstract void AddEmployee(String empName); 
#      abstract void AddSystem(String sysName); 
#      abstract void Associate(String empName, String sysName); 
#      abstract void Deassociate(String empName, String sysName); 
#      Object[][] Execute(String sqlCommand) {} 

# }

class Employee(db.Model):
    empKey = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(200), nullable=False)

class Systems(db.Model):
    sysKey = db.Column(db.Integer, primary_key=True)
    sysName = db.Column(db.String(200), nullable=False)

class Associated(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empKey = db.Column(db.Integer)
    sysKey = db.Column(db.Integer)

class Blanknames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(200), default='.')
    sysName = db.Column(db.String(200), default='.')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/deassociate/<int:id>')
def deassociate(id):
    task_to_delete = Associated.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deassociating'    

@app.route('/delemp/<int:id>')
def delemp(id):
    task_to_delete = Employee.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem removing Employee'    

@app.route('/delsys/<int:id>')
def delsys(id):
    task_to_delete = Systems.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem removing Systems'    

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
    else:
            tasks = Blanknames.query.order_by(Blanknames.id).all()
            con = engine.connect()
            statement = "select * from Associated as a left join Employee as e on a.empKey = e.empKey left join Systems as s on a.sysKey = s.sysKey order by 3,2"
            trans = con.execute(statement)
            statement = "select * from Employee where empKey not in (select empKey from Associated)"
            empnames = con.execute(statement)
            statement = "select * from Systems where sysKey not in (select sysKey from Associated)"
            sysnames = con.execute(statement)
            emparr = []
            for name in empnames:
                emparr.append((name.empName,name.empKey))
            sysarr = []
            for name in sysnames:
                sysarr.append((name.sysName,name.sysKey))
            arr = []
            for i in range(0,max(len(emparr),len(sysarr))):
                arr.append({"empName": "","empKey": "", "sysName": "", "sysKey": ""})
            for i in range(0,len(emparr)):
                arr[i]["empName"] = emparr[i][0]
                arr[i]["empKey"] = emparr[i][1]
            for i in range(0,len(sysarr)):
                arr[i]["sysName"] = sysarr[i][0]
                arr[i]["sysKey"] = sysarr[i][1]
            names = arr
            return render_template('index.html', tasks=tasks,trans=trans,names=names)


@app.route('/associate/', methods=['GET','POST'])
def associate():
    if request.method == 'POST':
        empName = request.form['empName']
        sysName = request.form['sysName']
        empKey = None
        sysKey = None
        try:
            con = engine.connect()
            statement0 = "select empKey from Employee where empName ='"+empName+"'"
            trans = con.execute(statement0)
            for tran in trans:
                empKey = str(tran.empKey)
            if empKey is None:
                return "Employee name not found"
            statement1 = "select sysKey from Systems where sysName = '"+sysName+"'"
            trans = con.execute(statement1)
            for tran in trans:
                sysKey = str(tran.sysKey)
            if sysKey is None:
                return 'System name not found'

            statement2 = "insert into Associated select ifnull(max(id),0)+1,'"+empKey+"','"+sysKey+"' from Associated where not exists ( select 1 from Associated where empKey = '"+empKey+"' and sysKey = '"+sysKey+"')"
            trans = con.execute(statement2)
            db.session.commit()
            statement3 = "update sqlite_sequence set seq = seq + 1 where name = 'Associated'"
            trans = con.execute(statement3)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue associating the names'
            
    else:
        return render_template('associate.html')

@app.route('/addemployee/', methods=['GET','POST'])
def addemployee():
    if request.method == 'POST':
        if request.form['empName'] is None:
                return "Employee name must not be blank"
        empName = request.form['empName'].strip()
        if empName == "":
                return "Employee name must not be blank"
        empKey = None
        try:
            con = engine.connect()
            statement0 = "select empKey from Employee where empName ='"+empName+"'"
            trans = con.execute(statement0)
            for tran in trans:
                empKey = str(tran.empKey)
            if empKey is not None:
                return "Employee name already exists"

            statement2 = "insert into Employee select ifnull(max(empKey),0)+1,'"+empName+"' from Employee"
            trans = con.execute(statement2)
            db.session.commit()
            statement3 = "update sqlite_sequence set seq = seq + 1 where name = 'Employee'"
            trans = con.execute(statement3)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue creating Employee name'
            
    else:
        return render_template('addemployee.html')

@app.route('/addsystem/', methods=['GET','POST'])
def addsystem():
    if request.method == 'POST':
        if request.form['sysName'] is None:
                return "System name must not be blank"
        sysName = request.form['sysName'].strip()
        if sysName == "":
                return "System name must not be blank"
        sysKey = None
        try:
            con = engine.connect()
            statement0 = "select sysKey from Systems where sysName ='"+sysName+"'"
            trans = con.execute(statement0)
            for tran in trans:
                sysKey = str(tran.sysKey)
            if sysKey is not None:
                return "System name already exists"

            statement2 = "insert into Systems select ifnull(max(sysKey),0)+1,'"+sysName+"' from Systems"
            trans = con.execute(statement2)
            db.session.commit()
            statement3 = "update sqlite_sequence set seq = seq + 1 where name = 'Systems'"
            trans = con.execute(statement3)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue creating Systems name'
            
    else:
        return render_template('addsystem.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
