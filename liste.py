class node: 
    def __init__(self, data):
        self.data = data
        self.next_node = None
        self.previous_node = None

class hashmap:
    def __init__(self,length):
        self.datas = []
        for i in range(length):
            self.datas.append([])

    def append(self, key, value):
        hashed_key = hash(key)
        indice = hashed_key % len(self.datas)
        self.datas[indice].append((key, value))

    def get(self, key):
        hashed_key = hash(key)
        indice = hashed_key % len(self.datas)
        for key_datas, value_datas in self.datas[indice]:
            if key == key_datas:
                return value_datas
        return None

class historique_commandes:
    def __init__(self):
        self.histories = hashmap(1000) # dictionnaire pour stocker les historiques de chaque utilisateur

    def clear(self, user_id):
        self.histories.append(user_id, None)
        self.current_node = None

    def add_command(self, user_id, data):
        new_node = node(data)

        if self.histories.get(user_id) is None:
            self.histories.append(user_id, new_node) # si l'utilisateur n'a pas d'historique, on en crée un nouveau
        else:
            current_node = self.histories.get(user_id)
            while current_node.next_node is not None:
                current_node = current_node.next_node
            current_node.next_node = new_node
            new_node.previous_node = current_node
        self.current_node = new_node # mettre à jour la position actuelle dans l'historique

    def get_last_command(self, user_id):
        if self.histories.get(user_id) is None:
            return "Aucune commande."
        else:
            current_node = self.histories.get(user_id)
            while current_node.next_node is not None:
                current_node = current_node.next_node
            return f"Dernière commande : {current_node.data}"

    def get_all_commands(self, user_id):
        if self.histories.get(user_id) is None:
            return "Aucune commande."
        else:
            commands = []
            current_node = self.histories.get(user_id)
            while current_node is not None:
                commands.append(current_node.data)
                current_node = current_node.next_node
            return commands

    def get_next_command(self, user_id):
        if self.histories.get(user_id) is None:
            return "Aucune commande."
        elif self.current_node.next_node is None:
            return "Vous êtes déjà à la dernière commande."
        else:
            self.current_node = self.current_node.next_node
            return self.current_node.data

    def get_previous_command(self, user_id):
        if self.histories.get(user_id) is None:
            return "Aucune commande."
        elif self.current_node.previous_node is None:
            return "Vous êtes déjà à la première commande."
        else:
            self.current_node = self.current_node.previous_node
            return self.current_node.data
