import time
import random
import string

class TreeNode:
    def __init__(self, song):
        self.song = song  # A Song object
        self.left = None
        self.right = None

class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def delete(self, key):
        if key in self.table:
            del self.table[key]

    def search(self, key):
        return self.table.get(key, None)

class MusicPlayer:
    def __init__(self):
        self.bst_root = None  # For BST
        self.hash_table = HashTable()  # For Hash Table

    def insert(self, song):
        # Insert into the BST
        self.bst_root = self._insert_bst(self.bst_root, song)
        # Insert into the hash table
        self.hash_table.insert(song.title, song)

    def _insert_bst(self, node, song):
        if node is None:
            return TreeNode(song)
        if song.title < node.song.title:
            node.left = self._insert_bst(node.left, song)
        elif song.title > node.song.title:
            node.right = self._insert_bst(node.right, song)
        return node

    def delete(self, title):
        song = self.hash_table.search(title)
        if song:
            self.bst_root = self._delete_bst(self.bst_root, song)
            self.hash_table.delete(title)

    def _delete_bst(self, node, song):
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
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, title):
        # Search in the hash table first
        return self.hash_table.search(title)

    def range_query(self, low, high):
        results = []
        self._range_query_bst(self.bst_root, low, high, results)
        return results

    def _range_query_bst(self, node, low, high, results):
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

def benchmark_music_player(num_songs):
    player = MusicPlayer()
    
    # Generate random songs
    songs = []
    for _ in range(num_songs):
        title = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
        artist = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
        songs.append(Song(title, artist))

    # Benchmark insertion
    start_time = time.time()
    for song in songs:
        player.insert(song)
    insertion_time = time.time() - start_time

    # Benchmark searching
    search_results = []
    start_time = time.time()
    for song in songs:
        search_results.append(player.search(song.title))
    search_time = time.time() - start_time

    # Benchmark deletion
    start_time = time.time()
    for song in songs:
        player.delete(song.title)
    deletion_time = time.time() - start_time

    print(f"Number of songs: {num_songs}")
    print(f"Insertion Time: {insertion_time:.6f} seconds")
    print(f"Search Time: {search_time:.6f} seconds")
    print(f"Deletion Time: {deletion_time:.6f} seconds")
    print("-" * 40)

if __name__ == "__main__":
    # Test with varying sizes of datasets
    sizes = [100, 1000, 5000, 10000]
    for size in sizes:
        benchmark_music_player(size)