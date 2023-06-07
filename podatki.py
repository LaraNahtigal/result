import requests
import psycopg2, psycopg2.extras


def ustvari_bazo(cur):
    
    cur.execute(open("baza.sql", "r").read())
    

def pridobi_podatke(conn, cur):
    posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
    comments = requests.get('https://jsonplaceholder.typicode.com/comments').json()
    todos = requests.get('https://jsonplaceholder.typicode.com/todos').json()
    users = requests.get('https://jsonplaceholder.typicode.com/users').json()


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
