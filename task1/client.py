import sys
import glob
import math
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/alexey/thrift-0.11.0/lib/py/build/lib*')[0])

from task1 import MetaScrapper
from task1.ttypes import Meta, InvalidUrl, NoMetadata, InvalidMetadata

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

DEFAULT_URL = 'https://www.imdb.com/title/tt0117500/'

def truncate(string, maxlength=80):
  strlen = len(string)
  if strlen <= maxlength:
    return string
  return string[:maxlength / 2] + '.. ..' + string[strlen - (maxlength / 2):]

def metaToString(meta):
    str = '\ntitle\t\t= ' + meta.title + '\n'
    str += 'type\t\t= ' + meta.type + '\n'
    str += 'url\t\t= ' + meta.url + '\n'
    str += 'image\t\t= ' + truncate(meta.image) + '\n'
    str += ('audio\t\t= ' + meta.audio + '\n' if meta.audio else '')
    str += ('description\t= ' + truncate(meta.description) + '\n' if meta.description else '')
    str += ('determiner \t= ' + meta.determiner  + '\n' if meta.determiner  else '')
    str += ('locale\t= ' + meta.locale + '\n' if meta.locale else '')
    str += ('locale:alternate \t= ' + meta.localeAlternate  + '\n' if meta.localeAlternate else '')
    str += ('site_name\t= ' + meta.site_name + '\n' if meta.site_name else '')
    str += ('video\t= ' + meta.video + '\n' if meta.video else '')
    return str

def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = MetaScrapper.Client(protocol)

    # Connect!
    transport.open()
    
    if len(sys.argv) > 1:
      url = sys.argv[1]
    else:
      url = raw_input('Enter website (default is \'' + DEFAULT_URL + '\'): ')
      if url == "":
        url = DEFAULT_URL

    try:
		  meta = client.extractMetaFromUrl(url)
		  print(metaToString(meta))
		  
    except InvalidUrl as e:
	  	print('Couldn\'t load website with url ' + e.url + (('. Error message is:\n' + e.message) if e.message else ''))
    except NoMetadata:
	    print('Website ' + url + ' doesn\'t have any OG metadata')
    except InvalidMetadata as e:
	    print('Website ' + url + ' has invalid metadata:\n' + e.message)
    
    transport.close()
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
