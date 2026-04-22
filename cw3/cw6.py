from abc import ABC, abstractmethod
from typing import List


class AbstractAPI(ABC):
    def __init__(self, rank: int) -> None:
        self.rank = rank
        self.permissions = []
        self.set_permissions(self.rank)

    def set_rank(self, rank: int) -> None:
        self.rank = rank
        self.set_permissions(rank)

    def set_permissions(self, rank: int) -> None:
        if rank == 1:
            self.permissions = ["read"]
        elif rank == 2:
            self.permissions = ["read", "write"]
        elif rank == 3:
            self.permissions = ["read", "write", "create", "delete"]
        else:
            self.permissions = []

    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self) -> str:
        pass

    @abstractmethod
    def create(self) -> str:
        pass

    @abstractmethod
    def delete(self) -> str:
        pass


class API(AbstractAPI):
    def read(self) -> str:
        return "Something read"

    def write(self) -> str:
        return "Something written"

    def create(self) -> str:
        return "Something created"

    def delete(self) -> str:
        return "Something deleted"


class ProxyAPI(AbstractAPI):
    def __init__(self, rank: int) -> None:
        super().__init__(rank)

    def read(self) -> str:
        if self.permissions.__contains__("read"):
            return "Something read"
        else:
            return "You dont have 'read' permissions"

    def write(self) -> str:
        if self.permissions.__contains__("write"):
            return "Something written"
        else:
            return "You dont have 'write' permissions"

    def create(self) -> str:
        if self.permissions.__contains__("create"):
            return "Something created"
        else:
            return "You dont have 'create' permissions"

    def delete(self) -> str:
        if self.permissions.__contains__("delete"):
            return "Something deleted"
        else:
            return "You dont have 'delete' permissions"


print("no api")
api = API(3)
print(api.read())
print(api.write())
print(api.create())
print(api.delete())
print("3")
proxy = ProxyAPI(3)
print(proxy.read())
print(proxy.write())
print(proxy.create())
print(proxy.delete())
print("2")
proxy = ProxyAPI(2)
print(proxy.read())
print(proxy.write())
print(proxy.create())
print(proxy.delete())
print("1")
proxy = ProxyAPI(1)
print(proxy.read())
print(proxy.write())
print(proxy.create())
print(proxy.delete())
print("0")
proxy = ProxyAPI(0)
print(proxy.read())
print(proxy.write())
print(proxy.create())
print(proxy.delete())


# -------------------------------------------------------


class AbstractHeavyObject(ABC):
    @abstractmethod
    def process(self) -> int:
        pass

    @abstractmethod
    def load_data(self) -> List[int]:
        pass


class HeavyObject(AbstractHeavyObject):
    def __init__(self):
        print("Creating Heavy Object...")
        self.data = self.load_data()

    def load_data(self):
        return [i for i in range(1000000000)]

    def process(self):
        print("Processing data...")
        return sum(self.data)


class HeavyObjectProxy(AbstractHeavyObject):
    def __init__(self):
        self._real_object = None

    def load_data(self):
        if self._real_object is None:
            self._real_object = HeavyObject()

    def process(self):
        self.load_data()
        return self._real_object.process()


ho_proxy = HeavyObjectProxy()
inp = input("Insert 'load' to load heavy object")
if inp == "load":
    result = ho_proxy.process()


# ---------------------------------------------------------


class AbstractFileSystem(ABC):
    def __init__(self, rank: int, dirs: List, dir_paths: List, files: List, file_paths: List, file_contents: List) -> None:
        self.rank = rank
        self.dirs = dirs
        self.dir_paths = dir_paths
        self.files = files
        self.file_paths = file_paths
        self.file_contents = file_contents
        self.current_path = ""

    @abstractmethod
    def cd(self, directory):
        pass

    @abstractmethod
    def cat(self, filename):
        pass
    
    @abstractmethod
    def ls(self, current_path):
        pass

    @abstractmethod
    def rm(self, filename):
        pass


