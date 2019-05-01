﻿"""
pyart.retrieve.quasi_vertical_profile
=====================================

Retrieval of QVPs from a radar object

.. autosummary::
    :toctree: generated/

    quasi_vertical_profile
    compute_qvp
    compute_rqvp
    compute_evp
    compute_svp
    compute_vp
    compute_directional_stats
    project_to_vertical
    find_rng_index
    get_target_elevations
    find_nearest_gate
    find_neighbour_gates
    _create_qvp_object
    _update_qvp_metadata

"""

from copy import deepcopy
from warnings import warn

import numpy as np
from scipy.interpolate import interp1d
from netCDF4 import num2date

from ..core.transforms import antenna_to_cartesian
from ..io.common import make_time_unit_str
from ..util.xsect import cross_section_rhi
from ..util.datetime_utils import datetime_from_radar


def quasi_vertical_profile(
        radar, desired_angle=None, fields=None, gatefilter=None):

    """
    Quasi Vertical Profile.

    Creates a QVP object containing fields from a radar object that can
    be used to plot and produce the quasi vertical profile

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field : string
        Radar field to use for QVP calculation.
    desired_angle : float
        Radar tilt angle to use for indexing radar field data.
        None will result in wanted_angle = 20.0.

    Other Parameters
    ----------------
    gatefilter : GateFilter
        A GateFilter indicating radar gates that should be excluded
        from the import qvp calculation.

    Returns
    -------
    qvp : Dictonary
        A quasi vertical profile object containing fields
        from a radar object.

    References
    ----------
    Troemel, S., M. Kumjian, A. Ryzhkov, and C. Simmer, 2013: Backscatter
    differential phase - estimation and variability. J Appl. Meteor. Clim..
    52, 2529 - 2548.

    Troemel, S., A. Ryzhkov, P. Zhang, and C. Simmer, 2014: Investigations
    of backscatter differential phase in the melting layer. J. Appl. Meteorol.
    Clim. 54, 2344 - 2359.

    Ryzhkov, A., P. Zhang, H. Reeves, M. Kumjian, T. Tschallener, S. Tromel,
    C. Simmer, 2015: Quasi-vertical profiles - a new way to look at
    polarimetric radar data. Submitted to J. Atmos. Oceanic Technol.

    """
    # Creating an empty dictonary
    qvp = {}

    # Setting the desired radar angle and getting index value for desired radar angle
    if desired_angle is None:
        desired_angle = 20.0
    index = abs(radar.fixed_angle['data'] - desired_angle).argmin()
    radar_slice = radar.get_slice(index)

    # Printing radar tilt angles and radar elevation
    print(radar.fixed_angle['data'])
    print(radar.elevation['data'][-1])

    # Setting field parameters
    # If fields is None then all radar fields pulled else defined field is used
    if fields is None:
        fields = radar.fields

        for field in fields:

            # Filtering data based on defined gatefilter
            # If none is defined goes to else statement
            if gatefilter is not None:
                get_fields = radar.get_field(index, field)
                mask_fields = np.ma.masked_where(
                    gatefilter.gate_excluded[radar_slice],
                    get_fields)
                radar_fields = np.ma.mean(mask_fields, axis=0)
            else:
                radar_fields = radar.get_field(index, field).mean(axis=0)

            qvp.update({field:radar_fields})

    else:
        # Filtering data based on defined gatefilter
        # If none is defined goes to else statement
        if gatefilter is not None:
            get_field = radar.get_field(index, fields)
            mask_field = np.ma.masked_where(
                gatefilter.gate_excluded[radar_slice],
                get_field)
            radar_field = np.ma.mean(mask_field, axis=0)
        else:
            radar_field = radar.get_field(index, fields).mean(axis=0)

        qvp.update({fields:radar_field})

    # Adding range, time, and height fields
    qvp.update({'range': radar.range['data'], 'time': radar.time})
    _, _, z = antenna_to_cartesian(qvp['range']/1000.0, 0.0,
                                   radar.fixed_angle['data'][index])
    qvp.update({'height': z})
    return qvp


