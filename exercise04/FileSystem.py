class File:

    def chown(self, new_owner, dashR=0):
        """
        Change owner of file.
        :param new_owner: name of the new owner
        :param dashR: -R flag, default value is 0 (not enabled),
                               set to 1 to process all files in the specified directory and its subdirectories.
        :return: None
        """
        self.owner = new_owner
        if type(self) == Directory and dashR == 1:
            for i in range(len(self.filesList)):
                self.filesList[i].chown(new_owner, dashR)  # recursion


class Directory(File):

    def __init__(self, name, fileslist=[], owner="default", read=1, write=1, execution=1):
        self.name = name
        self.filesList = fileslist
        self.owner = owner
        self.read = read
        self.write = write
        self.execution = execution

    def __str__(self):
        res = f"Directory({self.name},["
        if len(self.filesList) == 0:  # If directory is empty
            res += "])"
        for i in range(len(self.filesList)):  # If it is not empty
            res += self.filesList[i].__str__()  # recursion
            if i == len(self.filesList) - 1:
                res += "])"
            else:
                res += ","
        return res

    def ls(self, dashl=0, depth=1):
        """
        Recursively print the content of the directory and all the subdirectories,
        using indentation to represent how deep in the tree structure the file/directory is.
        :param dashl: -l flag, default value is 0 (not enabled),
                               set to 1 to show more detailed information about permissions and owner.
        :param depth: Internal parameter indicating the depth of the folder, the initial value is set to 1
                     and CANNOT be changed, otherwise an error would occur.
        :return:
        """

        def permstr(files):
            """
            Internal auxiliary function: Generating permission string.
            :return: Permission string
            """
            if files.read == 1:
                ps = "r"
            else:
                ps = "-"
            if files.write == 1:
                ps += "w"
            else:
                ps += "-"
            if files.execution == 1:
                ps += "x"
            else:
                ps += "-"
            return ps

        if depth == 1:  # If on the first layer, print the name current folder.
            if dashl == 1:  # If -l is enabled, show more detail.
                res = permstr(self) + "  {}{}| {}".format(self.owner, " " * (10 - len(self.owner)), self.name)
                # permission string + owner + (10 - len(self.owner)) blank spaces + file name
                # (10 - len(self.owner)) blank spaces make what follows align.
                # 10 can be changed, depending on the length of the longest owner name.
            else:
                res = self.name
            print(res)
        for i in range(len(self.filesList)):
            if dashl == 1:
                res = permstr(self.filesList[i]) + "  {}{}| {}{}".format(self.filesList[i].owner,
                                                                         " " * (10 - len(self.filesList[i].owner)),
                                                                         "    " * depth,
                                                                         self.filesList[i].name)
                # Similar to the previous.
            else:
                res = "{}{}".format("    " * depth, self.filesList[i].name)
                # 4 blank spaces time depth + file name
            print(res)
            if type(self.filesList[i]) == Directory:
                self.filesList[i].ls(dashl, depth + 1)  # If object is directory, recursively call ls()


class PlainFile(File):

    def __init__(self, name, owner="default", read=1, write=1, execution=1):
        self.name = name
        self.owner = owner
        self.read = read
        self.write = write
        self.execution = execution

    def __str__(self):
        return f"PlainFile({self.name})"


