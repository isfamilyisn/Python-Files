#height=256
#if (height>=160):
 #       if(height>=250):
  #          print("you're not a human, sorry")
#        else:
#            print("you can ride roller coaster!!!")
#elif (height<160):
 #   print("uh-oh your too tiny, sorry. go to the kiddy one")

# PROBLEM
# if height is more than 160, then allow to ride rollercoaster, and stop loop.
# if height is less than 160, say ("1 year later"), then ask again.
height=0
while (height<160):
    height=int(input("how tall are you?"))
    print(height)
    if (height>=160):
        print("you can ride roller coaster!!!")
    elif (height<160):
        print("Sorry you can't go. One year later....")

