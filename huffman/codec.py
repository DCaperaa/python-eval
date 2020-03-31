class Node:

    def __init__(self, figure, *char: str):
        # *char permet d'associer, éventuellement, un caractère au noeud
        # (pour les feuilles les plus hautes dans l'arbre de Huffman).
        self.figure = figure
        for character in char:
            self.char = character
        self.root = None
        self.leaves = []
        self.id = None  # Clef primaire.

    def add_id(self, list_id):
        '''Connaissant les id de tous les autres noeuds de l'arbre (dans
        list_id), donne un nouvel identifiant au nouveau noeud.'''
        self.id = max(list_id) + 1

    def add_root(self, root):
        self.root = root

    def add_leaves(self, left, right):
        self.leaves.append(left)
        self.leaves.append(right)
        # Le premier élément est toujours la feuille gauche.


class Tree:

    def __init__(self):
        self.nodes = []
        # On construit également une liste des noeuds basiques (contenant
        # un caractère), qui nous servira pour la lecture de l'arbre.
        self.basic_nodes = []

    def list_id(self):
        return [0] + [node.id for node in self.nodes]

    def add_basic_node(self, figure, char):
        '''Ajoute les noeuds initiaux de l'arbre, ie ceux associés à
        un caractère.'''
        basic_node = Node(figure, char)
        basic_node.add_id(self.list_id())
        self.nodes.append(basic_node)
        self.basic_nodes.append(basic_node)

    def add_node(self, left: Node, right: Node):
        '''Ajout d'un noeud normal, qui se fait toujours à partir de
        deux noeuds initiaux déjà présents dans l'arbre, left et right.
        Retourne également le noeud ajouté.'''
        new_figure = left.figure + right.figure
        new_node = Node(new_figure)
        new_node.add_id(self.list_id())
        new_node.add_leaves(left, right)
        left.add_root(new_node)
        right.add_root(new_node)
        self.nodes.append(new_node)
        return new_node


class TreeBuilder:

    def __init__(self, text: str):
        self.text = text
        self.length = len(text)

    def occurrences(self):
        '''Construit un dictionnaire donnant la fréquence d'apparition de
        chaque caractère contenu dans self.text.'''
        D = {}
        for char in self.text:
            # On initialise le compteur d'occurrence à 0 si nécessaire
            D.setdefault(char, 0)
            D[char] = D[char] + 1
        return D

    def tree(self):
        tree = Tree()
        D = self.occurrences()
        # Ajout de tous les noeuds initiaux
        for char, occurrences in D.items():
            tree.add_basic_node(occurrences, char)
        unrooteds = tree.nodes.copy()  # Contiendra tous les noeuds auxquels
        # on n'a pas encore affecté de racine.
        while len(unrooteds) != 1:
            figures = [node.figure for node in unrooteds]
            # On construit la liste des indices du minimum de la liste, car il
            # y distinction de cas selon que le minimum est unique ou pas.
            index_min = [i for i, x in enumerate(figures) if x == min(figures)]
            if len(index_min) == 1:
                i = index_min[0]
                figures_copy = figures.copy()
                figures.remove(min(figures))
                j = figures_copy.index(min(figures))  # indice du deuxième min
                new_node = tree.add_node(unrooteds[i], unrooteds[j])
                i, j = min(i, j), max(i, j)  # j>i
            else:
                i, j = index_min[0], index_min[1]  # j>i
                new_node = tree.add_node(unrooteds[i], unrooteds[j])
            del unrooteds[j], unrooteds[i]
            unrooteds.append(new_node)
        return tree


class Codec:

    def __init__(self, binary_tree: Tree):
        self.binary_tree = binary_tree
        # Longueur du texte associé à self.binary_tree
        self.length = sum(node.figure for node in self.binary_tree.basic_nodes)
        self.dict = {}  # donnera la traduction de chaque caractère de text.

    def fill_dict(self):
        '''Remplit self.dict.'''
        for node1 in self.binary_tree.basic_nodes:
            binary_code = ''
            roots = []
            node2 = node1
            # On va lister toutes les racines de node1.
            while node2:
                # node2 vaudra None lorsqu'on aura remonté tout l'arbre.
                roots.append(node2)
                node2 = node2.root
            # On cherche si les noeuds de roots sont les feuilles gauches ou
            # droites de leur racine, et on en déduit binary_code.
            roots.reverse()
            for c, node in enumerate(roots[:-1]):
                if node.leaves[0].id == roots[c+1].id:
                    # roots[c+1] est la feuille gauche de node.
                    binary_code += '0'
                else:
                    # roots[c+1] est la feuille droite de node.
                    binary_code += '1'
            self.dict[node1.char] = binary_code

    def encode(self, text):
        self.fill_dict()
        return ''.join([self.dict[char] for char in text])

    def decode(self, encoded):
        decoded = ''
        i = 0
        while i <= len(encoded)-1:
            j = 0
            possible_chars = [x for x in self.dict.keys()]
            while len(possible_chars) != 1:
                for char in possible_chars.copy():
                    if(j >= len(self.dict[char]) or self.dict[char][j] !=
                            encoded[i+j]):
                        possible_chars.remove(char)
                        # On supprime char dès que sa traduction en binaire ne
                        # correspond plus au texte.
                j += 1
            decoded += possible_chars[0]
            i += j
        return decoded


text = "a dead dad ceded a bad babe a beaded abaca bed"
builder = TreeBuilder(text)
binary_tree = builder.tree()
codec = Codec(binary_tree)
encoded = codec.encode(text)
decoded = codec.decode(encoded)
