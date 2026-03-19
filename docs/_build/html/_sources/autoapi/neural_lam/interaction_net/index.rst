neural_lam.interaction_net
==========================

.. py:module:: neural_lam.interaction_net




Module Contents
---------------

.. py:class:: InteractionNet(edge_index, input_dim, update_edges=True, hidden_layers=1, hidden_dim=None, edge_chunk_sizes=None, aggr_chunk_sizes=None, aggr='sum')

   Bases: :py:obj:`torch_geometric.nn.MessagePassing`


   Implementation of a generic Interaction Network,
   from Battaglia et al. (2016)


   .. py:method:: aggregate(inputs, index, ptr, dim_size)

      Overridden aggregation function to:
      * return both aggregated and original messages,
      * only aggregate to number of receiver nodes.



   .. py:method:: forward(send_rep, rec_rep, edge_rep)

      Apply interaction network to update receiver node representations.

      :param send_rep: Shape ``(N_send, d_h)``, vector representations of sender nodes.
      :type send_rep: torch.Tensor
      :param rec_rep: Shape ``(N_rec, d_h)``, vector representations of receiver nodes.
      :type rec_rep: torch.Tensor
      :param edge_rep: Shape ``(M, d_h)``, vector representations of edges.
      :type edge_rep: torch.Tensor

      :returns: * **rec_rep** (*torch.Tensor*) -- Shape ``(N_rec, d_h)``, updated receiver node representations.
                * **edge_rep** (*torch.Tensor, optional*) -- Shape ``(M, d_h)``, updated edge representations.
                  Only returned when ``update_edges=True``.



   .. py:method:: message(x_j, x_i, edge_attr)

      Compute messages from node j to node i.



   .. py:attribute:: num_rec


   .. py:attribute:: update_edges
      :value: True



.. py:class:: SplitMLPs(mlps, chunk_sizes)

   Bases: :py:obj:`torch.nn.Module`


   Module that feeds chunks of input through different MLPs.
   Split up input along dim -2 using given chunk sizes and feeds
   each chunk through separate MLPs.


   .. py:method:: forward(x)

      Chunk up input and feed through MLPs.

      :param x: Shape ``(..., N, d)`` where ``N = sum(chunk_sizes)``.
      :type x: torch.Tensor

      :returns: Shape ``(..., N, d)``, concatenated results from the MLPs.
      :rtype: torch.Tensor



   .. py:attribute:: chunk_sizes


   .. py:attribute:: mlps
