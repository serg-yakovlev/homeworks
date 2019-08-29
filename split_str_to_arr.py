def split_str_to_arr(string, divider):
    arr = []
    arr.append(string[:string.find(divider)])    
    tail = string[string.find(divider)+len(divider):]
    while tail.find(divider)>0:
        arr.append(tail[:tail.find(divider)])  
        tail = tail[tail.find(divider)+len(divider):]
    arr.append(tail)
    return arr
      
        
