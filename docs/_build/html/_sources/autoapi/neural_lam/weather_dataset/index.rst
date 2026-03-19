neural_lam.weather_dataset
==========================

.. py:module:: neural_lam.weather_dataset




Module Contents
---------------

.. py:class:: WeatherDataModule(datastore: neural_lam.datastore.base.BaseDatastore, ar_steps_train: int = 3, ar_steps_eval: int = 25, num_past_forcing_steps: int = 1, num_future_forcing_steps: int = 1, batch_size: int = 4, num_workers: int = 16, eval_split: str = 'test')

   Bases: :py:obj:`pytorch_lightning.LightningDataModule`


   DataModule for weather data.


   .. py:method:: setup(stage=None)

      Called at the beginning of fit (train + validate), validate, test, or predict. This is a good hook when you
      need to build models dynamically or adjust something about them. This hook is called on every process when
      using DDP.

      :param stage: either ``'fit'``, ``'validate'``, ``'test'``, or ``'predict'``

      Example::

          class LitModel(...):
              def __init__(self):
                  self.l1 = None

              def prepare_data(self):
                  download_data()
                  tokenize()

                  # don't do this
                  self.something = else

              def setup(self, stage):
                  data = load_data(...)
                  self.l1 = nn.Linear(28, data.num_classes)




   .. py:method:: test_dataloader()

      Load test dataset.



   .. py:method:: train_dataloader()

      Load train dataset.



   .. py:method:: val_dataloader()

      Load validation dataset.



   .. py:attribute:: ar_steps_eval
      :value: 25



   .. py:attribute:: ar_steps_train
      :value: 3



   .. py:attribute:: batch_size
      :value: 4



   .. py:attribute:: eval_split
      :value: 'test'



   .. py:attribute:: multiprocessing_context
      :type:  Union[str, None]
      :value: None



   .. py:attribute:: num_future_forcing_steps
      :value: 1



   .. py:attribute:: num_past_forcing_steps
      :value: 1



   .. py:attribute:: num_workers
      :type:  int
      :value: 16



   .. py:attribute:: test_dataset
      :value: None



   .. py:attribute:: train_dataset
      :value: None



   .. py:attribute:: val_dataset
      :value: None



.. py:class:: WeatherDataset(datastore: neural_lam.datastore.base.BaseDatastore, split: str = 'train', ar_steps: int = 3, num_past_forcing_steps: int = 1, num_future_forcing_steps: int = 1)

   Bases: :py:obj:`torch.utils.data.Dataset`


   Dataset class for weather data.

   This class loads and processes weather data from a given datastore.

   :param datastore: The datastore to load the data from (e.g. mdp).
   :type datastore: BaseDatastore
   :param split: The data split to use ("train", "val" or "test"). Default is "train".
   :type split: str, optional
   :param ar_steps: The number of autoregressive steps. Default is 3.
   :type ar_steps: int, optional
   :param num_past_forcing_steps: Number of past time steps to include in forcing input. If set to i,
                                  forcing from times t-i, t-i+1, ..., t-1, t (and potentially beyond,
                                  given num_future_forcing_steps) are included as forcing inputs at time t
                                  Default is 1.
   :type num_past_forcing_steps: int, optional
   :param num_future_forcing_steps: Number of future time steps to include in forcing input. If set to j,
                                    forcing from times t, t+1, ..., t+j-1, t+j (and potentially times before
                                    t, given num_past_forcing_steps) are included as forcing inputs at time
                                    t. Default is 1.
   :type num_future_forcing_steps: int, optional


   .. py:method:: create_dataarray_from_tensor(tensor: torch.Tensor, time: Union[datetime.datetime, list[datetime.datetime]], category: str)

      Construct a xarray.DataArray from a `pytorch.Tensor` with coordinates
      for `grid_index`, `time` and `{category}_feature` matching the shape
      and number of times provided and add the x/y coordinates from the
      datastore.

      The number if times provided is expected to match the shape of the
      tensor. For a 2D tensor, the dimensions are assumed to be (grid_index,
      {category}_feature) and only a single time should be provided. For a 3D
      tensor, the dimensions are assumed to be (time, grid_index,
      {category}_feature) and a list of times should be provided.

      :param tensor: The tensor to construct the DataArray from, this assumed to have
                     the same dimension ordering as returned by the __getitem__ method
                     (i.e. time, grid_index, {category}_feature). The tensor will be
                     copied to the CPU before constructing the DataArray.
      :type tensor: torch.Tensor
      :param time: The time or times of the tensor.
      :type time: datetime.datetime or list[datetime.datetime]
      :param category: The category of the tensor, either "state", "forcing" or "static".
      :type category: str

      :returns: **da** -- The constructed DataArray.
      :rtype: xr.DataArray



   .. py:attribute:: ar_steps
      :value: 3



   .. py:attribute:: da_forcing


   .. py:attribute:: da_state


   .. py:attribute:: datastore


   .. py:attribute:: num_future_forcing_steps
      :value: 1



   .. py:attribute:: num_past_forcing_steps
      :value: 1



   .. py:attribute:: split
      :value: 'train'
