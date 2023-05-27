import requests
import psycopg2, psycopg2.extras

# Povezava z bazo
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

def pridobi_posts(id_col='id'):
    for post in posts:
        select = f'SELECT id, title, body, user_id from posts WHERE {id_col} = %s';
        cur.execute(select, (post['id'],))
    
        row = cur.fetchone()
        if row:
            post['id'] = row[0]
            return post

        cur.execute(
            """INSERT INTO posts (id, title, body, user_id) VALUES (%s, %s, %s, %s)""",
            (post['id'], post['title'], post['body'], post['userId'])
        )
    conn.commit()


def pridobi_comments(id_col='id'):
    for comment in comments:
        select = f'SELECT id, name, email, body, post_id from comments WHERE {id_col} = %s';
        cur.execute(select, (comment['id'],))

        row = cur.fetchone()
        if row:
            comment['id'] = row[0]
            return comment

        cur.execute(
            "INSERT INTO comments (id, name, email, body, post_id) VALUES (%s, %s, %s, %s, %s)",
            (comment['id'], comment['name'], comment['email'], comment['body'], comment['postId'])
        )
    conn.commit()
     

def pridobi_todos(id_col='id'):
    for todo in todos:
        select = f'SELECT id, title, completed, user_id from todos WHERE {id_col} = %s';
        cur.execute(select, (todo['id'],))
    
        row = cur.fetchone()
        if row:
            todo['id'] = row[0]
            return todo

        cur.execute(
            "INSERT INTO todos (id, title, completed, user_id) VALUES (%s, %s, %s, %s)",
            (todo['id'], todo['title'], todo['completed'], todo['userId'])
        )
    conn.commit()

def pridobi_users(id_col='id'):
    for user in users:
        company = user['company']
        select = f'SELECT id, name, username, email, phone, company_name from users WHERE {id_col} = %s';
        cur.execute(select, (user['id'],))
    
        row = cur.fetchone()
        if row:
            user['id'] = row[0]
            return user

        cur.execute(
            "INSERT INTO users (id, name, username, email, phone, company_name) VALUES (%s, %s, %s, %s, %s, %s)",
            (user['id'], user['name'], user['username'], user['email'], user['phone'], company['name'])
        )
    conn.commit()

def pridobi_specificne_commente(zeljen_id:int, id_col = 'post_id'):
    select = f'SELECT body from comments WHERE {id_col} = %s';
    cur.execute(select, (zeljen_id,))
    print([s for s in cur.fetchall()])
    conn.commit()


# Kreira nov post preko API-ja in shrani respons object v tabelo v bazi
def kreiraj_post(title, body, user_id):
    post = {
        'title': title,
        'body': body,
        'userId': user_id
    }

    #cur.execute("""
    #    SELECT id, title, body, user_id from posts WHERE title = %s
    #    """, (post['title'],))
    #    
    #row = cur.fetchone()
    #if row:
    #    post['id'] = row[0]
    #    return post
    
    cur.execute(
        "INSERT INTO posts (title, body, user_id) VALUES (%s, %s, %s) RETURNING id;",
        (post['title'], post['body'], post['userId'])
    )
    post['id'] = cur.fetchone()[0]
    conn.commit()




pridobi_posts('id')
#pridobi_comments('id')
#pridobi_todos('id')
#pridobi_users('id')
#pridobi_specificne_commente(3,'post_id')
kreiraj_post('tralal','tralalal',3)
cur.close()

