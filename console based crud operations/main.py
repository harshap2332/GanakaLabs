from dbhelper import DBHelper

def main():
    db=DBHelper()
    while True:
        print("********WELCOME************")
        print()
        print("PRESS 1 to insert new user")
        print("PRESS 2 to display all user")
        print("PRESS 3 to delete user")
        print("PRESS 4 to update user")
        print("PRESS 5 to exit program")
        print()
        try:
            choice=int(input())
            if(choice==1):
                #insert user
                uid=int(input("Enter userid : "))
                username=eval(input("Enter username : "))
                userphone=eval(input("Enter user phone no. : "))
                db.insert_user(uid,username,userphone)
                pass
            elif choice==2:
                #display user
                db.fetch_all()
                pass
            elif choice==3:
                #delete user
                uid=int(input("Enter userid you want to delete : "))
                db.delete_data(uid)
                pass
            elif choice==4:
                #update user:
                uid=int(input("Enter userid : "))
                NEWusername=eval(input("Enter username : "))
                NEWuserphone=eval(input("Enter user phone no. : "))
                db.update_data(uid,NEWuserphone,NEWuserphone)
                pass
            elif choice==5:
                #exit
                break
            else:
                print("Invalid input ! Try again")
        except Exception as e:
            print(e)
            print("Invalid Details")

if __name__ == "__main__":
    main()