neural_lam.config
=================

.. py:module:: neural_lam.config








Module Contents
---------------

.. py:exception:: InvalidConfigError

   Bases: :py:obj:`Exception`


   Common base class for all non-exit exceptions.


.. py:class:: DatastoreSelection

   Configuration for selecting a datastore to use with neural-lam.

   .. attribute:: kind

      The kind of datastore to use, currently `mdp` or `npyfilesmeps` are
      implemented.

      :type: str

   .. attribute:: config_path

      The path to the configuration file for the selected datastore, this is
      assumed to be relative to the configuration file for neural-lam.

      :type: str


   .. py:attribute:: config_path
      :type:  str


   .. py:attribute:: kind
      :type:  str


.. py:class:: ManualStateFeatureWeighting

   Configuration for weighting the state features in the loss function where
   the weights are manually specified.

   .. attribute:: weights

      Manual weights for the state features.

      :type: Dict[str, float]


   .. py:attribute:: weights
      :type:  Dict[str, float]


.. py:class:: NeuralLAMConfig

   Bases: :py:obj:`dataclass_wizard.JSONWizard`, :py:obj:`dataclass_wizard.YAMLWizard`


   Dataclass for Neural-LAM configuration. This class is used to load and
   store the configuration for using Neural-LAM.

   .. attribute:: datastore

      The configuration for the datastore to use.

      :type: DatastoreSelection

   .. attribute:: training

      The configuration for training the model.

      :type: TrainingConfig


   .. py:attribute:: datastore
      :type:  DatastoreSelection


   .. py:attribute:: training
      :type:  TrainingConfig


.. py:class:: OutputClamping

   Configuration for clamping the output of the model.

   .. attribute:: lower

      The minimum value to clamp each output feature to.

      :type: Dict[str, float]

   .. attribute:: upper

      The maximum value to clamp each output feature to.

      :type: Dict[str, float]


   .. py:attribute:: lower
      :type:  Dict[str, float]


   .. py:attribute:: upper
      :type:  Dict[str, float]


.. py:class:: TrainingConfig

   Configuration related to training neural-lam

   .. attribute:: state_feature_weighting

                                  UnformFeatureWeighting]
      The method to use for weighting the state features in the loss
      function. Defaults to uniform weighting (`UnformFeatureWeighting`, i.e.
      all features are weighted equally).

      :type: Union[ManualStateFeatureWeighting,


   .. py:attribute:: output_clamping
      :type:  OutputClamping


   .. py:attribute:: state_feature_weighting
      :type:  Union[ManualStateFeatureWeighting, UniformFeatureWeighting]


.. py:class:: UniformFeatureWeighting

   Configuration for weighting the state features in the loss function where
   all state features are weighted equally.


.. py:function:: load_config_and_datastore(config_path: str) -> tuple[NeuralLAMConfig, Union[neural_lam.datastore.MDPDatastore, neural_lam.datastore.NpyFilesDatastoreMEPS]]

   Load the neural-lam configuration and the datastore specified in the
   configuration.

   :param config_path: Path to the Neural-LAM configuration file.
   :type config_path: str

   :returns: The Neural-LAM configuration and the loaded datastore.
   :rtype: tuple[NeuralLAMConfig, Union[MDPDatastore, NpyFilesDatastoreMEPS]]


