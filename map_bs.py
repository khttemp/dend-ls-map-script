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

print("DEND BS MAP SCRIPT ver1.0.0...")
file = input("railのbinファイル名を入力してください: ")

readFlag = False
printRailFlag = False
flag = True

railDict = []

try:
    try:
        f = open(file, "rb")
        line = f.read()
        f.close()
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
    if header != b'DEND_MAP_VER0102':
        print("BSのMapではありません")
        raise Exception

    #RailName
    readRailNameLen = line[index]
    index += 1
    print("RailName:{0}".format(line[index:index+readRailNameLen].decode("shift-jis")))
    index += readRailNameLen
    print()

    #Music(ダミー)
    musicCnt = line[index]
    index += 1

    for i in range(musicCnt):
        readMusicNameLen = line[index]
        index += 1
        print("MusicName:{0}".format(line[index:index+readMusicNameLen].decode("shift-jis")))
        index += readMusicNameLen
        readMusicFileLen = line[index]
        index += 1
        print("MusicFile:{0}".format(line[index:index+readMusicFileLen].decode("shift-jis")))
        index += readMusicFileLen
        print("Start       :{0}".format(readBinary(line[index:index+4], "float")))
        index += 4
        print("Loop Start  :{0}".format(readBinary(line[index:index+4], "float")))
        index += 4
    print()

    #ToRailCnt
    readToRailCnt = line[index]
    index += 1
    for i in range(readToRailCnt):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        railPos = readBinary(line[index:index+2], "short")
        index += 2
        a = readBinary(line[index:index+2], "short")
        index += 2
        b = readBinary(line[index:index+2], "short")
        index += 2
        print("{0}P -> [{1},{2},{3},{4}]".format(i+1,railNo, railPos, a, b))
        index += 1
    print()

    ##########unknown
    for i in range(2):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        railPos = readBinary(line[index:index+2], "short")
        index += 2
        temp = line[index]
        index += 1
        tempF = readBinary(line[index:index+4], "float")
        index += 4
        print("{0},{1},{2},{3}".format(railNo, railPos, temp, tempF))

    for i in range(2):
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        railPos = readBinary(line[index:index+2], "short")
        index += 2
        temp = line[index]
        index += 1
        tempF = readBinary(line[index:index+4], "float")
        index += 4
        temp2 = line[index]
        index += 1
        print("{0},{1},{2},{3},{4}".format(railNo, railPos, temp, tempF, temp2))

    tempF = readBinary(line[index:index+4], "float")
    index += 4
    print(tempF)

    cnt = line[index]
    index += 1
    for i in range(cnt):
        tempF = readBinary(line[index:index+4], "float")
        index += 4
        temp2F = readBinary(line[index:index+4], "float")
        index += 4

        index += 3
        print("{0},{1}".format(tempF, temp2F))
    print()
    ##########unknown

    #Light情報
    print("Read Light...")
    lightCnt = line[index]
    index += 1
    for i in range(lightCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        print("{0} -> {1}".format(i, text))
        index += b
    print()

    print("Read Object Bin...")
    binCnt = line[index]
    index += 1
    for i in range(binCnt):
        b = line[index]
        index += 1
        text = line[index:index+b].decode()
        print("{0} -> {1}".format(i, text))
        index += b
    print()

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 5
    ##########unknown
    
    #Model
    print("Read smf...")
    readModelCnt = line[index]
    index += 1
    for i in range(readModelCnt):
        modelNameLen = line[index]
        index += 1
        modelName = line[index:index+modelNameLen].decode("shift-jis")
        index += modelNameLen
        print("index:{0} -> {1}".format(i, modelName), end=", ")
        for j in range(3):
            print(line[index], end=", ")
            index += 1
        cnt = line[index]
        if cnt != 0xFF:
            index += 1
            print("[", end="")
            for j in range(cnt):
                for k in range(6):
                    print(line[index], end=", ")
                    index += 1
            print("]", end="")
        else:
            print(line[index], end=", ")
            index += 1
        print()
    print()

    #StationName
    readStationNameCnt = line[index]
    index += 1
    for i in range(readStationNameCnt):
        readNameLen = line[index]
        index += 1
        name = line[index:index+readNameLen].decode("shift-jis")
        index += readNameLen
        print("index{0} -> {1}".format(i, name), end=", ")

        temp20 = line[index]
        index += 1
        temp21 = readBinary(line[index:index+2], "short")
        index += 2

        print("[{0},{1}]".format(temp20, temp21))
    print()

    ##########unknown
    cnt = line[index]
    index += 1
    for i in range(cnt):
        index += 0x11
    print()
    ##########unknown

    
    #CPU Data
    print("Read Cpu Data...")
    readCpuDataCnt = line[index]
    index += 1
    for i in range(readCpuDataCnt):
        print("[", end="")
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        print("{0}".format(railNo), end=", ")

        cpuNo = line[index]
        index += 1
        cpuType = line[index]
        index += 1
        minLen = readBinary(line[index:index+4], "float")
        index += 4
        maxLen = readBinary(line[index:index+4], "float")
        index += 4
        maxSpeed = readBinary(line[index:index+4], "float")
        index += 4
        minSpeed = readBinary(line[index:index+4], "float")
        index += 4
        print("{0}, {1}, {2}, {3}, {4}, {5}".format(cpuNo, cpuType, minLen, maxLen, maxSpeed, minSpeed), end=", ")
        print("]")
    print()

    #COMIC SCRIPT
    print("Read Comic Script...")
    readComicScriptCnt = line[index]
    index += 1
    for i in range(readComicScriptCnt):
        comicNum = readBinary(line[index:index+2], "short")
        index += 2
        comicType = line[index]
        index += 1
        eventRailNo = readBinary(line[index:index+2], "short")
        index += 2
        print("{0}, {1}, {2}".format(comicNum, comicType, eventRailNo))
    print()

    print(hex(index))
    #Rail
    writeTxt = filename + ".csv"
    w = open(writeTxt, "w")
    readRailCnt = readBinary(line[index:index+2], "short")
    w.write("RailCnt:{0}\n".format(readRailCnt))
    index += 2
    print("RailCnt:{0}".format(readRailCnt))

    for i in range(readRailCnt):
        temp = readBinary(line[index:index+2], "short")
        writeText(w, line[index:index+2], "short")
        w.write(",")
        index += 2
        if temp == -1:
            writeText(w, line[index:index+2], "short")
            w.write(",")
            index += 2
            for j in range(6):
                writeText(w, line[index:index+4], "float")
                w.write(",")
                index += 4
        else:
            for j in range(7):
                w.write(",")

        writeText(w, line[index], "char")
        w.write(",")
        index += 1

        for j in range(3):
            writeText(w, line[index:index+4], "float")
            w.write(",")
            index += 4
        
        for j in range(3):
            writeText(w, line[index], "char")
            w.write(",")
            index += 1

        #0x0000803F
        writeText(w, line[index:index+4], "floatHex")
        w.write(",")
        index += 4

        #Flg
        for j in range(4):
            writeText(w, line[index], "char")
            w.write(",")
            index += 1

        r = line[index]
        writeText(w, line[index], "char")
        w.write(",")
        index += 1
        railInfo = {"prev":[], "next":[]}
        for j in range(r):
            nextRail = []
            prevRail = []
            writeText(w, line[index:index+2], "short")
            w.write(",")
            nextRail.append(readBinary(line[index:index+2], "short"))
            index += 2
            writeText(w, line[index:index+2], "short")
            w.write(",")
            nextRail.append(readBinary(line[index:index+2], "short"))
            index += 2
            railInfo["next"].append(nextRail)
            
            writeText(w, line[index:index+2], "short")
            w.write(",")
            prevRail.append(readBinary(line[index:index+2], "short"))
            index += 2
            writeText(w, line[index:index+2], "short")
            w.write(",")
            prevRail.append(readBinary(line[index:index+2], "short"))
            index += 2
            railInfo["prev"].append(prevRail)

        railDict.append(railInfo)

        temp = line[index]
        writeText(w, line[index], "char")
        w.write(",")
        index += 1

        for j in range(temp):
            for k in range(4):
                writeText(w, line[index], "char")
                w.write(",")
                index += 1

            for k in range(7):
                writeText(w, line[index:index+4], "float")
                w.write(",")
                index += 4
            
        temp = line[index]
        writeText(w, line[index], "char")
        w.write(",")
        index += 1

        for j in range(temp):
            for k in range(4):
                writeText(w, line[index:index+2], "short")
                w.write(",")
                index += 2

        w.write("\n")
    w.close()

    print("Map End!")
        
except Exception as e:
    print(e)
    sys.exit()
