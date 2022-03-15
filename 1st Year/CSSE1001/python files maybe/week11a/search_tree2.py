"""A more advanced implementation of a binary search tree."""


from itertools import chain


class BinarySearchTree(object) :
    """A binary search tree."""

    def __init__(self, iterable=[]) :
        self._root = None
        for element in iterable :
            self.insert(element)


    def insert(self, value) :
        """Add a value into the tree."""
        if self._root :
            self._root.insert(value)
        else :
            self._root = Node(value)


    def __iter__(self) :
        if self._root :
            return iter(self._root)
        else :
            return chain()


    def __contains__(self, value) :
        return self._root and value in self._root


    def __len__(self) :
        if self._root :
            return len(self._root)
        else :
            return 0


    def __str__(self) :
        if self._root :
            return str(self._root)
        else :
            return "()"


    def __repr__(self) :
        return "BinarySearchTree({0})".format(list(self))



class Node(object) :
    """A node in a binary search tree."""

    def __init__(self, value) :
        self._value = value
        self._left = BinarySearchTree()
        self._right = BinarySearchTree()


    def _choose_child(self, value) :
        """Choose the appropriate child to act on."""
        if value < self._value :
            return self._left
        else :
            return self._right


    def insert(self, value) :
        """Add a value into this node in the search tree."""
        self._choose_child(value).insert(value)


    def __contains__(self, value) :
        return value == self._value or value in self._choose_child(value)

    def __iter__(self) :
        return chain(self._left, [self._value], self._right)

    def __len__(self) :
        return len(self._left) + len(self._right) + 1

    def __str__(self) :
        return "({0}, {1}, {2})".format(self._left, self._value, self._right)



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
    return list(BinarySearchTree(lst))



if __name__ == "__main__":
    data = [5, 3, 2, 4, 7, 6, 8]
    print(tree_sort(data))

    tree = BinarySearchTree(data)
    print(tree)
    for value in tree :
        print(value, end="")