def compute_qvp(radar, field_names, ref_time=None, angle=0., ang_tol=1.,
                hmax=10000., hres=50., avg_type='mean', nvalid_min=30,
                interp_kind='none', qvp=None):
    """
    Computes quasi vertical profiles.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of str
        List of field names to add to the QVP.
    ref_time : datetime object
        Reference time for current radar volume.
    angle : int or float
        If the radar object contains a PPI volume, the sweep number to
        use, if it contains an RHI volume the elevation angle.
    ang_tol : float
        If the radar object contains an RHI volume, the tolerance in the
        elevation angle for the conversion into PPI.
    hmax : float
        The maximum height to plot [m].
    hres : float
        The height resolution [m].
    avg_type : str
        The type of averaging to perform. Can be either "mean" or "median".
    nvalid_min : int
        Minimum number of valid points to accept average.
    interp_kind : str
        Type of interpolation when projecting to vertical grid: 'none',
        or 'nearest', etc.
        'none' will select from all data points within the regular grid
        height bin that is the closest to the center of the bin.
        'nearest' will select the closest data point to the center of the
        height bin regardless if it is within the height bin or not.
        Data points can be masked values.
        If another type of interpolation is selected masked values will be
        eliminated from the data points before the interpolation.
    qvp : QVP object or None
        If it is None this is the QVP object where to store the data from the
        current time step. Otherwise a new QVP object will be created.

    Returns
    -------
    qvp : qvp object
        The computed QVP object.

    Reference
    ---------
    Ryzhkov A., Zhang P., Reeves H., Kumjian M., Tschallener T., Trömel S.,
    Simmer C. 2016: Quasi-Vertical Profiles: A New Way to Look at Polarimetric
    Radar Data. JTECH vol. 33 pp 551-562

    """
    if avg_type not in ('mean', 'median'):
        warn('Unsuported statistics ' + avg_type)
        return None

    radar_aux = deepcopy(radar)
    # transform radar into ppi over the required elevation
    if radar_aux.scan_type == 'rhi':
        radar_aux = cross_section_rhi(radar_aux, [angle], el_tol=ang_tol)
    elif radar_aux.scan_type == 'ppi':
        radar_aux = radar_aux.extract_sweeps([int(angle)])
    else:
        warn('Error: unsupported scan type.')
        return None

    if qvp is None:
        qvp = _create_qvp_object(
            radar_aux, field_names, qvp_type='qvp',
            start_time=ref_time, hmax=hmax, hres=hres)

    # modify metadata
    if ref_time is None:
        ref_time = datetime_from_radar(radar_aux)
    qvp = _update_qvp_metadata(
        qvp, ref_time, qvp.longitude['data'][0], qvp.latitude['data'][0],
        elev=qvp.fixed_angle['data'][0])

    for field_name in field_names:
        # compute QVP data
        if field_name not in radar_aux.fields:
            warn('Field ' + field_name + ' not in radar object')
            qvp_data = np.ma.masked_all(qvp.ngates)
        else:
            values, _ = compute_directional_stats(
                radar_aux.fields[field_name]['data'], avg_type=avg_type,
                nvalid_min=nvalid_min, axis=0)

            # Project to vertical grid:
            qvp_data = project_to_vertical(
                values, radar_aux.gate_altitude['data'][0, :],
                qvp.range['data'], interp_kind=interp_kind)

        # Put data in radar object
        if np.size(qvp.fields[field_name]['data']) == 0:
            qvp.fields[field_name]['data'] = qvp_data.reshape(1, qvp.ngates)
        else:
            qvp.fields[field_name]['data'] = np.ma.concatenate(
                (qvp.fields[field_name]['data'],
                 qvp_data.reshape(1, qvp.ngates)))

    return qvp


