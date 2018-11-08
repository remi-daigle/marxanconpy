import numpy
import os
import pandas
import marxanconpy

def calc_postHoc(filename,format,IDs,selectionIDs):
    """ Calculate PostHoc Metrics

    Calculate PostHoc Metrics for a given Marxan solution

    :param filename: filename of the connectivity data
    :param format: The format of the connectivity file (i.e. "Matrix", "Edge List", "Edge List with Type", "Edge List with Time"). See http://marxanconnect.ca/glossary.html#data_formats for a detailed description of formats
    :param IDs: Planning unit IDs
    :param selectionIDs: Planning unit IDs for those included in the Marxan solution
    :return:
    """
    if os.path.isfile(filename):
        if format == "Matrix":
            connectivity = pandas.read_csv(filename, index_col=0)
        elif format == "Edge List with Time":
            connectivity = pandas.read_csv(filename,
                            dtype = {'id1': str, 'id1': str})[['id1', 'id2', 'value']].groupby(['id1', 'id2']).mean()
        else:
            connectivity = pandas.read_csv(filename,
                            dtype = {'id1': str, 'id1': str})

        if connectivity.shape[1]==3 or format == "Matrix":
            all_type=['default_type_replace']
        else:
            all_type=numpy.unique(connectivity.drop(['id1', 'id2', 'value'], axis=1))

        postHoc = pandas.DataFrame()
        for type in all_type:
            if type=="default_type_replace":
                graph = marxanconpy.manipulation.connectivity2graph(connectivity,format,IDs)
            else:
                graph = marxanconpy.manipulation.connectivity2graph(connectivity[(connectivity.drop(['id1', 'id2', 'value'], axis=1)==type).values], format, IDs)

            sub = graph.subgraph([str(i) for i in selectionIDs])

            postHoc = postHoc.append(pandas.DataFrame({"Metric": ("Planning Units",
                                                                  "Connections",
                                                                  "Graph Density",
                                                                  "Eigenvalue"),
                                                       "Type": (type, type, type, type),
                                                       "Planning Area": (graph.vcount(),
                                                                         graph.ecount(),
                                                                         graph.density(),
                                                                         graph.evcent(weights=graph.es["weight"],
                                                                                      return_eigenvalue=True)[1]),
                                                       "Solution": (
                                                           sub.vcount(),
                                                           sub.ecount(),
                                                           sub.density(),
                                                           sub.evcent(weights=sub.es["weight"],
                                                                      return_eigenvalue=True)[1])}), ignore_index=True)

        postHoc["Percent"] = postHoc["Solution"]/postHoc["Planning Area"]*100
        postHoc = postHoc[['Metric','Type','Planning Area','Solution','Percent']]
        if "default_type_replace" in postHoc["Type"].unique():
            del(postHoc["Type"])
        return postHoc