import marimo

__generated_with = "0.10.2"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("""#3D Geometry File Formats""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## About STL

        STL is a simple file format which describes 3D objects as a collection of triangles.
        The acronym STL stands for "Simple Triangle Language", "Standard Tesselation Language" or "STereoLitography"[^1].

        [^1]: STL was invented for – and is still widely used – for 3D printing.
        """
    )
    return


@app.cell
def _(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


@app.cell
def _(mo):
    with open("data/teapot.stl", mode="rt", encoding="utf-8") as _file:
        teapot_stl = _file.read()

    teapot_stl_excerpt = teapot_stl[:723] + "..." + teapot_stl[-366:]

    mo.md(
        f"""
    ## STL ASCII Format

    The `data/teapot.stl` file provides an example of the STL ASCII format. It is quite large (more than 60000 lines) and looks like that:
    """
        + f"""```
    {teapot_stl_excerpt}
    ```
    """
        + """
    """
    )
    return teapot_stl, teapot_stl_excerpt


@app.cell
def _():
    ## Essayons d'abord de créer une seule face
    stl_carre = """ 
    solid carre
        facet normal 0 0 1
            outer loop
                vertex 0 0 0
                vertex 1 0 0 
                vertex 0 1 0 
            endloop
        endfacet
        facet normal 0 0 1
            outer loop
                vertex 1 1 0
                vertex 0 1 0 
                vertex 1 0 0 
            endloop
        endfacet
    endsolid carre
    """
    # Define the file path
    file_path = "data/carré.stl"

    # Write the STL data to the file
    with open(file_path, "w") as file:
        file.write(stl_carre)

    print(f"STL file saved as {file_path}")
    return file, file_path, stl_carre


@app.cell
def _():
    ## Construisons maintenant le cube
    stl_cube = """ 
    solid cube
        facet normal 0 0 1
            outer loop
                vertex 0 0 0
                vertex 0 1 0 
                vertex 1 0 0 
            endloop
        endfacet
        facet normal 0 0 1
            outer loop
                vertex 1 1 0
                vertex 1 0 0 
                vertex 0 1 0
            endloop
        endfacet
        facet normal 1 0 0
            outer loop
                vertex 0 0 0 
                vertex 0 0 1
                vertex 0 1 0
            endloop
        endfacet
        facet normal 1 0 0
            outer loop
                vertex 0 1 1 
                vertex 0 1 0
                vertex 0 0 1
            endloop
        endfacet
        facet normal 0 -1 0 
            outer loop 
                vertex 0 1 1 
                vertex 1 1 1
                vertex 0 1 0 
            endloop
        facet normal 0 -1 0 
            outer loop 
                vertex 1 1 0 
                vertex 0 1 0
                vertex 1 1 1 
            endloop
        endfacet
        facet normal 0 1 0 
            outer loop 
                vertex 0 0 0 
                vertex 1 0 1
                vertex 0 0 1
            endloop 
        endfacet
        facet normal 0 1 0 
            outer loop 
                vertex 0 0 0 
                vertex 1 0 0 
                vertex 1 0 1
            endloop
        endfacet
        facet normal -1 0 0
            outer loop
                vertex 1 0 0
                vertex 1 1 0
                vertex 1 0 1
            endloop
        endfacet
        facet normal -1 0 0 
            outer loop
                vertex 1 0 1 
                vertex 1 1 0
                vertex 1 1 1
            endloop
        endfacet
        facet normal 0 0 -1
            outer loop
                vertex 0 0 1 
                vertex 1 0 1
                vertex 1 1 1
            endloop
        endfacet
        facet normal 0 0 -1
            outer loop 
                vertex 0 1 1
                vertex 0 0 1
                vertex 1 1 1
            endloop 
        endfacet
    endsolid cube
    """
    # Define the file path
    file_path2 = "data/cube.stl"

    # Write the STL data to the file
    with open(file_path2, "w") as file2:
        file2.write(stl_cube)

    print(f"STL file saved as {file_path2}")
    return file2, file_path2, stl_cube


@app.cell
def _(mo):
    mo.md(f"""

      - Study the [{mo.icon("mdi:wikipedia")} STL (file format)](https://en.wikipedia.org/wiki/STL_(file_format)) page (or other online references) to become familiar the format.

      - Create a STL ASCII file `"data/cube.stl"` that represents a cube of unit length  
        (💡 in the simplest version, you will need 12 different facets).

      - Display the result with the function `show` (make sure to check different angles).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""## STL & NumPy""")
    return


@app.cell
def _(np):
    def make_STL(triangles, normals, name=None):
        stl_str = f"solid {name} \n"
        for i in range(len(triangles)):
            if normals:
                stl_str += f"\tfacet normal {normals[i][0]} {normals[i][1]}    {normals[i][2]}\n\t\touter loop\n\t\t\t"
            else: 
                AB=triangles[i][1]- triangles[i][0]
                BC=triangles[i][2]- triangles[i][1]
                stl_str += f"\tfacet normal {np.cross(AB,BC)[0]} {np.cross(AB,BC)[1]} {np.cross(AB,BC)[2]}\n\t\touter loop\n\t\t\t"
            stl_str+=f"vertex {triangles[i][0][0]} {triangles[i][0][1]} {triangles[i][0][2]}\n\t\t\t"
            stl_str+=f"vertex {triangles[i][1][0]} {triangles[i][1][1]} {triangles[i][1][2]}\n\t\t\t"
            stl_str+=f"vertex {triangles[i][2][0]} {triangles[i][2][1]} {triangles[i][2][2]}\n\t\t"
            stl_str+="endloop\n\tendfacet\n"
        stl_str +=f"endsolid {name}"
        return (stl_str)
    return (make_STL,)


@app.cell
def _(make_STL, np):
    print (make_STL(np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    ),normals=None, name="square"))
    return


