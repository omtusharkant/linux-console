import pexpect
import subprocess
from datetime import datetime

class Users:
    def __init__(self):
        self.system_users_script = "./backend/system_users.sh"
        self.regular_users_script = "./backend/regular_users.sh"
        self.rootpasswd = ""
    def _run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")
            return [-1]

    def _run_sudo_command(self,command):
        try:
            
            # Start the passwd command
            child = pexpect.spawn(f"sudo {command}")
            child.expect("password for ")
            if self.rootpasswd =="":
                self.rootpasswd = input("enter root password")
            child.sendline(self.rootpasswd) 
            child.expect(pexpect.EOF)
            return child.before.decode('utf-8')
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
        
        self.Username = basic_info[0]

        if basic_info[1] in ["x","*","!",""]:
            ispasswdprotected = "yes"
        else:
            ispasswdprotected = "no"

        self.userID = basic_info[2]
        
        self.GroupID = basic_info[3]

        self.pgroup = self._run_command(f"id -gn {user_name}")

        self.groupsnames = self._run_command(f"groups {self.Username}")[0].split(":")[-1].strip().replace(" ",",")

        self.fullName = basic_info[4]

        self.homeDIR = basic_info[5]

        self.shell = basic_info[6]   #other shell types /usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,


        userType = "regular user"  if int(self.userID)>=1000 else "system user"

        self.sudoPermission = self._run_sudo_command(f" -l -U {self.Username}")
        if "(ALL : ALL) ALL" in self.sudoPermission[-1]:
            
            self.sudoPermission = True
        else:
            self.sudoPermission = False
        if userType == "regular user":
            

            # for backup beacuse it does not give year "grep 'useradd' /var/log/auth.log | grep '{Username}' |grep 'UID={userID}'"     
            #command 2  stat -c %w /home/marcus  it returns creation date of this home dir

            userCreationdate = self._run_sudo_command(f"passwd -S {self.Username}").split(" ")[3]
            print(userCreationdate)
            if "new user:" in userCreationdate[0]:
                print("new user")
                date =  userCreationdate[0].split(":")
                print(date)
            elif "-1" in userCreationdate:
                datetime_obj = ""
            elif userCreationdate:
                

                # Format string to match the input timestamp
                format_str = "%m/%d/%Y"
                output_format_str = "%Y-%m-%d"
                # Parse the timestamp string into a datetime object
                datetime_obj = datetime.strptime(userCreationdate, format_str)
                datetime_obj.strftime(output_format_str)

        else:
            # this command return user creation date not time
            userCreationdate = self._run_sudo_command(f"passwd -S {self.Username}")
            print(userCreationdate)
            # Format string to match the input timestamp
            format_str = "%m/%d/%Y"
            output_format_str = "%Y-%m-%d"
            # Parse the timestamp string into a datetime object
            datetime_obj = datetime.strptime(userCreationdate, format_str)
            datetime_obj.strftime(output_format_str)


        last_login = self._run_command(f"last {self.Username}")
        
        

        print("-------------------------------------")
        print(f"User {self.Username} Detals")
        print("-------------------------------------")
        print(f"Username ==: {self.Username}")
        print(f"password protected ? : {ispasswdprotected}")
        print(f"UserID : {(self.userID)}")
        print(f"GroupID : {self.GroupID}")
        print(f"Primary Group : {self.pgroup}")
        print(f"Groups : {self.groupsnames}")
        print(f"FullName : {self.fullName}")
        print(f"HomeDIR : {self.homeDIR}")
        print(f"Shell : {self.shell}")
        print(f"UserType : {userType}")


        print(f"sudo permission : {self.sudoPermission}")

        print(f"User Creation : {datetime_obj}")
        
        print(f"last login :- ")
        print(f"-----------------------------------------------------------------------------")
        print(f"Name      terminal      Remote Host      Login            logout   duration")
        print(f"-----------------------------------------------------------------------------")
        
        for ll in last_login:
            print(ll)



    def createUser(self):
        username = input("Enter user name: ")
    
        Bcommand = f"sudo useradd -m {username}"  # base command
        
        choice = input("Do you want to add other values to save modification time (yes/no)? ").strip().lower()
        
        if choice == 'yes':
            HDIR = input("Enter home directory path: ")
            if HDIR:
                Bcommand += f" -d {HDIR}"
            
            Expire = input("Enter expire date [format: MMDDhhmmyy] (default: 0): ").strip()
            if Expire:
                Bcommand += f" -e {Expire}"
            
            comment = input("Enter full name, phone number, organization or department (comma-separated): ").strip()
            if comment:
                Bcommand += f" -c '{comment}'"
            
            Primegroup = input("Enter primary group: ").strip()
            if Primegroup:
                Bcommand += f" -g {Primegroup}"
            
            SecondaryGroup = input("Enter secondary group names (comma-separated): ").strip()
            if SecondaryGroup:
                Bcommand += f" -G {SecondaryGroup}"
            
            skelDIR = input("Enter skeletal directory: ").strip()
            if skelDIR:
                Bcommand += f" -k {skelDIR}"
            
            
            
            shell = input("Enter user shell: ").strip()
            if shell:
                Bcommand += f" -s {shell}"
            
            uid = input("Enter UID: ").strip()
            if uid:
                Bcommand += f" -u {uid}"
        
        print(f"Generated command: {Bcommand}")
        
        self._run_command(Bcommand)

        print(f"enter new password for {username}")
        self._run_sudo_command(f"passwd {username}")

    def modify_user(self,username):
        ...
        self.get_user_info(username)
        modcommand = f"usermod {username}"
        while True:
                print("1. edit comment")
                print("2. edit home dir")
                print("3. edit primary group")
                print("4. edit groups (comma separated)")
                print("5. edit new username")
                print("6. edit move content to new home dir")
                print("7. edit shell")
                print("8. edit UID")
                print("9. edit password")
                print("S.  show chnages")
                print("0. exit")
                choice = input("Input choice: ")

                # Example of using the details from get_user_info
                print(f"Current username: {self.Username}")
                print(f"Selected choice: {choice}")
                
                if choice == '0':
                    break
            
                # Implement modification based on choice
                if choice == '1':
                    print(f"prevous comment :{self.fullName}")
                    new_comment = input("Enter new comment: ")
                    #self._run_command(f"sudo usermod -c '{new_comment}' {self.Username}", shell=True)
                    modcommand+= f" -c {new_comment}"
                    
                elif choice == '2':
                    print(f"prevous home dir : {self.homeDIR}")
                    new_home_dir = input("Enter new home directory: ")
                    #self._run_command(f"sudo usermod -d {new_home_dir} {self.Username}", shell=True)
                    modcommand+= f" -d {new_home_dir}"

                elif choice == '3':
                    print(f"prevous primary group : {self.pgroup}")
                    new_primary_group = input("Enter new primary group: ")
                    #self._run_command(f"sudo usermod -g {new_primary_group} {self.Username}", shell=True)
                    modcommand+= f" -g {new_primary_group}"


                elif choice == '4':
                    print(f"prevous groups : {self.groupsnames}")
                    new_groups = input("Enter new groups (comma separated): ")
                    #self._run_command(f"sudo usermod -G {new_groups} {self.Username}", shell=True)
                    modcommand+= f" -G {new_groups}"


                elif choice == '5':
                    print(f"prevous username : {self.Username}")
                    new_username = input("Enter new username: ")
                    #self._run_command(f"sudo usermod -l {new_username} {self.Username}", shell=True)
                    modcommand+= f" -l {new_username}"


                elif choice == '6':   #doubt check 
                    print(f"prevous {self.fullName}")
                    new_home_dir = input("Enter new home directory: ")
                # self._run_command(f"sudo usermod -m -d {new_home_dir} {self.Username}", shell=True)
                    #modcommand+=


                elif choice == '7':
                    print(f"prevous shell : {self.shell}")
                    new_shell = input("Enter new shell: ")
                    #self._run_command(f"sudo usermod -s {new_shell} {self.Username}", shell=True)
                    modcommand+= f" -s {new_shell}"


                elif choice == '8':
                    print(f"prevous UID : {self.userID}")
                    new_uid = input("Enter new UID: ")
                    #self._run_command(f"sudo usermod -u {new_uid} {self.Username}", shell=True)
                    modcommand+= f" -u {new_uid}"

                elif choice == "S":
                    print(modcommand)
                else:
                    print("Invalid choice")
        print(modcommand)
        self._run_sudo_command(modcommand)

    def deleteuser(self,username):
        ...
        delcommand = f"deluser {username}"

        rm_all_files = input("do you want to remove all file (yes/no)")
        if rm_all_files == "yes":
            delcommand+= " --remove-all-files"
        rm_home = input("do you want to remove home (yes/no)")
        if rm_home == "yes":
            delcommand+= " --remove-home"

        print(delcommand)
        confirm = input(f"are you sure you want to delete {username}  (yes/no)")
        if confirm == "yes":
            self._run_sudo_command(delcommand)
def main():
    users = Users()
    
    print("1. List system users")
    print("2. List regular users")
    print("3. get user info")
    print("4. create User")
    print("5. modify user")
    print("6. delete user   (!with caution)")
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
        users.createUser()
        
    elif choice == "5":
        users.modify_user(input("enter username to edit"))

    elif choice == "6":
        users.deleteuser(input("enter username to delete"))
    else:
        print("Wrong choice")


if __name__ == "__main__":
    main()
