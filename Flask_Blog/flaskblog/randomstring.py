# cook your dish here
## importing modules
import random
import math

def loginstr(profession):
    ## storing strings in a list
    digits = [i for i in range(0, 10)]

    ## initializing a string
    random_str = ''
    stu = "stu"
    pro = "prof"
    admin = "admin"
    ## we can generate any lenght of string we want
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    number_str = random_str
    zero_filled_number = number_str.zfill(6)
    if profession.lower().startswith('s'):
        login = stu+str(zero_filled_number)
    elif profession.lower().startswith('p'):
        login = pro+str(zero_filled_number)
    else :
        login = admin+str(zero_filled_number)
    return login
