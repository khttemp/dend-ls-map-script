import struct
import os
import sys

def readBinary(line, mode):
    if mode == "short":
        s = struct.unpack("<h", line)[0]
        return s
    elif mode == "ushort":
        s = struct.unpack("<H", line)[0]
        return s
    elif mode == "int":
        i = struct.unpack("<i", line)[0]
        return i
    elif mode == "float":
        f = struct.unpack("<f", line)[0]
        return round(f, 3)
    else:
        return None

def writeText(w, line, mode):
    if mode == "shortHex":
        for i in range(2):
            text = str(hex(line[i]))[2:]
            if len(text) == 1:
                text = "0" + text
            w.write(text)
    elif mode == "ushortHex":
        for i in range(2):
            text = str(hex(line[i]))[2:]
            if len(text) == 1:
                text = "0" + text
            w.write(text)
    elif mode == "intHex":
        for i in range(4):
            text = str(hex(line[i]))[2:]
            if len(text) == 1:
                text = "0" + text
            w.write(text)
    elif mode == "floatHex":
        for i in range(4):
            text = str(hex(line[i]))[2:]
            if len(text) == 1:
                text = "0" + text
            w.write(text)
    elif mode == "charHex":
        text = str(hex(line))[2:]
        if len(text) == 1:
            text = "0" + text
        w.write(text)
        
    elif mode == "short":
        s = struct.unpack("<h", line)[0]
        w.write(str(s))
    elif mode == "ushort":
        s = struct.unpack("<H", line)[0]
        w.write(str(s))
    elif mode == "int":
        i = struct.unpack("<i", line)[0]
        w.write(str(i))
    elif mode == "float":
        f = struct.unpack("<f", line)[0]
        w.write(str(f))
    elif mode == "char":
        w.write(str(line))

print("DEND LS MAP REWRITE SCRIPT ver1.0.0...")
print("現在、ModelNoの辺りとレール情報のみ書き込み可能")
file = input("railのbinファイル名を入力してください: ")

flag = False
byteFiles = None
railDict = []
railCntIndex = -1
railEndIndex = -1

