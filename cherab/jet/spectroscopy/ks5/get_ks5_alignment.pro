
FUNCTION get_ks5_alignment, pulse=pulse, spec=spec
   print, 'agm_readspec'
   jpfdata=agm_readspec(pulse, spec=spec,/small)
   julian_date=jpfdata.data.juliandate
   help, julian_date

   print, 'cg_getalignment_cxsfit'
   cg_align=cg_getalignment_cxsfit(spec=spec, julian_date=julian_date)
   print, 'finished idl'

   RETURN,cg_align

end
