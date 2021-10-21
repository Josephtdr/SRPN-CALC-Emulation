def saturation(n):
    """ function to emulate desired saturation feature """
    n = float(n)
    if n>2147483646:
        return 2147483647
    elif n<-2147483647:
        return -2147483648
    else:
        return n

def is_int(char):
    """ custom int checker to not classify "+{int}" as an int"""
    try:
        int(char)
        return char[0]!="+" #dont want + included in ints
    except:
        return False
