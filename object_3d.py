
class Object_3D:
    def __init__(self, file_path: str):
        file = open(file_path)
        self.vertices = []
        self.faces = []
        for line in file:
            if line.startswith("v"):
                try:
                    _, x,y,z = line.split()
                except:
                    pass
                self.vertices.append([float(x),float(y),float(z),1])
            if line.startswith("f"):
                _, *indices = line.split()
                self.faces.append(indices)
    
