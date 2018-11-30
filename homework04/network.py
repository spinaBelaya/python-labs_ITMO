from api import get_friends
import time
import igraph


def get_network(user_id: int, as_edgelist=True) -> list:
    user_friends = get_friends(user_id, '')
    links = []
    for i, friend in enumerate(user_friends):
        f_friends = []
        try:
            f_friends = get_friends(friend, '')
        except BaseException:
            pass
        time.sleep(0.34)
        for j, f_friend in enumerate(f_friends):
            for k, another_friend in enumerate(user_friends):
                if f_friend == another_friend:
                    links.append((i, k))
    return links


def plot_graph(user_id):
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id, True)

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "vertex_label_dist": 1.6,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)


if __name__ == '__main__':
    plot_graph(232483598)
