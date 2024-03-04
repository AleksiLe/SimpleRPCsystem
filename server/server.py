from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
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


    # Run the server's main loop
    server.serve_forever()