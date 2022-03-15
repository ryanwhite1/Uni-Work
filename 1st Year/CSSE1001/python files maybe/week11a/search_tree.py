class Node(object) :
    """A node in a binary search tree."""
    
    def __init__(self, value) :
        """A new Node in a Binary Search Tree
     
        Parameters:
            value: Element to be stored in this Node.
                   Must be comparable by ==, > and <.
        """
        self._value = value
        self._left = None
        self._right = None


    def insert(self, value) :
        """Add 'value' into this Node in the search tree.
     
        Parameters:
            value: Element to be stored in this Node.
            Must be comparable by ==, &gt;, &lt;.
        """
        if value < self._value :
            if self._left is None :
                self._left = Node(value)
            else :
                self._left.insert(value)
        else :
            if self._right is None :
                self._right = Node(value)
            else :
                self._right.insert(value)


    def to_list(self) :
        """Return a sorted list of the values of this node's children."""
        result = []
        if self._left is not None :
            result.extend(self._left.to_list())
        result.append(self._value)
        if self._right is not None :
            result.extend(self._right.to_list())
        return result


    def __contains__(self, value) :
        if value == self._value :
            return True
        elif value < self._value and self._left is not None :
            return value in self._left
        elif value > self._value and self._right is not None :
            return value in self._right
        else :
            return False


    def __str__(self) :
        return "({0}, {1}, {2})".format(self._left, self._value, self._right)



class BinarySearchTree(object) :
    """A binary search tree."""
    
    def __init__(self) :
        """ A new empty binary search tree."""
        self._root = None
        

    def insert(self, value) :
        """Add 'value' into the tree.
        
        Preconditions:
            'value' is comparable by at least the ==, > and < operators.
        """
        if self._root is None :
            self._root = Node(value)
        else :
            self._root.insert(value)


    def to_list(self):
        """Return a sorted list of the values in this tree."""
        if self._root is None :
            return []
        return self._root.to_list()


    def __contains__(self, value) :
        return self._root is not None and value in self._root


    def __str__(self) :
        if self._root is None :
            return "()"
        return str(self._root)



def tree_sort(lst) :
    """A sort implementation using a tree.

    Parameters:
        lst: List of elements to be sorted.

    Return:
        Sorted list of elements.

    Preconditions:
        All elements of 'lst' are comparable by
        at least the ==, > and < operators.
    """
    tree = BinarySearchTree()
    for element in lst :
        tree.insert(element)
    return tree.to_list()



if __name__ == "__main__" :
    print(tree_sort([4,2,6,1]))
