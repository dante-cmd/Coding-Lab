import numpy as np
from sklearn.cluster import KMeans
import cv2, requests, time
import re
from urllib.parse import urlsplit
from matplotlib.image import imread
from scipy.spatial.distance import euclidean, pdist
from itertools import combinations

# METHOD #1: OpenCV, NumPy, and urllib
def parser_url(url) -> np.ndarray:
    if seeker:= re.search(r'(http\:\/\/127\.0\.0\.1\:8000.+)', url):
        path = seeker.group(1)
        split_path = urlsplit(path)    
        # Remove the prefix to read
        image_map = imread(split_path.path.removeprefix('/'))
        return image_map
    
    else :
        # download the image, convert it to a NumPy array, and then read
        resp = requests.get(url)
        image = np.asarray(bytearray(resp.content), dtype="uint8")
        
        # it into OpenCV format
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image

def classification_img(image_map:np.ndarray) -> np.ndarray:
    
    # init kmeans
    kmeans = KMeans(n_clusters=8, random_state=0)
    
    # reshape the image to be a list of pixels
    map_array = image_map.reshape(image_map.shape[0]*image_map.shape[1], image_map.shape[2])
    
    # Take a sample of 600 the pixels
    np.random.seed(0)
    idx = np.random.randint(0, len(map_array), size = int(len(map_array)*0.05))
    sample_map_array = map_array[idx]

    # fit the model k-means
    kmeans.fit(sample_map_array)

    clusters = kmeans.cluster_centers_
    # print(get_similarity(clusters))
    return get_similarity(clusters)


def get_rgb(url):
    image = parser_url(url)
    return classification_img(image)

def similarity_func(u, v):
    return 1/(1+euclidean(u,v))

def get_comb(matrix):
    return combinations(range(matrix.shape[0]), 2)

def get_index(comb, idx):
    return list(comb)[idx]

def get_similarity(matrix):
    idx = np.argmin(pdist(matrix, similarity_func))
    return matrix[get_index(get_comb(matrix), idx),:]

if __name__ == "__main__":
    # URL = "https://i0.wp.com/imagenesparapeques.com/wp-content/uploads/2021/05/Mario-Bros-png-transparente.png"
    URL = r'http://127.0.0.1:8000/static/img/5143393548834f6687f9ae7b012a569d_9366.png'
    time_start = time.time()
    map_array = parser_url(URL)
    time_middle = time.time()
    print(time_middle - time_start)
    classification_img(map_array)
    print(time.time()- time_middle)
    
