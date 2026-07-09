import requests
import sys


#responsible for sending api
def send_request(username:str):
    #Putting the try block here
    headers = {
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": "2026-03-10",
        }
        
    response = requests.get(f"https://api.github.com/users/{username}/events",headers=headers,timeout=5)
    #if bad req, raise it intentionally 
    response.raise_for_status()
    for dt in response.headers:
        print(dt)
    data = response.json() 
    return data #a list of dicts or []

#responsible for transforming and process data 
#take return json data (a list of dicts)
def process_data(data):
    #!if there is anything in there 
    #!append the output to a list 
    sentences = []
    if data:
        n_events = len(data)
        print(f"There is a total of {n_events} events for this user")
        for event in data:
            event_type = event.get("type",[]) #!if key do not exists, then we return [] which denotes to None 
            user = event.get("actor",[]).get("login")
            repo_name = event.get("repo",[]).get("name")
            date_create = event.get("created_at",[])
            sentences.append(f"{user} triggered a {event_type} nameed {repo_name} created at {date_create}")
        
        return sentences

    else:
        #!otherwise there is no recent activity, meaning it returned [] denotes to None 
        return []
    
#main function 
#def main():
    #check arguments from command line 
#    if len(sys.argv) != 2:
#        sys.exit("Invalid amount of arguments")
    
#    if not isinstance(sys.argv[2],str):
#        sys.exit("Wrong type, expected string")
    #try block here
#    try: 
    #send api requests, call api func 
#        data = send_request(sys.argv[2]) #return either a list of dicts, [] or error
        
#    except requests.ConnectionError as cnt:
#        print(f"Unable to establish connection: {cnt}")
#        return 
    
#    except requests.HTTPError as htp:
 #       print(f"HTTP error: {htp}")
#        return 
    
#    except requests.Timeout as t:
#        print(f"Server took too long to respond: {t}")
#        return 
    
#    except requests.RequestException as err: #this catches the raised specific error related to API 
#        print(f"Something went wrong: {err}")
#        return 
    
 #   process_data(data)

dt = send_request("nilbuild")
data = process_data(dt)
for sent in data:
    print(sent)
    print()

#!or you could raise the exception from the send api function with a meaningful message and catch it with a ambiguous request exception 
#!or you can create a custom exception but i dont think it is necessary in this context 
#! a bare raise is useful when the exception is deteced but do not want to handle it fully
#!using a bare raise is kind of redudant here as it does not gives meaninguful output or context 
#!even without the try except block, the api related errors still propagate 


#!instead of re-raising inside the sned req function, remove it and move it up to the main function 
#!the key error is being handled by using get inside the process data function, when accessing data 
#!i dont think custom exceptions is even necessary as this point 
#!should i process the api in the try except block and then process the data 