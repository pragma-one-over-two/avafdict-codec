# avafdict-codec
Encode and decode Avalanche dictionary files in the AVAFDICT 2.0 format, notably used in Hogwarts Legacy.

# How to use
### Drag and drop
- Drag and drop the .bin file over decode.exe
- Modify the decoded file
- Drag and drop the decoded file over encode.exe
- Pak it and you're done !
### CLI
Pass input file as the first parameter, with optional output filename as second parameter, and you're done. Eg:
>`encode.exe MAIN-enUS.bin`

>`decode.exe MAIN-enUS.bin.decoded.txt MAIN-enUS.modified.txt`

# Modifying the files
There are two types of files, MAIN and SUB: SUB contains mostly dialogue subtitles, MAIN contains the rest.

These files consist of a series of keys and values: the key helps the game find the value, the value contains the localized string. You can easily differentiate keys, they're generally numbered and often contain underscores `_`. Don't modify the keys, the game won't like it.

Some of the strings contain line breaks, they are decoded as "\n". Feel free to modify as you will, but make sure to always use "\n" to denote any line break you want to see in the game. Any real, extra line break will be interpreted as a different value, and you'll likely fuck up the file entirely.

# File format

### Header
```
0x00: "AVAFDICT 2.0   \0" in UTF-16 LE
0x20: number of key-value entries on 8 bytes, so technically, half the total number of strings
0x28: size of header on 8 bytes/start of dictionary offset
0x30: size of dictionary on 8 bytes
0x38: end of dictionary/start of text offset from start of file on 8 bytes
0x40: size of text block on 8 bytes
```
### Dictionary entries

Should start at 0x48, each 12 byte long, consisting of:
```
8 bytes: offset from beginning of text block
4 bytes: length of string
```

### Text block

Text strings are just glued to each other, no separator.

Encoding of strings is UTF-8, there are a few odd, incorrect characters but they're only alternate UTF-8 dashes, won't break the game to replace them with simple - dashes.

The file ends on the last character of the last string, no \0 nor \n ending.

### Extra notes

Be wary of text strings containing newline 0x0a characters, every \n gets swapped by a "\\n" on decode so they're not mixed up with the windows-friendly 0x0d0a newlines added between entries. On import, all newline characters are removed (Python's splitlines is generous enough) to ensure no line break remains, and "\\n" gets replaced by \n once again.

Strings are a series of key-value pairs, each localized string being preceded by a unique identifier, identical across locales. I didn't bother decoding these files in a key=value format, because it's obvious enough, easier to reencode afterwards, and it makes diffing them to check for modifications more efficient.

Code was thoroughly tested on EN, DE, FR, ES, IT, and JA locales, on both MAIN and SUBS files. After successive decoding and encoding, output files were identical to the originals. Reencoded files with modified content were successfully tested in the game to modify text strings.
