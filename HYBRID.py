class TreeNode:
    def __init__(self, song):
        self.song = song  # A Song object
        self.left = None
        self.right = None

class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        # Store value with a given key in the hash table
        self.table[key] = value

    def delete(self, key):
        # Remove the entry with the given key from the hash table
        if key in self.table:
            del self.table[key]

    def search(self, key):
        # Retrieve the value associated with the given key
        return self.table.get(key, None)

class MusicPlayer:
    def __init__(self):
        self.bst_root = None  # For BST
        self.hash_table = HashTable()  # For Hash Table

    def insert(self, song):
        
        # Insert the song into both the binary search tree and the hash table
        # 1. Call _insert_bst with the current root and the new song
        # 2. Insert the song into the hash table using the song's title as key
        self.bst_root = self._insert_bst(self.bst_root, song)
        self.hash_table.insert(song.title, song)

    def _insert_bst(self, node, song):
        
        # If the current node is None, create a new TreeNode for the song
        # If the song's title is less than the node's song title, recurse left
        # If the song's title is greater than the node's song title, recurse right
        if node is None:
            return TreeNode(song)
        if song.title < node.song.title:
            node.left = self._insert_bst(node.left, song)
        elif song.title > node.song.title:
            node.right = self._insert_bst(node.right, song)
        return node

    def delete(self, title):
        
        # Search for the song by title in the hash table
        # If found, delete it from both the hash table and the binary search tree
        song = self.hash_table.search(title)
        if song:
            self.bst_root = self._delete_bst(self.bst_root, song)
            self.hash_table.delete(title)

    def _delete_bst(self, node, song):
        
        # If the current node is None, return None (base case)
        # If the song's title is less, recurse left
        # If the song's title is greater, recurse right
        # If it is the node to be deleted:
        # 1. If it has one or zero children, return the non-null child or None
        # 2. If it has two children, find the smallest node in the right subtree,
        #    replace the song info with the smallest, and delete that smallest node
        if node is None:
            return node
        if song.title < node.song.title:
            node.left = self._delete_bst(node.left, song)
        elif song.title > node.song.title:
            node.right = self._delete_bst(node.right, song)
        else:
            # Node with one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._min_value_node(node.right)
            node.song = temp.song
            node.right = self._delete_bst(node.right, temp.song)
        return node

    def _min_value_node(self, node):
        
        # Traverse to the leftmost node in the subtree, which is the minimum value
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, title):
        
        # Search for a song in the hash table using the song's title
        return self.hash_table.search(title)

    def range_query(self, low, high):
        
        # Initialize an empty result list
        # Perform a range search in the BST for values within the low and high limits
        results = []
        self._range_query_bst(self.bst_root, low, high, results)
        return results

    def _range_query_bst(self, node, low, high, results):
        
        # If the current node is not None:
        # 1. Recursively check the left subtree if the low limit is less than the node's title
        # 2. If the node's title is within the range, add the song to results
        # 3. Recursively check the right subtree if the high limit is greater than the node's title
        if node is not None:
            if low < node.song.title:
                self._range_query_bst(node.left, low, high, results)
            if low <= node.song.title <= high:
                results.append(node.song)
            if high > node.song.title:
                self._range_query_bst(node.right, low, high, results)

class Song:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"'{self.title}' by {self.artist}"


# Example usage
player = MusicPlayer()
player.insert(Song("Song One", "Artist A"))
player.insert(Song("Song Two", "Artist B"))
player.insert(Song("Another Song", "Artist C"))

print("Searching for 'Song Two':", player.search("Song Two"))
print("Searching for 'Song Three':", player.search("Song Three"))

player.delete("Song One")

print("Range query for songs between 'Song' and 'Song Z':")
for song in player.range_query("Song", "Song Z"):
    print(song)