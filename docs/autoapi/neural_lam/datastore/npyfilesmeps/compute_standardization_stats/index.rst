neural_lam.datastore.npyfilesmeps.compute_standardization_stats
===============================================================

.. py:module:: neural_lam.datastore.npyfilesmeps.compute_standardization_stats






Module Contents
---------------

.. py:class:: PaddedWeatherDataset(base_dataset, world_size, batch_size)

   Bases: :py:obj:`torch.utils.data.Dataset`


   An abstract class representing a :class:`Dataset`.

   All datasets that represent a map from keys to data samples should subclass
   it. All subclasses should overwrite :meth:`__getitem__`, supporting fetching a
   data sample for a given key. Subclasses could also optionally overwrite
   :meth:`__len__`, which is expected to return the size of the dataset by many
   :class:`~torch.utils.data.Sampler` implementations and the default options
   of :class:`~torch.utils.data.DataLoader`. Subclasses could also
   optionally implement :meth:`__getitems__`, for speedup batched samples
   loading. This method accepts list of indices of samples of batch and returns
   list of samples.

   .. note::
     :class:`~torch.utils.data.DataLoader` by default constructs an index
     sampler that yields integral indices.  To make it work with a map-style
     dataset with non-integral indices/keys, a custom sampler must be provided.


   .. py:method:: get_original_indices()


   .. py:method:: get_original_window_indices(step_length)


   .. py:attribute:: base_dataset


   .. py:attribute:: batch_size


   .. py:attribute:: original_indices


   .. py:attribute:: padded_indices


   .. py:attribute:: padded_samples


   .. py:attribute:: total_samples


   .. py:attribute:: world_size


.. py:class:: StandardizedDatastore(datastore)

   Wrapper to ensure datastore returns standardized data.


   .. py:method:: get_dataarray(category, split, standardize=False)


.. py:function:: cli()

.. py:function:: get_rank()

.. py:function:: get_world_size()

.. py:function:: main(datastore_config_path, batch_size, step_length, n_workers, distributed)

   Pre-compute parameter weights to be used in loss function

   :param datastore_config_path: Path to datastore config file
   :type datastore_config_path: str
   :param batch_size: Batch size when iterating over the dataset
   :type batch_size: int
   :param step_length: Step length to consider single time step
   :type step_length: datetime.timedelta
   :param n_workers: Number of workers in data loader
   :type n_workers: int
   :param distributed: Run the script in distributed
   :type distributed: bool


.. py:function:: save_stats(static_dir_path, means, squares, flux_means, flux_squares, filename_prefix)

.. py:function:: setup(rank, world_size)

   Initialize the distributed group.


