import os
from flask import Flask, request, redirect, url_for, render_template, Response, send_from_directory
import sqlite3
from datetime import datetime

def create_enocean_table():
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS COURSES (ID INTEGER PRIMARY KEY AUTOINCREMENT, DATE TEXT, NAME TEXT, QUANTITY INT);")
    connection.commit()
    connection.close()


def insert_course(location, quantity):
    create_table()
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("INSERT INTO COURSES (DATE, NAME, QUANTITY) VALUES ( '"+str(datetime.now().strftime("%d-%m-%Y %H:%M"))+"', '"+location+"', "+str(quantity)+" );")
    connection.commit()
    connection.close()


def get_all_courses():
    create_table()
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    list_all = []
    for row in c.execute('SELECT * FROM courses ORDER BY id DESC'):
        list_all.append(row[1:])
    connection.commit()
    connection.close()
    return list_all


def export_courses():
    doc = SimpleDocTemplate('export.pdf', pagesize=letter)
    elements = []
    im = Image("static/ban.png", 7*inch, 0.8*inch)
    elements.append(im)
    styleSheet = getSampleStyleSheet()
    elements.append(Paragraph('''<br/><br/>''', styleSheet["Normal"]))
    elements.append(Paragraph('''<para fontSize="25">DATE DU RELEVE : '''+str(datetime.now().strftime("%d-%m-%Y %H:%M"))+'''<br/></para>''', styleSheet["Normal"]))
    elements.append(Paragraph('''<br/><br/><br/>''', styleSheet["Normal"]))
    head = ('DATE', 'LIEU', 'NB')
    heads = [head]
    h=Table(heads)
    table_style = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ('FONTSIZE', (0,0), (-1,-1), 23),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                           ('VALIGN', (0,0), (-1,-1), 'TOP'),
                           ])
    h.setStyle(table_style)
    h.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.green),
                           ]))
    h._argW[0]=2.75*inch
    h._argW[1]=4*inch
    h._argW[2]=0.75*inch
    for i in range(0,len(h._argH)):
        h._argH[i] = 0.50*inch
    elements.append(h)
    data = get_all_courses()
    if not len(data) == 0:
        t=Table(data)
        t.setStyle(table_style)
        t._argW[0]=2.75*inch
        t._argW[1]=4*inch
        t._argW[2]=0.75*inch
        for i in range(0,len(t._argH)):
            t._argH[i] = 0.45*inch
        elements.append(t)
    doc.build(elements)


app = Flask(__name__)
UPLOAD_FOLDER = '/home/romain/Documents/workspace/qrlabs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    courses = get_all_courses()
    return render_template('index.html', courses=courses)


@app.route('/formulaire', methods=['GET'])
@requires_auth
def formulaire():
    location = request.args.get('location')
    return render_template('formulaire.html', location=location)

@app.route('/confirm', methods=['POST'])
@requires_auth
def confirm():
    location = request.form['location']
    quantity = request.form['quantity']
    return render_template('confirm.html', location=location, quantity=quantity)


@app.route('/save', methods=['POST'])
@requires_auth
def save():
    location = request.form['location']
    quantity = request.form['quantity']
    insert_course(location, quantity)
    result = "OK"
    return render_template('save.html', result=result)


@app.route('/export', methods=['POST'])
@requires_auth
def export():
    export_courses()
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename='export.pdf')
    #return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='', port=80, debug=True)
    #http_server = WSGIServer(('', 80), app)
    #http_server.serve_forever()
