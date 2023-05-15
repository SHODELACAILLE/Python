class node:     
  def __init__(self, data):
    self.data = data
    self.next_node = None


class queue:
  def __init__(self, data):
    self.first_node = node(data)
    self.current_node = self.first_node

  def pop(self):
    if self.first_node is None:
      return

    data = self.first_node.data
    self.first_node = self.first_node.next_node
    return data

  def append(self, data):
    current_node = self.first_node
    while current_node.next_node is not None:
      current_node = current_node.next_node
    current_node.next_node = node(data)

  def is_empty(self):
    return self.first_node is None

  def next(self):
    if self.current_node is None:
      return "La file est vide."
    elif self.current_node.next_node is None:
      return "Vous êtes déjà à la dernière commande."
    else:
      self.current_node = self.current_node.next_node
      return self.current_node.data

  def previous(self):
    if self.current_node is None:
      return "La file est vide."
    elif self.current_node == self.first_node:
      return "Vous êtes déjà à la première commande."
    else:
      current_node = self.first_node
      while current_node.next_node != self.current_node:
        current_node = current_node.next_node
      self.current_node = current_node
      return self.current_node.data
