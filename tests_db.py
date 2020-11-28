import requests
import pymysql

token = "4bc72159b7b37fd4f95be2e2354a45db6da44a910f35677faac13dca4a018002c265118c53b85679009d9"
group_id = "-183605582"
version = "5.101"

connection = pymysql.connect(host='localhost', user='root', password='gs651zv3mlt8@#GHCZ', db='ege_bot', charset='utf8mb4')
cursor = connection.cursor()
print("SUCCESSFULLY CONNECTED")


def get_docsGet():
    r = requests.get('https://api.vk.com/method/docs.get', params={'access_token': token,
                                                                   'owner_id': group_id,
                                                                   'v': version
                                                                   }).json()
    count = 1
    doc_count = r['response']['count']

    while count < doc_count:
        doc_id = r['response']['items'][count]['id']
        doc_id = 'doc-183605582_' + str(doc_id)

        doc_full_name = r['response']['items'][count]['title']
        doc_name = doc_full_name.split(' ')[0]
        doc_number = doc_full_name.split(' ')[1].split('.')[0]
        count += 1
        cursor.execute("""
                        INSERT INTO tests (id, exam, numberTest)
                        VALUES
                        (%s, %s, %s)""", (doc_id, doc_name, doc_number))
        connection.commit()
        print(count)


def main():
    get_docsGet()


if __name__ == '__main__':
    main()