try:
    try:
        f = open(file, "rb")
        line = f.read()
        f.close()
        byteFiles = bytearray(line)
        filename = os.path.splitext(os.path.basename(file))[0]
    except FileNotFoundError:
        errorMsg = "指定されたファイルが見つかりません。終了します。"
        print(errorMsg)
        input()
        sys.exit()

    print("見つけました！")
    size = len(line)

    index = 16
    header = line[0:index]
    if header != b'DEND_MAP_VER0100' and header != b'DEND_MAP_VER0101':
        print("LSのMapではありません")
        raise Exception
    if header == b'DEND_MAP_VER0101':
        flag = True

    #Model
    readModelCnt = line[index]
    index += 1
    for i in range(readModelCnt):
        modelNameLen = line[index]
        index += 1
        index += modelNameLen
        for j in range(2):
            index += 1
        cnt = line[index]
        if cnt != 0xFF:
            index += 1
            for j in range(cnt):
                for k in range(2):
                    index += 2
        else:
            index += 1

    #Music
    readMusicNameLen = line[index]
    index += 1
    index += readMusicNameLen
    readMusicFileLen = line[index]
    index += 1
    index += readMusicFileLen
    index += 4
    index += 4

    #RailName
    readRailNameLen = line[index]
    index += 1
    index += readRailNameLen
    
    #???
    index += 0x3
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 4

    #ToRailCnt
    readToRailCnt = line[index]
    index += 1
    for i in range(readToRailCnt):
        index += 2
        index += 2
        index += 2
        index += 2
        index += 1

    #Rail
    railCntIndex = index
    readRailCnt = readBinary(line[index:index+2], "short")
    index += 2
    for i in range(readRailCnt):
        railInfo = []
        startIdx = index
        if flag:
            temp = readBinary(line[index:index+2], "short")
            
            index += 2
            if temp != -1:
                for j in range(6):
                    index += 4
        for j in range(2):
            index += 4
            index += 4
            index += 4

        endIdx = index
        railInfo.append(line[startIdx:endIdx])
        
        #Model No?
        index += 1
        #block?
        temp = readBinary(line[index:index+2], "short")
        index += 2

        startIdx = index
        if temp == -1:
            for j in range(3):
                index += 4

        for j in range(3):
            index += 1

        for j in range(2):
            for k in range(3):
                index += 4
            index += 1

        #0x0000803F
        index += 4

        #Flg?
        index += 4
        
        endIdx = index
        railInfo.append(line[startIdx:endIdx])
        railDict.append(railInfo)

        #RailInfo
        r = line[index]
        index += 1
        for j in range(r):
            #next rail
            index += 2
            index += 2
            
            #prev rail
            index += 2
            index += 2

        #rail effect?
        temp = line[index]
        index += 1
        if temp != 0:
            for j in range(temp):
                index += 1
                index += 1
                index += 1
                index += 1
                index += 1

    railEndIndex = index
    #StationName
    readStationNameCnt = line[index]
    index += 1
    for i in range(readStationNameCnt):
        readNameLen = line[index]
        index += 1
        index += readNameLen
        
        index += 1
        index += 2
        
        for j in range(6):
            index += 4
    
    #Camera
    cnt = line[index]
    index += 1
    flg = 0
    for i in range(cnt):
        for j in range(flg):
            for k in range(4):
                index += 4
            index += 1
        for j in range(3):
            index += 4
        flg = line[index]
        index += 1

    #CPU Data
    readCpuDataCnt = line[index]
    index += 1
    for i in range(readCpuDataCnt):
        #railNo
        index += 2
        for j in range(6):
            index += 4

        #cpuNo = line[index]
        index += 1
        #cpuType = line[index]
        index += 1
        #minLen = readBinary(line[index:index+4], "float")
        index += 4
        #maxLen = readBinary(line[index:index+4], "float")
        index += 4
        #maxSpeed = readBinary(line[index:index+4], "float")
        index += 4
        #minSpeed = readBinary(line[index:index+4], "float")
        index += 4
        #default = readBinary(line[index:index+4], "float")
        index += 4
        for j in range(3):
            index += 4

    #COMIC SCRIPT
    readComicScriptCnt = line[index]
    index += 1
    for i in range(readComicScriptCnt):
        #comicNum = readBinary(line[index:index+2], "short")
        index += 2
        #comicType = line[index]
        index += 1
        #eventRailNo = readBinary(line[index:index+2], "short")
        index += 2
        #print("{0}, {1}, {2}".format(comicNum, comicType, eventRailNo), end=", ")
        for j in range(9):
            #temp27 = readBinary(line[index:index+4], "float")
            index += 4
            #print("{0}".format(temp27), end=", ")
        #print()
    #print()

    #rewriteFile
    try:
        f = open(filename + ".csv")
        writeLines = f.readlines()
        f.close()
    except:
        errorMsg = "書き込みするファイルが見つかりません。終了します。"
        print(errorMsg)
        input()
        sys.exit()

    idx = railCntIndex
    newByteFile1 = byteFiles[0:railCntIndex]
    numList = struct.pack("<h", readRailCnt)
    newByteFile = bytearray()
    newByteFile2 = byteFiles[railEndIndex:]

    if flag:
        modelNoIdx = 13
        railInfoIdx = 31
    else:
        modelNoIdx = 6
        railInfoIdx = 24

    count = 0
    for wL in writeLines:
        wL = wL.strip()
        arr = wL.split(",")
        if "RailCnt:" in arr[0]:
            cnt = int(arr[0].strip("RailCnt:"))
            num = struct.pack("<h", cnt)
            newByteFile += num
            continue
        else:
            newByteFile += railDict[count][0]
            
            modelNo = int(arr[modelNoIdx])
            num = struct.pack("<c", bytes([modelNo]))
            newByteFile += num
            
            block = int(arr[modelNoIdx+1])
            num = struct.pack("<h", block)
            newByteFile += num

            newByteFile += railDict[count][1]

            railInfoCnt = int(arr[railInfoIdx])
            num = struct.pack("<c", bytes([railInfoCnt]))
            newByteFile += num
            for i in range(railInfoCnt):
                for j in range(4):
                    rail = int(arr[railInfoIdx + 4*i + j + 1])
                    num = struct.pack("<h", rail)
                    newByteFile += num

            effectIdx = railInfoIdx + 4 * railInfoCnt + 1
            effectCnt = int(arr[effectIdx])
            num = struct.pack("<c", bytes([effectCnt]))
            newByteFile += num
            for i in range(effectCnt):
                for j in range(5):
                    eff = int(arr[effectIdx + 5*i + j + 1])
                    num = struct.pack("<c", bytes([eff]))
                    newByteFile += num

            count += 1

    newFile = newByteFile1 + newByteFile + newByteFile2
    w = open(filename + "_new.bin", "wb")
    w.write(newFile)
    w.close()
        
except Exception as e:
    print(e)
    sys.exit()