@app.cell
def _(mo):
    mo.md(rf"""

    ### NumPy to STL

    Implement the following function:

    ```python
    def make_STL(triangles, normals=None, name=""):
        pass # 🚧 TODO!
    ```

    #### Parameters

      - `triangles` is a NumPy array of shape `(n, 3, 3)` and data type `np.float32`,
         which represents a sequence of `n` triangles (`triangles[i, j, k]` represents 
         is the `k`th coordinate of the `j`th point of the `i`th triangle)

      - `normals` is a NumPy array of shape `(n, 3)` and data type `np.float32`;
         `normals[i]` represents the outer unit normal to the `i`th facet.
         If `normals` is not specified, it should be computed from `triangles` using the 
         [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

      - `name` is the (optional) solid name embedded in the STL ASCII file.

    #### Returns

      - The STL ASCII description of the solid as a string.

    #### Example

    Given the two triangles that make up a flat square:

    ```python

    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    ```

    then printing `make_STL(square_triangles, name="square")` yields
    ```
    solid square
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 0.0 0.0 0.0
          vertex 1.0 0.0 0.0
          vertex 0.0 1.0 0.0
        endloop
      endfacet
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 1.0 1.0 0.0
          vertex 0.0 1.0 0.0
          vertex 1.0 0.0 0.0
        endloop
      endfacet
    endsolid square
    ```

    """)
    return


@app.cell
def _(np):
    import copy
    def tokenize(file):
        with open(file, mode="rt", encoding="us-ascii") as file:
            str_file = file.read()
        liste_mots=str_file.split()
        liste_mots_copy= copy.deepcopy(liste_mots)
        for i, mot in enumerate(liste_mots): 
            if mot.replace('.', '', 1).replace('-', '', 1).isdigit(): #isdigit ne marche pas directement avec des flottants!!
                liste_mots_copy[i]=np.float32(mot)

        return liste_mots_copy
    return copy, tokenize


@app.cell
def _(tokenize):
    print(tokenize("data/teapot.stl"))
    return


