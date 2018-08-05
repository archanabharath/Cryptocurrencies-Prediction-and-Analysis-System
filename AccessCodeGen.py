#Program to generate random numbers and store them as access code for different user PINs

import random

access_dict={}

for i in range(1001,1021):

    a = i
    b = random.randint(10,1000)
    print("[a,b]:[",a,b,"]")
    x = i
    access_dict[x] = b

access_file_obj = open("users.dat", "w")
access_file_obj.write(str(access_dict))
access_file_obj.close()

access_file_read = open("users.dat","r")
print(access_file_read.readline())
access_file_obj.close()


