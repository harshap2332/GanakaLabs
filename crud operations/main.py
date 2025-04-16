import mysql.connector as connector

class DBHelper:
    #create table
    def __init__(self):
        self.con = connector.connect(host='localhost',
                  port='3306',
                  user='root',
                  password='ASDasd@234',
                  database='pythontest')
        query = 'create table if not exists user(userID int primary key, userName varchar(200),phone varchar(12))'
        cur = self.con.cursor()
        cur.execute(query)
        print("Created")


    #insert data into table
    def insert_user(self,userid,username,phone):
        query="insert into user(userID,userName,phone) values({},'{}','{}')".format(userid,username,phone)
        print(query)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("user data saved to db")


    #fetching all data
    def fetch_all(self):
        query="select * from user"
        cur=self.con.cursor()
        cur.execute(query)
        for row in cur:
            print("Uder Id : ",row[0])
            print("User Name : ",row[1])
            print("User Phone : ", row[2])
            print()
            print()


    #fetching particular data
    def fetch_par(self, userid):
        query = "SELECT * FROM user WHERE userID = %s"
        cur = self.con.cursor()
        cur.execute(query, (userid,))  # Pass the 'userid' as a parameter
        row = cur.fetchone()  # Fetch only one row since we're searching by a specific userID
        if row:
            print("User Id : ", row[0])
            print("User Name : ", row[1])
            print("User Phone : ", row[2])
        else:
            print(f"No user found with userID: {userid}")
        print()
        print()


    #deleting data
    def delete_data(self,userId):
        query= "delete from user where userid = {}".format(userId)
        print(query)
        c=self.con.cursor()
        c.execute(query)
        self.con.commit() #Comment out if we dont want to delete permanently
        print("deleted")


    #Update data
    # def update_data(self, userid, newusername, newphone):
    #     query = "UPDATE user SET userName = %s, phone = %s WHERE userID = %s"
    #     cur = self.con.cursor()
    #     cur.execute(query, (newusername, newphone, userid))  # Pass parameters safely
    #     # self.con.commit()  # Commit the transaction
    #     print("User data updated successfully.")

    #OR

    #Update data
    def update_data(self, userid, newusername, newphone):
        query = "UPDATE user SET userName = {}, phone = {} WHERE userID = {}".format(newusername,newphone,userid)
        print(query)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()  # Commit the transaction
        print("User data updated successfully.")




# --main code
helper = DBHelper()

#--inserting data
# helper.insert_user(123,"abc","1234567890")
# helper.insert_user(111,"asd","1234567890")
# helper.insert_user(222,"hrf","1234567890")
# helper.insert_user(333,"ytv","1234567890")
# helper.insert_user(444,"wef","1234567890")
# helper.insert_user(555,"ar3","1234567890")
# helper.insert_user(666,"iyg","1234567890")

# --fetching data
# helper.fetch_all()

# --fetching particular data
# helper.fetch_par(222)

# --deleting particular data and fetching data
 
# helper.delete_data(123)
# helper.fetch_all()

# --updating data
# helper.update_data(123,'HARSHA','6363796221')
# helper.fetch_all()