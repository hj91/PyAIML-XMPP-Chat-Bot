#Author :lawrence175 aka lawrence kisembo
#http://www.alicebot.org/documentation/aiml-reference.html

#-----------------------------------------------------------------------------------------------------
# Sessions and Predicates
# By specifying a session, the AIML can tailor different conversations to different users. 
# For example, if one user tells the bot their name is Alice, 
# and the other user tells the bot their name is Bob, the bot can differentiate the two users.
# To specify which session you are using you pass it as a second parameter to respond().
#########################################################################################################################

sessionId = 12345
kernel.respond(raw_input(">>>"), sessionId)

# This is good for having personalized conversations with each user. 
# You will have to generate your own session Id some how and track them. 
# According to my analysis,I found out that saving the brain file does not save all the session values.

sessionId = 12345

# Get session info as dictionary. Contains the input
# and output history as well as any predicates known
sessionData = kernel.getSessionData(sessionId)

# Each session ID needs to be a unique value
# The predicate name is the name of user
# that the bot knows about in session with the bot
# The bot might know me as "lawrence" and that your "dog" is named "jeepers"
kernel.setPredicate("jeepers", "lawrence", sessionId)
clients_dogs_name = kernel.getPredicate("jeepers", sessionId)

kernel.setBotPredicate("homevillage", "127.0.0.1")
bot_hometown = kernel.getBotPredicate("homevillage")

# In the AIML we can set predicates using the set response in template
##########################################################################################################################################################
<aiml version="1.0.1" encoding="UTF-8">
   <category>
      <pattern>MY DOGS NAME IS *</pattern>
      <template>
         That is interesting that you have a dog named <set name="dog"><star/></set>
      </template>  
   </category>  
   <category>
      <pattern>WHAT IS MY DOGS NAME</pattern>
      <template>
         Your dogs name is <get name="dog"/>
      </template>  
   </category>  
</aiml>

# this is a snippet of the  input and output.
#Basing on the AIML above you could tell the bot:
##########################################################################################################################################


# My dogs name is jeepers
# # And the bot will respond with

# That is interesting that you have a dog named jeepers
# # And if you ask the bot:

# What is my dogs name?
# # The bot will respond:

# Your dogs name is jeepers

#############################################################################################################################################