
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


function get_cherab_pinialignment, pulse=pulse

   subsystem='DG'
   julian_date=agm_pulse_to_julian(pulse, subsystem, type='on', ier=ier, verbose=verbose)


   ;; this routine is for pini alignment, whcih should be the same for
   ;; octant 7 and octant 1

   o1=cg_periscope_oct1_hist_align(julian_date=julian_date)

   restore, o1.file_align

   octant=8
   pini=ptrpini.pini
   bank=ptrpini.bank

   origin=ptrpini.source.cartesian_ref  ;; (x,y,x) ipini
   vector=ptrpini.direction.vector.cartesian_ref  ;;(x,y,x) ipini
   divu=ptrpini.direction.divergence.deuterium.divu   ;; in radian, ipini          (u,v,z) is the 
   divv=ptrpini.direction.divergence.deuterium.divv    ;;in radian,  ipini


   return, {octant:octant, pini:pini, bank:bank, origin:origin, vector:vector, divu:divu, divv:divv}


end