def compute_rqvp(radar, field_names, ref_time=None, hmax=10000., hres=2.,
                 avg_type='mean', nvalid_min=30, interp_kind='nearest',
                 rmax=50000., weight_power=2., qvp=None):
    """
    Computes range-defined quasi vertical profiles.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of str
        List of field names to add to the QVP.
    ref_time : datetime object
        Reference time for current radar volume.
    hmax : float
        The maximum height to plot [m].
    hres : float
        The height resolution [m].
    avg_type : str
        The type of averaging to perform. Can be either "mean" or "median".
    nvalid_min : int
        Minimum number of valid points to accept average.
    interp_kind : str
        Type of interpolation when projecting to vertical grid: 'none',
        or 'nearest', etc.
        'none' will select from all data points within the regular grid
        height bin that is the closest to the center of the bin.
        'nearest' will select the closest data point to the center of the
        height bin regardless if it is within the height bin or not.
        Data points can be masked values.
        If another type of interpolation is selected masked values will be
        eliminated from the data points before the interpolation
    rmax : float
        Ground range up to which the data is intended for use [m].
    weight_power : float
        Power p of the weighting function 1/abs(grng-(rmax-1))**p given to
        the data outside the desired range. -1 will set the weight to 0.
    qvp : QVP object or None
        If it is None this is the QVP object where to store the data from the
        current time step. Otherwise a new QVP object will be created.

    Returns
    -------
    rqvp : qvp object
        The computed range defined quasi vertical profile.

    Reference
    ---------
    Tobin D.M., Kumjian M.R. 2017: Polarimetric Radar and Surface-Based
    Precipitation-Type Observations of ice Pellet to Freezing Rain
    Transitions. Weather and Forecasting vol. 32 pp 2065-2082

    """
    if avg_type not in ('mean', 'median'):
        warn('Unsuported statistics ' + avg_type)
        return None

    radar_aux = deepcopy(radar)
    # transform radar into ppi over the required elevation
    if radar_aux.scan_type == 'rhi':
        target_elevations, el_tol = get_target_elevations(radar_aux)
        radar_ppi = cross_section_rhi(
            radar_aux, target_elevations, el_tol=el_tol)
    elif radar_aux.scan_type == 'ppi':
        radar_ppi = radar_aux
    else:
        warn('Error: unsupported scan type.')
        return None

    if qvp is None:
        rqvp = _create_qvp_object(
            radar_aux, field_names, qvp_type='rqvp',
            start_time=ref_time, hmax=hmax, hres=hres)

    # modify metadata
    if ref_time is None:
        ref_time = datetime_from_radar(radar_ppi)
    rqvp = _update_qvp_metadata(
        rqvp, ref_time, rqvp.longitude['data'][0], rqvp.latitude['data'][0],
        elev=90.)

    rmax_km = rmax/1000.
    grng_interp = np.ma.masked_all((radar_ppi.nsweeps, rqvp.ngates))
    val_interp = dict()
    for field_name in field_names:
        val_interp.update({field_name: np.ma.masked_all(
            (radar_ppi.nsweeps, rqvp.ngates))})

    for sweep in range(radar_ppi.nsweeps):
        radar_aux = deepcopy(radar_ppi)
        radar_aux = radar_aux.extract_sweeps([sweep])
        height = radar_aux.gate_altitude['data'][0, :]

        # compute ground range [Km]
        grng = np.sqrt(
            np.power(radar_aux.gate_x['data'][0, :], 2.) +
            np.power(radar_aux.gate_y['data'][0, :], 2.))/1000.

        # Project ground range to grid
        f = interp1d(
            height, grng, kind=interp_kind, bounds_error=False,
            fill_value='extrapolate')
        grng_interp[sweep, :] = f(rqvp.range['data'])

        for field_name in field_names:
            if field_name not in radar_aux.fields:
                warn('Field ' + field_name + ' not in radar object')
                continue

            # Compute QVP for this sweep
            values, _ = compute_directional_stats(
                radar_aux.fields[field_name]['data'], avg_type=avg_type,
                nvalid_min=nvalid_min, axis=0)

            # Project to grid
            val_interp[field_name][sweep, :] = project_to_vertical(
                values, height, rqvp.range['data'], interp_kind=interp_kind)

    # Compute weight
    weight = np.ma.abs(grng_interp-(rmax_km-1.))
    weight[grng_interp <= rmax_km-1.] = 1./np.power(
        weight[grng_interp <= rmax_km-1.], 0.)

    if weight_power == -1:
        weight[grng_interp > rmax_km-1.] = 0.
    else:
        weight[grng_interp > rmax_km-1.] = 1./np.power(
            weight[grng_interp > rmax_km-1.], weight_power)

    for field_name in field_names:

        # mask weights where there is no data
        mask = np.ma.getmaskarray(val_interp[field_name])
        weight_aux = np.ma.masked_where(mask, weight)

        # Weighted average
        rqvp_data = (
            np.ma.sum(val_interp[field_name]*weight_aux, axis=0)
            / np.ma.sum(weight_aux, axis=0))

        # Put data in radar object
        if np.size(rqvp.fields[field_name]['data']) == 0:
            rqvp.fields[field_name]['data'] = rqvp_data.reshape(
                1, rqvp.ngates)
        else:
            rqvp.fields[field_name]['data'] = np.ma.concatenate(
                (rqvp.fields[field_name]['data'],
                 rqvp_data.reshape(1, rqvp.ngates)))

    return rqvp


