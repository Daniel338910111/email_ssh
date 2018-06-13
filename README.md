# email_ssh
Controlle your pc with your gmail!

please don't use this without the pc user permissions

fill the required field in the bottom of the script under __name__=='__main__'


__build in commands:__

    q = quit (exiting the program)
    shutdown = shutdown the computer
    screenshot = takes a screen shot and sending it to your email


__how to activate:__
    send to yourself email with one of thoes commands
    the program will check every 20s and if it got a command 
    it will replay

    it wont replay only when you call shutdown function and q 


easy to add commands
just add a function to the class
and then add the function to the dict in the __send_by_command()__ but don't call it

__easy to read__

__short and understandable script with alot of power!__
