###############################################################################
# Copyright (C) Philipp Rouast - All Rights Reserved                          #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Philipp Rouast <philipp@rouast.com>, December 2022               #
###############################################################################

import sys
sys.path.append('../propy')

from propy.numpy.stride_tricks import window_view, reduce_window_view, resolve_1d_window_view

import numpy as np
import pytest
import random

def test_window_view():
  x_view, pad_start, pad_end = \
    window_view(x=np.array([[0., 5.], [1., 6.], [2., 7.], [3., 8.], [4., 9.]]),
                min_window_size=1, max_window_size=3, overlap=2)
  np.testing.assert_allclose(x_view,
    np.array([[[np.nan, np.nan], [np.nan, np.nan], [0., 5.]],
              [[np.nan, np.nan], [0., 5.], [1., 6.]],
              [[0., 5.], [1., 6.], [2., 7.]],
              [[1., 6.], [2., 7.], [3., 8.]],
              [[2., 7.], [3., 8.], [4., 9.]]]))
  assert pad_start == 2
  assert pad_end == 0

@pytest.mark.parametrize("max_window_size", [2, 5, 9, 16])
def test_reduce_window_view(max_window_size):
  overlap = int(random.uniform(0, max_window_size-1))
  x = np.random.uniform(size=(64, 2))
  x_view, _, pad_end = \
    window_view(x=x, min_window_size=max_window_size, max_window_size=max_window_size, overlap=overlap)
  x_view_reduced = reduce_window_view(x_view, overlap=overlap, pad_end=pad_end)
  np.testing.assert_allclose(x, x_view_reduced)

@pytest.mark.parametrize("n_data", [6, 20])
@pytest.mark.parametrize("window_size", [3, 5])
@pytest.mark.parametrize("overlap", [0, 2])
@pytest.mark.parametrize("fill_method", ['mean', 'zero', 'start'])
def test_resolve_1d_window_view(n_data, window_size, overlap, fill_method):
  x = np.zeros((n_data,))
  x_view, _, pad_end = window_view(
      x=x, min_window_size=window_size, max_window_size=window_size, overlap=overlap)
  x_view_prc = np.nanmean(x_view, axis=-1)
  x_view_prc_res = resolve_1d_window_view(
      x=x_view_prc, window_size=window_size, overlap=overlap,
      pad_end=pad_end, fill_method=fill_method)
  np.testing.assert_allclose(x, x_view_prc_res)