class FileSystem:

    def __init__(self, directory):

        self.file = directory
        self.layer = []  # Internal variable, recording object of parent directories, used to implement cd and cp method
        self.location = ""  # Internal variable, recording path, used to implement find method.
        self.flag = False  # Internal variable, indicating find target file or not, used to implement find method.

    def pwd(self):
        """
        Print current working directory.
        :return: A string of self file name.
        """
        return self.file.name

    def ls(self, dashl=0):
        """
        Calling the ls() method of the class Directory.
        :param dashl: -l flag
        :return: None
        """
        self.file.ls(dashl)

    def cd(self, dest, report=1):
        """
        Change directory.
        :param dest: Name of destination directory at current working directory.
                     Input '..', back to parent directory, if it has.
        :param report: report flag, default value is 1 (enabled),
                                    set to 0 to report anything.
        :return: Bool
        """
        if dest == "..":  # If cd ..
            if len(self.layer) == 0:  # No parent directory
                return False
            else:
                self.file = self.layer[-1]  # Change directory on FileSystem to it parent directory.
                self.layer = self.layer[:-1]  # Get rid of the last directory in layer list.
                return True
        if len(self.file.filesList) == 0:  # If current working directory is empty.
            if report == 1:
                print(f"cd: {dest}: No such file or directory")
            return False
        for i in range(len(self.file.filesList)):
            if self.file.filesList[i].name == dest:  # Find it.
                self.layer += [self.file]  # Record itself to layer list.
                self.file = self.file.filesList[i]  # Change to its subdirectory.
                return True
            if i == len(self.file.filesList) - 1:  # Didn't find anything.
                if report == 1:
                    print(f"cd: {dest}: No such file or directory")
                return False

    def create_file(self, name, read=1, write=1, execution=1, report=1):
        """
        Create a plain file.
        :param name: name of plain file.
        :param read: read permission, default value is 1(readable), set to 0 to state it unreadable.
        :param write: write permission, default value is 1(writable), set to 0 to state it's not writable.
        :param execution: execution permission, default value is 1(executable), set to 0 to state it's not executable.
        :param report: report flag, default value is 1 (enabled),
                                    set to 0 to report anything.
        :return: None
        """
        if len(self.file.filesList) == 0:  # If current working directory is empty, create file directly.
            self.file.filesList += [PlainFile(name, self.file.owner, read, write, execution)]
            return
        for i in range(len(self.file.filesList)):  # Traversing current directory.
            if name == self.file.filesList[i].name:  # If file already exists, break.
                if report == 1:
                    print(f"The file'{name}' to be created already exists within the working directory!")
                break
            if i == len(self.file.filesList) - 1:
                self.file.filesList += [PlainFile(name, self.file.owner, read, write, execution)]
                # After traversing the directory without a file of that name, create the file.
                # Its owner decided by the owner of its directory's owner.

    def mkdir(self, name, owner="default", report=1):
        """
        Make directory.
        :param name: Name of directory.
        :param owner: Name of owner, default value is 'default'.
        :param report: report flag, default value is 1 (enabled),
                                    set to 0 to report anything.
        :return: None
        """
        if len(self.file.filesList) == 0:  # If current working directory is empty, make directory directly.
            self.file.filesList += [Directory(name, [], owner)]
            return True
        for i in range(len(self.file.filesList)):  # Traversing current directory.
            if name == self.file.filesList[i].name:  # If directory already exists, break.
                if report == 1:
                    print(f"The directory'{name}' to be created already exist within the working directory!")
                return False
            if i == len(self.file.filesList) - 1:
                self.file.filesList += [Directory(name, [], owner)]
                # After traversing the directory without a file of that name, make the directory.
                return True

    def rm(self, name, coerce=0, report=1):
        """
        Remove file or directory at current working directory.
        :param name: name of destination file or directory.
        :param coerce: coerce flag, default value is 0 (not enabled), only remove empty directory,
                                    set to 1 to remove file or directory as long as name match.
        :param report: report flag, default value is 1, report information,
                                    set to 0 to report nothing.
        :return: None
        """
        if len(self.file.filesList) == 0:  # If current working directory is empty.
            if report == 1:
                print(f"rm: {name}: No such file or directory")
        for i in range(len(self.file.filesList)):  # If it is not empty, traversing current directory.
            if name == self.file.filesList[i].name and type(self.file.filesList[i]) == PlainFile:
                self.file.filesList = self.file.filesList[: i] + self.file.filesList[i + 1:]
                # Name match, process file list, break.
                break
            elif name == self.file.filesList[i].name and type(self.file.filesList[i]) == Directory:
                if coerce == 1:
                    self.file.filesList = self.file.filesList[: i] + self.file.filesList[i + 1:]
                if self.file.filesList[i].filesList == []:  # If destination directory is empty.
                    self.file.filesList = self.file.filesList[: i] + self.file.filesList[i + 1:]
                    break
                else:  # If destination directory is not empty.
                    if report == 1:
                        print(f"Sorry, the directory is not empty.")
                        break
            if i == len(self.file.filesList) - 1:  # If no file or directory match.
                if report == 1:
                    print(f"rm: {name}: No such file or directory")

    def find(self, name, depth=0):
        """
        Find file on current working directory and its subdirectories.
        :param name: Name of file you want to find.
        :param depth: Internal irrevocable variable, used to indicate the depth of file system, default value is 0.
        :return: False or path.
        """
        self.location += f"{self.file.name}/"
        if self.file.filesList == [] and depth != 0:  # If subdirectory is empty.
            return self.flag, ""  # return False and Null path
        elif self.file.filesList == []:  # If root directory is empty.
            return self.flag  # return False
        for i in range(len(self.file.filesList)):  # Traversing current folder.
            if name == self.file.filesList[i].name:  # Find it.
                self.location += f"{name}"  # append path
                self.flag = True  # change flag
                if depth == 0:  # at root
                    path, self.location, self.flag = self.location, "", False  # reset flag and location
                    return path
                return self.flag, self.location  # at subdirectory, return flag and location to previous recursion.
            elif type(self.file.filesList[i]) == Directory:  # meet directory
                self.flag, temp = FileSystem(self.file.filesList[i]).find(name, depth + 1)
                # new a FileSystem and call its find method, and use self.flag and temp to receive what it return
                if self.flag:  # If find target.
                    self.location += temp  # append path
                    if depth != 0:  # Not at root
                        return self.flag, self.location  # return flag and location to previous recursion.
                    else:
                        path, self.location, self.flag = self.location, "", False  # reset
                        return path  # return path
            if i == len(self.file.filesList) - 1 and depth != 0:  # at subdirectory, find nothing
                return self.flag, self.location
        if not self.flag:  # at root, find nothing
            return self.flag
        path, self.location, self.flag = self.location, "", False  # else, reset, return path
        return path

    def chown(self, new_owner, name, dashR=0):
        """
        Change the owner of a single file or directory at current working directory.
        Can process recursively to all files and sub directories of a folder.
        :param new_owner: name of new owner
        :param name: name of destination file or folder
        :param dashR: -R flag, default value is 0 (not enabled),
                               set to 1 to process all files in the specified directory and its subdirectories.
        :return:
        """
        if len(self.file.filesList) == 0:
            print(f"chown: {name}: No such file or directory")
        for i in range(len(self.file.filesList)):
            if self.file.filesList[i].name == name:
                self.file.filesList[i].chown(new_owner, dashR)
                break
            if i == len(self.file.filesList) - 1:
                print(f"chown: {name}: No such file or directory")

    def chmod(self, name, mode):
        """
        Change mode.
        :param name: name of file or directory you want to change mode.
        :param mode: which mode you want to change to. Support number(0-7) and str(like,rwx,101) of mode.
        :return: None
        """
        def is_legal(string):
            """
            Determining if a string is legal.
            :param string: input string
            :return: bool
            """
            if len(string) != 3:
                return False
            if string[0] != "-" and string[0] != "r" and string[0] != "0" and string[0] != "1":
                return False
            if string[1] != "-" and string[1] != "w" and string[0] != "0" and string[0] != "1":
                return False
            if string[2] != "-" and string[2] != "x" and string[0] != "0" and string[0] != "1":
                return False
            return True

        if (type(mode) == str and not is_legal(mode)) or (type(mode) == int and (0 > mode or mode > 7)):
            # Determining if mode is legal
            print(f"Invalid file mode: {mode}")
            return

        for i in range(len(self.file.filesList)):
            if self.file.filesList[i].name == name:  # Find target
                if type(mode) == int:  # Number mode
                    num2 = [None, None, None]
                    num2[2] = mode % 2
                    num2[1] = int((mode - num2[2]) / 2 % 2)
                    num2[0] = int((mode - num2[1] * 2 - num2[2]) / 4 % 2)
                    self.file.filesList[i].read = num2[0]
                    self.file.filesList[i].write = num2[1]
                    self.file.filesList[i].execution = num2[2]
                if type(mode) == str:  # Str mode
                    if mode[0] == "r" or mode[0] == "1":
                        self.file.filesList[i].read = 1
                    else:
                        self.file.filesList[i].read = 0
                    if mode[1] == "w" or mode[1] == "1":
                        self.file.filesList[i].write = 1
                    else:
                        self.file.filesList[i].write = 0
                    if mode[2] == "x" or mode[2] == "1":
                        self.file.filesList[i].execution = 1
                    else:
                        self.file.filesList[i].execution = 0
                return
            if i == len(self.file.filesList) - 1:  # Find nothing
                print(f"chmod: {name}: No such file or directory")

    def mv(self, source, destpath):
        """
        Move file to destination path(absolute path) with file's new name.
        :param source: name of source file at current working directory.
        :param destpath: absolute path you want to move to, like, AAA/BBB/ccc.txt.
                         it will make directories which do not exist.
                         it can rename your file.
        :return: None
        """
        for i in range(len(self.file.filesList)):  # find target
            if self.file.filesList[i].name == source and type(self.file.filesList[i]) == PlainFile:
                break
            if i == len(self.file.filesList) - 1:
                print(f"mv: {source}: No such file or directory")
                return
        self.cp(source, destpath, report=0)  # copy file silently.
        self.rm(source, 1, 0)  # remove source file compulsorily and silently.

    def cp(self, source, destpath, report=1):
        """
        Copy file to destination path(absolute path) with file's new name.
        :param source: name of source file at current working directory.
        :param destpath: absolute path you want to move to, like, AAA/BBB/ccc.txt.
                        it will make directories which do not exist.
                        it can rename your file.
        :param report: report flag, default value is 1, report information,
                                    set to 0 to report nothing.
        :return: None
        """
        def path_to_list(path):
            """
            Create a list from a string of path
            :param path: string of path
            :return: list
            """
            lst = []
            start = 0
            for index in range(len(path)):
                if path[index] == "/":
                    lst += [path[start: index]]
                    start = index + 1
                if index == len(path) - 1:
                    lst += [path[start:]]
            return lst

        def bak2root():
            """
            Make file system back to the root directory.
            :return: None
            """
            while len(self.layer) != 0:
                self.cd("..")

        dirs = path_to_list(destpath)[1:]  # split dest path to list
        for i in range(len(self.file.filesList)):  # Find target
            if self.file.filesList[i].name == source and type(self.file.filesList[i]) == PlainFile:
                temp = self.file.filesList[i]  # temp alia of target
                initlayer = self.layer[1:] + [self.file]  # current position
                bak2root()  # back to root
                for j in range(len(dirs) - 1):  # cd to destination directory, if doesn't exist, make it.
                    self.mkdir(dirs[j], report=0)
                    self.cd(dirs[j], report=0)
                self.create_file(dirs[-1], temp.read, temp.write, temp.execution, report=0)
                # create file like source file, with new name.
                bak2root()  # back to root
                for k in range(len(initlayer)):  # cd to initial directory
                    self.cd(initlayer[k].name, report=0)
                return
            if i == len(self.file.filesList) - 1:  # Find nothing
                if report == 1:
                    print(f"cp: {source}: No such file or directory")
                return


