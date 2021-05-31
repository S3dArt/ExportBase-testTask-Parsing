import pymysql
from config import host, user, password, db_name
from scrap_test_task import company_names, company_info, company_status

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('successfully connected...')
    print('#' * 20)

    try:
        #create table
        # with connection.cursor() as cursor:
        #     create_table_query = "CREATE TABLE companies(name VARCHAR(128)," \
        #                          "ogrn CHAR(128), " \
        #                          "inn VARCHAR(128)," \
        #                          "status VARCHAR(128)," \
        #                          "dateCreation VARCHAR(128)," \
        #                          "capital VARCHAR(128))"
        #     cursor.execute(create_table_query)
        #     print("Table created successfully")

        #insert data
        with connection.cursor() as cursor:
            for item in range(len(company_names)):
                name = company_names[item]
                ogrn = company_info[item][1]
                if company_info[item][0] == 'None':
                    inn = 'None'
                else:
                    inn = company_info[item][0]
                status = company_status[item]
                reg_date = company_info[item][2]
                # status = 'status'
                # reg_date = 'reg_date'
                if company_info[item][3] == 'None':
                    capital = 'None'
                else:
                    capital = company_info[item][3]
                # print(name, ogrn, inn, status, reg_date, capital)
                insert_query = "INSERT INTO companies(name, ogrn, inn, status, dateCreation, capital) " \
                               "VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_query, (name, ogrn, inn, status, reg_date, capital))
                connection.commit()

        # drop table
        # with connection.cursor() as cursor:
        #     drop_table_query = "DROP TABLE companies"
        #     cursor.execute(drop_table_query)

        # select all data from table
        with connection.cursor() as cursor:
            select_all_rows = "SELECT * FROM companies"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print('#' * 20)

    finally:
        connection.close()
except Exception as ex:
    print("Connection refused..")
    print(ex)