def compute_evp(radar, field_names, lon, lat, ref_time=None,
                latlon_tol=0.0005, delta_rng=15000., delta_azi=10,
                hmax=10000., hres=250., avg_type='mean', nvalid_min=1,
                interp_kind='none', qvp=None):
    """
    Computes enhanced vertical profiles.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of str
        List of field names to add to the QVP.
    lat, lon : float
        Latitude and longitude of the point of interest [deg].
    ref_time : datetime object
        Reference time for current radar volume.
    latlon_tol : float
        Tolerance in latitude and longitude in deg.
    delta_rng, delta_azi : float
        Maximum range distance [m] and azimuth distance [degree] from the
        central point of the evp containing data to average.
    hmax : float
        The maximum height to plot [m].
    hres : float
        The height resolution [m].
    avg_type : str
        The type of averaging to perform. Can be either "mean" or "median".
    nvalid_min : int
        Minimum number of valid points to accept average.
    interp_kind : str
        Type of interpolation when projecting to vertical grid: 'none',
        or 'nearest', etc.
        'none' will select from all data points within the regular grid
        height bin the closest to the center of the bin.
        'nearest' will select the closest data point to the center of the
        height bin regardless if it is within the height bin or not.
        Data points can be masked values.
        If another type of interpolation is selected masked values will be
        eliminated from the data points before the interpolation.
    qvp : QVP object or None
        If it is None this is the QVP object where to store the data from the
        current time step. Otherwise a new QVP object will be created.

    Returns
    -------
    evp : qvp object
        The computed enhanced vertical profile.

    Reference
    ---------
    Kaltenboeck R., Ryzhkov A. 2016: A freezing rain storm explored with a
    C-band polarimetric weather radar using the QVP methodology.
    Meteorologische Zeitschrift vol. 26 pp 207-222

    """
    if avg_type not in ('mean', 'median'):
        warn('Unsuported statistics ' + avg_type)
        return None

    radar_aux = deepcopy(radar)
    # transform radar into ppi over the required elevation
    if radar_aux.scan_type == 'rhi':
        target_elevations, el_tol = get_target_elevations(radar_aux)
        radar_ppi = cross_section_rhi(
            radar_aux, target_elevations, el_tol=el_tol)
    elif radar_aux.scan_type == 'ppi':
        radar_ppi = radar_aux
    else:
        warn('Error: unsupported scan type.')
        return None

    radar_aux = radar_ppi.extract_sweeps([0])

    if qvp is None:
        evp = _create_qvp_object(
            radar_aux, field_names, qvp_type='evp',
            start_time=ref_time, hmax=hmax, hres=hres)

    # modify metadata
    if ref_time is None:
        ref_time = datetime_from_radar(radar_aux)
    evp = _update_qvp_metadata(evp, ref_time, lon, lat, elev=90.)

    height = dict()
    values = dict()
    for field_name in field_names:
        height.update({field_name: np.array([], dtype=float)})
        values.update({field_name: np.ma.array([], dtype=float)})

    for sweep in range(radar_ppi.nsweeps):
        radar_aux = deepcopy(radar_ppi)
        radar_aux = radar_aux.extract_sweeps([sweep])

        # find nearest gate to lat lon point
        ind_ray, _, azi, rng = find_nearest_gate(
            radar_aux, lat, lon, latlon_tol=latlon_tol)

        if ind_ray is None:
            continue

        # find neighbouring gates to be selected
        inds_ray, inds_rng = find_neighbour_gates(
            radar_aux, azi, rng, delta_azi=delta_azi, delta_rng=delta_rng)

        for field_name in field_names:
            if field_name not in radar_aux.fields:
                warn('Field ' + field_name + ' not in radar object')
                continue

            height[field_name] = np.append(
                height[field_name],
                radar_aux.gate_altitude['data'][ind_ray, inds_rng])

            # keep only data we are interested in
            field = radar_aux.fields[field_name]['data'][:, inds_rng]
            field = field[inds_ray, :]

            vals, _ = compute_directional_stats(
                field, avg_type=avg_type, nvalid_min=nvalid_min, axis=0)
            values[field_name] = np.ma.append(values[field_name], vals)

    for field_name in field_names:
        # Project to vertical grid:
        evp_data = project_to_vertical(
            values[field_name], height[field_name], evp.range['data'],
            interp_kind=interp_kind)

        # Put data in radar object
        if np.size(evp.fields[field_name]['data']) == 0:
            evp.fields[field_name]['data'] = evp_data.reshape(1, evp.ngates)
        else:
            evp.fields[field_name]['data'] = np.ma.concatenate(
                (evp.fields[field_name]['data'],
                 evp_data.reshape(1, evp.ngates)))

    return evp


