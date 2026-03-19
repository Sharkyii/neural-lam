neural_lam.metrics
==================

.. py:module:: neural_lam.metrics






Module Contents
---------------

.. py:function:: crps_gauss(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   (Negative) Continuous Ranked Probability Score (CRPS).

   Closed-form expression based on Gaussian predictive distribution.
   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: get_metric(metric_name)

   Get a defined metric with given name.

   :param metric_name: Name of the metric.
   :type metric_name: str

   :returns: Function implementing the metric.
   :rtype: callable


.. py:function:: mae(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   (Unweighted) Mean Absolute Error.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: mask_and_reduce_metric(metric_entry_vals, mask, average_grid, sum_vars)

   Mask and optionally reduce entry-wise metric values.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param metric_entry_vals: Shape ``(..., N, d_state)``.
   :type metric_entry_vals: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: mse(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   (Unweighted) Mean Squared Error.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: nll(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   Negative Log Likelihood loss for isotropic Gaussian likelihood.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: wmae(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   Weighted Mean Absolute Error.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:function:: wmse(pred, target, pred_std, mask=None, average_grid=True, sum_vars=True)

   Weighted Mean Squared Error.

   ``(...)`` is any number of batch dimensions, potentially different
   but broadcastable.

   :param pred: Shape ``(..., N, d_state)``, prediction.
   :type pred: torch.Tensor
   :param target: Shape ``(..., N, d_state)``, target.
   :type target: torch.Tensor
   :param pred_std: Shape ``(..., N, d_state)`` or ``(d_state,)``, predicted std.-dev.
   :type pred_std: torch.Tensor
   :param mask: Shape ``(N,)``, boolean mask for which grid nodes to include.
   :type mask: torch.Tensor or None
   :param average_grid: If True, reduce grid dimension ``-2`` by mean over N.
   :type average_grid: bool
   :param sum_vars: If True, reduce variable dimension ``-1`` by sum over d_state.
   :type sum_vars: bool

   :returns: One of ``(...,)``, ``(..., d_state)``, ``(..., N)``, or
             ``(..., N, d_state)`` depending on reduction arguments.
   :rtype: torch.Tensor


.. py:data:: DEFINED_METRICS
