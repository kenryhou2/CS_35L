#!/usr/bin/env python3

"""

Creator: Henry Kou 2019
UID: 204921239
CS35L: Section 8

Goal: Create a topological sorted list from an input Git repository
From following 5 steps:
1. Discover .git directory
2. Get list of local branch names
3. Build Commit Graph
4. Generate a topological ordering of commits in graph
5. Print commit hashes in order generated by step 4
   from smallest to largest.

Achievement Summary FOR GRADER
Steps 1, 2, 3, made modular for ease of grading. I'm sorry I couldn't finish in time :'(
Step 1 is pretty trivial to obtain the directory.
Step 2, the list of local branch names is in the list, local_branch_names.
Step 3, I performed an initial DFS to find my root commits stored in the form of Commit_Nodes.
Step 4 was not achieved.
Personally I thought this project was pretty fun except for the time limit. I spent a lot of time,
perhaps too much time trying to plan it all out instead of diving into it. It resulted in some early on design errors
like creating the git_obj_module variable, which accumulated error down the road.
I made some effort to disinclude global variables, also to explore different data structure capabilities in python.
Finally, I made a bunch of clean functions to aid my organization of main.
Thanks for a great quarter! I'll be excited to take CS111 next quarter. I really hope I don't get a terrible grade... I'm an EE major my gpa is shoddy enough :'(((
"""

import os, sys, zlib
from os import walk

#Classes

class CommitNode:
    def __init__(self, commit_hash):
        #member variables
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()        #set() without args returns empty set
        self.children = set()       #set() without args returns empty set

        #comparison operators for commitnode objects
    def __eq__ (self, other):
        return self.commit_hash == other.commit_hash
    def __hash__ (self):
        return id(self.commit_hash)
   

#Each head module is named the branch and the hash is stored as a string member variable.
#Git_Obj_Modules are created in step two to keep track of our head commit node info
#for when we search in the objects directory with the hash.

class Git_Obj_Module:
    def __init__(self, name, commit_hash):
        self.name = name
        commit_hash = commit_hash.replace("\n","")
        commit_hash = commit_hash.replace(" ","")
        self.commit_hash = commit_hash
        self.commit_dirname = commit_hash[0:2] #substring of first two chars of hash
        self.commit_filename = commit_hash[2:] #substring of rest of chars in hash besides first two.
    def __eq__ (self, other):
        return self.commit_hash == other.commit_hash
    def __hash__ (self):
        return id(self.commit_hash)


#Helper Functions

def getCurrFiles(myPath):
    f = []
    for (dirpath, dirnames, filenames) in walk(myPath):    #place all filenames within curr directory into filenames array 
        f.extend(filenames)                             #files all now in f.
        break
    return f

def getCurrDirs(myPath):
    f = []
    for (dirpath, dirnames, filenames) in walk(myPath):    #place all filenames within curr directory into filenames array 
        f.extend(dirnames)                             #files all now in f.
        break
    return f

def listDirs(myPath):
    f = []
    for (dirpath, dirnames, filenames) in walk(myPath):    #place all filenames within curr directory into filenames array 
        f.extend(dirnames)                             #files all now in f.
        break
    flag_git_exists = 0;
    for dir in f:
        #print(dir)
        if dir.endswith(".git"):
            flag_git_exists = 1;
        #iterate through the files.
    return flag_git_exists;

def decomp(objName):
    compressed_git_obj = open(objName, 'rb').read() #TODO open error catch
    decompressed_git_obj = zlib.decompress(compressed_git_obj)
    return decompressed_git_obj


#findAdjNodes(Node_Module, out): has to be called from the /object directory
#input is the git_obj_module to find the adj nodes of, 
#and output array of adj nodes with type git_obj_module, returns the number of parents.
def findAdjNodes(Node_Module, out): 
    #sample for one branch head
    os.chdir(Node_Module.commit_dirname)
    currPath = os.getcwd()
    #print(currPath)
    git_obj_bytes = decomp(Node_Module.commit_filename)
    #git obj is now text with the commit message...need to convert to string literal.
    git_obj_str = git_obj_bytes.decode()
    #print(git_obj_str)   
    commit_msg_list = git_obj_str.split("\n")
    
    adj_nodes = []
    numParent = 0
    for i in range(len(commit_msg_list)): #obtaining our parent hashes and info.
        #print(commit_msg_list[i])
        if "parent" in commit_msg_list[i]:
            numParent += 1
            parentStr = commit_msg_list[i].split(" ")
            #print("parent found") 
            #print(commit_msg_list[i])
            parent_hash = parentStr[1] #I should save this information
            #print(parent_hash)
            adj_nodes.append(Git_Obj_Module(str(1),parent_hash)) #think of parent commit objects as adjacent nodes in DFS

    #we now have adj_nodes hold all adjacent nodes with info
    for e in adj_nodes:
        out.append(e)
    os.chdir("..")
    return numParent

