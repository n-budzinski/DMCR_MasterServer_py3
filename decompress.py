from zlib import decompress

filename = input("Enter the file name:")

try:
    with open(f"{filename}", "rb") as file:
        file = file.read()
        output = decompress(file[12:])
        output = output[16:-7]
        print(output.decode('utf-8').replace("#", "\n#"))
        file = open(f"{filename}_", "wb")
        file.write(output)

except FileNotFoundError:
    print("Couldn't find the file")