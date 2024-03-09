# import socket
# import tqdm
# import os
# import threading
#
# # 由使用者端向伺服器傳資料，檔案
from doctest import testfile
from re import T
import phe as paillier
import json
import threading
import socket
import tqdm
import os
import csv
from time import ctime, sleep
def loadAnswer():
    with open('answer.json', 'r') as file: 
        ans=json.load(file)
        answer=json.loads(ans)
        return answer

def loadPkey():
    with open('DataPUBkeys.json', 'r') as file: 
        dett=json.load(file)
        return dett
    
def storeKeys():
	public_key, private_key = paillier.generate_paillier_keypair()
	keys={}
	keys['public_key'] = {'n': public_key.n}
	keys['private_key'] = {'p': private_key.p,'q':private_key.q}
	with open('custkeys.json', 'w') as file: 
		json.dump(keys, file)
def getData():
	with open('data.json', 'r') as file: 
		d=json.load(file)
	data=json.loads(d)
	return data
def getKeys():
	with open('custkeys.json', 'r') as file: 
		keys=json.load(file)
		pub_key=paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
		priv_key=paillier.PaillierPrivateKey(pub_key,keys['private_key']['p'],keys['private_key']['q'])
		return pub_key, priv_key 

def serializeData(public_key, data, pport):
    
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    encrypted_data={}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['pport'] = {'pp': pport}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    serialized = json.dumps(encrypted_data)
    return serialized

def serializeData2(public_key, data, name):
    
    encrypted_data_list = [public_key.encrypt(x) for x in data]
    encrypted_data={}
    encrypted_data['check'] = {'cc':"sak"}
    encrypted_data['public_key'] = {'n': public_key.n}
    encrypted_data['pport'] = [str(x) for x in name]
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in encrypted_data_list]
    serialized = json.dumps(encrypted_data)
    return serialized

def serializeanss2(public_key, data, pport):
    
    encrypted_data={}
    encrypted_data['check'] = {'cc':"sak"}
    encrypted_data['pubkey'] = {'n': public_key.n}
    encrypted_data['pport'] = {'pp': pport}
    encrypted_data['values'] = [(str(x.ciphertext()), x.exponent) for x in data]
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

def serializeDataan():
	results, pubkey = computeData()
	encrypted_data={}
	encrypted_data['pubkey'] = {'n': pubkey.n}
	encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
	serialized = json.dumps(encrypted_data)
	return serialized
def computeData():
    data=getData()
    testf=[]
    mycoef=[]

    with open('person.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                testf.append(row)
    print(testf)
    for i in range(len(testf)-2):
        mycoef.append(int(float(testf[i+1][0])*100))
    print("computedata:")
    print(mycoef)
    myweight=[0.002,0.002,0.005,0.5,0.5]
    pk=data['public_key']
    pubkey= paillier.PaillierPublicKey(n=int(pk['n']))
    enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in data['values']]
    results=sum([myweight[i]*((mycoef[i]-enc_nums_rec[i])) for i in range(len(mycoef))])
    return results, pubkey


