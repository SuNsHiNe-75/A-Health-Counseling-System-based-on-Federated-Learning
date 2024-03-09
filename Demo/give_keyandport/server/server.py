from pydoc import cli
import socket
import tqdm
import os
import threading
import phe as paillier
import json
import csv
from time import ctime, sleep
# 使用UDP傳輸視訊，全雙工，但只需一方接，一方收即可

# 設定伺服器的ip和 port
# 伺服器資訊
# sever_host = '127.0.0.1'
# sever_port =1234
def getaddresss():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    asda=s.getsockname()[0]
    s.close()
    return asda

def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p,'q':private_key.q}
	with open('Datakeys.json', 'w') as file: 
		json.dump(keys, file)

def getKeys():
	with open('custkeys.json', 'r') as file: 
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key
def getDKeys():
	with open('Datakeys.json', 'r') as file: 
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key
 

def storePUBKeys():
    pkk={}
    with open('Datakeys.json', 'r') as file: 
        keys=json.load(file)
        pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
    pkk['public_key'] = {'n': pub_key.n}
    with open('DataPUBkeys.json', 'w') as file: 
        json.dump(pkk, file)

def serializeData(public_key, data):
	encrypted_data_list = [public_key.encrypt(x) for x in data]
	encrypted_data={}
	encrypted_data['public_key'] = {'n': public_key.n}
	encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in         encrypted_data_list]
	serialized = json.dumps(encrypted_data)
	return serialized

def serializeportData(data,data2):
    port_data={}
    port_data['pools'] = [(str(x)) for x in data]
    port_data['addrs'] = [(str(x)) for x in data2]
    with open('portpool.json', 'w') as file:
        json.dump(port_data, file)
    return 

def getData():
	with open('data.json', 'r') as file: 
		d=json.load(file)
	data=json.loads(d)
	return data
def serializeDataan():
	results, pubkey = computeData()
	encrypted_data={}
	encrypted_data['pubkey'] = {'n': pubkey.n}
	encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
	serialized = json.dumps(encrypted_data)
	return serialized
def computeData():
	data=getData()
	mycoef=[5,6,7,8]
	print("computedata:")
	print(mycoef)
	myweight=[0.5,0.5,0.2,1]
	pk=data['public_key']
	pubkey= paillier.PaillierPublicKey(n=int(pk['n']))
	enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in data['values']]
	results=sum([myweight[i]*(mycoef[i]-enc_nums_rec[i]) for i in range(len(mycoef))])
	return results, pubkey


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
    while((s.connect((host, port)))):
        print('伺服器連線中...')
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
                s.close()
                break
            # sendall 確保絡忙碌的時候，資料仍然可以傳輸
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)
    # 關閉資源
    s.close()


def recvived(address, port):

    # 傳輸資料間隔符
    SEPARATOR = '<SEPARATOR>'
    # 檔案緩衝區
    Buffersize = 4096*10


    print('Waiting for new client!')

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

if __name__ == '__main__':
    cliarr=[]
    cliadd=[]
    # address = ("127.0.0.1", 1234)
    port = 1248
    address = getaddresss()
    #storeKeys()
    #storePUBKeys()
    while 1:
        port = 1248
        address = getaddresss()
        address=str(address)
        recvived(address, port)
        with open('port.json', 'r') as file: 
            d=json.load(file)
        porttdt=json.loads(d)
        temp=porttdt['check']
        print(temp)
        temper=temp['cc']
        print(temper)
        if(temper == "gk"):
            temp=porttdt['port']
            clientport = temp['p']
            cliarr.append(clientport)
            temp=porttdt['addr']
            clientaddr = temp['ad']
            cliadd.append(clientaddr)
            serializeportData(cliarr,cliadd)
            print(clientport)
            print("Connected to the client and sending DataPublicKey!!")
            location=(clientaddr,clientport)
            filename="DataPUBkeys.json"
            sleep(0.101)
            send(location, filename)
        if(temper == "sk"):
            temp=porttdt['port']
            clientport = temp['p']
            temp=porttdt['addr']
            clientaddr = temp['ad']
            location=(clientaddr ,clientport)
            filename="portpool.json"
            sleep(0.101)
            send(location, filename)
        if(temper == "sak"):
            anss=[]
            answer_key=paillier.PaillierPublicKey(n=int(porttdt['pubkey']['n']))
            print("answer:")
            for i in range(len(porttdt['values'])):
                answer = paillier.EncryptedNumber(answer_key, int(porttdt['values'][i][0]), int(porttdt['values'][i][1]))
                pub_key, priv_key=getDKeys()
                aas=priv_key.decrypt(answer)
                print(aas)
                anss.append(aas)
            with open("final.txt","w") as f:                                   
                for i in anss:                                                               
                    f.write(str(i))
                    f.write("\n")
            temp=porttdt['pport']
            clientport = temp['pp']
            temp=porttdt['addr']
            clientaddr = temp['ad']
            location=(clientaddr,clientport)
            filename="final.txt"
            sleep(0.101)
            send(location, filename) 
                    
