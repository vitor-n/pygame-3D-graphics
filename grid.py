
vertices = [[0,0,0], [0,0,1], [1,0,0], [1,0,1]]

faces = [[1,2], [1,3], [2,4], [3,4]]

pos = 0

with open('grid.obj', 'w') as file:
    for i in range(-10,10):
        for j in range(-10,10):


            for v in vertices:
                file.write(f"v {v[0] + i} {0} {v[2] + j}")
                file.write("\n")
            
            for f in faces:
                file.write(f"f {f[0] + pos} {f[1] + pos}")
                file.write("\n")
            
            pos += 4
            file.write("\n")
