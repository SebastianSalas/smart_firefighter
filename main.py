import numpy as np

class SmartFirefighter:
  def main(self):
    with open("resources/map.txt", "r") as file:
        file_map = file.read()

    map = [int(n) for n in file_map.split(',')]

    print(map)
    
if __name__ == "__main__":
    SmartFirefighter().main()