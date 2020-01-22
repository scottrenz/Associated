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

class Empsysnames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(200), default='.')
    sysName = db.Column(db.String(200), default='.')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Blanknames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empName = db.Column(db.String(200), default='.')
    sysName = db.Column(db.String(200), default='.')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Associated.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'    

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        emp_content = request.form['empName']
        if emp_content is not None:
            new_task1 = Employee(empName=emp_content)
            try:
                db.session.add(new_task1)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your Employee'
        sys_content = request.form['sysName']
        if sys_content is not None:
            new_task2 = Systems(sysName=sys_content)
            try:
                db.session.add(new_task2)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your System'    
        a_sys_content = request.form['AsysName']
        d_sys_content = request.form['DsysName']
        a_emp_content = request.form['DsysName']
        d_emp_content = request.form['DsysName']
        if a_sys_content is not None and a_emp_content is not None:
            con = engine.connect()
            statement = "INSERT INTO Associated(empKey, sysKey) select empKey, sysKey from Employee, Systems where empName ='" + emp_content + "' and sysName ='" + sys_content + "'"
            con.execute(statement)
        if d_sys_content is not None and d_emp_content is not None:
            con = engine.connect()
            statement = "delete from Associated where id in (select id from company.empsys where empName ='" + d_emp_content + "' and sysName ='" + d_sys_content + "')"
            con.execute(statement)

    else:
            tasks = Blanknames.query.order_by(Blanknames.id).all()
            con = engine.connect()
            statement = "select * from empsys order by 3,2"
            trans = con.execute(statement)
            # con.close()
            return render_template('index.html', tasks=tasks,trans=trans)


@app.route('/update/', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        empName = request.form['empName']
        sysName = request.form['sysName']
        empKey = None
        sysKey = None
        if True:
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

            statement2 = "insert into Associated select seq,'"+empKey+"','"+sysKey+"' from sqlite_sequence where name ='Associated' and not exists ( select 1 from Associated where empKey = '"+empKey+"' and sysKey = '"+sysKey+"')"
            trans = con.execute(statement2)
            db.session.commit()
            statement3 = "update sqlite_sequence set seq = seq + 1 where name = 'Associated'"
            trans = con.execute(statement3)
            db.session.commit()
            return redirect('/')
        # except:
            return 'There was an issue associating the names'
            
    else:
        return render_template('update.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
