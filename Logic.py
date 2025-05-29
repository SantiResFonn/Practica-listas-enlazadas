class Cancion:
    def __init__(self,titulo: str, artista: str,duracion: int):
        self.titulo: str = titulo
        self.autor: str = artista
        self.duracion: int = duracion
        self.prev: Cancion = None
        self.next: Cancion = None
    def __repr__(self) -> str:
        representacion = str(self.titulo) + "Autor:" + str(self.artista) + "Duracion:" + str(self.duracion) + "segundos"
        return representacion


class DoubleLinkedList:
    def __init__(self):
        self.head: Cancion = None
        self.tail: Cancion = None
        self.size: int = 0
    def append(self,titulo: str, artista: str,duracion: int):
        new_dnode = Cancion(titulo,artista,duracion)
        if self.size == 0:
            self.head = new_dnode
            self.tail = new_dnode
            self.size +=1
        else:
            self.tail.next = new_dnode
            new_dnode.prev = self.tail
        self.tail = new_dnode
        self.size +=1
    def insert(self, position: int, titulo: str, artista: str,duracion: int):
        new_dnode = Cancion(titulo,artista,duracion)
        current_node = self.head
        i = 0
        while current_node is not None:
            if position == 0:
                new_dnode.next = self.head
                self.head.prev = new_dnode
                self.head = new_dnode
                self.size +=1
                break
            if position == self.size:
                new_dnode.prev = self.tail
                self.tail.next = new_dnode
                self.tail = new_dnode
                self.size +=1
                break
            if i == position:
                current_node.prev.next = new_dnode
                new_dnode.next = current_node
                new_dnode.prev = current_node.prev
                current_node.prev = new_dnode
                self.size +=1
                break
            if position > self.size:
                print("Valor fuera de rango")
                break
        i+=1
        current_node = current_node.next
    def delete(self, position):
        current_node = self.head
        i=0
        while current_node is not None:
            if position == 0:
                current_node.next.prev = None
                self.head = current_node.next
                self.size-=1
                break
            if position >= self.size:
                print("Valor fuera de rango")
                break
            if i == position:
                if current_node == self.tail:
                    current_node.prev.next = current_node.next
                    self.size-=1
                    break
                current_node.prev.next = current_node.next
                current_node.next.prev = current_node.prev
                self.size-=1
                break
        i+=1
        current_node = current_node.next
    def delete_title(self, titulo:str):
        current_node = self.head
        while current_node is not None:
            if current_node.titulo.lower() == titulo.lower():
                if current_node == self.head:
                    current_node.next.prev = None
                    self.head = current_node.next
                    self.size-=1
                    break
                if current_node == self.tail:
                    current_node.prev.next = current_node.next
                    self.size-=1
                    break
                current_node.prev.next = current_node.next
                current_node.next.prev = current_node.prev
                self.size-=1
                break
        current_node = current_node.next
    def first(self):
        if self.head is None:
            return None
        return self.head
    def search(self, titulo: str):
        current_node = self.head
        while current_node is not None:
            if current_node.titulo.lower() == titulo.lower():
                return current_node
            current_node = current_node.next
        return 
    def __repr__(self) -> str:
        repr = ""
        current_node = self.head
        while(current_node is not None):
            repr += str(current_node.titulo) + "Autor:" + str(current_node.artista) + "Duracion:" + str(current_node.duracion) + "segundos" + "<->"
            current_node = current_node.next
        return repr.strip("<->")