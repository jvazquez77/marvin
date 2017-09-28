# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-09-20 15:14:40
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-09-28 14:17:19

from __future__ import print_function, division, absolute_import
from .base import QueryDataModel
import copy
from marvin.utils.datamodel.query.base import query_params
from marvin.utils.datamodel.query.MPL5 import EXCLUDE

GROUPS = copy.deepcopy(query_params)

# list of tables to exclude
EXCLUDE = set(EXCLUDE) - set(['obsinfo', 'dapall'])

MPL6 = QueryDataModel(release='MPL-6', groups=GROUPS, aliases=['MPL6', 'v2_2_0', 'trunk'], exclude=EXCLUDE)

GRPDICT = {'Emission': 'spaxelprop.emline', 'Kinematic': 'spaxelprop.stellar', 'Spectral Indices': 'spaxelprop.specindex', 'NSA Catalog': 'nsa'}
MPL6.regroup(GRPDICT)
MPL6.add_group('Other')
MPL6.add_to_group('Other')
