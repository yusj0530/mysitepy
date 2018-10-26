import MySQLdb
from django.db import models

# Create your models here.
from mysitepy.settings import DATABASES


def connect():
    try:
        conn = MySQLdb.connect(
            host=DATABASES['default'][ 'HOST' ],
            port=int(DATABASES['default'][ 'PORT' ]),
            user=DATABASES['default'][ 'USER' ],
            password=DATABASES['default'][ 'PASSWORD' ],
            db=DATABASES['default'][ 'NAME' ],
            charset='utf8')
        return  conn

    except MySQLdb.Error as e:
        print('Error %d: %d' % (e.args[0], e.args[1]))
        return None

def insert(board):
    try:
        conn = connect()
   # 2. 커서 생성
        cursor = conn.cursor()

    # 3. SQL문 실행
        sql ='''
                    insert into board 
                    values(null, '%s', '%s', 0,  now(), ifnull(
                    (select max(group_no) from board as board1),0)+1,
                     1, 0, '%s')
                     '''% board
        count = cursor.execute(sql)

   # 4. 자원 정리
        cursor.close()
        conn.commit()
        conn.close()

       # 5. 결과 처리
        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d'% (e.args[0], e.args[1]))


def insert1(board):
    try:
        conn = connect()
   # 2. 커서 생성
        cursor = conn.cursor()

    # 3. SQL문 실행
        sql ='''
                 insert into board 
                    values(null, '%s', '%s', 0,  now(), %d,
                     %d, %d, '%s')
                     '''% board
        count = cursor.execute(sql)

   # 4. 자원 정리
        cursor.close()
        conn.commit()
        conn.close()

       # 5. 결과 처리
        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d'% (e.args[0], e.args[1]))


def re_update(p_order_no, p_group_no):
    try:
        conn=connect()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql='''
            update board
                set order_no = order_no+1
                where order_no > %d
                and group_no = %d
            '''%(p_order_no, p_group_no)

        count=cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d' % (e.args[0], e.args[1]))
        return False


def order():
    try:
        conn = connect()
   # 2. 커서 생성
        cursor = conn.cursor()

    # 3. SQL문 실행
        sql = '''select * 
	                from board
                    order by group_no desc, order_no asc'''
        count = cursor.execute(sql)

   # 4. 자원 정리
        cursor.close()
        conn.commit()
        conn.close()

       # 5. 결과 처리
        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d'% (e.args[0], e.args[1]))

def  fetchall():
    # 2. 커서 생성
    try:
        conn= connect()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # 3. SQL문 실행
        sql = '''
          select *
            from board
             order by group_no desc, order_no asc
            '''
        cursor.execute(sql)
        # 4. 결과 받아오기(fetch)
        #  한 로우씩 넣어준다.
        results = cursor.fetchall()
           #return  count

        # 5. 자원 정리
        cursor.close()
        conn.close()

        return results

    except MySQLdb.Error as e:
        print('Error %d: %d' % (e.args[0], e.args[1]))
        return  None

def delete(board):
    try:
        conn = connect()
   # 2. 커서 생성
        cursor = conn.cursor()

    # 3. SQL문 실행
        sql = "delete from board where id=%d and user_id='%s'" %board

        count = cursor.execute(sql)

   # 4. 자원 정리
        cursor.close()
        conn.commit()
        conn.close()

       # 5. 결과 처리
        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d'% (e.args[0], e.args[1]))



def fetchone(id):
    try:
        conn = connect()

        # 2. 커서 생성
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # 3. SQL문 실행
        sql = '''
          select *
              from board
              where id=%d
              ''' % id
        cursor.execute(sql)


    # 4. 자원 정리

        row = cursor.fetchone()
        cursor.close()

        conn.close()

        # 5. 결과 처리
        return row
    except MySQLdb.Error as e:
            print('Error %d: %d' % (e.args[0], e.args[1]))
            return None


def maxfetchone(id):
    try:
        conn = connect()

        # 2. 커서 생성
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # 3. SQL문 실행
        sql = '''
          select *
              from board
              where max(id)=%d
              ''' % id
        cursor.execute(sql)


    # 4. 자원 정리

        row = cursor.fetchone()
        cursor.close()

        conn.close()

        # 5. 결과 처리
        return row
    except MySQLdb.Error as e:
            print('Error %d: %d' % (e.args[0], e.args[1]))
            return None

def update(title,content,id):
    try:
        conn=connect()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql='''
        update board
            set title='{0}', content='{1}'
            where id={2}
            '''.format(title,content,id)
        print(sql,type(sql))

        count=cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d' % (e.args[0], e.args[1]))
        return False

def hitupdate(id):
    try:
        conn=connect()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql='''
        update board
            set hit=hit+1
            where id={0}
            '''.format(id)

        count=cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1
    except MySQLdb.Error as e:
        print('Error %d: %d' % (e.args[0], e.args[1]))
        return False
