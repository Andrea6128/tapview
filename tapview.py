import sys


# TAP Viewer
print("tapview - ZX Spectrum TAP file viewer v0.1 - (c) 2020 Aki")
print("Usage: python tapview.py [TAP file]")
print()

# converts to lower case and saves shell argument into FILE var
FILE = sys.argv[1].lower()

# set global things
hex_numbers = ["0", "1", "2", "3", "4", "5", "6", "7",
               "8", "9", "a", "b", "c", "d", "e", "f"]
header = [[]]

# check cmd line stuff
if "-h" in FILE or "--help" in FILE:
    print("This program shows content of a ZX Spectrum TAP file.")
    sys.exit()

if ".tap" not in FILE:
    print("Please enter a valid TAP file (example: manicminer.tap)")
    sys.exit()


def open_file():
    with open(FILE, "rb") as file:
        content = file.read()
        print("TAP file inspected:", FILE)
        print()
        return content

def search_for_headers(content):
    header_count = 0
    for byte in range(len(content)):
        if content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 0 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 1 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 2 \
            or content[byte] == 19 and content[byte + 1] == 0 and content[byte + 2] == 0 and content[byte + 3] == 3:
            for i in range(byte, byte + 19):
                header[header_count].append(str(content[i]))
            # print("header=", header)
            header_count += 1
            header.append([])
    return True

def parse_single_header(header):
    # something that has to be done (why?????????????? idk)
    header.pop(-1)
    # header[0].pop(0)

    for sub_header in header:
        # show header number
        print("Header number:", header.index(sub_header))

        # convert strings to integers
        for i in range(len(sub_header)):
            sub_header[i] = int(sub_header[i])

        # print("sub_header=", sub_header)
        for index in range(len(sub_header)):
            # print("index=", index)

            # flag byte (header)
            if index == 2:
                if sub_header[index] == 0:
                    print("Flag: header")
                if sub_header[index] == 255:
                    print("Flag: body")

            # file type
            if index == 3:
                if sub_header[index] == 0:
                    print("Type: Program")
                if sub_header[index] == 1:
                    print("Type: Number array")
                if sub_header[index] == 2:
                    print("Type: Character array")
                if sub_header[index] == 3:
                    print("Type: Bytes")

            # file name
            if index == 4:
                print("Filename: ", end="")
                for character in range(4, 14):
                    print(chr(sub_header[character]), end="")

            # length of body
            if index == 14:
                print()
                highByte = hex(sub_header[index + 1])[2:]
                lowByte = hex(sub_header[index])[2:]
                if highByte in hex_numbers:
                    highByte = "0" + highByte
                if lowByte in hex_numbers:
                    lowByte = "0" + lowByte
                byteHex = int("0x" + highByte + lowByte, 16)
                print("Length:", byteHex, " Hex:", hex(byteHex))
            
            # start address
            if index == 16:
                highByte = hex(sub_header[index + 1])[2:]
                lowByte = hex(sub_header[index])[2:]
                if highByte in hex_numbers:
                    highByte = "0" + highByte
                if lowByte in hex_numbers:
                    lowByte = "0" + lowByte
                byteHex = int("0x" + highByte + lowByte, 16)
                print("Start:", byteHex, " Hex:", hex(byteHex))
                
        print()  # insert empty line

if __name__ == '__main__':
    content = open_file()
    if search_for_headers(content) == True:
        parse_single_header(header)
    else:
        print("No header found.")
    print("Done.")