def compute_svp(radar, field_names, lon, lat, angle, ref_time=None,
                ang_tol=1., latlon_tol=0.0005, delta_rng=15000., delta_azi=10,
                hmax=10000., hres=250., avg_type='mean', nvalid_min=1,
                interp_kind='none', qvp=None):
    """
    Computes slanted vertical profiles.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of str
        List of field names to add to the QVP.
    lat, lon : float
        Latitude and longitude of the point of interest [deg].
    angle : int or float
        If the radar object contains a PPI volume, the sweep number to
        use, if it contains an RHI volume the elevation angle.
    ref_time : datetime object
        Reference time for current radar volume.
    ang_tol : float
        If the radar object contains an RHI volume, the tolerance in the
        elevation angle for the conversion into PPI.
    latlon_tol : float
        Tolerance in latitude and longitude in deg.
    delta_rng, delta_azi : float
        Maximum range distance [m] and azimuth distance [degree] from the
        central point of the evp containing data to average.
    hmax : float
        The maximum height to plot [m].
    hres : float
        The height resolution [m].
    avg_type : str
        The type of averaging to perform. Can be either "mean" or "median".
    nvalid_min : int
        Minimum number of valid points to accept average.
    interp_kind : str
        Type of interpolation when projecting to vertical grid: 'none',
        or 'nearest', etc.
        'none' will select from all data points within the regular grid
        height bin the closest to the center of the bin.
        'nearest' will select the closest data point to the center of the
        height bin regardless if it is within the height bin or not.
        Data points can be masked values.
        If another type of interpolation is selected masked values will be
        eliminated from the data points before the interpolation.
    qvp : QVP object or None
        If it is None this is the QVP object where to store the data from the
        current time step. Otherwise a new QVP object will be created.


    Returns
    -------
    svp : qvp object
        The computed slanted vertical profile

    Reference
    ---------
    Bukovcic P., Zrnic D., Zhang G. 2017: Winter Precipitation Liquid-Ice
    Phase Transitions Revealed with Polarimetric Radar and 2DVD Observations
    in Central Oklahoma. JTECH vol. 56 pp 1345-1363

    """
    if avg_type not in ('mean', 'median'):
        warn('Unsuported statistics ' + avg_type)
        return None

    radar_aux = deepcopy(radar)
    # transform radar into ppi over the required elevation
    if radar_aux.scan_type == 'rhi':
        radar_aux = cross_section_rhi(
            radar_aux, [angle], el_tol=ang_tol)
    elif radar_aux.scan_type == 'ppi':
        radar_aux = radar_aux.extract_sweeps([int(angle)])
    else:
        warn('Error: unsupported scan type.')
        return None

    if qvp is None:
        svp = _create_qvp_object(
            radar_aux, field_names, qvp_type='svp',
            start_time=ref_time, hmax=hmax, hres=hres)

    # modify metadata
    if ref_time is None:
        ref_time = datetime_from_radar(radar_aux)
    svp = _update_qvp_metadata(
        svp, ref_time, lon, lat, elev=svp.fixed_angle['data'][0])

    # find nearest gate to lat lon point
    ind_ray, _, azi, rng = find_nearest_gate(
        radar_aux, lat, lon, latlon_tol=latlon_tol)

    if ind_ray is None:
        warn('No data in selected point')
        svp_data = np.ma.masked_all(svp.ngates)

        for field_name in field_names:
            # Put data in radar object
            if np.size(svp.fields[field_name]['data']) == 0:
                svp.fields[field_name]['data'] = svp_data.reshape(
                    1, svp.ngates)
            else:
                svp.fields[field_name]['data'] = np.ma.concatenate(
                    (svp.fields[field_name]['data'],
                     svp_data.reshape(1, svp.ngates)))
        return svp

    # find neighbouring gates to be selected
    inds_ray, inds_rng = find_neighbour_gates(
        radar_aux, azi, rng, delta_azi=delta_azi, delta_rng=delta_rng)
    height = radar_aux.gate_altitude['data'][ind_ray, inds_rng]

    for field_name in field_names:
        if field_name not in radar_aux.fields:
            warn('Field ' + field_name + ' not in radar object')
            svp_data = np.ma.masked_all(svp.ngates)
        else:
            # keep only data we are interested in
            field = radar_aux.fields[field_name]['data'][:, inds_rng]
            field = field[inds_ray, :]

            # compute values
            values, _ = compute_directional_stats(
                field, avg_type=avg_type, nvalid_min=nvalid_min, axis=0)

            # Project to vertical grid:
            svp_data = project_to_vertical(
                values, height, svp.range['data'], interp_kind=interp_kind)

        # Put data in radar object
        if np.size(svp.fields[field_name]['data']) == 0:
            svp.fields[field_name]['data'] = svp_data.reshape(1, svp.ngates)
        else:
            svp.fields[field_name]['data'] = np.ma.concatenate(
                (svp.fields[field_name]['data'],
                 svp_data.reshape(1, svp.ngates)))

    return svp


