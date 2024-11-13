import copy
import random
from collections import deque


def generate_crossword(n, tree):
    # go from top left to bottom right
    # do dfs, randomize letter chosen
    # check if state is valid before appending to queue
    # this can be done by checking if current column can be extended
    q = deque()
    q.append((0, 0, [['.'] * n for _ in range(n)]))
    while q:
        i, j, grid = q.pop()
        node = tree.get_prefix_child(''.join(grid[i][:j]))
        # print(i, j, grid, node.val)
        for child in random.sample(node.children, len(node.children)):
            down_prefix = ''.join(grid[k][j] for k in range(i)) + child.val
            child_node = tree.get_prefix_child(down_prefix)
            # print(down_prefix, child_node)
            if child_node:
                next_grid = copy.deepcopy(grid)
                next_grid[i][j] = child_node.val
                if i == n - 1 and j == n - 1:
                    return next_grid
                next_i = i + 1 if j == n - 1 else i
                next_j = 0 if j == n - 1 else j + 1
                q.append((next_i, next_j, next_grid))
    return None


class LetterNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def __eq__(self, other):
        return self.val == other.val

    # get node corresponding to given prefix or None if doesn't exist
    def get_prefix_child(self, prefix):
        curr = self
        for c in prefix:
            if LetterNode(c) not in curr.children:
                return None
            curr = curr.children[curr.children.index(LetterNode(c))]
        return curr


def build_tree(words):
    # build a tree of height 5
    root = LetterNode('.')
    for word in words:
        curr = root
        for c in word:
            if LetterNode(c) in curr.children:
                curr = curr.children[curr.children.index(LetterNode(c))]
            else:
                curr.children.append(LetterNode(c))
                curr = curr.children[-1]
    return root


def get_padded_words(word, length):
    pads = length - len(word)
    return [l * '.' + word + (pads - l) * '.' for l in range(pads + 1)]


if __name__ == '__main__':
    file_path = 'data/raw/google-10000-english.txt'
    # file_path = '5word.txt'
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            if 3 <= len(word) <= 5:
                words.extend(get_padded_words(word, 5))
    tree = build_tree(words)
    res = generate_crossword(5, tree)
    for row in res:
        print(' '.join(row))
