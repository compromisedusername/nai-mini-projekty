import os
import random


def read_data(file):
    with open(file, 'r') as p:
        tekst = p.read()
    p.close()
    tekst = tekst.replace(",", ".")
    return tekst


def make_vector(data):
    column = data.split()
    vector = column[:-1]
    return [vector,column[-1]]


def make_vectors(data):
    vector = []
    for line in data.splitlines():
        vector.append(make_vector(line))
    return vector


def kmeans_algorithm(vectors):

    k_groups = int(input("Input number of groups: "))
    if(k_groups > len(vectors)):
        print("To much groups for given data set!")
        return
    centroids = make_initial_centroids(k_groups,vectors)
    print(centroids, "CENTROIDS")

    square_distances = 0
    vector_set = set(([tuple(x[0]) for x in vectors]))
    clusters = {}
    while True:
        for vec in vector_set: # dla kazdego wektora
            changes = 0
            distances = [] # dystanse dla kazdego wektora od danego centroidu
            for cluster_number in range(0, len(centroids)):
                distance = euclidean_square_distance(vec, centroids[cluster_number])
                distances.append([vec, distance, cluster_number])
                if cluster_number in clusters:
                    new_centroid = calculate_new_centroid(clusters[cluster_number])
                    if centroids[cluster_number] != new_centroid: # zmiany odleglosci
                        changes += 1
                        print("ZMIANY: ",changes)
                    centroids[cluster_number] = new_centroid # aktualizujemy centroid



            min_distance = min(distances, key=lambda x: x[1])
            old_square_distance = square_distances
            square_distances += min_distance[1]

            print(square_distances, "SQUARE DISTANCE")

            cluster_id = min_distance[2]

            if cluster_id not in clusters:
                clusters[cluster_id] = [min_distance]
            else:
                clusters[cluster_id].append(min_distance)

            if changes >= k_groups:
                return clusters


def calculate_new_centroid(c):
    print(c, "CALCULATE NEW CENTROID")
    cluster = []
    for i,j,k in c:
        cluster.append(i)
    centroid = [0 for _ in range(0,len(cluster[0]))]
    for j in range(0, len(cluster[0])):
        for i in range(0, len(cluster)):
            centroid[j] += float(cluster[i][j])
        centroid[j] /= len(cluster)
    return centroid


def euclidean_square_distance(vector, point):
    distance = 0
    for x in range(0,len(vector)):
        distance += ((float(vector[x])-float(point[x]))**2)
    return distance

def make_initial_centroids(k,vectors):
    centroids = []
    centroids.append(vectors[0][0])
    vectors_and_distance = {}
    vectors_already_taken = []
    vector_set = set(([tuple(x[0]) for x in vectors]))

    for x in range(0, k-1):
        for vec in vector_set:
            distance = euclidean_square_distance(vec,centroids[x])
            key = tuple(vec)
            if not key in vectors_and_distance and vec not in vectors_already_taken:
                vectors_and_distance[key] = [distance]
            elif vec not in vectors_already_taken:
                vectors_and_distance[key].append(distance)
        max_k = (max(vectors_and_distance.items(), key=lambda item: sum(item[1])))
        print(sorted(vectors_and_distance.items(),key=lambda item: sum(item[1])))
        print("CHOSEN MAX",max_k)

        centroids.append( max_k[0]) # dodajemy do centroidow, wektor ktorego kwadraty sum odleglosci od centroidow sa najwieksze
        vectors_already_taken.append((max_k[0])) # dodajemy wektor ktory dodalismy wyzej, by uniknac powtarzania sie centroidow

    return centroids

print("INPUT --> input your own vector")
print("EXIT --> use file")

cwd = os.getcwd()
print('\nFILES in ', cwd, ' :\n--------------------')

for filename in os.listdir(cwd):
    if (filename.endswith(".txt")):
        print(filename)
print("--------------------\n")
file = input("Input  file name [Or type enter to use standard set]:")
if (file == ""):
    file = "../iris_training.txt"

if (not os.path.isfile(file)):
    print(f"File \'{file}\' doesnt exists! Used file: \'iris_training.txt\'")
    file = "../iris_training.txt"
data = read_data(file)
vectors = make_vectors(data)

kmeans_algorithm(vectors)

