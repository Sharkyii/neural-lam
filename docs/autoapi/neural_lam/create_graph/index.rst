neural_lam.create_graph
=======================

.. py:module:: neural_lam.create_graph




Module Contents
---------------

.. py:function:: cli(input_args=None)

.. py:function:: create_graph(graph_dir_path: str, xy: numpy.ndarray, n_max_levels: Optional[int] = None, hierarchical: Optional[bool] = False, create_plot: Optional[bool] = False)

   Create graph components from `xy` grid coordinates and store in
   `graph_dir_path`.

   Creates the following files for all graphs:
   - g2m_edge_index.pt  [2, N_g2m_edges]
   - g2m_features.pt    [N_g2m_edges, d_features]
   - m2g_edge_index.pt  [2, N_m2m_edges]
   - m2g_features.pt    [N_m2m_edges, d_features]
   - m2m_edge_index.pt  list of [2, N_m2m_edges_level], length==n_levels
   - m2m_features.pt    list of [N_m2m_edges_level, d_features],
                        length==n_levels
   - mesh_features.pt   list of [N_mesh_nodes_level, d_mesh_static],
                        length==n_levels

   where
     d_features:
           number of features per edge (currently d_features==3, for
           edge-length, x and y)
     N_g2m_edges:
           number of edges in the graph from grid-to-mesh
     N_m2g_edges:
           number of edges in the graph from mesh-to-grid
     N_m2m_edges_level:
           number of edges in the graph from mesh-to-mesh at a given level
           (list index corresponds to the level)
     d_mesh_static:
           number of static features per mesh node (currently
           d_mesh_static==2, for x and y)
     N_mesh_nodes_level:
           number of nodes in the mesh at a given level

   And in addition for hierarchical graphs:
   - mesh_up_edge_index.pt
       list of [2, N_mesh_updown_edges_level], length==n_levels-1
   - mesh_up_features.pt
       list of [N_mesh_updown_edges_level, d_features], length==n_levels-1
   - mesh_down_edge_index.pt
       list of [2, N_mesh_updown_edges_level], length==n_levels-1
   - mesh_down_features.pt
       list of [N_mesh_updown_edges_level, d_features], length==n_levels-1

   where N_mesh_updown_edges_level is the number of edges in the graph from
   mesh-to-mesh between two consecutive levels (list index corresponds index
   of lower level)


   :param graph_dir_path: Path to store the graph components.
   :type graph_dir_path: str
   :param xy: Grid coordinates, expected to be of shape (Nx, Ny, 2).
   :type xy: np.ndarray
   :param n_max_levels: Limit multi-scale mesh to given number of levels, from bottom up
                        (default: None (no limit)).
   :type n_max_levels: int
   :param hierarchical: Generate hierarchical mesh graph (default: False).
   :type hierarchical: bool
   :param create_plot: If graphs should be plotted during generation (default: False).
   :type create_plot: bool

   :rtype: None


.. py:function:: create_graph_from_datastore(datastore: neural_lam.datastore.base.BaseRegularGridDatastore, output_root_path: str, n_max_levels: Optional[int] = None, hierarchical: bool = False, create_plot: bool = False)

.. py:function:: from_networkx_with_start_index(nx_graph, start_index)

.. py:function:: mk_2d_graph(xy, nx, ny)

.. py:function:: plot_graph(graph, title=None)

.. py:function:: prepend_node_index(graph, new_index)

.. py:function:: save_edges(graph, name, base_path)

.. py:function:: save_edges_list(graphs, name, base_path)

.. py:function:: sort_nodes_internally(nx_graph)