print("====================TEST====================")

print("Testing question 1")

# question 1 should allow to create simple files and folders:
file = PlainFile("boot.exe")
folder = Directory("Downloads", [])

root = Directory("root", [PlainFile("boot.exe"),
                          Directory("home", [
                              Directory("thor",
                                        [PlainFile("hunde.jpg"),
                                         PlainFile("quatsch.txt")]),
                              Directory("isaac",
                                        [PlainFile("gatos.jpg")])])])

print("Testing question 2")

# question 2: implement the str

print(root)
"""
Directory(root,[PlainFile(boot.exe),Directory(home,[Directory(thor,[PlainFile(hunde.jpg),PlainFile(quatsch.txt)],Directory(isaac,[PlainFile(gatos.jpg)]]]
"""

print("Testing question 3")

# question 3: test chown()
# file = PlainFile("boot.exe")
# folder = Directory("Downloads",[])
print(f'file.owner: {file.owner}; folder: {folder.owner}')
file.chown("root")
folder.chown("isaac")
print(f'file.owner: {file.owner}; folder: {folder.owner}')

print("Testing question 4")

# question 4: ls() doesn't return anything but prints.
root.ls()
"""
root
	boot.exe
	home
		thor
			hunde.jpg
			quatsch.txt
		isaac
			gatos.jpg
"""

