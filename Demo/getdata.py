import serial

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1
tt=0
ss=0
while True:
    for line in ser.read():
        
        print(str(count) + str(': ') + chr(line) )
        count = count+1
        if chr(line)=='0' or chr(line)=='1' or chr(line)=='2' or chr(line)=='3' or chr(line)=='4' or chr(line)=='5' or chr(line)=='6' or chr(line)=='7'  or chr(line)=='8' or chr(line)=='9':
            tt=tt*10+int(line)-48
        if chr(line)==',':
            ss+=1
            if ss==1:
                
                path2 = 'steps.csv'
                with open(path2, 'a') as ff:
                    ff.write('\n')
                    ff.write(str(tt))
                ff.close()
            path = 'personal.csv'
            with open(path, 'a') as f:
                f.write('\n')
                f.write(str(tt))
            f.close()
            tt=0
        if ss==2:
         exit()
ser.close()
