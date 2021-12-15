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
        return f
    else:
        return None

print("DEND LS MAP SCRIPT ver1.0.0...")
file = input("railのbinファイル名を入力してください: ")

readFlag = False

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
    if header != b'DEND_MAP_VER0100' and header != b'DEND_MAP_VER0101':
        print("LSのMapではありません")
        raise Exception

    #Model
    readModelCnt = line[index]
    index += 1
    for i in range(readModelCnt):
        modelNameLen = line[index]
        index += 1
        modelName = line[index:index+modelNameLen]
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
    print("MusicName:{0}".format(line[index:index+readMusicNameLen]))
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
    print("RailName:{0}".format(line[index:index+readRailNameLen]))
    index += readRailNameLen

except Exception as e:
    print(e)
    sys.exit()