@app.cell
def _(mo):
    mo.md(
        """
        ### STL to NumPy

        Implement a `tokenize` function


        ```python
        def tokenize(stl):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `stl`: a Python string that represents a STL ASCII model.

        #### Returns

          - `tokens`: a list of STL keywords (`solid`, `facet`, etc.) and `np.float32` numbers.

        #### Example

        For the ASCII representation the square `data/square.stl`, printing the tokens with

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        print(tokens)
        ```

        yields

        ```python
        ['solid', 'square', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(0.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'endloop', 'endfacet', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(1.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'endloop', 'endfacet', 'endsolid', 'square']
        ```
        """
    )
    return


@app.cell
def _(np, tokenize):
    def parse (stl_file):
        tokens=tokenize(stl_file)
        triangles = []
        normals = []
        if tokens[2]== "facet":
                name= tokens[1]
        else:
            name = ""
        for i in range (len(tokens)): 
            if tokens[i] == "normal":
                normals.append([tokens[i+1],tokens[i+2],tokens[i+3]])
            if tokens[i]=="loop":
                triangles.append ([[tokens[i+2],tokens[i+3],tokens[i+4]],[tokens[i+6],tokens[i+7],tokens[i+8]],[tokens[i+10],tokens[i+11],tokens[i+12]]])
        return (np.array(triangles, dtype=np.float32),np.array(normals, dtype=np.float32),name)
    return (parse,)


@app.cell
def _(parse):
    triangles, normals, name = parse("data/teapot.stl")
    print(repr(triangles))
    print(repr(normals))
    print(repr(name))
    return name, normals, triangles


@app.cell
def _(mo):
    mo.md(
        """
        Implement a `parse` function


        ```python
        def parse(tokens):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `tokens`: a list of tokens

        #### Returns

        A `triangles, normals, name` triple where

          - `triangles`: a `(n, 3, 3)` NumPy array with data type `np.float32`,

          - `normals`: a `(n, 3)` NumPy array with data type `np.float32`,

          - `name`: a Python string.

        #### Example

        For the ASCII representation `square_stl` of the square,
        tokenizing then parsing

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        triangles, normals, name = parse(tokens)
        print(repr(triangles))
        print(repr(normals))
        print(repr(name))
        ```

        yields

        ```python
        array([[[0., 0., 0.],
                [1., 0., 0.],
                [0., 1., 0.]],

               [[1., 1., 0.],
                [0., 1., 0.],
                [1., 0., 0.]]], dtype=float32)
        array([[0., 0., 1.],
               [0., 0., 1.]], dtype=float32)
        'square'
        ```
        """
    )
    return


