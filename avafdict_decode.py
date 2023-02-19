import sys
import struct

HEADER_FILECODESIZE = 32

HEADER_NUMENTRIES = 0x20
HEADER_HEADERSIZE = 0x28
HEADER_OFFSETDICT = 0x30
HEADER_OFFSETTEXT = 0x38
HEADER_SIZEOFTEXT = 0x40

OFFSET_STARTOFDICT = 0x48
ENTRY_SIZE = 12

def decode(inf, outf):
    print('Input file: ' + inf)
    print('Output file: ' + outf)
    with open(inf, 'rb') as binfile:
        di = binfile.read()
        numEntries = struct.unpack("Q", di[HEADER_NUMENTRIES:HEADER_NUMENTRIES+8])[0]
        headerSize = struct.unpack("Q", di[HEADER_HEADERSIZE:HEADER_HEADERSIZE+8])[0]
        dictSize = struct.unpack("Q", di[HEADER_OFFSETDICT:HEADER_OFFSETDICT+8])[0]
        textblockOffset = struct.unpack("Q", di[HEADER_OFFSETTEXT:HEADER_OFFSETTEXT+8])[0]
        textblockSize = struct.unpack("Q", di[HEADER_SIZEOFTEXT:HEADER_SIZEOFTEXT+8])[0]

        print('format: (' + str(di[0:HEADER_FILECODESIZE].decode("utf-16le")) + ')')
        print('ENTRIES: ' + str(numEntries))
        print('HEADER SIZE: ' + str(headerSize))
        print('DICTIONARY SIZE: ' + str(dictSize))
        print('DICTIONARY END/TEXT START: ' +  str(textblockSize))
        print('TEXT SIZE: ' +  str(textblockSize))

        dictionary = di[headerSize:textblockOffset]
        rawtext    = di[textblockOffset:textblockOffset+textblockSize]

        with open(outf, 'wb') as cleartext:
            for entryindex in range(0, numEntries*2):
                entryoffset = entryindex*ENTRY_SIZE
                textoffset = struct.unpack("Q", dictionary[entryoffset:entryoffset+8])[0]
                textsize = struct.unpack("i", dictionary[entryoffset+8:entryoffset+12])[0]

                cleartext.write(rawtext[textoffset:textoffset+textsize].replace(b"\x0a", b"\x5c\x6e"))#replace newlines by "\n"
                cleartext.write(b"\x0d\x0a")#insert newlines between entries

def main(argv):
    inf = argv[0]
    outf = argv[1] if len(argv) > 1 else inf + '.decoded.txt'
    decode(inf, outf)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print ("Arguments: <inputfile> (<outputfile>)\nSpecify .bin file as input, it'll be decoded in the specified output file, or 'input.decoded.txt' by defaut")
        exit(0)
    main(sys.argv[1:])
