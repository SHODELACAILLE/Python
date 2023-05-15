class node:
  def __init__(self, question, answer_to_go_here):
    self.answer_to_go_here = answer_to_go_here
    self.question = question
    self.next_nodes = []
    

  def size(self):
    count = 1   
    for node in self.next_nodes:
      count += node.size()  
    return count

  def deepth(self):
    Max = 0
    for node in self.next_nodes:
      if node.deepth() > Max:
        Max = node.deepth()
    return Max + 1
  
  def append(self,question,reponses,question_precedente):  
    if question_precedente == self.question:
      self.next_nodes.append(node(question,reponses))
    for n in self.next_nodes:
      n.append(question,reponses,question_precedente)


class tree:
  def __init__(self,question):
    self.first_node = node(question,"")
    self.current_node = self.first_node

  def size(self):
    return self.first_node.size()

  def deepth(self):
    return self.first_node.deepth()

  def append(self,question,reponses,question_precedente):  
    self.first_node.append(question,reponses,question_precedente)

  def get_question(self):
    return self.current_node.question

  def choice(self, message):
        if message == "quitter":
         exit()
        if message == "reset":
            self.reset()
            return self.current_node.question
        for n in self.current_node.next_nodes:
            if message in n.answer_to_go_here:
                self.current_node = n
                return n.question
        return "Réponse invalide, Réessayez"

  
  def reset(self):
    self.current_node = self.first_node