class FileSystem(AbstractFileSystem):
    def __init__(self, rank: int, dirs: List, dir_paths: List, files: List, file_paths: List, file_contents: List) -> None:
        super().__init__(rank, dirs, dir_paths, files, file_paths, file_contents)

    def cd(self, directory):
        if directory == "" or directory == "." or directory is None:
            self.current_path = ""
        else:
            try:
                if self.dirs.__contains__(directory):
                    self.current_path = str(directory)
                else:
                    print(f"Directory {directory} does not exist")

            except ValueError:
               print("Invalid directory")

    def cat(self, filename):
        if self.files.__contains__(filename):
            if self.current_path == self.file_paths[self.files.index(filename)]:
                index = self.files.index(filename)
                print(f"{self.file_contents[index]}")
            else:
                print(f"File {filename} not found")
        else:
            print(f"File {filename} does not exist")

    def ls(self, current_path):
        for directory in self.dirs:
            print(directory)
            for fp in self.file_paths:
                if fp == directory:
                    filename = self.files[self.file_paths.index(fp)]
                    print(f"|    {filename}")

    def rm(self, filename):
        if self.files.__contains__(filename):
            if self.current_path == self.file_paths[self.files.index(filename)]:
                index = self.files.index(filename)
                fs.file_paths.pop(index)
                fs.file_contents.pop(index)
                fs.files.pop(index)
            else:
                print(f"File {filename} not found")
        else:
            print(f"File {filename} does not exist")


class FileSystemWithProxy(AbstractFileSystem):
    def __init__(self, rank: int, dirs: List, dir_paths: List, files: List, file_paths: List, file_contents: List) -> None:
        super().__init__(rank, dirs, dir_paths, files, file_paths, file_contents)

    def cd(self, directory):
        if self.rank >= 0:
            if directory == "" or directory == "." or directory is None:
                self.current_path = ""
            else:
                try:
                    if self.dirs.__contains__(directory):
                        self.current_path = str(directory)
                    else:
                        print(f"Directory {directory} does not exist")

                except ValueError:
                   print("Invalid directory")
        else:
            print("You don't have required permissions to change the directory")

    def cat(self, filename):
        if self.rank >= 1:
            if self.files.__contains__(filename):
                if self.current_path == self.file_paths[self.files.index(filename)]:
                    index = self.files.index(filename)
                    print(f"{self.file_contents[index]}")
                else:
                    print(f"File {filename} not found")
            else:
                print(f"File {filename} does not exist")
        else:
            print("You don't have required permissions to read this file")

    def ls(self, current_path):
        for directory in self.dirs:
            print(directory)
            for fp in self.file_paths:
                if fp == directory:
                    filename = self.files[self.file_paths.index(fp)]
                    print(f"|    {filename}")

    def rm(self, filename):
        if self.rank >= 2:
            if self.files.__contains__(filename):
                if self.current_path == self.file_paths[self.files.index(filename)]:
                    index = self.files.index(filename)
                    fs.file_paths.pop(index)
                    fs.file_contents.pop(index)
                    fs.files.pop(index)
                else:
                    print(f"File {filename} not found")
            else:
                print(f"File {filename} does not exist")
        else:
            print("You don't have required permissions to delete this file")


dirs = ["", "home", "bin", "home1", "home2", "bin1", "bin2"]
dir_paths = ["", "", "", "", "", "", ""]
files = ["to_do.txt", "trash1.txt", "trash2.txt", "trash3.txt", "to_do1.txt", "to_do2.txt", "trash4.txt", "trash5.txt",
         "trash6.txt", "trash7.txt"]
file_contents = ["- buy eggs\n- call mom", "dhfngjd", "adfgghtrad", "adgdhbdfg", "- write an essay\n- read a book", "- buy skateboard", "sdg", "grdgfd", "gddfg", "hatdr"]
file_paths = ["home", "bin", "bin", "bin", "home1", "home2", "bin1", "bin2", "bin1", "bin2"]

fs = FileSystem(1, dirs, dir_paths, files, file_paths, file_contents)

print("File system no proxy")
while True:
    prompt = input(f"{fs.current_path}> ")
    if len(prompt.split()) == 1:
        if prompt == "quit":
            break
        elif prompt == "cd":
            fs.cd(None)
        elif prompt == f"ls":
            fs.ls(fs.current_path)

    elif len(prompt.split()) == 2:
        part1, part2 = prompt.split()

        if prompt == f"cd {part2}":
            fs.cd(part2)
        elif prompt == f"cat {part2}":
            fs.cat(part2)
        elif prompt == f"rm {part2}":
            fs.rm(part2)


fs = FileSystemWithProxy(1, dirs, dir_paths, files, file_paths, file_contents)
print("File system with proxy")
while True:
    prompt = input(f"{fs.current_path}> ")
    if len(prompt.split()) == 1:
        if prompt == "quit":
            break
        elif prompt == "cd":
            fs.cd(None)
        elif prompt == f"ls":
            fs.ls(fs.current_path)

    elif len(prompt.split()) == 2:
        part1, part2 = prompt.split()

        if prompt == f"cd {part2}":
            fs.cd(part2)
        elif prompt == f"cat {part2}":
            fs.cat(part2)
        elif prompt == f"rm {part2}":
            fs.rm(part2)
