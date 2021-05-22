
# Copyright 2014-2017 United Kingdom Atomic Energy Authority
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

from .polychromator import PolychromatorFilter, Polychromator, global_polychromator, array_polychromator
from .polychromator import d_alpha_filter, baseline_523nm_filter, be_ii_527nm_filter, c_iii_465nm_filter, w_i_410nm_filter, he_i_668nm_filter, n_ii_567nm_filter
from .spectrometer import HighResSpectrometer, SurveySpectrometer, ksra, ksrb, ksrc, ksrd
from .load_ks3_sightlines import load_ks3_inner_array, load_ks3_outer_array