@app.cell
def _(np, parse):
    def diagnostic_(stl_file):
        triangles, normals, _ = parse(stl_file)

        # Positive Octant Rule 
        count_neg = 0  
        for triangle in triangles:
            for elem in triangle:
                count_neg += sum(coord < 0 for coord in elem)

        if count_neg == 0:
            octant_result = "Verified"
        else:
            percentage_violation = (count_neg / (len(triangles) * 9)) * 100
            octant_result = f"Not verified: {percentage_violation:.2f}% of coordinates are negative"


        #Orientation rule
        count_orientation=0 # compte nombre de normales qui ne verifient pas la règle d'orientation
        for i,normal in enumerate (normals):
            if not np.allclose (np.linalg.norm(normal), 1):
            # On laisse une marge d'erreur due au calcul et aux arrondis en python
                count_orientation+=1
            else:
                triangle_associe = triangles[i]
                AB=triangles[i][1]- triangles[i][0]
                BC=triangles[i][2]- triangles[i][1]
                pdt_vect =np.cross(AB,BC)

                if not np.allclose(normal/np.linalg.norm(normal),pdt_vect/np.linalg.norm(pdt_vect)):
    #On normalise les deux vecteurs pour ne comparer que leur orientation!  
                    count_orientation +=1

        orientation_result=""
        if count_orientation==0:
            orientation_result = "Orientation rule verified"
        else:
            orientation_result = f"Orientation rule not verified for {(count_orientation/(len(normals)))*100: 2f} % of the normals"

    # Shared edge rule 
        lonely_edges = [] 

        for i in range(len(triangles)):
            A = tuple(triangles[i][0])  
            B = tuple(triangles[i][1])  
            C = tuple(triangles[i][2])  

            edge_AB = tuple(sorted([A, B]))  # Trier pour éviter l'ordre
            edge_BC = tuple(sorted([B, C]))  
            edge_CA = tuple(sorted([C, A]))  

            if edge_AB in lonely_edges:
                lonely_edges.remove(edge_AB)  # On supprime l'élément trouvé
            else:
                lonely_edges.append(edge_AB)

            if edge_BC in lonely_edges:
                lonely_edges.remove(edge_BC)  
            else:
                lonely_edges.append(edge_BC)

            if edge_CA in lonely_edges:
                lonely_edges.remove(edge_CA)  
            else:
                lonely_edges.append(edge_CA)
        edges_result =""
        if len(lonely_edges) == 0:
            edges_result= "Shared edge rule verified"
        else: 
            edges_result = f"Shared edge rule not verified for {(len(lonely_edges)/(3*len(triangles)))*100: .2f} % of the edges"

        # Ascending Rule
        count_ascending_violations = 0
        barycenters = [np.mean(triangle, axis=0) for triangle in triangles]
        z_coords = [barycenter[2] for barycenter in barycenters]

        for i in range(1, len(z_coords)):
            if z_coords[i] < z_coords[i - 1]:
                count_ascending_violations += 1

        if count_ascending_violations == 0:
            escending_result = "Verified"
        else:
            percentage_violation = (count_ascending_violations / len(z_coords)) * 100
            ascending_result = f"Not verified: {percentage_violation:.2f}% of barycenters violate the z-coordinate order"

        return octant_result,orientation_result, edges_result, ascending_result
    return (diagnostic_,)


@app.cell
def _(diagnostic_):
    diagnostic_("data/teapot.stl")
    return


@app.cell
def _(mo):
    mo.md(
        rf"""
    ## Rules & Diagnostics



        Make diagnostic functions that check whether a STL model satisfies the following rules

          - **Positive octant rule.** All vertex coordinates are non-negative.

          - **Orientation rule.** All normals are (approximately) unit vectors and follow the [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

          - **Shared edge rule.** Each triangle edge appears exactly twice.

          - **Ascending rule.** the z-coordinates of (the barycenter of) each triangle are a non-decreasing sequence.

    When the rule is broken, make sure to display some sensible quantitative measure of the violation (in %).

    For the record, the `data/teapot.STL` file:

      - 🔴 does not obey the positive octant rule,
      - 🟠 almost obeys the orientation rule, 
      - 🟢 obeys the shared edge rule,
      - 🔴 does not obey the ascending rule.

    Check that your `data/cube.stl` file does follow all these rules, or modify it accordingly!

    """
    )
    return


@app.cell
def _(make_STL, np, tokenize):
    def obj_to_stl(obj_file):
        liste_obj = tokenize(obj_file)
        triangles =[]
        normals=None
        name=""
        count=0
        while liste_obj[count]!='f':
            count+=1
        coordinates,ind_facets=liste_obj[:count],liste_obj[count+1:]
        coordinates = [elem for elem in coordinates if elem != 'v']
        vertices =[coordinates[i:i + 3] for i in range(0,len(coordinates),(3))]
        ind_facets= [elem for elem in ind_facets if elem != 'f']

        facets = [ind_facets[i:i + 3] for i in range(0,len(ind_facets),(3))]
        for elem in facets:
            triangles.append([vertices[int(elem[0])-1],vertices[int(elem[1])-1],vertices[int(elem[2])-1]])
        return make_STL(np.array(triangles),normals,name)
    return (obj_to_stl,)


