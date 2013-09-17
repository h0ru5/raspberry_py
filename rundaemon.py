#!/usr/local/bin/python2.7
# encoding: utf-8
'''
rundaemon -- starts GPIO server

rundaemon is a server exposing GPIOs via HTTP-REST and XMPP

@author:     h0ru5
        
@copyright:  2013. All rights reserved.
        
@license:    Apache 2.0

@contact:    johannes.hund@gmail.com
@deffield    updated: Updated
'''

import sys
import os
import logging

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from rasp.xmpp.GpioClient import GpioClient

__all__ = []
__version__ = 0.1
__date__ = '2013-09-15'
__updated__ = '2013-09-15'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument("-P", "--port", help="set port for rest access [default: ]", metavar="PORT_NUMBER",type=int)
        parser.add_argument("-j", "--jid", dest="jid", help="set jid to connect xmpp", metavar="JID")
        parser.add_argument("-p", "--pass", dest="passwd", help="set password to connect xmpp")
        parser.add_argument("-s", "--service", dest="host", help="set host to connect xmpp")
 
        parser.add_argument("--no-rest", dest="norest", action="store_true", help="disable rest binding")
        parser.add_argument("--no-xmpp", dest="noxmpp", action="store_true", help="disable xmpp binding")
        
        parser.add_argument("-v", "--verbose", dest="verbose", action="count",help="set verbosity level")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        
        # set defaults
        parser.set_defaults(verbose=0,port=8080)
        
        # Process arguments
        args = parser.parse_args()
        
        #paths = args.paths
        port = args.port
        jid = args.jid
        passwd=args.passwd
        host = args.host
        if(not host):
            host = jid.split("@").pop()
        
        
        
        if args.verbose > 0:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Verbose mode on")
        else:
            logging.basicConfig(level=logging.INFO)
        
        #create and init GPIOs
        logging.info("initializing GPIOs")
        
        if(not args.norest):
            #startup web backend
            logging.info("starting up HTTP-REST frontend using port %s" % port)
            
        if(not args.noxmpp):
            #startup xmpp backend
            logging.info("starting up XMPP frontend using jid %s to connect to server %s" % (jid, host)) 
            xmpp = GpioClient(jid,passwd)
            xmpp.connect()
            xmpp.process(block=not args.norest)
            
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'rundaemon_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())