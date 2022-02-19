from chat_data import data
def giveAns(query):
    query = query.lower()
    ans = ""
    try:
        ans = data[query]
    except:
        if( len(query.split()) > 2):
            for a,b in enumerate(data):
                if query in b:
                    ans = data[b]
    
    if ans == "":
        ans =  "sorry, i can't understand"  
    
    return ans