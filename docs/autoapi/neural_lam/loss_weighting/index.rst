neural_lam.loss_weighting
=========================

.. py:module:: neural_lam.loss_weighting




Module Contents
---------------

.. py:function:: get_manual_state_feature_weights(weighting_config: neural_lam.config.ManualStateFeatureWeighting, datastore: neural_lam.datastore.base.BaseDatastore) -> list[float]

   Return the state feature weights as a list of floats in the order of the
   state features in the datastore.

   :param weighting_config: Configuration object containing the manual state feature weights.
   :type weighting_config: ManualStateFeatureWeighting
   :param datastore: Datastore object containing the state features.
   :type datastore: BaseDatastore

   :returns: List of floats containing the state feature weights.
   :rtype: list[float]


.. py:function:: get_state_feature_weighting(config: neural_lam.config.NeuralLAMConfig, datastore: neural_lam.datastore.base.BaseDatastore) -> list[float]

   Return the state feature weights as a list of floats in the order of the
   state features in the datastore. The weights are determined based on the
   configuration in the NeuralLAMConfig object.

   :param config: Configuration object for neural-lam.
   :type config: NeuralLAMConfig
   :param datastore: Datastore object containing the state features.
   :type datastore: BaseDatastore

   :returns: List of floats containing the state feature weights.
   :rtype: list[float]


.. py:function:: get_uniform_state_feature_weights(datastore: neural_lam.datastore.base.BaseDatastore) -> list[float]

   Return the state feature weights as a list of floats in the order of the
   state features in the datastore.

   The weights are uniform, i.e. 1.0/n_features for each feature.

   :param datastore: Datastore object containing the state features.
   :type datastore: BaseDatastore

   :returns: List of floats containing the state feature weights.
   :rtype: list[float]
