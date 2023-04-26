import multiprocessing


def map_worker(chunk):
    word_counts = {}
    for word in chunk.split():
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1
    return [(word, count) for word, count in word_counts.items()]

def shuffle_worker(tuples):
    word_groups = {}
    for word, count in tuples:
        if word not in word_groups:
            word_groups[word] = []
        word_groups[word].append(count)
    return [(word, counts) for word, counts in word_groups.items()]

def reduce_worker(word_counts):
    return (word_counts[0], sum(word_counts[1]))

def map_reduce(input_data, num_map_workers, num_reduce_workers):
    # Step 1: Split the input data into chunks
    chunk_size = len(input_data) // num_map_workers
    chunks = [input_data[i:i+chunk_size] for i in range(0, len(input_data), chunk_size)]
    # Step 2: Map step
    with multiprocessing.Pool(num_map_workers) as pool:
        map_results = pool.map(map_worker, chunks)
    # Step 3: Shuffle step
    tuples = [item for sublist in map_results for item in sublist]
    with multiprocessing.Pool(num_reduce_workers) as pool:
        shuffle_results = pool.map(shuffle_worker, [tuples])
    # Step 4: Reduce step
    reduced_tuples = [item for sublist in shuffle_results for item in sublist]
    with multiprocessing.Pool(num_reduce_workers) as pool:
        final_results = pool.map(reduce_worker, reduced_tuples)
    return final_results

def main():
    # Read the input text from file
    with open('input.txt', 'r') as f:
        input_data = f.read()
    # Call the MapReduce function
    result = map_reduce(input_data, num_map_workers=2, num_reduce_workers=2)
    # Print the output
    for pair in result:
        print(pair)

if _name_ == '_input.txt*_':
    main()
    