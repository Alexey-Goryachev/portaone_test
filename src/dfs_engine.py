def run_exact_dfs(fragments):
    """
    Exact search algorithm (DFS) with pruning optimization.
    Guarantees finding the global maximum.
    """
    # Building a prefix map for instant neighbor search
    prefix_map = {}
    for idx, frag in enumerate(fragments):
        prefix = frag[:2]
        if prefix not in prefix_map:
            prefix_map[prefix] = []
        prefix_map[prefix].append(idx)

    best_path = []
    visited = [False] * len(fragments)
    total_available = len(fragments)

    def dfs(current_idx, current_path):
        nonlocal best_path, total_available
        
        if len(current_path) > len(best_path):
            best_path = list(current_path)

        # The logic of cutting off unpromising branches
        if len(current_path) + total_available <= len(best_path):
            return

        current_frag = fragments[current_idx]
        suffix = current_frag[-2:]
        neighbors = prefix_map.get(suffix, [])

        for next_idx in neighbors:
            if not visited[next_idx]:
                visited[next_idx] = True
                current_path.append(next_idx)
                total_available -= 1
                
                dfs(next_idx, current_path)
                
                total_available += 1
                current_path.pop()
                visited[next_idx] = False

    # Running DFS from each fragment
    for start_idx in range(len(fragments)):
        visited[start_idx] = True
        total_available -= 1
        
        dfs(start_idx, [start_idx])
        
        total_available += 1
        visited[start_idx] = False

    if not best_path:
        return None, 0

    # Make the final result
    result_str = fragments[best_path[0]]
    for idx in best_path[1:]:
        result_str += fragments[idx][2:]

    return result_str, len(best_path)