def compute_vp(radar, field_names, lon, lat, ref_time=None,
               latlon_tol=0.0005, hmax=10000., hres=50.,
               interp_kind='none', qvp=None):
    """
    Computes vertical profiles.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of str
        List of field names to add to the QVP.
    lat, lon : float
        Latitude and longitude of the point of interest [deg].
    ref_time : datetime object
        Reference time for current radar volume.
    latlon_tol : float
        Tolerance in latitude and longitude in deg.
    hmax : float
        The maximum height to plot [m].
    hres : float
        The height resolution [m].
    interp_kind : str
        Type of interpolation when projecting to vertical grid: 'none',
        or 'nearest', etc.
        'none' will select from all data points within the regular grid
        height bin the closest to the center of the bin.
        'nearest' will select the closest data point to the center of the
        height bin regardless if it is within the height bin or not.
        Data points can be masked values.
        If another type of interpolation is selected masked values will be
        eliminated from the data points before the interpolation.
    qvp : QVP object or None
        If it is None this is the QVP object where to store the data from the
        current time step. Otherwise a new QVP object will be created.

    Returns
    -------
    vp : qvp object
        The computed vertical profile

    """
    radar_aux = deepcopy(radar)
    # transform radar into ppi over the required elevation
    if radar_aux.scan_type == 'rhi':
        target_elevations, el_tol = get_target_elevations(radar_aux)
        radar_ppi = cross_section_rhi(
            radar_aux, target_elevations, el_tol=el_tol)
    elif radar_aux.scan_type == 'ppi':
        radar_ppi = radar_aux
    else:
        warn('Error: unsupported scan type.')
        return None

    if qvp is None:
        vp = _create_qvp_object(
            radar_ppi, field_names, qvp_type='vp',
            start_time=ref_time, hmax=hmax, hres=hres)

    # modify metadata
    if ref_time is None:
        ref_time = datetime_from_radar(radar_ppi)
    vp = _update_qvp_metadata(vp, ref_time, lon, lat, elev=90.)

    height = dict()
    values = dict()
    for field_name in field_names:
        height.update({field_name: np.array([], dtype=float)})
        values.update({field_name: np.ma.array([], dtype=float)})

    for sweep in range(radar_ppi.nsweeps):
        radar_aux = deepcopy(radar_ppi.extract_sweeps([sweep]))

        # find nearest gate to lat lon point
        ind_ray, ind_rng, _, _ = find_nearest_gate(
            radar_aux, lat, lon, latlon_tol=latlon_tol)

        if ind_ray is None:
            continue

        for field_name in field_names:
            if field_name not in radar_aux.fields:
                warn('Field ' + field_name + ' not in radar object')
                continue
            else:
                height[field_name] = np.append(
                    height[field_name],
                    radar_aux.gate_altitude['data'][ind_ray, ind_rng])
                values[field_name] = np.ma.append(
                    values[field_name],
                    radar_aux.fields[field_name]['data'][ind_ray, ind_rng])

    for field_name in field_names:
        # Project to vertical grid:
        vp_data = project_to_vertical(
            values[field_name], height[field_name], vp.range['data'],
            interp_kind=interp_kind)

        # Put data in radar object
        if np.size(vp.fields[field_name]['data']) == 0:
            vp.fields[field_name]['data'] = vp_data.reshape(1, vp.ngates)
        else:
            vp.fields[field_name]['data'] = np.ma.concatenate(
                (vp.fields[field_name]['data'],
                 vp_data.reshape(1, vp.ngates)))

    return vp


def compute_directional_stats(field, avg_type='mean', nvalid_min=1, axis=0):
    """
    Computes the mean or the median along one of the axis (ray or range).

    Parameters
    ----------
    field : ndarray
        The radar field.
    avg_type : str
        The type of average: 'mean' or 'median'.
    nvalid_min : int
        The minimum number of points to consider the stats valid. Default 1.
    axis : int
        The axis along which to compute (0=ray, 1=range).

    Returns
    -------
    values : ndarray 1D
        The resultant statistics.
    nvalid : ndarray 1D
        The number of valid points used in the computation.

    """
    if avg_type == 'mean':
        values = np.ma.mean(field, axis=axis)
    else:
        values = np.ma.median(field, axis=axis)

    # Set to non-valid if there is not a minimum number of valid gates
    valid = np.logical_not(np.ma.getmaskarray(field))
    nvalid = np.sum(valid, axis=0, dtype=int)
    values[nvalid < nvalid_min] = np.ma.masked

    return values, nvalid


