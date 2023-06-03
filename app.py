import psycopg2
from bottle import get, delete, post, run
import os
import json


SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

conn = psycopg2.connect(
    host="localhost",
    dbname="lnDatabase",
    user="postgres",
    password="qwert2001",
    port="5432"
)


cur = conn.cursor() 

@get('/')
def osnova():
    return('')


@get('/specificni-komentarji/<zeljen_id>')
def pridobi_specificne_commente(zeljen_id:int): 
    vsi_komentarji = {}
    select = f'SELECT body from comments WHERE post_id = %s';
    cur.execute(select, (zeljen_id,))
    komentarji = [s for s in cur.fetchall()]
    vsi_komentarji[zeljen_id] = komentarji
    return(json.dumps(vsi_komentarji))


@post('/kreiraj-post/<title>/<body>/<user_id>')
def kreiraj_post(title, body, user_id):
    post = {
        'title': title,
        'body': body,
        'userId': user_id
    }

    cur.execute("""
        SELECT id, title, body, user_id from posts WHERE title = %s and body = %s
        """, (post['title'], post['body'],))
        
    row = cur.fetchone()
    if row:
        post['id'] = row[0]
        return post
    
    cur.execute("""
        INSERT INTO posts (title, body, user_id)
        VALUES (%s, %s, %s) RETURNING id; """, (post['title'], post['body'], post['userId'],))
    post['id'] = cur.fetchone()[0]
    conn.commit()
    return post


@delete('/brisanje-posta/<id_posta>')
def brisanje_posta(id_posta):
    cur.execute("""
    DELETE FROM posts WHERE id = %s""", (id_posta,))
    cur.execute("""
    DELETE FROM comments WHERE post_id = %s""", (id_posta,))
    conn.commit()
    return ('Post je zbrisan!')

@post('/posodabljanje-posta/<id_posta>/<title>/<body>')
def posodabljanje_posta(id_posta, title, body):
    cur.execute("""
    UPDATE posts SET title=%s, body=%s WHERE id=%s""", (title, body, id_posta,))
    conn.commit()
    return ('Post je posodobljen!')

@get('/posti')
def pridobivanje_posts():
    vsi_posti = []
    cur.execute(""" SELECT * FROM posts """)
    rows = cur.fetchall()
    for row in rows:
        post = {}
        post['id'] = row[0]
        post['title'] = row[1]
        post['body'] = row[2]
        post['userId'] = row[3]
        vsi_posti.append(post)
    return(json.dumps(vsi_posti))

@get('/komentarje')
def pridobivanje_comments():
    vsi_commenti = []
    cur.execute(""" SELECT * FROM comments """)
    rows = cur.fetchall()
    for row in rows:
        comment = {}
        comment['id'] = row[0]
        comment['name'] = row[1] 
        comment['email'] = row[2] 
        comment['body'] = row[3] 
        comment['postId'] = row[4]
        vsi_commenti.append(comment)
    return(json.dumps(vsi_commenti))


@get('/todose')
def pridobivanje_todos():
    vsi_todosi = []
    cur.execute(""" SELECT * FROM todos """)
    rows = cur.fetchall()
    for row in rows:
        todo = {}
        todo['id'] = row[0]
        todo['title'] = row[1] 
        todo['completed'] = row[2] 
        todo['userId'] = row[3]
        vsi_todosi.append(todo)
    return(json.dumps(vsi_todosi))
    

@get('/userje')
def pridobivanje_users():
    vsi_userji = []
    cur.execute(""" SELECT * FROM users """)
    rows = cur.fetchall()
    for row in rows:
        user = {}
        user['id'] = row[0]
        user['name'] = row[1] 
        user['username'] = row[2] 
        user['email'] = row[3] 
        user['phone'] = row[4] 
        user['companyName'] = row[5]
        vsi_userji.append(user)
    return(json.dumps(vsi_userji))


@get('/pridobi-poste/<id_userja>')
def pridobivanje_postov_userja(id_userja):
    vsi_posti = []
    cur.execute(""" SELECT id, title, body FROM posts WHERE user_id = %s """, (id_userja,))
    rows = cur.fetchall()
    for row in rows:
        post = {}
        post['id'] = row[0]
        post['title'] = row[1]
        post['body'] = row[2]
        vsi_posti.append(post)
    return(json.dumps(vsi_posti))


@get('/pridobi-poste/<id_posta>')
def pridobivanje_posta_s_commenti(id_posta):
    vsi_commenti = []
    post = {}
    cur.execute(
            """
            SELECT i.id, i.title, i.body, i.user_id, j.name, j.email, j.body 
            FROM posts i left join comments j on i.id = j.post_id WHERE i.id = %s
            """, (id_posta,))
    rows = cur.fetchall()
    for row in rows:
        comment = {}
        comment['name'] = row[4]
        comment['email'] = row[5]
        comment['body'] = row[6]
        vsi_commenti.append(comment)
    post['id'] = rows[0][0]
    post['title'] = rows[0][1]
    post['body'] = rows[0][2]
    post['userId'] = rows[0][3]
    post['comments'] = vsi_commenti
    return(json.dumps(post))

if __name__ == '__main__':
   run(host='localhost', port=SERVER_PORT, reloader=RELOADER)