# question 5: create FileSystem
print("Testing question 5a: basic filesystem and pwd")

fs = FileSystem(root)

# 5a:
print(fs.pwd())

print("Testing question 5b: ls in working directory")

# 5b:
fs.ls()

# 5c:

print("Testing question 5c: cd")

# if you try to move to a non existing directory or to a file,
# the method should complain:
fs.cd("casa")
# But you can move to an existing directory in the working directory.
fs.cd("home")
# if we now do ls(), you should only see the content in home:
fs.ls()

# you can't go backwards yet...

print("Testing question 5d:  mkdir and create file")
fs = FileSystem(root)  # re-initialise fs

fs.mkdir("test", "isaac")
# the owner of the directory should be 'default' as not indicated. fs.mkdir("test","isaac") would set the owner to isaac
fs.cd("test")
fs.create_file("test.txt")
fs.ls()

print("Testing question 5e:  dot dot")

# to test this properly, let's create the entire file system using our previous functions!

root = Directory("root", [], owner="root")
fs = FileSystem(root)
fs.create_file("boot.exe")
# when creating a file we do not need to indicate owner, it will be the same as the working directory
fs.mkdir("test")
fs.cd("test")
fs.create_file("test.txt")
fs.cd("..")
fs.chown("ryan", "test", 1)
fs.mkdir("home", owner="root")
fs.cd("home")
fs.mkdir("thor", owner="thor")
fs.mkdir("isaac", owner="isaac")
fs.cd("thor")
fs.create_file("hunde.jpg")
fs.create_file("quatsch.txt")
fs.cd("..")
fs.cd("isaac")
fs.create_file("gatos.jpg")
fs.cd("..")
fs.cd("..")
fs.ls(dashl=1)