def project_to_vertical(data_in, data_height, grid_height, interp_kind='none',
                        fill_value=-9999.):
    """
    Projects radar data to a regular vertical grid

    Parameters
    ----------
    data_in : ndarray 1D
        The radar data to project.
    data_height : ndarray 1D
        The height of each radar point.
    grid_height : ndarray 1D
        The regular vertical grid to project to.
    interp_kind : str
        The type of interpolation to use: 'none' or 'nearest'.
    fill_value : float
        The fill value used for interpolation.

    Returns
    -------
    data_out : ndarray 1D
        The projected data.

    """
    if data_in.size == 0:
        data_out = np.ma.masked_all(grid_height.size)
        return data_out

    if interp_kind == 'none':
        hres = grid_height[1]-grid_height[0]
        data_out = np.ma.masked_all(grid_height.size)
        for ind_r, h in enumerate(grid_height):
            ind_h = find_rng_index(data_height, h, rng_tol=hres/2.)
            if ind_h is None:
                continue
            data_out[ind_r] = data_in[ind_h]
    elif interp_kind == 'nearest':
        data_filled = data_in.filled(fill_value=fill_value)
        f = interp1d(
            data_height, data_filled, kind=interp_kind, bounds_error=False,
            fill_value=fill_value)
        data_out = np.ma.masked_values(f(grid_height), fill_value)
    else:
        valid = np.logical_not(np.ma.getmaskarray(data_in))
        height_valid = data_height[valid]
        data_valid = data_in[valid]
        f = interp1d(
            height_valid, data_valid, kind=interp_kind, bounds_error=False,
            fill_value=fill_value)
        data_out = np.ma.masked_values(f(grid_height), fill_value)

    return data_out


def find_rng_index(rng_vec, rng, rng_tol=0.):
    """
    Find the range index corresponding to a particular range.

    Parameters
    ----------
    rng_vec : float array
        The range data array where to look for.
    rng : float
        The range to search.
    rng_tol : float
        Tolerance [m].

    Returns
    -------
    ind_rng : int
        The range index.

    """
    dist = np.abs(rng_vec-rng)
    ind_rng = np.argmin(dist)
    if dist[ind_rng] > rng_tol:
        return None

    return ind_rng


def get_target_elevations(radar):
    """
    Gets RHI target elevations.

    Parameters
    ----------
    radar : Radar object
        Current radar object.

    Returns
    -------
    target_elevations : 1D-array
        Azimuth angles.
    el_tol : float
        azimuth tolerance.

    """
    sweep_start = radar.sweep_start_ray_index['data'][0]
    sweep_end = radar.sweep_end_ray_index['data'][0]
    target_elevations = np.sort(
        radar.elevation['data'][sweep_start:sweep_end+1])
    el_tol = np.median(target_elevations[1:]-target_elevations[:-1])

    return target_elevations, el_tol


def find_nearest_gate(radar, lat, lon, latlon_tol=0.0005):
    """
    Find the radar gate closest to a lat, lon point.

    Parameters
    ----------
    radar : radar object
        The radar object.
    lat, lon : float
        The position of the point.
    latlon_tol : float
        The tolerance around this point.

    Returns
    -------
    ind_ray, ind_rng : int
        The ray and range index.
    azi, rng : float
        The range and azimuth position of the gate.

    """
    # find gates close to lat lon point
    inds_ray_aux, inds_rng_aux = np.where(np.logical_and(
        np.logical_and(
            radar.gate_latitude['data'] < lat+latlon_tol,
            radar.gate_latitude['data'] > lat-latlon_tol),
        np.logical_and(
            radar.gate_longitude['data'] < lon+latlon_tol,
            radar.gate_longitude['data'] > lon-latlon_tol)))

    if inds_ray_aux.size == 0:
        warn('No data found at point lat ' + str(lat) + ' +- '
             + str(latlon_tol) + ' lon ' + str(lon) + ' +- '
             + str(latlon_tol) + ' deg')

        return None, None, None, None

    # find closest latitude
    ind_min = np.argmin(np.abs(
        radar.gate_latitude['data'][inds_ray_aux, inds_rng_aux]-lat))
    ind_ray = inds_ray_aux[ind_min]
    ind_rng = inds_rng_aux[ind_min]

    azi = radar.azimuth['data'][ind_ray]
    rng = radar.range['data'][ind_rng]

    return ind_ray, ind_rng, azi, rng


