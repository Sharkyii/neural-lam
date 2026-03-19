neural_lam.utils
================

.. py:module:: neural_lam.utils






Module Contents
---------------

.. py:class:: BufferList(buffer_tensors, persistent=True)

   Bases: :py:obj:`torch.nn.Module`


   A list of torch buffer tensors that sit together as a Module with no
   parameters and only buffers.

   This should be replaced by a native torch BufferList once implemented.
   See: https://github.com/pytorch/pytorch/issues/37386


   .. py:attribute:: n_buffers


.. py:function:: fractional_plot_bundle(fraction)

   Get the tueplots bundle, but with figure width as a fraction of
   the page width.


.. py:function:: get_integer_time(tdelta) -> tuple[int, str]

   Get the largest time unit that can represent the given timedelta as an
   integer.

   :returns:

             The integer value of the timedelta in the largest time unit, or
                     1 if no such unit exists.
             str: The time unit as a string ('weeks', 'days', 'hours', 'minutes',
                     'seconds', 'milliseconds', 'microseconds'). If no unit can
                     represent the timedelta as an integer, returns 'unknown'.
   :rtype: int

   .. rubric:: Examples

   >>> from datetime import timedelta
   >>> get_integer_time(timedelta(days=14))
   (2, 'weeks')
   >>> get_integer_time(timedelta(hours=5))
   (5, 'hours')
   >>> get_integer_time(timedelta(milliseconds=1000))
   (1, 'seconds')
   >>> get_integer_time(timedelta(days=0.001))
   (1, 'unknown')


.. py:function:: has_working_latex()

   Check if LaTeX is available or its toolchain


.. py:function:: init_training_logger_metrics(training_logger, val_steps)

   Set up logger metrics to track


.. py:function:: inverse_sigmoid(x)

   Inverse of torch.sigmoid

   Sigmoid output takes values in [0,1], this makes sure input is just within
   this interval.
   Note that this torch.clamp will make gradients 0, but this is not a problem
   as values of x that are this close to 0 or 1 have gradients of 0 anyhow.


.. py:function:: inverse_softplus(x, beta=1, threshold=20)

   Inverse of torch.nn.functional.softplus

   Input is clamped to approximately positive values of x, and the function is
   linear for inputs above x*beta for numerical stability.

   Note that this torch.clamp will make gradients 0, but this is not a
   problem as values of x that are this close to 0 have gradients of 0 anyhow.


.. py:function:: load_graph(graph_dir_path, device='cpu')

   Load all tensors representing the graph from `graph_dir_path`.

   Needs the following files for all graphs:
   - m2m_edge_index.pt
   - g2m_edge_index.pt
   - m2g_edge_index.pt
   - m2m_features.pt
   - g2m_features.pt
   - m2g_features.pt
   - mesh_features.pt

   And in addition for hierarchical graphs:
   - mesh_up_edge_index.pt
   - mesh_down_edge_index.pt
   - mesh_up_features.pt
   - mesh_down_features.pt

   :param graph_dir_path: Path to directory containing the graph files.
   :type graph_dir_path: str
   :param device: Device to load tensors to.
   :type device: str

   :returns: * **hierarchical** (*bool*) -- Whether the graph is hierarchical.
             * **graph** (*dict*) -- Dictionary containing the graph tensors, with keys as follows:
               - g2m_edge_index
               - m2g_edge_index
               - m2m_edge_index
               - mesh_up_edge_index
               - mesh_down_edge_index
               - g2m_features
               - m2g_features
               - m2m_features
               - mesh_up_features
               - mesh_down_features
               - mesh_static_features


.. py:function:: make_mlp(blueprint, layer_norm=True)

   Create MLP from list blueprint, with
   input dimensionality: blueprint[0]
   output dimensionality: blueprint[-1] and
   hidden layers of dimensions: blueprint[1], ..., blueprint[-2]

   if layer_norm is True, includes a LayerNorm layer at
   the output (as used in GraphCast)


.. py:function:: rank_zero_print(*args, **kwargs)

   Print only from rank 0 process


.. py:function:: setup_training_logger(datastore, args, run_name)

   :param datastore: Datastore object.
   :type datastore: Datastore
   :param args: Arguments from command line.
   :type args: argparse.Namespace
   :param run_name: Name of the run.
   :type run_name: str

   :returns: **logger** -- Logger object.
   :rtype: pytorch_lightning.loggers.base
