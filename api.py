from cassandra.cluster import Cluster
from flask import Flask, render_template, request


# Connect to Cassandra cluster
cluster = Cluster(['192.168.64.21', '192.168.64.22'])
session = cluster.connect()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def welcome():
   return render_template('index.html')


@app.route('/schedule', methods=['POST'])
def process_dates():
   start_date = request.form['from']
   end_date = request.form['to']
   row = session.execute(f"SELECT * FROM oncall.roster WHERE from_date >= '{start_date}' AND from_date <= '{end_date}'  ALLOW FILTERING ;")
  
   return render_template('table.html', results=row)


@app.route('/insert', methods=['POST'])
def insert_schedule():
   return render_template('insert.html')

@app.route('/insertdata', methods=['POST'])
def insert_data():
   emp_id = request.form['employee-id']
   emp_name = request.form['employee-name']
   team_name = request.form['team-name']
   from_date = request.form['from-date']
   to_date = request.form['to-date']
   comments = request.form['comments']
   insertquery = session.execute(f"insert into oncall.roster (empid, emp_name, team_name, comments, from_date, to_date) values ({emp_id},'{emp_name}', '{team_name}', '{comments}', '{from_date}', '{to_date}');")
   return render_template('index.html')


@app.route('/update', methods=['POST'])
def update_schedule():
   return render_template('update.html')

@app.route('/updatedata', methods=['POST'])
def update_data():
   emp_id = request.form['employee-id']
#    emp_name = request.form['employee-name']
#   team_name = request.form['team-name']
   from_date = request.form['from-date']
   to_date = request.form['to-date']
#   comments = request.form['comments']
   insertquery = session.execute(f"update oncall.roster set  from_date = '{from_date}' , to_date = '{to_date}' where empid = {emp_id} ")
   return render_template('index.html')


if __name__ == '__main__':
   app.run(host = '0.0.0.0', debug=True)


# Close connection
session.shutdown()
cluster.shutdown()
