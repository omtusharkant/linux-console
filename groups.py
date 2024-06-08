import pexpect
import subprocess


class Groups:
    def __init__(self):
        self.list_group_script = "./backend/list_group_script.sh"
        self.rootpasswd = ""

    def _run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command '{command}': {e.stderr.strip()}")
            return [-1]

    def _run_sudo_command(self, command):
        try:
            child = pexpect.spawn(f"sudo {command}")
            print(f"Running command: {command}")
            child.expect("password for ")
            if not self.rootpasswd:
                self.rootpasswd = input("Enter root password: ")
            child.sendline(self.rootpasswd)
            child.expect(pexpect.EOF)
            return child.before.decode('utf-8')
        except pexpect.ExceptionPexpect as e:
            print(f"An error occurred while running the command '{command}': {str(e)}")
            return [-1]

    def list_system_groups(self):
        return self._run_command(self.list_group_script)

    def list_regular_groups(self):
        return self._run_command(self.list_group_script + " -r")

    def get_group_info(self, group_name):
        basic_info = self._run_command(f"getent group {group_name}")

        if basic_info and isinstance(basic_info[0], str):
            basic_info = basic_info[0].split(":")

            groupname = basic_info[0]
            is_passwd_protected = "yes" if basic_info[1] in ["x", "*", "!", ""] else "no"
            group_id = basic_info[2]
            members = self._run_command(f"members {group_name}")

            if members and isinstance(members[0], int):
                members = None
            else:
                members = [member.strip() for member in members[0].split(",")]

            group_type = False if int(group_id) >= 1000 else True
            sudo_permission_output = self._run_sudo_command(f"grep -E '^%{group_name}' /etc/sudoers /etc/sudoers.d/*")
            sudo_permission = "(ALL : ALL) ALL" in sudo_permission_output or "ALL=(ALL) ALL" in sudo_permission_output

            print("-------------------------------------")
            print(f"Group {groupname} Details")
            print("-------------------------------------")
            print(f"Groupname : {groupname}")
            print(f"Password protected? : {is_passwd_protected}")
            print(f"GroupID : {group_id}")
            print(f"Members : {', '.join(members) if members else 'None'}")
            print(f"Is system group : {group_type}")
            print(f"Sudo permission : {sudo_permission}")
        else:
            print("Group not found")

    def create_group(self):
        groupname = input("Enter Group name: ")

        command = f"sudo groupadd -f {groupname}"

        choice = input("Do you want to add other values to save modification time (yes/no)? ").strip().lower()

        if choice == 'yes':
            gid = input(f"Enter GID for {groupname}: ").strip()
            if gid:
                command += f" -g {gid}"

            gkey = input("Enter Key : value").strip()
            if gkey:
                command += f" -K {gkey}"

            password = input("Enter encrypted password: ").strip()
            if password:
                command += f" -p '{password}'"

            non_unique = input("Duplicate GID? (True/False)").strip()
            if non_unique.lower() == 'true':
                command += " -o"

            chroot = input("Enter Path to chroot: ").strip()
            if chroot:
                command += f" -R {chroot}"

            prefix = input("Enter path to prefix: ").strip()
            if prefix:
                command += f" -P {prefix}"

            system_group = input("System Group (True/False): ").strip()
            if system_group.lower() == 'true':
                command += " -r"

        print(f"Generated command: {command}")
        self._run_sudo_command(command)

    def modify_group(self, groupname):
        self.get_group_info(groupname)
        mod_command = f"sudo groupmod {groupname}"

        while True:
            print("1. Edit group name")
            print("2. Edit GID")
            print("3. Set non-unique")
            print("4. Edit password")
            print("6. Chroot")
            print("7. Prefix")
            print("S. Show changes")
            print("0. Exit")
            choice = input("Input choice: ")

            if choice == '0':
                break

            if choice == '1':
                new_groupname = input("Enter new group name: ")
                mod_command += f" -n {new_groupname}"

            elif choice == '2':
                new_gid = input("Enter new GID: ")
                mod_command += f" -g {new_gid}"

            elif choice == '3':
                new_non_unique = input("Enter non-unique (True/False): ")
                if new_non_unique.lower() == 'true':
                    mod_command += " -o"

            elif choice == '4':
                new_password = input("Enter new password: ")
                mod_command += f" -p {new_password}"

            elif choice == '6':
                new_chroot = input("Enter new chroot: ")
                mod_command += f" -R {new_chroot}"

            elif choice == '7':
                new_prefix = input("Enter new prefix: ")
                mod_command += f" -P {new_prefix}"

            elif choice == "S":
                print(mod_command)
            else:
                print("Invalid choice")

        print(f"Final command: {mod_command}")
        self._run_sudo_command(mod_command)

    def delete_group(self, groupname):
        del_command = f"sudo delgroup {groupname}"

        sys_rem = input("Do you want to remove this group if it is a system group (y/n): ").strip().lower()
        if sys_rem == "y":
            del_command += " --system"

        emp_user = input("Do you want to remove this group only if it is empty (y/n): ").strip().lower()
        if emp_user == "y":
            del_command += " --only-if-empty"

        print(del_command)
        confirm = input(f"Are you sure you want to delete {groupname} (yes/no): ").strip().lower()
        if confirm == "yes":
            self._run_sudo_command(del_command)


def main():
    groups = Groups()

    while True:
        print("1. List system groups")
        print("2. List regular groups")
        print("3. Get group info")
        print("4. Create group")
        print("5. Modify group")
        print("6. Delete user")
        print("0. Exit")
        choice = input("Input: ").strip()

        if choice == "1":
            system_groups = groups.list_system_groups()
            print("System groups:")
            for group in system_groups:
                print(group)

        elif choice == "2":
            regular_groups = groups.list_regular_groups()
            print("Regular groups:")
            for group in regular_groups:
                print(group)

        elif choice == "3":
            groups.get_group_info(input("Group name: ").strip())

        elif choice == "4":
            groups.create_group()

        elif choice == "5":
            groups.modify_group(input("Enter group to edit: ").strip())

        elif choice == "6":
            groups.delete_group(input("Enter group name to delete: ").strip())

        elif choice == "0":
            break

        else:
            print("Wrong choice")


if __name__ == "__main__":
    main()
