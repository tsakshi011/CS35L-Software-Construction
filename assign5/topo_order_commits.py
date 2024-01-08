#!/usr/local/cs/bin/python3
import os
import sys
import zlib


class CommitNode:

    def __init__(self, commit_hash):
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

    def add_parent(self, parent_hash):  # each CommitNode set of parents
        self.parents.add(parent_hash)

    def add_child(self, child_hash):  # each CommitNode set of children
        self.children.add(child_hash)

    def get_num_of_children(self):
        return len(self.children)

    def remove_child(self, child):
        self.children.remove(child)

    def copy(self):  # create copy of each node
        new_node = CommitNode(self.commit_hash)
        new_node.parents = self.parents.copy()
        new_node.children = self.children.copy()
        return new_node


def get_git_dir():  # gets path of top-level .git
    current_path = os.getcwd()
    parent_path = os.path.dirname(current_path)
    while os.path.exists(parent_path) and current_path != '/':
        if os.access(current_path, os.R_OK):  # checking if access to read
            if ".git" in os.listdir(
                    current_path):  # check .git in directories of path
                current_path = os.path.join(current_path, ".git")
                os.chdir(current_path)
                return
        os.chdir(parent_path)
        current_path = os.getcwd()
        parent_path = os.path.dirname(current_path)

    sys.stderr.write("Not inside a Git repository")
    exit(1)


def local_branch_heads():  # returns branch heads
    branches = {}
    current_path = os.path.join(os.getcwd(),
                                "refs/heads")  # move to refs/heads in .git
    os.chdir(current_path)
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd(), topdown=True):
        for dir in dirnames:  # for each directory
            if not dir.startswith('.'):  # checks not hidden directory
                path = os.path.join(dirpath, dir)
                list_files = os.listdir(path)
                branch_name = dir
                for file in list_files:  # each file in directory
                    relative_path = os.path.join(path, file)
                    if os.path.isfile(relative_path):  # if path is a file
                        branch_name += "/" + file
                        with open(relative_path, 'rb') as f:
                            text = f.read()
                            decode_text = text.decode('utf-8')
                            hash = decode_text.strip(
                                '\n')  # extract the hash value
                            branches[branch_name] = hash
                        branch_name = branch_name[:branch_name.rfind("/")]
                    else:  # if path is a directory
                        branch_name = file
                        for i in os.listdir(
                                relative_path
                        ):  # go through each nested subdirectory
                            branch_name += "/" + i
                            list_files.append(branch_name)
                            branch_name = branch_name[:branch_name.rfind("/")]
            else:
                continue

        for file in filenames:  # for each file
            full_path = os.path.join(dirpath, file)
            with open(full_path, 'rb') as f:  # open the file
                text = f.read()
                decode_text = text.decode('utf-8')  # convert to readable text
                hash = decode_text.strip('\n')  # extract the hash value
                branches[file] = hash

        os.chdir('../../')  # move to parent-parent directory
        return branches


def get_parent_hash(hash):
    current_path = os.path.join(os.getcwd(), hash[0:2])
    os.chdir(current_path)
    file = os.getcwd() + "/" + hash[2:]  # extract file from hash
    compressed_contents = open(file, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    decode = decompressed_contents.decode(
        'utf-8')  # decompress and decode file contents
    parent_index = decode.find("parent")  # search for parent
    parent_list = []
    while parent_index != -1:
        start = parent_index + 7
        end = parent_index + 47
        parent_hash = decode[start:end]  # extract parent hash
        parent_index = decode.find("parent", end)
        parent_list.append(parent_hash)  # append parent hash to list
    return parent_list


def build_graph(branch_heads):  # build commit node graph
    graph = {}
    visited = set()  # keep track of visited sets
    process = []
    for branch_name, commit_hash in branch_heads.items():
        process.append(commit_hash)  # append head branches to process
    while process:
        curr_hash = process.pop()
        if curr_hash in visited:
            continue
        visited.add(curr_hash)  # update visited hash

        if curr_hash not in graph:  # if hash not in graph
            graph[curr_hash] = CommitNode(curr_hash)  # create new commitNode

        parent_list = get_parent_hash(curr_hash)  # get parents of commit hash

        for parent in parent_list:  # more than one parent
            graph[curr_hash].add_parent(parent)  # add parent to current hash
            if parent not in visited:
                process.append(parent)

            if parent not in graph:
                graph[parent] = CommitNode(parent)
            graph[parent].add_child(
                curr_hash)  # add to child/parent relationship

        os.chdir(os.path.dirname(os.getcwd()))

    return graph


def topological_sort(graph):  # sort the graph topologically
    result = []
    no_children = []

    for commit_hash, commit in graph.items():
        if commit.get_num_of_children() == 0:
            no_children.append(commit_hash)

    while len(no_children) > 0:  # while no_children is not empty
        n = no_children.pop()
        result.append(n)  # append to result

        for parent_hash, parent in graph.items():
            if n in parent.children:
                parent.remove_child(n)  # remove edge from child to parent
                if parent.get_num_of_children() == 0:
                    no_children.append(parent_hash)

    if len(result) < len(
            graph):  # error if resulting sorted list is smaller than graph
        return "ERROR"

    return result


def print_graph(sorted_list, graph, branch_heads):  # print the sorted graph
    for i in range(len(sorted_list) - 1):
        c1 = graph[sorted_list[i]]
        if c1.commit_hash in branch_heads.values():
            print(sorted_list[i], end=' ')
            names = []
            for name in branch_heads.keys():
                if branch_heads[name] == c1.commit_hash:
                    names.append(name)
            names.sort()
            print(*names, sep=' ')  # print branch heads names
        else:
            print(sorted_list[i])
        if sorted_list[i + 1] not in c1.parents:
            c2 = graph[sorted_list[i + 1]]
            sorted(c1.parents)
            print(*c1.parents, sep=' ', end='=')  # sticky end: print parents
            print()
            print()
            sorted(c2.children)
            print("=" + " ".join(c2.children))  # sticky start: print children
    c_final = graph[sorted_list[len(sorted_list) - 1]]
    if c_final.commit_hash in branch_heads.values():
        print(sorted_list[len(sorted_list) - 1], end=' ')
        names = []
        for name in branch_heads.keys():
            if branch_heads[name] == c_final.commit_hash:
                names.append(name)
        names.sort()
        print(*names, sep='')  # replace with name of branch
    else:
        print(sorted_list[len(sorted_list) - 1])


def topo_order_commits():
    get_git_dir()  # find the nearest git directory
    branch_heads = local_branch_heads()  # get branch heads
    branches = branch_heads.copy()

    new_path = os.path.join(os.getcwd(), "objects")
    os.chdir(new_path)

    commit_graph = build_graph(
        branch_heads)  # build the graph from the branches
    graph = {}
    for commit_hash, commit in commit_graph.items():
        graph[commit_hash] = commit_graph[commit_hash].copy()

    res = topological_sort(commit_graph)  # sort the graph

    if res != "ERROR":  # strace.out all PIDs same no subprocesses were spawned
        print_graph(res, graph, branches)


if __name__ == '__main__':
    topo_order_commits()
