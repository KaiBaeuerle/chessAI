plays_list = []

def visualize_data(current_node):
    if len(current_node.children) > 0:
        for child in current_node.children:
            visualize_data(child)
    found = False
    for numb_plays in plays_list:
        if numb_plays[0] == float(current_node.plays):
            found = True
            numb_plays[1] = numb_plays[1] + 1
    if not found:
        plays_list.append([float(current_node.plays), 1])

def visualize_data_print(current_node):
    visualize_data(current_node)
    print(plays_list)
    print("fnish")