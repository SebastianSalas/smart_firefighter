with open("mapa.txt", "r") as file:
    file_map = file.read()

file_map = file_map.replace('[', '')
file_map = file_map.replace(']', '')

map = [int(n) for n in file_map.split(',')]

print(map)