-- SCHEMA
-- ======

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name TEXT NOT NULL UNIQUE, description TEXT NOT NULL);

CREATE TABLE algorithms (id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, category_id INTEGER NOT NULL, name TEXT UNIQUE NOT NULL, description TEXT, asymptotics INTEGER NOT NULL, video TEXT);

-- DATA
-- ====

-- Data for table: categories
INSERT INTO categories (id, name, description) VALUES (1, 'Сортировки', 'Алгоритмы для упорядочивания элементов в определенной последовательности (по возрастанию, убыванию или другому критерию).

Когда применяются:

Подготовка данных для бинарного поиска

Ускорение других алгоритмов, работающих с отсортированными данными

Анализ и визуализация данных

Поиск медиан, квартилей

Удаление дубликатов

Базы данных и индексация');
INSERT INTO categories (id, name, description) VALUES (2, 'Алгоритмы поиска', 'Алгоритмы для нахождения элементов в структурах данных, удовлетворяющих определенным условиям.

Когда применяются:

Поиск информации в базах данных

Реализация функций автодополнения

Поиск маршрутов в навигационных системах

Анализ текстов и поиск по ключевым словам

Проверка наличия элементов в коллекциях');
INSERT INTO categories (id, name, description) VALUES (3, 'Теория чисел', 'Алгоритмы для работы с целыми числами, их свойствами и взаимосвязями.

Когда применяются:

Криптография и шифрование данных

Генерация простых чисел для RSA-шифрования

Проверка чисел на простоту

Вычисление наибольшего общего делителя

Компьютерная алгебра');
INSERT INTO categories (id, name, description) VALUES (4, 'Динамическое программирование', 'Метод решения сложных задач путем разбиения на более простые подзадачи с запоминанием результатов.

Когда применяются:

Оптимизационные задачи

Поиск кратчайших путей

Задачи распределения ресурсов

Биоинформатика (выравнивание последовательностей)

Экономическое планирование');
INSERT INTO categories (id, name, description) VALUES (5, 'Графы', 'Алгоритмы для работы с графами - структурами, состоящими из вершин (узлов) и ребер (связей).

Когда применяются:

Социальные сети (поиск друзей, рекомендации)

Навигационные системы (поиск маршрутов)

Сетевые технологии (маршрутизация)

Рекомендательные системы

Анализ зависимостей в проектах');

-- Data for table: algorithms
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (1, 1, 'Сортировка пузырьком', 'def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr', 'O(n²)', 'Bubblesort.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (2, 1, 'Сортировка подсчетом', 'def counting_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    min_val = min(arr)
    count_range = max_val - min_val + 1
    count = [0] * count_range
    for num in arr:
        count[num - min_val] += 1
    result = []
    for i in range(count_range):
        result.extend([i + min_val] * count[i])
    return result', 'O(n + r — l)', 'Bucketsort.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (3, 1, 'Быстрая сортировка', 'def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)', 'O(n log n)', 'Quicksort.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (4, 1, 'Сортировка слиянием', 'def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result', 'O(n log n)', 'Mergesort.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (5, 2, 'Бинарный поиск', 'def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1', 'O(log n)', 'Binsearch.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (6, 2, 'Поиск в ширину(BFS)', 'from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=" ")
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)', 'O(V + E)', 'BFS.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (7, 2, 'Поиск в глубину(DFS)', 'def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=" ")
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)', 'O(V + E)', 'DFS.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (8, 3, 'Решето Эратосфена', 'def sieve_of_eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, n + 1) if is_prime[i]]', 'O(n log log n)', 'Eratosfen.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (9, 3, 'Алгоритм Евклида', 'def euclidean_algorithm(a, b):
    while b:
        a, b = b, a % b
    return a', 'O(n log log n)', 'GCD.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (10, 4, 'Последовательность Фибоначчи', 'def fibonacci(n):
    if n <= 1:
        return n
    fib = [0, 1]
    for i in range(2, n + 1):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib[n]', 'O(n)', 'Fibonacci.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (11, 4, 'Задача о рюкзаке', 'def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]', 'O(nW)', 'Knapsack.mp4');
INSERT INTO algorithms (id, category_id, name, description, asymptotics, video) VALUES (12, 5, 'Алгоритм Дейкстры', 'import heapq

def dijkstra(graph, start):
    distances = {node: float(''inf'') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    
    return distances', 'O(E + V log V)', 'Dijkstra.mp4');

