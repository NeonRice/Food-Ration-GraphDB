import logging
from option import *
from queryManager import *

if __name__ == "__main__":
    scheme = "neo4j"
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(
        scheme=scheme, 
        host_name=host_name, 
        port=port)
    user = "neo4j"
    password = "s3cr3t"

    query = QueryManager(url, user, password)
    options = initOptions(query)

    while(True):
        drawOptions(options)
        handleInput(options)
        clearOutput()
    
    query.close()