@app.cell
def _():
    #On crée un c&rré en OBJ

    import os

    def create_square_obj_ascii(filepath):
        # Définir les sommets du carré
        vertices = [
            "v 0.0 0.0 0.0",  # Sommet 1
            "v 1.0 0.0 0.0",  # Sommet 2
            "v 1.0 1.0 0.0",  # Sommet 3
            "v 0.0 1.0 0.0"   # Sommet 4
        ]

        # Définir la face du carré (1 face composée de 4 sommets)
        faces = [
            "f 1 2 3 f 2 3 4"  # Indices des sommets (1-indexé)
        ]

        # Vérifier si le dossier existe, sinon le créer
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Écrire les données dans le fichier en mode ASCII
        with open(filepath, 'w', encoding='ascii') as obj_file:
            obj_file.write("\n".join(vertices) + "\n")
            obj_file.write("\n".join(faces) + "\n")

    # Chemin du fichier où enregistrer le carré
    output_path = "data/carre.obj"

    # Appeler la fonction pour créer et enregistrer le fichier
    create_square_obj_ascii(output_path)

    print(f"Carré OBJ (ASCII) enregistré sous : {output_path}")
    return create_square_obj_ascii, os, output_path


@app.cell
def _(obj_to_stl):
    print(obj_to_stl("data/carre.obj"))
    return


@app.cell
def _(mo):
    mo.md(
    rf"""
    ## OBJ Format

    The OBJ format is an alternative to the STL format that looks like this:

    ```
    # OBJ file format with ext .obj
    # vertex count = 2503
    # face count = 4968
    v -3.4101800e-003 1.3031957e-001 2.1754370e-002
    v -8.1719160e-002 1.5250145e-001 2.9656090e-002
    v -3.0543480e-002 1.2477885e-001 1.0983400e-003
    v -2.4901590e-002 1.1211138e-001 3.7560240e-002
    v -1.8405680e-002 1.7843055e-001 -2.4219580e-002
    ...
    f 2187 2188 2194
    f 2308 2315 2300
    f 2407 2375 2362
    f 2443 2420 2503
    f 2420 2411 2503
    ```

    This content is an excerpt from the `data/bunny.obj` file.

    """
    )
    return


@app.cell
def _(mo, show):
    mo.show_code(show("data/bunny.obj", scale="1.5"))
    return


@app.cell
def _(mo):
    mo.md(
        """
        Study the specification of the OBJ format (search for suitable sources online),
        then develop a `OBJ_to_STL` function that is rich enough to convert the OBJ bunny file into a STL bunny file.
        """
    )
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        rf"""
    ## Binary STL

    Since the STL ASCII format can lead to very large files when there is a large number of facets, there is an alternate, binary version of the STL format which is more compact.

    Read about this variant online, then implement the function

    ```python
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        pass  # 🚧 TODO!
    ```

    that will convert a binary STL file to a ASCII STL file. Make sure that your function works with the binary `data/dragon.stl` file which is an example of STL binary format.

    💡 The `np.fromfile` function may come in handy.

        """
    )
    return


@app.cell
def _(mo, show):
    mo.show_code(show("data/dragon.stl", theta=75.0, phi=-20.0, scale=1.7))
    return


@app.cell
def _(make_STL, np):
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        with open(stl_filename_in, mode="rb") as file:
            _ = file.read(80)
            n = np.fromfile(file, dtype=np.uint32, count=1)[0]
            normals = []
            faces = []
            for i in range(n):
                normals.append(np.fromfile(file, dtype=np.float32, count=3))
                faces.append(np.fromfile(file, dtype=np.float32, count=9).reshape(3, 3))
                _ = file.read(2)
        stl_text = make_STL(faces, normals)
        with open(stl_filename_out, mode="wt", encoding="utf-8") as file:
            file.write(stl_text)
    return (STL_binary_to_text,)


@app.cell
def _(STL_binary_to_text, mo, show):
    STL_binary_to_text("data/dragon.stl", "data/dragon_texte_test.stl")
    mo.show_code(show("data/dragon_texte_test.stl", theta=75.0, phi=-20.0, scale=1.7))
    return


@app.cell
def _(mo):
    mo.md(rf"""## Constructive Solid Geometry (CSG)

    Have a look at the documentation of [{mo.icon("mdi:github")}fogleman/sdf](https://github.com/fogleman/) and study the basics. At the very least, make sure that you understand what the code below does:
    """)
    return


