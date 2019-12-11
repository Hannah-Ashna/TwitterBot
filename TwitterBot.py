# Import relevant modules
import tweepy
import tkinter as tk

# Import our own file-handling module
import FileHandle

# Variable for GUI Status Updates
StatusText = ""

# File containing the Twitter ID of the last person the bot responded to
PreviousIDFile = "Previous_ID.txt"

# File containing all of the jokes
JokesFile = "Stored_Jokes.txt"

# File containing all of the quotes
QuotesFile = "Stored_Quotes.txt"

AuthStatus = False

# Authentication process in order to access the twitter account @Spoopy_B0t
# Access Tokens for the Accounts

#auth = tweepy.OAuthHandler( "API KEY" , "API SECRET KEY" )
#auth.set_access_token( "ACCESS TOKEN" , "ACCESS TOKEN SECRET" )

api = tweepy.API(auth)

# Authenticate the Tokens
try:
    api.verify_credentials()
    StatusText = "Authentication OK - Ready to go"
    AuthStatus = True
except:
    StatusText = "Error during authentication - Bot is unavailable"
    AuthStatus = False



def ReplyingToTweets():
    
    # Obtain the Authentication Status to check whether or not it was succesful
    global AuthStatus
    
    # Only run this program if AuthStatus == True
    if AuthStatus:
        StatusUpdate.insert(tk.END, "Checking for new tweets in my @mentions")
        
        # Update the Bot's Bio to tell people they're online
        api.update_profile(description = "Hey there! I'm back online at the moment :) Feel free to message me!")
    
        # Find the Twitter ID of the last person the bot replied to
        LastID = FileHandle.RetrieveID(PreviousIDFile)
        
        # Get the mentions timeline of the Bot
        Mentions = api.mentions_timeline(LastID, tweet_mode = "extended")
    
        # Reverse it due to how the twitter timeline is structured (Read from Bottom --> Top)
        for Mention in reversed (Mentions):
            
            # Display the Mention tweet with the User ID attached to it (For main console only NOT GUI)
            NewMention = str(Mention.id) + " --- " + Mention.full_text
            print (NewMention)
            
            # Update the Status Box with the User ID and their Tweet
            try:
                StatusUpdate.insert(tk.END, "New Mention From: " + str(Mention.id) + " --- " + Mention.full_text)
            except:
                StatusUpdate.insert(tk.END, "New Mention From: " + str(Mention.id) + " --- " + " Message too long")
            
            # Store the new ID as previous ID
            LastID = Mention.id
            FileHandle.StoreID(LastID, PreviousIDFile)
            
            # Say hello to some friends!
            if "#hellobot" in Mention.full_text.lower():
                try:
                    api.update_status('@' + Mention.user.screen_name + 
                                      " Heyo! Thanks for checking in on me :) Hope you're having a swell day! Checkout my pinned tweets for some cool commands.")
                    StatusUpdate.insert(tk.END, "Saying hello!")
                    
                except:
                    StatusUpdate.insert(tk.END, "Error: Unable to say hello")
            
            # Dad Joke TIME :)
            if "#dadjoke" in Mention.full_text.lower():
                try:
                    api.update_status("Hello there " + "@" + Mention.user.screen_name + 
                                      ", I'm dad." + " Here's a joke: " + FileHandle.FileReader(JokesFile))
                    StatusUpdate.insert(tk.END, "Dad Joke TIME - finding a joke")
                    
                except:
                    StatusUpdate.insert(tk.END, "Error: Unable to make a dad joke")
            
            # Send a DM :)
            if "#dmtime" in Mention.full_text.lower():
                try:
                    api.send_direct_message(Mention.user.id, "Send binary")
                    StatusUpdate.insert(tk.END, "It's DM o'clock")
                    
                except:
                    StatusUpdate.insert(tk.END, "Error: Unable to DM this person")
                    api.update_status("Sorry " + "@" + Mention.user.screen_name + 
                                      ", but I can't seem to DM you due to one of your privacy settings")
            
            # Get some inspiration
            if "#inspiration" in Mention.full_text.lower():
                try:
                    api.update_status("@" + Mention.user.screen_name + " " + FileHandle.FileReader(QuotesFile))
                    StatusUpdate.insert(tk.END, "Providing some daily inspiration")
                    
                except:
                    StatusUpdate.insert(tk.END, "Error: Unable to send a quote")
                    
            # Follow the user
            if "#followme" in Mention.full_text.lower():
                try:
                    api.create_friendship(Mention.user.id)
                    StatusUpdate.insert(tk.END,"Helping them up their follower count")
                    
                except:
                    StatusUpdate.insert(tk.END, "Error: Unable to Follow this person")
                    
        # Inform user that all mentions have been responded to
        StatusUpdate.insert(tk.END, "No more new pending @mentions, try checking again later")
    
    # If AuthStatus == False stop user from trying to check timeline
    else:
        StatusUpdate.insert(tk.END, "Authentication Failed - Stop Bot and Check Tokens")
    


# Run the program
def StartProgram():
    # Clear previous msgs to avoid crowding
    StatusUpdate.delete(0, tk.END)
    ReplyingToTweets()
    
# Stop the program  
def StopProgram():
    # Clear previous msgs to avoid crowding
    StatusUpdate.delete(0, tk.END)
    
    StatusUpdate.insert(tk.END, "Shutting down the bot - You may exit now")
    api.update_profile(description = "Hey there! I'm currently offline at the moment but don't worry, I'll be back soon :D")

    

# Design the window for the Twitter Bot Application
AppWindow = tk.Tk()
        
# Create the Title
AppLabel = tk.Label(AppWindow, text = "Twitter Bot: SpoopyBot", fg = "grey1", font = ("Helvetica", 20))
AppLabel.pack()
  
# Create the Start Button
StartBtn = tk.Button(AppWindow, text = "Check & Reply to Tweets", fg = "grey1", font = ("Helvetica", 14), command = StartProgram)
StartBtn.pack()

# Create the Stop Button
StopBtn = tk.Button(AppWindow, text = "Close the Program", fg = "grey1", font = ("Helvetica", 14), command = StopProgram)
StopBtn.pack()

# Create a Status Update Box
StatusUpdate = tk.Listbox(AppWindow, width = 90, height = 90)
StatusUpdate.insert(tk.END, StatusText)
StatusUpdate.pack()

# Create the Main Window's Outline/Features
AppWindow.title("Twitter Bot")
AppWindow.geometry("600x600")
AppWindow.mainloop()
