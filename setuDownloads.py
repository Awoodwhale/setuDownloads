import requests
import re
import threading
import time

# 填写自己的headers
headers = {'user-agent': ''}
# 填写自己的下载路径
downloadPath = ""


# 获取json数据
def getApiJSON(url,headers):
    try:
        print('Try to connect api!')
        res = requests.get(url,headers=headers)
        print('Successful connecting!')
    except:
        print('Connect error!')
        return getApiJSON(url,headers)
    JSON_data = res.json()
    return JSON_data

# 进行图片下载
def download(url, pid, way):
    global errCount,downloadPath
    try:
        res = requests.get(url).content
    except:
        # 将错误url写入err.txt
        print('Download error!')
        lock.acquire()
        errCount += 1
        lock.release()
        with open (downloadPath + "err.txt","a") as file :
            file.write(setu_url + '\n')
        return
    with open(downloadPath + pid + way, "wb") as file:
        file.write(res)
    print('Success!')

allTime = 0
allSuccess = 0

# 每次循环下载100张图
for i in range(5):
    print(f'The {i+1} time!')
    url = 'https://api.lolicon.app/setu/?num=100&r18=1'
    lock = threading.Lock()
    threads = []
    errCount = 0
    startTime = time.time()
    jsons = getApiJSON(url, headers)
    jsons = jsons['data']

    for json in jsons:
        setu_url = json['url']
        setu_pid = str(json['pid'])
        way = re.findall('(.png|.jpg)', setu_url, re.S)[0]
        t = threading.Thread(target=download, args=(setu_url,setu_pid,way,))
        t.start()
        threads.append(t)
        time.sleep(1.5)

    for t in threads:
        t.join()
        print(f'{t.name} over!')

    endTime = time.time()
    print(f'The {i+1} time over! It takes {endTime-startTime}! It has {100-errCount} successes!')
    allTime += endTime - startTime
    allSuccess += 100 - errCount
    time.sleep(1)

print(f"All over! It takes {allTime}! It has {allSuccess} successes!")