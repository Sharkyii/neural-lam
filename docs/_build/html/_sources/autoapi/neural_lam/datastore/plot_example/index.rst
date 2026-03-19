neural_lam.datastore.plot_example
=================================

.. py:module:: neural_lam.datastore.plot_example




Module Contents
---------------

.. py:function:: plot_example_from_datastore(category, datastore, col_dim, split='train', standardize=True, selection={}, index_selection={})

   Create a plot of the data from the datastore.

   :param category: Category of data to plot, one of "state", "forcing", or "static".
   :type category: str
   :param datastore: Datastore to retrieve data from.
   :type datastore: Datastore
   :param col_dim: Dimension to use for plot facetting into columns. This can be a
                   template string that can be formatted with the category name.
   :type col_dim: str
   :param split: Split of data to plot, by default "train".
   :type split: str, optional
   :param standardize: Whether to standardize the data before plotting, by default True.
   :type standardize: bool, optional
   :param selection: Selections to apply to the dataarray, for example
                     `time="1990-09-03T0:00" would select this single timestep, by default
                     {}.
   :type selection: dict, optional
   :param index_selection: Index-based selection to apply to the dataarray, for example
                           `time=0` would select the first item along the `time` dimension, by
                           default {}.
   :type index_selection: dict, optional

   :returns: Matplotlib figure object.
   :rtype: Figure