print("Testing question 5f:  rm")

fs.rm("test")  # shouldn't work!
fs.cd("test")
fs.rm("test.txt")
fs.cd("..")
fs.rm("test")
fs.ls()

print("Testing question 5g:  find")

print(fs.find("gatos.jpg"))
print(fs.find("thor"))
fs.cd("home")
print(fs.find("boot.exe"))  # shouldn't find it!
fs.cd("..")
print(fs.find("thor"))

print("Testing question 5h")
print("Testing chown -R:")

fs.chown("ryan", "boot.exe")  # common chown
fs.chown("rui", "home", dashR=1)  # chown -R
fs.ls(dashl=1)

print("Testing chmod:")

fs.chmod("boot.exe", "-w-")  # test "rwx" mode
fs.chmod("home", 0)  # test number mode
fs.create_file("abc.name")
fs.chmod("abc.name", 1)
fs.ls(dashl=1)
fs.chmod("abc.name", "abc")  # invalid file mode
fs.chmod("abc.nam", 0)  # invalid name
fs.chmod("abc.name", "101")  # test number mode
fs.ls(dashl=1)


print("Testing ls -l:")

fs.ls(dashl=1)

print("Testing mv:\ncase 1")

fs.ls(dashl=1)
fs.mv("boot.exe", "root/home/isaac/ace.mp4")  # move and rename
print("================= after mv =================")
fs.ls(dashl=1)

print("case 2")

fs.mv("abc.name", "root/test/ABC.uppercase")  # move and make directory doesn't exist.
fs.ls(dashl=1)

print("case 3")

fs.cd("home")
fs.cd("isaac")
fs.ls(dashl=1)
print("+++++++++++++++++++++++++++++++++++++++++++")
fs.mv("gatos.jpg", "root/home/thor/gatos.change")  # after moving, back to current directory
fs.ls(dashl=1)
print("+++++++++++++++++++++++++++++++++++++++++++")
fs.cd("..")
fs.cd("..")
fs.ls(dashl=1)
