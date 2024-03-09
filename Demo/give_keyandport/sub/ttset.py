# import socket
# import tqdm
# import os
# import threading
#
# # 由使用者端向伺服器傳資料，檔案
import phe as paillier
import json
import threading
import socket
import tqdm
import os
import cv2
from time import ctime, sleep
def loadAnswer():
    with open('answer.json', 'r') as file: 
        ans=json.load(file)
        answer=json.loads(ans)
        return answer
    
def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p,'q':private_key.q}
	with open('custkeys.json', 'w') as file: 
		json.dump(keys, file)

def getKeys():
	with open('custkeys.json', 'r') as file: 
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key 

def serializeData(public_key, data):
	encrypted_data_list = [public_key.encrypt(x) for x in data]
	encrypted_data={}
	encrypted_data['public_key'] = {'n': public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in         encrypted_data_list]
	serialized = json.dumps(encrypted_data)
	return serialized
	
def recvived(address, port):

    # 傳輸資料間隔符
    SEPARATOR = '<SEPARATOR>'
    # 檔案緩衝區
    Buffersize = 4096*10

    
    print('準備接收新的檔案...')

    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind((address, port))
    recv_data = udp_socket.recvfrom(Buffersize)
    recv_file_info = recv_data[0].decode('utf-8')  # 儲存接收到的資料,檔名
    print(f'接收到的檔案資訊{recv_file_info}')
    c_address = recv_data[1]  # 儲存客戶的地址資訊
        # 列印使用者端ip
    print(f'使用者端{c_address}連線')
        # recv_data = udp_socket.recv()
        # 接收使用者端資訊
        # received = udp_socket.recvfrom(Buffersize).decode()
    filename ,file_size = recv_file_info.split(SEPARATOR)
        # 獲取檔案的名字,大小
    filename = os.path.basename(filename)
    file_size = int(file_size)


        # 檔案接收處理
    progress = tqdm.tqdm(range(file_size), f'接收{filename}', unit='B', unit_divisor=1024, unit_scale=True)

    with open(filename,'wb') as f:
            for _ in progress:
                # 從使用者端讀取資料

                bytes_read = udp_socket.recv(Buffersize)
                # 如果沒有資料傳輸內容
                # print(bytes_read)
                if bytes_read == b'file_download_exit':
                    print('完成傳輸！')
                    print(bytes_read)
                    break
                # 讀取寫入
                f.write(bytes_read)
                # 更新進度條
                progress.update(len(bytes_read))

    udp_socket.close()



def send(address, filename):

    # 傳輸資料間隔符
    SEPARATOR = '<SEPARATOR>'
    # 伺服器資訊
    host, port = address

    # 檔案緩衝區
    Buffersize = 4096*10
    # 傳輸檔案名字
    filename = filename
    # 檔案大小)
    file_size = os.path.getsize(filename)
    # 建立socket連結
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print(f'伺服器連線中{host}:{port}')
    s.connect((host, port))
    print('與伺服器連線成功')

    # 傳送檔案名字和檔案大小，必須進行編碼處理
    # s.sendto(f'{filename}{SEPARATOR}{file_size}'.encode(), ("127.0.0.1", 1234))
    s.send(f'{filename}{SEPARATOR}{file_size}'.encode('utf-8'))

    # 檔案傳輸
    progress = tqdm.tqdm(range(file_size), f'傳送{filename}', unit='B', unit_divisor=1024)


    with open(filename, 'rb') as f:
        # 讀取檔案
        for _ in progress:
            bytes_read = f.read(Buffersize)
            # print(bytes_read)
            if not bytes_read:
                print('exit退出傳輸，傳輸完畢！')
                s.sendall('file_download_exit'.encode('utf-8'))
                break
            # sendall 確保絡忙碌的時候，資料仍然可以傳輸
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)

    # 關閉資源
    s.close()


if __name__ == '__main__':
    newline=[]
    ewline2=[]
    lewline2=[]
    lewline211=[]
    data = [12,2.2,3,4,1,2,233,4,1,42,3,4,1,2,3,4,11,2,3,4,1,2,3,24,1,2,3,64,1,2,323,4,1,2,3,4,121,2,3,4,1,2,3,4,121,2,3,121,2,3,12,2.2,3,4,1,2,233,4,1,42,3,4,1,2,3,4,11,2,3,4,1,2,3,24,1,2,3,64,1,2,323,4,1,2,3,4,121,2,3,4,1,2,3,4,121,2,3,121,2,3]
    data2 = [144,2.2,3,444,1,2,23322412312312,1,42,3,4,1,2,2,3,2224,11,2,3,4,1,2,3,24,1,2,3,64,1,2,323,4,1,2,3,4,121,2,3,4,1,2,3,4,121,2,3,121,2,3,12,2.2,3,4,1,2,233,4,1,42,3,4,1,2,3,4,11,2,3,4,1,2,3,24,1,2,3,64,1,2,323,4,1,2,3,4,121,2,3,4,1,2,3,4,121,2,3,121,2,3]
    pub_key, priv_key = getKeys()
    encrypted_data_list = [pub_key.encrypt(x) for x in data]
    encrypted_data_list2 = [pub_key.encrypt(x) for x in data2]
    for i in range(len(encrypted_data_list)):
        anss=(encrypted_data_list[i]+encrypted_data_list2[i])/2
        newline.append(anss)
    for i in range(len(encrypted_data_list)):
        anss=(newline[i]+encrypted_data_list2[i])/2
        ewline2.append(anss)
    for i in range(len(encrypted_data_list)):
        anss=(ewline2[i]+encrypted_data_list2[i])/2
        lewline2.append(anss)
    for i in range(len(encrypted_data_list)):
        anss=(lewline2[i]+encrypted_data_list2[i])/2
        lewline211.append(anss)

    for i in range(len(newline)):
        print(priv_key.decrypt(lewline2[i]))
    
    
    
    
