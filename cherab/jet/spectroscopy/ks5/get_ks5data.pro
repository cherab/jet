FUNCTION get_ks5data, pulse=pulse, spec=spec

   jpfdata=agm_readspec(pulse, spec=spec,/small)
   julian_date=jpfdata.data.juliandate

   data = cg_calibrate_cxsfitks5data(jpfdata=jpfdata, spec=detector, userwave_ref=userwave_ref, userwaveref_units=userwaveref_units, userpix_ref=userpix_ref, _extra1=extra1, /cal_si)

   oinst = cg_get_instfunc_cherab(pulse=pulse,julian_date=data.juliandate, spec=spec, grating=grating, unit_slit=data.slitunit, slit=data.slit, userwave_ref=data.wave_cal[0,0,0], userwaveref_units=data.wave_calunits)

   cg_align=cg_getalignment_cxsfit(spec=spec, julian_date=julian_date)
   cg_cxsfit_track=cg_align.cxsfit_track
   cg_ccd_track=cg_align.track

   inst_data = oinst.data
   inst_wave = oinst.wave

   ret = CREATE_STRUCT('cg_align',cg_align,'data', data.data, 'error', data.randerror, 'wave_cal', data.wave_cal, $
   'time', data.time, 'datatrack', data.track, 'inst_data', inst_data, 'inst_wave', inst_wave)

   RETURN,ret

end
