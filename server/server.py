from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
        allow_none=True, requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def inputData(topicData, noteData, textData, timeData):
        tree = ET.parse('./server/db.xml')
        topics = tree.getroot()

        topicRoot = topics.find(".//topic[@name='%s']" % topicData)
        if (topicRoot == None):
            child = ET.SubElement(topics, "topic")
            child.set("name", topicData)
            note = ET.SubElement(child, "note")
            note.set("name", noteData)
            text = ET.SubElement(note, "text")
            text.text = textData
            timestamp = ET.SubElement(note, "timestamp")
            timestamp.text = timeData
            tree.write('./server/db.xml')
            return "New topic created"
        else:
            note = ET.SubElement(topicRoot, "note")
            note.set("name", noteData)
            text = ET.SubElement(note, "text")
            text.text = textData
            timestamp = ET.SubElement(note, "timestamp")
            timestamp.text = timeData
            tree.write('./server/db.xml')
            return "Added to old topic"
    server.register_function(inputData, 'inputData')

    def getDataByTopic(topic):
        tree = ET.parse('./server/db.xml')
        topics = tree.getroot()
        topicRoot = topics.find(".//topic[@name='%s']" % topic)
        if (topicRoot == None):
            return "No notes under the topic"
        else:
            string = ""
            for descendant in topicRoot.iter():
                if (descendant.tag == "note"):
                    string += "Note: %s" % descendant.get('name')
                elif (descendant.tag == "text"):
                    string += " %s" % descendant.text
                elif (descendant.tag == "timestamp"):
                    string += " at %s" % descendant.text.strip()
            return string
    server.register_function(getDataByTopic, 'getDataByTopic')

    def searchWiki(searchTerm, topic):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": searchTerm,
            "limit": "1",
            "namespace": "0",
            "format": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()
        if (data[0]):
            print("Link: ", data[3])
            print("Description: ", data[2][0])
       
        if (topic != ""): # Add the query to topic
            pass
        return "Testing" #https://phabricator.wikimedia.org/T241437
        
    server.register_function(searchWiki, 'searchWiki')
    # Run the server's main loop
    server.serve_forever()