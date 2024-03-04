import xmlrpc.client
import datetime

def options(proxy):
    choise = ""
    while(choise != "0"):
        print("0) End program")
        print("1) Add entry")
        choise = input("What you want to do: ")
        match choise:
            case "0":
                print("Program ends")
            case "1":
                topic = input("Give topic name: ")
                note = input("Give note name: ")
                text = input("Give text to note:")
                now = datetime.datetime.now()
                date_time = now.strftime("%m/%d/%Y - %H:%M:%S")
                try:
                    print(proxy.inputData(topic, note, text, date_time))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)
            case _:
                print("Please give suggested input")


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2", allow_none=True)
    options(proxy)

main()