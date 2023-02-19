import sys

HEADER_FILECODESIZE = 32

HEADER_NUMENTRIES = 0x20
HEADER_HEADERSIZE = 0x28
HEADER_OFFSETDICT = 0x30
HEADER_OFFSETTEXT = 0x38
HEADER_SIZEOFTEXT = 0x40

OFFSET_STARTOFDICT = 0x48

ENTRY_SIZE = 12

def encode(inf, outf):
    print('Input file: ' + inf)
    print('Output file: ' + outf)
    blockotext = bytearray()
    dictionary = bytearray()
    entryoffset = 0
    entrycount = 0

    with open(inf, 'rb') as cleartext:
        for line in cleartext.read().splitlines():
            line = line.replace(b"\x5c\x6e", b"\x0a")
            blockotext.extend(line)
            linelen = len(line)
            dictionary.extend(entryoffset.to_bytes(8, byteorder='little'))
            dictionary.extend(linelen.to_bytes(4, byteorder='little'))
            entryoffset = entryoffset + linelen
            entrycount = entrycount + 1

    print('ENTRIES: ' + str(entrycount))
    print('DICTIONARY SIZE: ' + str(entrycount*12))
    print('DICTIONARY END/TEXT START: ' +  str(entrycount*12+OFFSET_STARTOFDICT))
    print('TEXT SIZE: ' +  str(len(blockotext)))

    with open(outf, 'wb') as binfile:
        binfile.write("AVAFDICT 2.0   \0".encode('utf_16_le'))
        binfile.write(int(entrycount/2).to_bytes(8, byteorder='little'))#key-value pairs
        binfile.write((OFFSET_STARTOFDICT).to_bytes(8, byteorder='little'))#header size/dict offset, hardcoded, unlikely to change, if it does everything's fucked anyway
        binfile.write((entrycount*12).to_bytes(8, byteorder='little'))#size of dict = entries * 12
        binfile.write((entrycount*12+OFFSET_STARTOFDICT).to_bytes(8, byteorder='little'))#text start = header + size of dict
        binfile.write(len(blockotext).to_bytes(8, byteorder='little'))#text start = header + size of dict
        binfile.write(dictionary)
        binfile.write(blockotext)

def main(argv):
    inf = argv[0]
    outf = argv[1] if len(argv) > 1 else inf + '.encoded.bin'
    encode(inf, outf)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print ("Arguments: <inputfile> (<outputfile>)\nSpecify decoded file as input, it'll be decoded in the specified output file, or 'input.encoded.bin' by defaut")
        exit(0)
    main(sys.argv[1:])
