import csv
import sqlite3


def csv_reader(table, file_obj, cursor, index_model):
    reader = csv.reader(file_obj)
    index = 0

    for row in reader:
        if index == 0:
            index = 1
            continue

        if index_model == 1:
            values = ",".join(["?" for i in range(0, len(row))])
            sql = f'insert into {table} values({values})'
            print(sql, row[1])
            cursor.execute(sql, row)


def main():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    tables = {
        #'api_genre': 'data/genre.csv',
        #'api_title': 'data/titles.csv',
        #'api_category': 'data/category.csv',
        'api_reviews': 'data/review.csv',
        'api_comments': 'data/comments.csv',
        #'api_user': 'data/users.csv',
    }

    for key, value in tables.items():
        with open(value, "r", encoding='utf-8') as f_obj:
            csv_reader(key, f_obj, cursor, 1)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
