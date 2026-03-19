neural_lam.vis
==============

.. py:module:: neural_lam.vis




Module Contents
---------------

.. py:function:: plot_error_map(errors, datastore: neural_lam.datastore.base.BaseRegularGridDatastore, title=None)

   Plot a heatmap of errors of different variables at different
   predictions horizons
   errors: (pred_steps, d_f)


.. py:function:: plot_prediction(datastore: neural_lam.datastore.base.BaseRegularGridDatastore, da_prediction: xarray.DataArray, da_target: xarray.DataArray, title=None, vrange=None)

   Plot example prediction and grond truth.

   Each has shape (N_grid,)



.. py:function:: plot_spatial_error(error, datastore: neural_lam.datastore.base.BaseRegularGridDatastore, title=None, vrange=None)

   Plot errors over spatial map
   Error and obs_mask has shape (N_grid,)