if __name__ == '__main__':
    myport = 1898
    # address = ("127.0.0.1", 1234)
    port = 1248
    address = "127.0.0.1"
    portdata={}
    portdata['check'] = {'cc':"gk"}
    portdata['port'] = {'p':myport}
    serializedport = json.dumps(portdata)
    with open('port.json', 'w') as file:
    	json.dump(serializedport, file)
    targett = (address , port)
    filename= "port.json"
    print("trying to get the publicKey")
    send(targett, filename)
    recvived(address, myport)
    print("Recieved DataPublicKey!!")
    choice_str = input("Ready to Exchange data?(Y/N)")
    if choice_str == "Y":
        storeKeys()
        data = []
        testf=[]
        with open('person.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                testf.append(row)
        for i in range(len(testf)-2):
            data.append(int(float(testf[i+1][0])*100))
            print(testf[i+1][0])
        
        portdata={}
        portdata['check'] = {'cc':"sk"}
        portdata['port'] = {'p':myport}
        serializedport = json.dumps(portdata)
        with open('port.json', 'w') as file:
            json.dump(serializedport, file)
        targett = (address , port)
        filename= "port.json"
        send(targett, filename)
        recvived(address, myport)
        
        clientport=[]
        with open('portpool.json', 'r') as file: 
            d=json.load(file)
        temp=d['pools']
        for i in range(len(temp)-1):
            clientport.append(temp[i])

        print(clientport)

        

        
        sameclient=[]
        
        
            
            
        
        for i in range(len(clientport)):
            print("find my partner")
            port = int(clientport[i])
            address = ('127.0.0.1', port)
            
            	
          
            print(float(testf[1][0]))
            print("my data")
            print(data)
            pub_key, priv_key = getKeys()
            datafile=serializeData(pub_key, data,'1235')
            with open('data.json', 'w') as file:
                json.dump(datafile, file)
                file.close()
            filename = "data.json"
            sleep(0.101)
            send(address, filename)
            port = 1235
            address = "127.0.0.1"
            recvived(address, port)
            answer_file=loadAnswer()
            answer_key=paillier.PaillierPublicKey(n=int(answer_file['pubkey']['n']))
            answer = paillier.EncryptedNumber(answer_key, int(answer_file['values'][0]), int(answer_file['values'][1]))
            print("answer:")
            if (answer_key==pub_key):
                aas=priv_key.decrypt(answer)
                print(aas)
            sameclient.append(i)
            #if(-5<aas<5):
                #sameclient.append(i)
        print("similar client:")
        for i in range(len(sameclient)):
            print("client%d" %((int(sameclient[i]))+2))
        
        myscore=[]
        with open('scores.txt', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                myscore.append(row)
        mynamelist=[]
        resnamelist=[]
        print("My weight now")
        for i in range(len(myscore)):
            print(myscore[i])
            mynamelist.append(myscore[i][0])
        for i in range(len(myscore)):
            resnamelist.append(mynamelist[i])
        ressocelist=[]
        for i in range(len(myscore)):
            ressocelist.append(int(float(myscore[i][1])*1000))
        pp_file=loadPkey()
        pp_key=paillier.PaillierPublicKey(n=int(pp_file['public_key']['n']))
        ressocelist = [pp_key.encrypt(x) for x in ressocelist]
        namelist=[]
        for i in range(len(sameclient)):
            print("Exchange weight...")
            port = int(clientport[sameclient[i]])
            address = ('127.0.0.1', port)
            filename = "data.json"
            sleep(0.101)
            send(address, filename)
            port = 1235
            address = "127.0.0.1"
            recvived(address, port)
            anss=loadAnswer()
            pk=anss['public_key']
            pubkey= paillier.PaillierPublicKey(n=int(pk['n']))
            enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in anss['values']]
            namelist.clear()
            for j in range(len(anss['pport'])):
                namelist.append(anss['pport'][j])
            print(namelist)
            print(len(namelist))
            print(len(enc_nums_rec))
            for j in range(len(namelist)):
                flag=0
                for xx in range(len(resnamelist)):
                    if(namelist[j]==resnamelist[xx]):
                        ressocelist[xx]=(((ressocelist[xx]))+enc_nums_rec[j])/2
                        flag=1
                        break
                if flag!=1:
                    resnamelist.append(namelist[j])
                    resss=enc_nums_rec[j]
                    ressocelist.append(resss)

            #namelist = [for x in anss['pport']]

            
            #resss=[(myscore[i][1]+enc_nums_rec[i])/2 for i in range(len(enc_nums_rec))]
            print(ressocelist)
        datafile=serializeanss2(pubkey, ressocelist, 1235)
        with open('port.json', 'w') as file:
            json.dump(datafile, file)
            file.close()
        filename="port.json"
        addresss = ("127.0.0.1" , 1248)
        send(addresss, filename)
        recvived(address, port)
        finalans=[]
        with open('final.txt') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                finalans.append(row)
        mynamelist.clear()
        for i in range(len(myscore)):
            print(myscore[i])
            mynamelist.append(myscore[i][0])
        newsocre=[]
        for ss in range(len(mynamelist)):
            sleep(0.011)
            newsocre.append(mynamelist[ss]+","+str(float(finalans[ss][0])/1000)+",old")
            print("%s : %f" % (mynamelist[ss] ,float(finalans[ss][0])/1000))

        
        for sss in range(len(resnamelist)-len(mynamelist)):
            sleep(0.011)
            newsocre.append(mynamelist[ss]+","+str(float(finalans[ss][0])/1000)+",new")
            print("%s : %f NEW!!" %(resnamelist[sss+ss+1] ,float(finalans[sss+ss+1][0])/1000))
        print(newsocre)
        with open('scnew.csv', 'w') as file:
            for ii in range(len(newsocre)):
                file.write("%s\n" % (newsocre[ii]))
            

    else:
        print("Wait for Other users")
        port = 1898
        address = "127.0.0.1"
        recvived(address, port)
        datafile=serialized=serializeDataan()
        with open('data.json', 'r') as file: 
            d=json.load(file)
            porttdt=json.loads(d)
            temp=porttdt['pport']
            print(temp)
            temper=int(temp['pp'])
        with open('answer.json', 'w') as file:
            json.dump(datafile, file)
        
        addresss = ("127.0.0.1" , temper)
        filename= "answer.json"

        send(addresss, filename)
        recvived(address, port)
        with open('data.json', 'r') as file: 
            d=json.load(file)
            porttdt=json.loads(d)
            temp=porttdt['pport']
            print(temp)
            temper=int(temp['pp'])
        testf=[]
        weitf=[]
        namef=[]
        with open('scores.txt', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                testf.append(row)
        for i in range(len(testf)):
            weitf.append(int(float(testf[i][1])*1000))
        for i in range(len(testf)):
            namef.append(testf[i][0])
        pp_file=loadPkey()
        pp_key=paillier.PaillierPublicKey(n=int(pp_file['public_key']['n']))
        
        datafile=serializeData2(pp_key, weitf, namef)
        with open('answer.json', 'w') as file:
                json.dump(datafile, file)
                file.close()
        addresss = ("127.0.0.1" , temper)
        filename= "answer.json"
        send(addresss, filename)

    
    
    
    
