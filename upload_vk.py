import requests
import time
import json
import glob

token = '1fc0fdb76ca49994cdea69eb742789c914643073727e7ef45b00ba3a174b3535d2e90dbd061d97ffafcca'
group_id = "183605582"
version = "5.101"

all_test = glob.glob('*.pdf')


def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def get_upload_server():
    r = requests.get('https://api.vk.com/method/docs.getUploadServer', params={'access_token': token,
                                                                               'group_id': group_id,
                                                                               'v': version
                                                                               }).json()
    return r['response']['upload_url']


def main():
    for ALL in all_test:
        upload_url = get_upload_server()
        file = {'file': open(ALL, 'rb')}
        ur = requests.post(upload_url, files=file).json()
        result = requests.get('https://api.vk.com/method/docs.save', params={'access_token': token,
                                                                             'file': ur['file'],
                                                                             'v': version
                                                                             }).json()
        if 'error' in result:
            print('I sleeping')
            time.sleep(60)
            # exit(result['error']['error_msg'])
        else:
            print(ALL)



if __name__ == '__main__':
    main()
