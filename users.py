import subprocess
from datetime import datetime

class Users:
    def __init__(self):
        self.system_users_script = "./backend/system_users.sh"
        self.regular_users_script = "./backend/regular_users.sh"
        
    def _run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")
            return [-1]

    def _run_sudo_command(self,command):
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")
            return [-1]
        
    
    def list_system_users(self):
        return self._run_command(self.system_users_script)

    def list_regular_users(self):
        return self._run_command(self.regular_users_script)

    def get_user_info(self,user_name):
        ...
        """User Details for 'tom':
        -----------------------------
        Username    : 
        Full Name   : 
        User ID     : 
        Group ID    : 
        Home Directory: 
        Shell       : 
        User Type   : 
        Groups      : 
        Last Login  : 
        Current Login Sessions:
        
        Sudo Privileges:
        
        

        getent group "groupname"   # for listing users in a group

        grep 'useradd' /var/log/auth.log    #account creation date for system software

        """
        ...


        basic_info = self._run_command(f"getent passwd {user_name} ")[0].split(":")
        
        Username = basic_info[0]

        if basic_info[1] in ["x","*","!",""]:
            ispasswdprotected = "yes"
        else:
            ispasswdprotected = "no"

        userID = basic_info[2]
        
        GroupID = basic_info[3]

        groups = self._run_command(f"groups {Username}")[0].split(":")[-1].strip().replace(" ",",")

        fullName = basic_info[4]

        homeDIR = basic_info[5]

        shell = basic_info[6]

        userType = "regular user"  if int(userID)>=1000 else "system user"

        sudoPermission = True if "sudo" in groups else False

        if userType == "regular user":
            # for backup beacuse it does not give year "grep 'useradd' /var/log/auth.log | grep '{Username}' |grep 'UID={userID}'"
            userCreationdate = self._run_command(f"stat -c %w /home/{Username}")
            print(userCreationdate)
            if -1 in userCreationdate:
                datetime_obj = ""
            elif userCreationdate:
                # Timestamp string
                timestamp_str = userCreationdate[0].replace(" ",",").split(",")
                
                newtimestamp = timestamp_str[0]+" "+timestamp_str[1].split(".")[0]
                
                # Format string to match the input timestamp%H:%M:%S.%f 
                format_str = "%Y-%m-%d %H:%M:%S"

                # Parse the timestamp string into a datetime object
                datetime_obj = datetime.strptime(newtimestamp, format_str)

        else:
            userCreationdate = self._run_sudo_command(["sudo","passwd", "-S", f"{Username}"]).split(" ")[2]

            # Format string to match the input timestamp
            format_str = "%m/%d/%Y"
            output_format_str = "%Y-%m-%d"
            # Parse the timestamp string into a datetime object
            datetime_obj = datetime.strptime(userCreationdate, format_str)
            datetime_obj.strftime(output_format_str)


        last_login = self._run_command(f"last {Username}")
        
        

        print("-------------------------------------")
        print("User {Username} Detals")
        print("-------------------------------------")
        print(f"Username ==: {Username}")
        print(f"password protected ? : {ispasswdprotected}")
        print(f"UserID : {(userID)}")
        print(f"GroupID : {GroupID}")
        print(f"Groups : {groups}")
        print(f"FullName : {fullName}")
        print(f"HomeDIR : {homeDIR}")
        print(f"Shell : {shell}")
        print(f"UserType : {userType}")


        if sudoPermission == Username:
            print("Sudo Privileges {True}")
        else:
            print("Sudo Privileges {False}")

        print(f"User Creation : {datetime_obj}")
        
        print(f"last login :- ")
        print(f"-----------------------------------------------------------------------------")
        print(f"Name      terminal      Remote Host      Login            logout   duration")
        print(f"-----------------------------------------------------------------------------")
        
        for ll in last_login:
            print(ll)



        
def main():
    users = Users()
    
    print("1. List system users")
    print("2. List regular users")
    print("3. get user info")
    print("4. create User")
    
    choice = input("Input: ")

    if choice == "1":
        system_users = users.list_system_users()
        print("System Users/Software:")
        for user in system_users:
            print(user)
    
    elif choice == "2":
        regular_users = users.list_regular_users()
        print("Regular Users/Software:")
        for user in regular_users:
            print(user)

    elif choice == "3":
        users.get_user_info(input("Username : "))
    
    elif choice == "4":
        
        ...
    else:
        print("Wrong choice")


if __name__ == "__main__":
    main()
