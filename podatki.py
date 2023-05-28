import requests
import psycopg2, psycopg2.extras


conn = psycopg2.connect(
    host="localhost",
    database="lnDatabase",
    user="postgres",
    password="qwert2001"
)


posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
comments = requests.get('https://jsonplaceholder.typicode.com/comments').json()
todos = requests.get('https://jsonplaceholder.typicode.com/todos').json()
users = requests.get('https://jsonplaceholder.typicode.com/users').json()

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def podatki_posts():
    for post in posts:
        cur.execute("""
            SELECT id, title, body, user_id from posts WHERE title = %s
            """, (post['title'],))
        
        row = cur.fetchone()
        if row:
            post['id'] = row[0]
        else:
            cur.execute("""
                INSERT INTO posts (title, body, user_id)
                VALUES (%s, %s, %s) RETURNING id; """, (post['title'], post['body'], post['userId']))
            post['id'] = cur.fetchone()[0]
            conn.commit()



def podatki_comments():
    for comment in comments:
        cur.execute("""
            SELECT id, name, email, body, post_id from comments WHERE name = %s AND body = %s
            """, (comment['name'], comment['body'],))
        
        row = cur.fetchone()
        if row:
            comment['id'] = row[0]
        else:
            cur.execute("""
                INSERT INTO comments (name, email, body, post_id)
                VALUES (%s, %s, %s, %s) RETURNING id; """, (comment['name'], comment['email'], comment['body'], comment['postId'],))
            comment['id'] = cur.fetchone()[0]
            conn.commit()

     

def podatki_todos():
    for todo in todos:
        cur.execute("""
            SELECT id, title, completed, user_id from todos WHERE title = %s
        """, (todo['title'],))


        row = cur.fetchone()
        if row:
            todo['id'] = row[0]
        else:
            cur.execute("""
                INSERT INTO todos (title, completed, user_id) 
                VALUES (%s, %s, %s) RETURNING id;""", (todo['title'], todo['completed'], todo['userId'],))
            todo['id'] = cur.fetchone()[0]
            conn.commit()

def podatki_users():
    for user in users:
        cur.execute("""
            SELECT id, name, username, email, phone, company_name from users WHERE name = %s
        """, (user['name'],))


        row = cur.fetchone()
        if row:
            user['id'] = row[0]
        else:
            company = user['company']
            cur.execute("""
                INSERT INTO users (name, username, email, phone, company_name) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id;""", (user['name'], user['username'], user['email'], user['phone'], company['name'],))
            user['id'] = cur.fetchone()[0]
            conn.commit()


def pridobi_specificne_commente(zeljen_id:int):
    select = f'SELECT body from comments WHERE post_id = %s';
    cur.execute(select, (zeljen_id,))
    print([s for s in cur.fetchall()])


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

def brisanje_posta(id_post):
    cur.execute("""
    DELETE FROM posts WHERE id = %s""", (id_post,))
    cur.execute("""
    DELETE FROM comments WHERE post_id = %s""", (id_post,))
    conn.commit()

def posodabljanje_posta(id_posta, title, body):
    cur.execute("""
    UPDATE posts SET title=%s, body=%s WHERE id=%s""", (title, body, id_posta,))
    conn.commit()


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
    print(vsi_posti)

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
    print(vsi_commenti)

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
    print(vsi_todosi)
    
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
    print(vsi_userji)

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
    print(vsi_posti)

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
    print(post)

#podatki_posts()
#podatki_comments()
#podatki_todos()
#podatki_users()
#pridobi_specificne_commente(3)
#kreiraj_post('juhuhu','juhuhu',3)
#brisanje_posta(100)
#posodabljanje_posta(102, 'lalala', 'lalala')
#pridobivanje_posts()
#pridobivanje_comments()
#pridobivanje_todos()
#pridobivanje_users()
#pridobivanje_postov_userja(3)
#pridobivanje_posta_s_commenti(3)
cur.close()

