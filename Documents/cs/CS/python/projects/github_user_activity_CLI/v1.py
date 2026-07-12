import requests
import sys


#responsible for sending api
def send_request(username:str):
    #Putting the try block here
    params = {
        "per_page": 100,
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "X-Github-Api-Version": "2026-03-10",
        }
        
    response = requests.get(f"https://api.github.com/users/{username}/events",params=params, headers=headers,timeout=5)
    #if bad req, raise it intentionally 
    response.raise_for_status()
    data = response.json() 
    return data #a list of dicts or []

#responsible for transforming and process data 
#take return json data (a list of dicts)
#the previous version of this function shows all types of events in a structured format, but each one is almost the same 
#This version product a more structured output for each specific type of event
#Focusing on the most common event types 
def process_data(data:list[dict]) -> list:
    #?if there is anything in there in the returned data and user provide a specified event_type
    action_taken = []
    commits = 0
    n_events = len(data)
    if data:
        print(f"There is a total of {n_events} events for this user")
        for event in data:
        #we define the actor, performaed action and reponame
            actor = event.get("actor",[]).get("login")
            type = event.get("type",[])
            repo_name = event.get("repo",[]).get("name")
            time_create = event.get("created_at",[])
            #the type of the event determines the specific payload, some events might share the same key 
            payload = event.get("payload",[]) #each event has its payload, specific details regarding what happended in this even type 

            #!this might be inefficient but we are targeting specific events in here so 
            if type == "PushEvent":
                commits+=1 
                action_taken.append(f"{actor} pushed {commits} commits to {repo_name} at {time_create}")
        
            elif type == "CreateEvent":
                action_taken.append(f"{actor} created branch {repo_name} at {time_create}")
        
            elif type == "DeleteEvent":
                action_taken.append(f"{actor} deleted branch {repo_name} at {time_create}")
        
            elif type == "ForkEvent":
                action_taken.append(f"{actor} {payload.get('action')} repository {repo_name} at {time_create}")
            
            elif type == "IssuesEvent":
                action_taken.append(f"{actor} {payload.get('action')} issue in {repo_name} at {time_create}")
            
            elif type == "PullRequestEvent":
                action_taken.append(f"{actor} {payload.get('action')} pull request on {repo_name} at {time_create}")
            
            elif type == "WatchEvent":
                action_taken.append(f"{actor} {payload.get('action')} repository {repo_name} at {time_create}")
            
            elif type == "ReleaseEvent":
                action_taken.append(f"{actor} {payload.get('action')} release on {repo_name} at {time_create}")
            
            else:
                action_taken.append(f"{actor} triggered a {type} event on {repo_name} at {time_create}") #!for all the other unknown events 

        return action_taken

    else:
        return [] #!if there is no recent activity in the repo, return [] which denotes to None 
    
#main function 
#anyting entered in the command line default to a string, how to enforce it, but the api expects a username, why would people enter a number
def execution():
    #check arguments from command line 
    n_args = len(sys.argv)
    if n_args != 3: #receives two user provided arguments, plus the script filename 
        sys.exit(f"Invalid amount of arguments -> {sys.argv}, expected 3 arguments, not {n_args}")
    
    if sys.argv[2].isalpha() == False:
        sys.exit(f"Non alphabetic characters detected -> {sys.argv[2]}")

    #try block here
    try: 
    #send api requests, call api func 
        data = send_request(sys.argv[2]) #return either a list of dicts, [] or error
        
    except requests.ConnectionError as cnt: #the alias is an instance of the current exception which allows for accessing other arguments or data 
        print(f"Unable to establish connection: {cnt}")
        return 
    
    except requests.HTTPError as htp:
        print(f"HTTP error: {htp.response.status_code}")
        return 
    
    except requests.Timeout as t:
        print(f"Server took too long to respond: {t}")
        return 
    except requests.RequestException as err: #this catches the raised specific error related to API 
        print(f"Something went wrong: {err}")
        return 
    #we process data when the API requests is successful
    result = process_data(data)

    #display the result 
    for dt in result:
        print(dt)
        print()

execution()

#!or you could raise the exception from the send api function with a meaningful message and catch it with a ambiguous request exception 
#!or you can create a custom exception but i dont think it is necessary in this context 
#! a bare raise is useful when the exception is deteced but do not want to handle it fully
#!using a bare raise is kind of redudant here as it does not gives meaninguful output or context 
#!even without the try except block, the api related errors still propagate 


#!instead of re-raising inside the sned req function, remove it and move it up to the main function 
#!the key error is being handled by using get inside the process data function, when accessing data 
#!i dont think custom exceptions is even necessary as this point 
#!should i process the api in the try except block and then process the data 

#!the payload for each eventtype contans data and details releavt to the specific event 
#!the ref in the pushevent payload indicates a branch or tag is being updated by the push event 
#!when a new commit is pushed, git creates a new commit and moves the branch reference forward 
#!using a small commit to a large structure 


#shell selected interpreter vs code selected interpreter 
# a runtime error occurs when the runtime understands the intention of the code but fail to execute the code insturctions as written, comes up during execution 

