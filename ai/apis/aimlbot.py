'''
This is mostly for handling aiml requests

initialize_aiml fuciton is used to initialize the aiml engine with all the files

reply_aiml function is used to get the reply to any query
'''
import aiml
import glob

# Add aiml sources here
filenames = glob.glob('ai/apis/aiml_files/*.aiml')

def initialize_aiml():
    # The Kernel object is the public interface to the AIML interpreter.
    global aiml_engine
    aiml_engine = aiml.Kernel()

    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    # eg : aiml_engine.learn("std-startup.xml")
    for x in filenames:
        aiml_engine.learn(x)
    print "Completed intialization"

def reply_aiml(query):
    global aiml_engine
    return aiml_engine.respond(query)
