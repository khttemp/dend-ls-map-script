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

print("DEND LS MAP SCRIPT ver1.0.0...")
file = input("railのbinファイル名を入力してください: ")

readFlag = False
printRailFlag = False

try:
    try:
        f = open(file, "rb")
        line = f.read()
        f.close()
    except FileNotFoundError:
        errorMsg = "指定されたファイルが見つかりません。終了します。"
        print(errorMsg)
        input()
        sys.exit()

    print("見つけました！")
    size = len(line)

    index = 16
    header = line[0:index]
    if header == b'DEND_MAP_VER0101':
        print("まだ未対応のMapデータです")
        raise Exception
    elif header != b'DEND_MAP_VER0100':
        print("LSのMapではありません")
        raise Exception

    #Model
    readModelCnt = line[index]
    index += 1
    for i in range(readModelCnt):
        modelNameLen = line[index]
        index += 1
        modelName = line[index:index+modelNameLen].decode("shift-jis")
        index += modelNameLen
        print("index:{0} -> {1}".format(i, modelName), end=", ")
        for j in range(2):
            print(line[index], end=", ")
            index += 1
        cnt = line[index]
        if cnt != 0xFF:
            index += 1
            print("[", end="")
            for j in range(cnt):
                for k in range(2):
                    print(readBinary(line[index:index+2], "short"), end=", ")
                    index += 2
            print("]", end="")
        else:
            print(line[index], end=", ")
            index += 1
        print()
    print()

    #Music
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

    #RailName
    readRailNameLen = line[index]
    index += 1
    print("RailName:{0}".format(line[index:index+readRailNameLen].decode("shift-jis")))
    index += readRailNameLen

    #???
    index += 0x20
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
    
    #Rail
    readRailCnt = readBinary(line[index:index+2], "short")
    index += 2
    print("RailCnt:{0}".format(readRailCnt))
    if not printRailFlag:
        print("Rail情報省略")
    for i in range(readRailCnt):
        if printRailFlag:
            print("index{0}".format(i))
        for j in range(2):
            temp = readBinary(line[index:index+4], "float")
            index += 4
            temp2 = readBinary(line[index:index+4], "float")
            index += 4
            temp3 = readBinary(line[index:index+4], "float")
            index += 4
            if printRailFlag:
                print("[{0}, {1}, {2}]".format(temp, temp2, temp3), end=", ")

        temp4 = line[index]
        index += 1
        temp5 = readBinary(line[index:index+2], "short")
        index += 2

        if printRailFlag:
            print("[{0}, {1}]".format(temp4, temp5), end=", ")
        if temp5 == -1:
            if printRailFlag:
                print("(", end="")
            for j in range(3):
                temp6 = readBinary(line[index:index+4], "float")
                index += 4
                if printRailFlag:
                    print("{0}".format(temp6), end=", ")
            if printRailFlag:
                print(")", end="")

        if printRailFlag:
            print()
            print("[", end="")
        for j in range(3):
            temp7 = line[index]
            index += 1
            if printRailFlag:
                print("{0}".format(temp7), end=", ")

        if printRailFlag:
            print("]", end=", ")

        for j in range(2):
            if printRailFlag:
                print("[", end="")
            for k in range(3):
                temp8 = readBinary(line[index:index+4], "float")
                index += 4
                if printRailFlag:
                    print("{0}".format(temp8), end=", ")
            temp9 = line[index]
            index += 1
            if printRailFlag:
                print("{0}]".format(temp9), end=", ")
        if printRailFlag:
            print()
        temp10 = readBinary(line[index:index+4], "float")
        index += 4
        if printRailFlag:
            print("{0}".format(temp10), end=", ")

        if printRailFlag:
            print("[", end="")
        for j in range(2):
            temp11 = readBinary(line[index:index+2], "short")
            index += 2
            if printRailFlag:
                print("{0}".format(temp11), end=", ")
        if printRailFlag:
            print("]")

        r = line[index]
        index += 1
        for j in range(r):
            temp12 = readBinary(line[index:index+2], "short")
            index += 2
            temp13 = readBinary(line[index:index+2], "short")
            index += 2
            if printRailFlag:
                print("next{0}:[{1},{2}]".format(j, temp12, temp13), end=", ")
            temp14 = readBinary(line[index:index+2], "short")
            index += 2
            temp15 = readBinary(line[index:index+2], "short")
            index += 2
            if printRailFlag:
                print("prev{0}:[{1},{2}]".format(j, temp14, temp15))

        temp16 = line[index]
        index += 1
        if temp16 != 0:
            for j in range(temp16):
                temp17 = readBinary(line[index:index+2], "short")
                index += 2
                temp18 = readBinary(line[index:index+2], "short")
                index += 2
                temp19 = line[index]
                index += 1
                if printRailFlag:
                    print("???:{0},{1},{2}".format(temp17, temp18, temp19))

        if printRailFlag:
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

        print("[{0},{1}]".format(temp20, temp21), end=", ")
        
        print("[", end="")
        for j in range(6):
            temp22 = readBinary(line[index:index+4], "float")
            index += 4
            print("{0}".format(temp22), end=", ")
        print("]")
    print()
    
    #???
    cnt = line[index]
    index += 1
    for i in range(cnt):
        print("[", end="")
        for j in range(3):
            temp23 = readBinary(line[index:index+4], "float")
            index += 4
            print("{0}".format(temp23), end=", ")
        print("]", end=", ")
        index += 1
    print()

    #CPU Data
    print()
    readCpuDataCnt = line[index]
    index += 1
    for i in range(readCpuDataCnt):
        print("[", end="")
        railNo = readBinary(line[index:index+2], "short")
        index += 2
        print("{0}".format(railNo), end=", ")
        for j in range(6):
            temp25 = readBinary(line[index:index+4], "int")
            index += 4
            print("{0}".format(temp25), end=", ")
        print()

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
        default = readBinary(line[index:index+4], "float")
        index += 4
        print("{0}, {1}, {2}, {3}, {4}, {5}, {6}".format(cpuNo, cpuType, minLen, maxLen, maxSpeed, minSpeed, default), end=", ")
        for j in range(3):
            temp26 = readBinary(line[index:index+4], "float")
            index += 4
            print("{0}".format(temp26), end=", ")
        print("]")
    print()

    #COMIC SCRIPT
    readComicScriptCnt = line[index]
    index += 1
    for i in range(readComicScriptCnt):
        comicNum = readBinary(line[index:index+2], "short")
        index += 2
        comicType = line[index]
        index += 1
        eventRailNo = readBinary(line[index:index+2], "short")
        index += 2
        print("{0}, {1}, {2}".format(comicNum, comicType, eventRailNo), end=", ")
        for j in range(9):
            temp27 = readBinary(line[index:index+4], "float")
            index += 4
            print("{0}".format(temp27), end=", ")
        print()
    print()
        

except Exception as e:
    print(e)
    sys.exit()