@app.cell
def _(X, Y, Z, box, cylinder, mo, show, sphere):
    demo_csg = sphere(1) & box(1.5)
    _c = cylinder(0.5)
    demo_csg = demo_csg - (_c.orient(X) | _c.orient(Y) | _c.orient(Z))
    demo_csg.save('output/demo-csg.stl', step=0.05)
    mo.show_code(show("output/demo-csg.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg,)


@app.cell
def _(mo):
    mo.md("""ℹ️ **Remark.** The same result can be achieved in a more procedural style, with:""")
    return


@app.cell
def _(
    box,
    cylinder,
    difference,
    intersection,
    mo,
    orient,
    show,
    sphere,
    union,
):
    demo_csg_alt = difference(
        intersection(
            sphere(1),
            box(1.5),
        ),
        union(
            orient(cylinder(0.5), [1.0, 0.0, 0.0]),
            orient(cylinder(0.5), [0.0, 1.0, 0.0]),
            orient(cylinder(0.5), [0.0, 0.0, 1.0]),
        ),
    )
    demo_csg_alt.save("output/demo-csg-alt.stl", step=0.05)
    mo.show_code(show("output/demo-csg-alt.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg_alt,)


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(
        rf"""
    ## JupyterCAD

    [JupyterCAD](https://github.com/jupytercad/JupyterCAD) is an extension of the Jupyter lab for 3D geometry modeling.

      - Use it to create a JCAD model that correspond closely to the `output/demo_csg` model;
    save it as `data/demo_jcad.jcad`.

      - Study the format used to represent JupyterCAD files (💡 you can explore the contents of the previous file, but you may need to create some simpler models to begin with).

      - When you are ready, create a `jcad_to_stl` function that understand enough of the JupyterCAD format to convert `"data/demo_jcad.jcad"` into some corresponding STL file.
    (💡 do not tesselate the JupyterCAD model by yourself, instead use the `sdf` library!)


        """
    )
    return


@app.cell
def _(mo):
    mo.md("""## Appendix""")
    return


@app.cell
def _(mo):
    mo.md("""### Dependencies""")
    return


@app.cell
def _():
    # Python Standard Library
    import json

    # Marimo
    import marimo as mo

    # Third-Party Librairies
    import numpy as np
    import matplotlib.pyplot as plt
    import mpl3d
    from mpl3d import glm
    from mpl3d.mesh import Mesh
    from mpl3d.camera import Camera

    import meshio

    np.seterr(over="ignore")  # 🩹 deal with a meshio false warning

    import sdf
    from sdf import sphere, box, cylinder
    from sdf import X, Y, Z
    from sdf import intersection, union, orient, difference

    mo.show_code()
    return (
        Camera,
        Mesh,
        X,
        Y,
        Z,
        box,
        cylinder,
        difference,
        glm,
        intersection,
        json,
        meshio,
        mo,
        mpl3d,
        np,
        orient,
        plt,
        sdf,
        sphere,
        union,
    )


@app.cell
def _(mo):
    mo.md(r"""### STL Viewer""")
    return


@app.cell
def _(Camera, Mesh, glm, meshio, mo, plt):
    def show(
        filename,
        theta=0.0,
        phi=0.0,
        scale=1.0,
        colormap="viridis",
        edgecolors=(0, 0, 0, 0.25),
        figsize=(6, 6),
    ):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
        ax.axis("off")
        camera = Camera("ortho", theta=theta, phi=phi, scale=scale)
        mesh = meshio.read(filename)
        vertices = glm.fit_unit_cube(mesh.points)
        faces = mesh.cells[0].data
        vertices = glm.fit_unit_cube(vertices)
        mesh = Mesh(
            ax,
            camera.transform,
            vertices,
            faces,
            cmap=plt.get_cmap(colormap),
            edgecolors=edgecolors,
        )
        return mo.center(fig)

    mo.show_code()
    return (show,)


@app.cell
def _(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


if __name__ == "__main__":
    app.run()
