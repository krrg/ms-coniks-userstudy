import sys
import mysql.connector as mariadb
from flask import Flask, request, abort
app = Flask(__name__)

mariadb_connection = None
cursor = None

@app.route('/checkin', methods=['POST'])
def checkin():
	if request.method == 'POST':
		data = request.get_json()
		if 'id' in data:
			uid = data['id']
			if 'type' not in data:
				typ = 'normal'
			else:
				typ = data['type']
			try:
				if mariadb_connection is not None and cursor is not None:
					cursor.execute('INSERT INTO checkins(id, stamp, type) VALUES (%s, now(), %s)',(uid,typ))
					mariadb_connection.commit()
				else:
					app.logger.info('No database connection for checkin UUID: %s' % uid)
			except:
				e = sys.exc_info()[0]
				app.logger.info('Caught exception during mariadb insert: %s' % e)
			return ('', 204)
		else:
			abort(400)

if __name__ == '__main__':
	mariadb_connection = mariadb.connect(user='brad', password='password', database='thesis')
	cursor = mariadb_connection.cursor()
	app.run('127.0.0.1')

#curl -H "Content-Type: application/json" -X POST -d '{"id":"3126bd03-7365-4256-85e7-7e607ce35e01","type":"fromvm"}' http://138.68.43.10:5000/checkin
