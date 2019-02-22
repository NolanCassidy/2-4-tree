from sys import argv

class Node24:
    def __init__(self):
        self.parent = None
        self.nkeys = 0
        self.key = [None] * 3
        self.nchildren = 0
        self.child = [None] * 4

    def connect_child(self, child_number, child_pointer):
        self.child[child_number] = child_pointer
        if child_pointer != None:
            child_pointer.parent = self
            self.nchildren = min(self.nchildren+1, 4)

    def disconnect_child(self, child_number):
        child_pointer = self.child[child_number]
        self.child[child_number] = None
        if child_pointer != None:
            self.nchildren = max(self.nchildren-1, 0)
        return child_pointer

    def is_leaf(self):
        return self.nchildren == 0

    def is_full(self):
        return self.nkeys == 3

    def find_key(self, key):
        for j in range(3):
            if self.key[j] != None and self.key[j] == key:
                return j
        return -1

    def insert_key(self, key):
        self.nkeys += 1
        for j in range(2,-1,-1):
            if self.key[j] == None:
                pass
            else:
                if key < self.key[j]:
                    self.key[j+1] = self.key[j]
                else:
                    self.key[j+1] = key
                    return j+1
        self.key[0] = key
        return 0

    def remove_key(self): # remove largest item
        self.nkeys -= 1
        key = self.key[self.nkeys]
        self.key[self.nkeys] = None
        return key

class Tree24:
    class EmptyTree(Exception):
        def __init__(self, data=None):
            super().__init__(data)

    class NotFound(Exception):
        def __init__(self, data=None):
            super().__init__(data)

    def __init__(self):
        self.root = Node24()

    def root_key(self):
        if self.root.nkeys == 0:
            raise Tree24.EmptyTree('root() called on empty tree')
        l = []
        for i in range(self.root.nkeys):
            l.append(str(self.root.key[i]))
        return ' '.join(l)

    def height(self):
        if self.root.nkeys == 0:
            return 0
        h = 1
        x = self.root
        while x.nchildren != 0:
            h += 1
            x = x.child[0]
        return h

    def split(self, node):
        key2 = node.remove_key()
        child3 = node.disconnect_child(3)
        key1 = node.remove_key()
        child2 = node.disconnect_child(2)
        nodez = Node24()
        nodez.insert_key(key2)
        nodez.connect_child(0, child2)
        nodez.connect_child(1, child3)
        if node == self.root:
            self.root = Node24()
            parent = self.root
        else:
            parent = node.parent
        key_index = parent.insert_key(key1)
        j = parent.nkeys - 1
        while j > key_index:
            parent.child[j+1] = parent.child[j]
            j -= 1
        parent.connect_child(key_index+1, nodez)
        parent.connect_child(key_index, node)
        return parent

    def next_child(self, node, key):
        j = 0
        while j < node.nkeys:
            if key < node.key[j]:
                return node.child[j]
            j += 1
        return node.child[j]

    def insert(self, key):
        node = self.root
        found = False
        while not found:
            if node.is_full():
                parent = self.split(node)
                node = self.next_child(parent, key)
            elif node.is_leaf():
                found = True
            else:
                node = self.next_child(node, key)
        node.insert_key(key)

    def search_recursive(self, node, key):
        if node == None:
            return (None, 0)
        i = 0
        while i < node.nkeys and key > node.key[i]:
                i += 1
        if i < node.nkeys and key == node.key[i]:
            return (node, i)
        if node.nchildren == 0:
            return (None, 0)
        else:
            return self.search_recursive(node.child[i], key)

    def search(self, key):
        node, index = self.search_recursive(self.root, key)
        if node == None:
            raise Tree24.NotFound('{} not found in tree'.format(key))
        return node

    def inorder_recursive(self, node, l):
        if node != None:
            i = 0
            while i < node.nkeys:
                self.inorder_recursive(node.child[i], l)
                l.append(node.key[i])
                i += 1
            self.inorder_recursive(node.child[i], l)

    def to_list_inorder(self):
        l = []
        self.inorder_recursive(self.root, l)
        return l

def main() -> None:
    st = Tree24()
    f = open(argv[1], "r")
    nl = int(f.readline().strip())
    for i in range(nl):
        l = f.readline().strip()
        if l == 'inprint':
            keys = st.to_list_inorder()
            if len(keys) == 0:
                print('Empty')
            else:
                strings = [str(x) for x in keys]
                print(' '.join(strings))
        elif l == 'root':
            try:
                print(st.root_key())
            except Tree24.EmptyTree as e:
                print('Empty')
        elif l == 'height':
            print(st.height())
        else:
            v = l.split()
            if v[0] == 'insert':
                k = int(v[1])
                st.insert(k)
            elif v[0] == 'search':
                k = int(v[1])
                try:
                    z = st.search(k)
                    print('Found')
                except Tree24.NotFound as e:
                    print('NotFound')
            else:
                print("illegal input line:", l)
    f.close()

if __name__ == "__main__":
    main()
