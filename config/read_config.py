def read_config(file_name):
    f = open(file_name, "r")
    temp_data = {}
    temporary = []
    for x in f:
        if (x[0] == ";" or x[0] == "["):
            continue
        else:
            temporary = x.rstrip('\n').rstrip('\r').split(" = ")
            if (len(temporary) > 1):
                temp_data[temporary[0]] = temporary[1]
    f.close()
    return temp_data