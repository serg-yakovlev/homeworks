#import requests
#from bs4 import BeautifulSoup
#from urllib import parse

def double_iterate_items(extract, nr):
    print(type(extract))
    i=0
    for item in extract:
        while i<nr:            
            print('\n###'+str(i), type(item),'###\t')
            i+=1
            j=0
            for tag in item:
                print("\t###"+str(j), type(tag),'###\t', tag, '\n')
                j+=1

def iterate_items(extract):
    items=[]
    i=0
    for item in extract:
        #while i<10000:
        a=("\t###"+str(i),type(item),'###\t', item, '\n')            
        items.append(a)
        i+=1
    return(items)

def find_in_string(string, start, end):
    rest=str(string)
    result=""
    res_array = []
    start_symb=0
    end_symb=10000000

    while True:

        start_symb = rest.find(start)+len(start)
        #print('start_symb\n',start_symb)        
        rest=rest[start_symb:]
        #print('rest',rest)
        end_symb = rest.find(end)
        #print('end_symb\n',end_symb)
        if start_symb==-1 or end_symb==-1:
            return(res_array)
        result = rest[:end_symb]
        #print('result\n',result)
        res_array.append(result)
        rest=rest[end_symb+len(end):]
        #print('rest',rest)


def find_in_bs_object(obj, start, end,fr,till):
    arr=[]
    for item in obj:

            #print("\t###"+str(i),type(item),'###\t', item, '\n')
        arr.append(find_in_string(item, start, end)[fr:till])
    return(arr)


#print(find_in_string('qwertyuiowwwertyupppcvbwwwgbnjkpppdfgh','www','ppp'))

    
            

