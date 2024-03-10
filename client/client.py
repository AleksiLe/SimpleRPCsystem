import xmlrpc.client
import datetime

def searchWiki(proxy):
    searchTerm = input("Give search term: ")
    permission = input("Do you want to append search to topic? (y/n): ")
    if (permission == "y"):
        topic = input("Give topic name: ")
        try:
            print(proxy.searchWiki(searchTerm, topic))
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)
    if (permission == "n"):
        try:
            print(proxy.searchWiki(searchTerm, ""))
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)
    else:
        print("Not a valid input")

def getTopic(proxy):
    topic = input("Give topic name: ")
    try:
        print(proxy.getDataByTopic(topic))
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
    return None

def inputData(proxy):
    topic = input("Give topic name: ")
    note = input("Give note name: ")
    text = input("Give text to note: ")
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y - %H:%M:%S")
    try:
        print(proxy.inputData(topic, note, text, date_time))
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
    return None

def options(proxy):
    choise = ""
    while(choise != "0"):
        print("0) End program")
        print("1) Add entry")
        print("2) Get topic")
        print("3) Search Wikipedia")
        choise = input("What you want to do: ")
        match choise:
            case "0":
                print("Program ends")
            case "1":
                inputData(proxy)
            case "2":
                getTopic(proxy)
            case "3":
                searchWiki(proxy)
            case _:
                print("Please give suggested input")


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2", allow_none=True)
    options(proxy)

main()