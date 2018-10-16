import numpy
import geopandas as gpd
import pandas
import igraph
import marxanconpy

def graph2vertexdegree(graph,mode='ALL'):
    """ Connectivity graph
    
    :param graph: igraph formatted graph
    :param mode: String describing mode (i.e. 'ALL', 'IN', 'OUT")
    :return: 
    """
    vertexdegree = graph.degree(mode=mode)
    return vertexdegree

def graph2betweencent(graph):
    """ Connectivity graph to betweeness centrality
    
    :param graph: igraph formatted graph 
    :return: 
    """
    betweencent = graph.betweenness()
    return betweencent

def graph2eigvectcent(graph):
    """ Connectivity graph to eigenvector centrality
    
    :param graph: igraph formatted graph 
    :return: 
    """
    eigvectcent = graph.evcent(weights=graph.es["weight"])
    return eigvectcent

def graph2google(graph):
    """ Connectivity graph to Google Page Rank
    
    :param graph: igraph formatted graph 
    :return: 
    """
    eigvectcent = graph.pagerank(weights=graph.es["weight"])
    return eigvectcent

def graph2outflow(graph):
    """ Connectivity graph to outflow
    
    :param graph: igraph formatted graph 
    :return: 
    """
    return graph.strength(mode="OUT", loops=False, weights=graph.es["weight"])

def graph2inflow(graph):
    """ Connectivity graph to inflow
    
    :param graph: igraph formatted graph 
    :return: 
    """
    return graph.strength(mode="IN", loops=False, weights=graph.es["weight"])

def graph2diagonal(graph):
    """ Connectivity graph to diagonal
    
    :param graph: igraph formatted graph 
    :return: 
    """
    from_list = numpy.array([x[0] for x in graph.get_edgelist()])
    to_list = numpy.array([x[1] for x in graph.get_edgelist()])
    loops = from_list == to_list
    IDs = numpy.unique([numpy.unique(from_list), numpy.unique(to_list)])
    diag = numpy.repeat(0., len(IDs))
    for i in from_list[loops]:
        diag[IDs == i] = numpy.array(graph.es["weight"])[(from_list == i) & (to_list == i)]
    diag[IDs == i] = 1
    return diag

def get_intersect_id(area_filepath, pu_filepath,pu_id='ID'):
    """ 
    
    :param area_filepath: 
    :param pu_filepath: 
    :param pu_id: 
    :return: 
    """
    area = gpd.GeoDataFrame.from_file(area_filepath)
    pu = gpd.GeoDataFrame.from_file(pu_filepath)

    if pu.crs!=area.crs:
        area_proj = marxanconpy.spatial.get_appropriate_projection(pu, 'area')
        area = area.to_crs(area_proj)
        pu = pu.to_crs(area_proj)

    area_id = ()
    for index, arearow in area.iterrows():
        for index, purow in pu.iterrows():
            if purow.geometry.intersects(arearow.geometry):
                area_id = area_id + (purow[pu_id],)
                break
    return area_id

def graph2recipients(graph, area_filepath, pu_filepath, pu_id='ID',inverse=False):
    """ Connectivity graph to recipients
    
    :param graph: igraph formatted graph 
    :param area_filepath: 
    :param pu_filepath: 
    :param pu_id: 
    :param inverse: 
    :return: 
    """
    area_id = get_intersect_id(area_filepath, pu_filepath, pu_id)
    recipients = numpy.array(graph.strength(area_id,mode="IN", loops=False, weights=graph.es["weight"]))
    if inverse:
        return max(recipients)-recipients
    else:
        return recipients

def graph2donors(graph, area_filepath, pu_filepath, pu_id='ID',inverse=False):
    """ Connectivity graph to donors
    
    :param graph: igraph formatted graph 
    :param area_filepath: 
    :param pu_filepath: 
    :param pu_id: 
    :param inverse: 
    :return: 
    """
    area_id = get_intersect_id(area_filepath, pu_filepath, pu_id)
    donors = numpy.array(graph.strength(area_id, mode="OUT", loops=False, weights=graph.es["weight"]))
    if inverse:
        return max(donors)-donors
    else:
        return donors

def graph2connboundary(graph):
    """ Connectivity graph to spatial dependency
    
    :param graph: igraph formatted graph 
    :return: 
    """
    id1 = numpy.array([x[0] for x in graph.get_edgelist()])
    id2 = numpy.array([x[1] for x in graph.get_edgelist()])
    boundary = graph.es["weight"]
    boundary_dat = pandas.DataFrame(data={"id1": id1,
                                          "id2": id2,
                                          "boundary": boundary}).to_json(orient='split')
    return boundary_dat

def graphtime2temp_conn_cov(graph_time, fa_filepath, pu_filepath):
    """ Connectivity graph with time to temporal connectivity covariance
    
    :param graph_time: 
    :param fa_filepath: 
    :param pu_filepath: 
    :return: 
    """
    
    fa = gpd.GeoDataFrame.from_file(fa_filepath)
    pu = gpd.GeoDataFrame.from_file(pu_filepath)


    fa_id = ()
    for index, farow in fa.iterrows():
        for index, purow in pu.iterrows():
            if purow.geometry.intersects(farow.geometry):
                fa_id = fa_id + (purow.ID,)
                break
    if any([fid in graph_time.id2.unique().tolist() for fid in fa_id]):
        cov_list = []
        for fa1 in fa_id:
            for fa2 in fa_id:
                if not fa1 == fa2:
                    con_fa = graph_time.value[(graph_time.id1 == fa1) & (graph_time.id2 == fa2)]
                    for id1 in fa_id:
                        for id2 in graph_time.id2.unique():
                            if not id1 == id2:
                                cov = \
                                numpy.cov(con_fa, graph_time.value[(graph_time.id1 == id1) &
                                                                    (graph_time.id2 == id2)])[0, 1]
                                cov_list.append({'id2': id2, 'cov': cov})
        cov_list = pandas.DataFrame.from_dict(cov_list)

        score = -cov_list.groupby('id2').sum()
        return score['cov'].tolist()
    else:
        return [0] * len(graph_time.id2.unique())