def runFindRootCommits(current_node, visited_set, commit_node_set, root_commits):
    DFS_Stack = []
    DFS_Stack.append(current_node) #current_node is a commit_node
    while DFS_Stack:
        cnode = DFS_Stack.pop()
        #print("\n\nchild:")
        #print(cnode.commit_hash)
        if cnode.commit_hash in visited_set:
            continue
        visited_set.add(cnode.commit_hash)
        #currCommit_Node = CommitNode(cnode.commit_hash)
        commit_node_set.add(cnode)    #set our curr commit node here
        adj_module_nodes = []
        current_git_node = Git_Obj_Module("current",cnode.commit_hash)
        numP = findAdjNodes(current_git_node,adj_module_nodes)
        if numP == 0:
            root_commits.append(cnode)
        for parent in adj_module_nodes:
            parent_Commit_Node = CommitNode(parent.commit_hash)
            if parent_Commit_Node.commit_hash not in visited_set:
                DFS_Stack.append(parent_Commit_Node)
            cnode.parents.add(parent_Commit_Node)
            parent_Commit_Node.children.add(cnode)  #set our child params and childs parents here
            commit_node_set.add(parent_Commit_Node)
            #print("parent:")
            #print(parent.commit_hash)
    return root_commits



     
def main():
    # 1) Discover .git directory
    # Search method: No input arguments, start in current directory and then move to parent directory
    
    #Search condition variables
    flag_git_exists = 0; #initialize our if .git folder is found flag to 0.
    currPath = os.getcwd() #used to check error condition.
    #print(currPath)
    if currPath == "/":
        print("Not inside a Git repository")
        exit(1)
    flag_git_exists = listDirs(".")

    #if the .git directory is not found, and parent directory is not '/', 
    #go to parent directory and search for .git again
    while flag_git_exists == 0:
        os.chdir("..")

        if currPath == "/":
            print("Not inside a Git repository")
            exit(1)

        flag_git_exists = listDirs(".")
        currPath = os.getcwd()
        #print(currPath)
    #otherwise if we have reached this point, we have found .git directory.
    #print("found .git directory")
   

    # 2) Get list of local branch names
    #focus on refs and object directories.
    #beware branch names with forward slashes.
    #use zlib library to decompress Git objects.
    #assume all objects are loose.
    #at this point we are in parent directory of .git directory.
    
    os.chdir(".git/refs/heads") #TODO error checks of the navigation
    #at this point we are in .git/refs/heads.
    currPath = os.getcwd()
    local_branch_names = getCurrFiles(currPath)
    local_header_modules = [] #gonna hold the Git_Obj_Modules for each branch.
    for l  in range(len(local_branch_names)):
        #print(l)
        commit_hash_str = ""
        with open(local_branch_names[l], 'r') as data:
            commit_hash_str = data.read()
        temp = Git_Obj_Module(local_branch_names[l],commit_hash_str)
        #print(temp.name)
        #print(temp.commit_dirname + temp.commit_filename)
        #print(temp.commit_hash)
        local_header_modules.append(temp)
  
    # 3) Build the commit graph
    # Each commit can be represented as an instance of the CommitNode class
    #The commit graph consists of all the commit nodes from all the branches. 
    #Each commit node might have multiple parents and children. 
    #after finding the heads for each branch, perform a depth-first search traversal 
    #starting from the branch head, 
    #i.e. the commit pointed to by the branch, 
    #to establish the parent-child relationships between the commit nodes. 
    #The traversal should trace through the parents, and 
    #for every possible pair of parent and child, add the child hash to the parent node's children, 
    #and add the parent hash to the child node's parents. 
    #The leaf nodes for each branch will be the root commits for that branch, 
    #where the leaf nodes are the nodes without any parents. 
    #Let root_commits be the union of all the leaf nodes across all the branches.

    os.chdir("../../objects") #TODO error check on navigation
    currPath = os.getcwd()
    #print(currPath) #-> should be in objects dir.

    #create data structures per DFS run
    visited_set = set()         #used to contain visited commit hashes
    commit_node_set = set()     #used to contain commit nodes
    #blacked_set = set()         #used to contain visited commit hashes
    #DFS_Stack = []              #holds the commit nodes in order we want #initialize a stack the same as a list in python3??
    all_root_commits = []
    #performing DFS on one branch head.
    
    
    #print(current_node.commit_hash)

    # 4) Generate a topological ordering of the commits in the graph
    # where the nodes in root_commits are the oldest ancestors. 
    # One way to generate a topological ordering is to use a depth-first search
    #perform DFS from root_commits and navigate through commit nodes with children pointer.

    for i in range(len(local_header_modules)):
        current_node = local_header_modules[i]
        current_Commit_node = CommitNode(current_node.commit_hash)
        runFindRootCommits(current_Commit_node,visited_set,commit_node_set,all_root_commits)
    
    #make root_commits unique
    root_commits_set = list(set(all_root_commits))
    commit_Node_List = list(commit_node_set) # making our commit_Node_List iterable.
    #from our root_commit we'll run DFS again to generate our topological sort.
    
    DFS_Stack = []
    visited = set()
    topoSortedList = []
    
    for i in range(len(root_commits_set)):
        curr_root = root_commits_set[i]
        DFS_Stack.append(curr_root)
        
    while DFS_Stack:
            r = DFS_Stack.pop()
            if r not in visited:
                visited.add(r)
            else:
                continue
            childs = list(r.children)
            all_childs_visited = 0
            for c in childs:
                if c not in visited:
                    DFS_Stack.append(c)
                else: #coves case that childs is 0
                    all_childs_visited = 1
            if all_childs_visited:
                topoSortedList.append(r)
                all_childs_visited = 0
                #do something
            
            #do something

    
    for i in commit_Node_List:
        print(i.commit_hash)

    
    


    """ Recursive commit node creation... Not the right way.
    visited_set.add(current_node.commit_hash)
    #find adjacent nodes aka child nodes with type Git_Obj_Module
    adj_nodes = []
    numP = findAdjNodes(local_header_modules[0],adj_nodes) #when u call findAdj nodes, make sure you are in objects dir.
    #print(adj_nodes)
    currCommit_Node = CommitNode(current_node.commit_hash)
    commit_node_set.add(currCommit_Node)
    #now iterate through all the adjacent nodes and set corresponding info into commit_node objects          
    Child_Commit_Nodes = []
    for n in range(numP): 
        currCommit_Node.children.add(adj_nodes[n].commit_hash)
        child_Commit_Node = CommitNode(adj_nodes[n].commit_hash) #create a child Commit Node and set to the hash of the child
        child_Commit_Node.parents.add(currCommit_Node.commit_hash) #Set the parent hash of child Commit Node to currCommit's hash.
        Child_Commit_Nodes.append(child_Commit_Node)
        commit_node_set.add(child_Commit_Node)
    #at this point we have our children in an array in type Commit_Node, fully filled..

    blacked = 0 #use as flag for case where node has no children or it has all visited children
    
    
    for l in range(len(Child_Commit_Nodes)): #iterate through children to see if all visited or no children exist
        if Child_Commit_Nodes[l].commit_hash in visited_set or len(Child_Commit_Nodes) == 0:
            blacked = 1
    if blacked:
        blacked_set.add(Child_Commit_Nodes[l].commit_hash)
        blacked = 0 #reset this flag
    else: #not blacked
        #put curr node in the stack
        DFS_Stack.append(current_node)
        #print(current_node.commit_hash)
        #put curr node's adjacent nodes on the stack
        for i in range(numP):
            DFS_Stack.append(adj_nodes[i])
            #print(adj_nodes[i].commit_hash)

    if not DFS_Stack: #if the stack is empty,
       #we are done with DFS
       print("Done with DFS in this branch")
    else:
    #else if stack is not empty,
        processingNode = DFS_Stack.pop()
        #print(processingNode.commit_hash)
        if processingNode not in visited_set:
            #print("not visited")
    """


    
    """
    print(commit_node_set)
    print(currCommit_Node.commit_hash)
    print(currCommit_Node.children)
    print(Child_Commit_Nodes[0].commit_hash)
    print(Child_Commit_Nodes[0].parents)
    """

    """ Stack playground
    mystack = []
    mystack.append('1')
    mystack.append('2')
    var = mystack.pop()
    var = mystack.pop()
    print(mystack)
    print(var)
    if not mystack:
        print("yo it's empty")
    """
    
    #GIT_OBJ_COMPARISON_OPERATOR TEST
    #git1 = Git_Obj_Module("909","jkjk")
    #git2 = Git_Obj_Module("1","jkjk")
    #print(git1 == git2)







    #Now perform for each branch head
    #for l in range(len(local_header_modules)):





    exit(1)




    
    




    
if __name__ == "__main__":
    main()