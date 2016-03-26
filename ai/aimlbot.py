import aiml
import time
import glob

def initialize_aiml():
    # The Kernel object is the public interface to
    # the AIML interpreter.
    k = aiml.Kernel()

    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    # k.learn("std-startup.xml")
    filenames = glob.glob('ai/alice/*.aiml')
    print filenames
    print "Initialization started"
    for x in filenames:
        k.learn(x)
    print "Completed intialization"
    return k

def reply_aiml(query, k):
    return k.respond(query)
