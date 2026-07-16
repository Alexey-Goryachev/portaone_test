def look_ahead_score_fast(graph, current_node, visited_flags, depth, memo=None):
    """
    Ultra-fast path richness estimation with memoization (caching) support.
    Uses beam search to avoid bottlenecks on large graphs.
    """
    if depth == 0 or current_node not in graph:
        return 0
    
    # Create a local cache for the current search branch to avoid re-computations
    if memo is None:
        memo = {}
    
    # The cache key is the node and depth (we don't include the entire visited_flags for speed reasons,
    # but locally within a single simulation it provides a significant boost)
    memo_key = (current_node, depth)
    if memo_key in memo:
        return memo[memo_key]
    
    max_score = 0
    edges = graph[current_node]
    
    seen_destinations = set()
    evaluated_count = 0
    
    for next_node, edge_idx in edges:
        if not visited_flags[edge_idx]:
            if next_node in seen_destinations:
                continue
            seen_destinations.add(next_node)
            
            # Temporarily mark the edge as visited
            visited_flags[edge_idx] = True
            
            # Recursive step with cache passing
            score = 1 + look_ahead_score_fast(graph, next_node, visited_flags, depth - 1, memo)
            if score > max_score:
                max_score = score
                
            # Rolling back the state
            visited_flags[edge_idx] = False
            
            # We limit the maximum search width at each step
            evaluated_count += 1
            if evaluated_count >= 4:
                break
                
    memo[memo_key] = max_score
    return max_score


def run_fast_eulerian(fragments, depth=3):
    """
    A fast heuristic algorithm based on Euler graph traversal.
    With protection against combinatorial explosions on big data.
    """
    num_fragments = len(fragments)
    if num_fragments == 0:
        return "", 0
    
    # We construct a junction graph and simultaneously calculate the incoming/outgoing degrees of vertices
    graph = {}
    in_degrees = {}   # Number of incoming edges for each node
    out_degrees = {}  # Number of outgoing edges for each node
    
    for idx, frag in enumerate(fragments):
        u, v = frag[:2], frag[-2:]
        
        if u not in graph:
            graph[u] = []
        graph[u].append((v, idx))
        
        # Counting degrees for smart starting point selection
        out_degrees[u] = out_degrees.get(u, 0) + 1
        in_degrees[v] = in_degrees.get(v, 0) + 1

    best_result_str = ""
    max_chain_len = 0

    # SMART SELECTION OF STARTING POINTS:
    # In an ideal path, we should start with nodes whose out_degree > in_degree (sources).
    # Sort the nodes so that the most promising starts appear first.
    def get_start_priority(node):
        out_deg = out_degrees.get(node, 0)
        in_deg = in_degrees.get(node, 0)
        # Priority is given to those with many outputs and few (or no) inputs.
        return out_deg - in_deg

    start_nodes = sorted(graph.keys(), key=get_start_priority, reverse=True)
    
    # On large graphs (10,000+ nodes), there's no point in checking ALL vertices as a starting point.
    # We limit the pool to the first 50 most promising vertices.
    max_start_attempts = min(50, len(start_nodes))
    nodes_to_try = start_nodes[:max_start_attempts]

    for start_node in nodes_to_try:
        current_node = start_node
        visited_flags = [False] * num_fragments
        path_edges_idx = []

        while True:
            if current_node not in graph:
                break
                
            # Quickly collect available options
            available_options = [
                (next_node, edge_idx) 
                for next_node, edge_idx in graph[current_node] 
                if not visited_flags[edge_idx]
            ]

            if not available_options:
                break

            if len(available_options) == 1:
                next_node, edge_idx = available_options[0]
            else:
                # We evaluate only one (first available) edge for each unique next_node
                best_option = None
                best_score = -1
                
                unique_destinations = set()
                memo_cache = {}  # Cache for look_ahead within the current decision step
                
                for next_node, edge_idx in available_options:
                    if next_node in unique_destinations:
                        continue
                    unique_destinations.add(next_node)
                    
                    visited_flags[edge_idx] = True
                    score = look_ahead_score_fast(
                        graph, next_node, visited_flags, depth=depth, memo=memo_cache
                    )
                    visited_flags[edge_idx] = False
                    
                    if score > best_score:
                        best_score = score
                        best_option = (next_node, edge_idx)
                
                # If all options lead to dead ends, we take the first available one
                if best_option is None:
                    next_node, edge_idx = available_options[0]
                else:
                    next_node, edge_idx = best_option

            # Fix the transition
            visited_flags[edge_idx] = True
            path_edges_idx.append(edge_idx)
            current_node = next_node

        # Check if we got a longer chain
        if len(path_edges_idx) > max_chain_len:
            max_chain_len = len(path_edges_idx)
            
            res = fragments[path_edges_idx[0]]
            for e_idx in path_edges_idx[1:]:
                res += fragments[e_idx][2:]
            best_result_str = res
            
            # If we find a perfect chain that covers all the fragments, we exit
            if max_chain_len == num_fragments:
                break

    # If no chain is built, return an empty string
    return best_result_str, max_chain_len