def find_neighbour_gates(radar, azi, rng, delta_azi=None, delta_rng=None):
    """
    Find the neighbouring gates within +-delta_azi and +-delta_rng.

    Parameters
    ----------
    radar : radar object
        The radar object.
    azi, rng : float
        The azimuth [deg] and range [m] of the central gate.
    delta_azi, delta_rng : float
        The extend where to look for.

    Returns
    -------
    inds_ray_aux, ind_rng_aux : int
        The indices (ray, rng) of the neighbouring gates.

    """
    # find gates close to lat lon point
    if delta_azi is None:
        inds_ray = np.ma.arange(radar.azimuth['data'].size)
    else:
        azi_max = azi+delta_azi
        azi_min = azi-delta_azi
        if azi_max > 360.:
            azi_max -= 360.
        if azi_min < 0.:
            azi_min += 360.
        if azi_max > azi_min:
            inds_ray = np.where(np.logical_and(
                radar.azimuth['data'] < azi_max,
                radar.azimuth['data'] > azi_min))[0]
        else:
            inds_ray = np.where(np.logical_or(
                radar.azimuth['data'] > azi_min,
                radar.azimuth['data'] < azi_max))[0]
    if delta_rng is None:
        inds_rng = np.ma.arange(radar.range['data'].size)
    else:
        inds_rng = np.where(np.logical_and(
            radar.range['data'] < rng+delta_rng,
            radar.range['data'] > rng-delta_rng))[0]

    return inds_ray, inds_rng


def _create_qvp_object(radar, field_names, qvp_type='qvp', start_time=None,
                       hmax=10000., hres=200.):
    """
    Creates a QVP object containing fields from a radar object that can
    be used to plot and produce the quasi vertical profile.

    Parameters
    ----------
    radar : Radar
        Radar object used.
    field_names : list of strings
        Radar fields to use for QVP calculation.
    qvp_type : str
        Type of QVP. Can be qvp, rqvp, evp.
    start_time : datetime object
        The QVP start time.
    hmax : float
        The maximum height of the QVP [m]. Default 10000.
    hres : float
        The QVP range resolution [m]. Default 50.

    Returns
    -------
    qvp : Radar-like object
        A quasi vertical profile object containing fields
        from a radar object.

    """
    qvp = deepcopy(radar)

    # prepare space for field
    qvp.fields = dict()
    for field_name in field_names:
        qvp.add_field(field_name, deepcopy(radar.fields[field_name]))
        qvp.fields[field_name]['data'] = np.array([], dtype='float64')

    # fixed radar objects parameters
    qvp.range['data'] = np.arange(hmax/hres)*hres+hres/2.
    qvp.ngates = len(qvp.range['data'])

    if start_time is None:
        qvp.time['units'] = radar.time['units']
    else:
        qvp.time['units'] = make_time_unit_str(start_time)

    qvp.time['data'] = np.array([], dtype='float64')
    qvp.scan_type = qvp_type
    qvp.sweep_number['data'] = np.array([0], dtype='int32')
    qvp.nsweeps = 1
    qvp.sweep_mode['data'] = np.array([qvp_type])
    qvp.sweep_start_ray_index['data'] = np.array([0], dtype='int32')

    if qvp.rays_are_indexed is not None:
        qvp.rays_are_indexed['data'] = np.array(
            [qvp.rays_are_indexed['data'][0]])
    if qvp.ray_angle_res is not None:
        qvp.ray_angle_res['data'] = np.array([qvp.ray_angle_res['data'][0]])

    if qvp_type in ('rqvp', 'evp', 'vp'):
        qvp.fixed_angle['data'] = np.array([90.], dtype='float64')

    # ray dependent radar objects parameters
    qvp.sweep_end_ray_index['data'] = np.array([-1], dtype='int32')
    qvp.rays_per_sweep['data'] = np.array([0], dtype='int32')
    qvp.azimuth['data'] = np.array([], dtype='float64')
    qvp.elevation['data'] = np.array([], dtype='float64')
    qvp.nrays = 0

    return qvp


def _update_qvp_metadata(qvp, ref_time, lon, lat, elev=90.):
    """
    updates a QVP object metadata with data from the current radar volume.

    Parameters
    ----------
    qvp : QVP object
        QVP object.
    ref_time : datetime object
        The current radar volume reference time.

    Returns
    -------
    qvp : QVP object
        The updated QVP object.

    """
    start_time = num2date(0, qvp.time['units'], qvp.time['calendar'])
    qvp.time['data'] = np.append(
        qvp.time['data'], (ref_time - start_time).total_seconds())
    qvp.sweep_end_ray_index['data'][0] += 1
    qvp.rays_per_sweep['data'][0] += 1
    qvp.nrays += 1

    qvp.azimuth['data'] = np.ones((qvp.nrays, ), dtype='float64')*0.
    qvp.elevation['data'] = (
        np.ones((qvp.nrays, ), dtype='float64')*elev)

    qvp.gate_longitude['data'] = (
        np.ones((qvp.nrays, qvp.ngates), dtype='float64')*lon)
    qvp.gate_latitude['data'] = (
        np.ones((qvp.nrays, qvp.ngates), dtype='float64')*lat)
    qvp.gate_altitude['data'] = np.broadcast_to(
        qvp.range['data'], (qvp.nrays, qvp.ngates))

    return qvp
