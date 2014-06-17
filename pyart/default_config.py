"""
Configuration file for the Python ARM Radar Toolkit (Py-ART)

The values for a number of Py-ART parameters and the default metadata created
when reading files, correcting fields, etc. is controlled by this single
Python configuration file.

Py-ART's configuration can be modified by setting the environment variable
PYART_CONFIG to point to a configuration file with formatting similar to this
file.

The recommended method for changing these defaults is for users to copy this
file into their home directory, rename it to .pyart_config.py, make any
desired changes, and adjust their login scripts to set the PYART_CONFIG
environment variable to point to .pyart_config.py in their home directory.

Py-ART's configuration can also be modified within a script or shell session
using the load_config functions, such modification will last until the end of
the script/session or until a new configuration is loaded.

"""

##############################################################################
##############################################################################
# Simple configuration
#
# Adjust the values of the variable (right hand side of the equal sign) in
# this section for an easy method of customizing Py-ART.  Do not change the
# variable names (the left hand side of the equal sign). More advanced
# settings are based upon these variables.  Most users will find that
# adjusting this section is all that is needed.
##############################################################################
##############################################################################

# The default fill value for masked arrays and _FillValue keys
fill_value = -9999.0

# Field names used when reading in radar files and in the various correction
# and retrieval algorithms. The comments in this section provide additional
# information about the fields in that section.

# Radar reflectivity fields, DZ
reflectivity = 'reflectivity'
corrected_reflectivity = 'corrected_reflectivity'
total_power = 'total_power'

# Mean Doppler velocity fields, VEL
velocity = 'velocity'
corrected_velocity = 'corrected_velocity'

# Spectral width fields, SW
spectrum_width = 'spectrum_width'

# Differential reflectivity fields, ZDR
differential_reflectivity = 'differential_reflectivity'
corrected_differential_reflectivity = 'corrected_differential_reflectivity'

# Cross correlation ratio, correlation coefficient, RhoHV
cross_correlation_ratio = 'cross_correlation_ratio'

# Normalized coherent power, signal quality index, SQI, NCP
normalized_coherent_power = 'normalized_coherent_power'

# Differential phase shift, PhiDP
differential_phase = 'differential_phase'
unfolded_differential_phase = 'unfolded_differential_phase'
corrected_differential_phase = 'corrected_differential_phase'

# Specific differential phase shift, KDP
specific_differential_phase = 'specific_differential_phase'
corrected_specific_differential_phase = 'corrected_specific_differential_phase'

# Linear depolarization ration (h - horizontal, v - vertical), LDR
linear_depolarization_ratio = 'linear_polarization_ratio'
linear_depolarization_ratio_h = 'linear_polarization_ratio_h'
linear_depolarization_ratio_v = 'linear_polarization_ratio_v'

# Misc fields
signal_to_noise_ratio = 'signal_to_noise_ratio'
rain_rate = 'rain_rate'
radar_estimated_rain_rate = 'radar_estimated_rain_rate'
radar_echo_classification = 'radar_echo_classification'
specific_attenuation = 'specific_attenuation'

# Wind retrieval fields
eastward_wind_component = 'eastward_wind_component'
northward_wind_component = 'northward_wind_component'
vertical_wind_component = 'vertical_wind_component'

# End of Simple Configuration section

##############################################################################
##############################################################################
# Advanced Configuration
#
# Most users will not want to make any changes in this section.  For users
# who want a more fine-grained control over Py-ART's configuration this
# section provides access to these controls.  The layout of this section can
# be changed, the only requirement for a valid configuration file is that
# the ALL CAPITALIZED variable must must be present with the formatting
# present in this file.  These required variables are:
#
# FILL_VALUE, DEFAULT_METADATA, FILE_SPECIFIC_METADATA, FIELD_MAPPINGS,
# DEFAULT_FIELD_NAMES
#
# This section makes generous use of the variables in the Simple Configuration
# section, this is not required, but simplifies and enforces uniformity on
# the configuration.
##############################################################################
##############################################################################


##############################################################################
# Parameters
#
# Various parameters used in Py-ART.
##############################################################################

FILL_VALUE = fill_value     # the default fill value for masked arrays and
                            # the _FillValue key.

# The DEFAULT_FIELD_NAMES controls the field names which are used in the
# correction and retrieval algorithms in Py-ART. The keys of the dictionary
# are "internal" names which cannot change, the values are the field names
# which will be used in the algorithms by default. For best results use the
# names defined by the variables in simple configuration section which are
# also used in the DEFAULT_METADATA and FIELD_MAPPINGS variable. If you
# choose to change a field name the names should also be changed in the
# DEFAULT_METADATA and FIELD_MAPPINGS variable. This is not required but
# highly suggested.

DEFAULT_FIELD_NAMES = {
    # Internal field name (do not change): field name used (can change)
    'reflectivity': reflectivity,
    'corrected_reflectivity': corrected_reflectivity,
    'total_power': total_power,
    'velocity': velocity,
    'corrected_velocity': corrected_velocity,
    'spectrum_width': spectrum_width,
    'differential_reflectivity': differential_reflectivity,
    'corrected_differential_reflectivity':
    corrected_differential_reflectivity,
    'cross_correlation_ratio': cross_correlation_ratio,
    'normalized_coherent_power': normalized_coherent_power,
    'differential_phase': differential_phase,
    'unfolded_differential_phase': unfolded_differential_phase,
    'corrected_differential_phase': corrected_differential_phase,
    'specific_differential_phase': specific_differential_phase,
    'corrected_specific_differential_phase':
    corrected_specific_differential_phase,
    'linear_depolarization_ratio': linear_depolarization_ratio,
    'linear_depolarization_ratio_h': linear_depolarization_ratio_h,
    'linear_depolarization_ratio_v': linear_depolarization_ratio_v,
    'signal_to_noise_ratio': signal_to_noise_ratio,
    'rain_rate': rain_rate,
    'radar_estimated_rain_rate': radar_estimated_rain_rate,
    'radar_echo_classification': radar_echo_classification,
    'specific_attenuation': specific_attenuation,
    'eastward_wind_component': eastward_wind_component,
    'northward_wind_component': northward_wind_component,
    'vertical_wind_component': vertical_wind_component,
}


##############################################################################
# Default metadata
#
# The DEFAULT_METADATA dictionary contains dictionaries which provide the
# default radar attribute and field metadata. When reading in a file with
# Py-ART the FILE_SPECIFIC_METADATA variable is first queued for a metadata
# dictionary, if it is not found then the metadata in DEFAULT_METADATA is
# utilized.
##############################################################################

DEFAULT_METADATA = {

    # Metadata for radar attributes. These closely follow the CF/Radial
    # standard
    'azimuth': {
        'units': 'degrees',
        'standard_name': 'beam_azimuth_angle',
        'long_name': 'azimuth_angle_from_true_north',
        'axis': 'radial_azimuth_coordinate',
        'comment': 'Azimuth of antenna relative to true north'},

    'elevation': {
        'units': 'degrees',
        'standard_name': 'beam_elevation_angle',
        'long_name': 'elevation_angle_from_horizontal_plane',
        'axis': 'radial_elevation_coordinate',
        'comment': 'Elevation of antenna relative to the horizontal plane'},

    'range': {
        'units': 'meters',
        'standard_name': 'projection_range_coordinate',
        'long_name': 'range_to_measurement_volume',
        'axis': 'radial_range_coordinate',
        'spacing_is_constant': 'true',
        'comment': (
            'Coordinate variable for range. Range to center of each bin.')},

    'time': {
        'units': 'seconds',
        'standard_name': 'time',
        'long_name': 'time_in_seconds_since_volume_start',
        'calendar': 'gregorian',
        'comment': ('Coordinate variable for time. '
                    'Time at the center of each ray, in fractional seconds '
                    'since the global variable time_coverage_start')},

    'sweep_mode': {
        'units': 'unitless',
        'standard_name': 'sweep_mode',
        'long_name': 'Sweep mode',
        'comment': ('Options are: "sector", "coplane", "rhi", '
                    '"vertical_pointing", "idle", "azimuth_surveillance", '
                    '"elevation_surveillance", "sunscan", "pointing", '
                    '"manual_ppi", "manual_rhi"')},

    'sweep_number': {
        'units': 'count',
        'standard_name': 'sweep_number',
        'long_name': 'Sweep number'},

    'metadata': {
        'Conventions': 'CF/Radial instrument_parameters',
        'version': '1.3',
        'title': '',
        'institution': '',
        'references': '',
        'source': '',
        'history': '',
        'comment': '',
        'instrument_name': ''},

    # Metadata for radar sweep information dictionaries
    'sweep_start_ray_index': {
        'long_name': 'Index of first ray in sweep, 0-based',
        'units': 'count'},

    'sweep_end_ray_index': {
        'long_name': 'Index of last ray in sweep, 0-based',
        'units': 'count'},

    'fixed_angle': {
        'long_name': 'Target angle for sweep',
        'units': 'degrees',
        'standard_name': 'target_fixed_angle'},

    # Metadata for radar location attributes
    'latitude': {
        'long_name': 'Latitude',
        'standard_name': 'Latitude',
        'units': 'degrees_north'},

    'longitude': {
        'long_name': 'Longitude',
        'standard_name': 'Longitude',
        'units': 'degrees_east'},

    'altitude': {
        'long_name': 'Altitude',
        'standard_name': 'Altitude',
        'units': 'meters',
        'positive': 'up'},

    # Metadata for instrument_parameter dictionary
    'prt_mode': {
        'comments': ('Pulsing mode Options are: "fixed", "staggered", '
                     '"dual". Assumed "fixed" if missing.'),
        'meta_group': 'instrument_parameters',
        'long_name': 'Pulsing mode',
        'units': 'unitless'},

    'nyquist_velocity': {
        'units': 'meters_per_second',
        'comments': "Unambiguous velocity",
        'meta_group': 'instrument_parameters',
        'long_name': 'Nyquist velocity'},

    'prt': {
        'units': 'seconds',
        'comments': ("Pulse repetition time. For staggered prt, "
                     "also see prt_ratio."),
        'meta_group': 'instrument_parameters',
        'long_name': 'Pulse repetition time'},

    'unambiguous_range': {
        'units': 'meters',
        'comments': 'Unambiguous range',
        'meta_group': 'instrument_parameters',
        'long_name': 'Unambiguous range'},

    # Metadata for radar_parameter sub-convention
    'radar_beam_width_h': {
        'units': 'degrees',
        'meta_group': 'radar_parameters',
        'long_name': 'Antenna beam width H polarization'},

    'radar_beam_width_v': {
        'units': 'degrees',
        'meta_group': 'radar_parameters',
        'long_name': 'Antenna beam width V polarization'},

    # Reflectivity fields
    reflectivity: {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Reflectivity',
        'coordinates': 'elevation azimuth range'},

    corrected_reflectivity: {
        'units': 'dBZ',
        'standard_name': 'corrected_equivalent_reflectivity_factor',
        'long_name': 'Corrected reflectivity',
        'coordinates': 'elevation azimuth range'},

    total_power: {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Total power',
        'coordinates': 'elevation azimuth range'},

    # Velocity fields
    velocity: {
        'units': 'meters_per_second',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'long_name': 'Mean dopper velocity',
        'coordinates': 'elevation azimuth range'},

    corrected_velocity: {
        'units': 'meters_per_second',
        'standard_name': (
            'corrected_radial_velocity_of_scatterers_away_from_instrument'),
        'long_name': 'Corrected mean doppler velocity',
        'coordinates': 'elevation azimuth range'},

    # Spectrum width fields
    spectrum_width: {
        'units': 'meters_per_second',
        'standard_name': 'doppler_spectrum_width',
        'long_name': 'Doppler spectrum width',
        'coordinates': 'elevation azimuth range'},

    # Dual-polarization fields
    differential_reflectivity: {
        'units': 'dB',
        'standard_name': 'log_differential_reflectivity_hv',
        'long_name': 'Differential reflectivity',
        'coordinates': 'elevation azimuth range'},

    corrected_differential_reflectivity: {
        'units': 'dB',
        'standard_name': 'corrected_log_differential_reflectivity_hv',
        'long_name': 'Corrected differential reflectivity',
        'coordinates': 'elevation azimuth range'},

    cross_correlation_ratio: {
        'units': 'ratio',
        'standard_name': 'cross_correlation_ratio_hv',
        'long_name': 'Cross correlation ratio (RHOHV)',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    normalized_coherent_power: {
        'units': 'ratio',
        'standard_name': 'normalized_coherent_power',
        'long_name': 'Normalized coherent power',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'comment': 'Also know as signal quality index (SQI)',
        'coordinates': 'elevation azimuth range'},

    differential_phase: {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'Differential phase (PhiDP)',
        'valid_max': 180.0,
        'valid_min': -180.0,
        'coordinates': 'elevation azimuth range'},

    unfolded_differential_phase: {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'Unfolded differential phase',
        'coordinates': 'elevation azimuth range'},

    corrected_differential_phase: {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'Corrected differential phase',
        'coordinates': 'elevation azimuth range'},

    specific_differential_phase: {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'Specific differential phase (KDP)',
        'coordinates': 'elevation azimuth range'},

    corrected_specific_differential_phase: {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'Corrected specific differential phase (KDP)',
        'coordinates': 'elevation azimuth range'},


    # Depolarization ratio fields
    linear_depolarization_ratio: {
        'units': 'dB',
        'standard_name': 'log_linear_depolarization_ratio_hv',
        'long_name': 'Linear depolarization ratio',
        'coordinates': 'elevation azimuth range'},

    linear_depolarization_ratio_h: {
        'units': 'dB',
        'standard_name': 'log_linear_depolarization_ratio_h',
        'long_name': 'Linear depolarization ratio horizontal',
        'coordinates': 'elevation azimuth range'},

    linear_depolarization_ratio_v: {
        'units': 'dB',
        'standard_name': 'log_linear_depolarization_ratio_v',
        'long_name': 'Linear depolarization ratio vertical',
        'coordinates': 'elevation azimuth range'},

    # Misc fields
    signal_to_noise_ratio: {
        'units': 'dB',
        'standard_name': 'signal_to_noise_ratio',
        'long_name': 'Signal to noise ratio',
        'coordinates': 'elevation azimuth range'},

    rain_rate: {
        'units': 'kg/m2/s',
        'standard_name': 'rain_rate',
        'long_name': 'Rain rate',
        'coordinates': 'elevation azimuth range'},

    radar_estimated_rain_rate: {
        'units': 'mm/hr',
        'standard_name': 'radar_estimated_rain_rate',
        'long_name': 'Radar estimated rain rate',
        'coordinates': 'elevation azimuth range'},

    radar_echo_classification: {
        'units': 'legend',
        'standard_name': 'radar_echo_classification',
        'long_name': 'Radar Echo classification',
        'coordinates': 'elevation azimuth range'},

    specific_attenuation: {
        'units': 'dB/km',
        'standard_name': 'specific_attenuation',
        'long_name': 'Specific attenuation',
        'valid_min': 0.0,
        'valid_max': 1.0,
        'coordinates': 'elevation azimuth range'},

    # Wind retrieval fields
    eastward_wind_component: {
        'units': 'meters_per_second',
        'standard_name': 'eastward_wind_component',
        'long_name': 'Eastward wind component'},

    northward_wind_component: {
        'units': 'meters_per_second',
        'standard_name': 'northward_wind_component',
        'long_name': 'Northward wind component'},

    vertical_wind_component: {
        'units': 'meters_per_second',
        'standard_name': 'vertical_wind_component',
        'long_name': 'Vertical wind component'},
}


##############################################################################
# File specific metadata
#
# These dictionaries define metadata that is to be used only when reading in
# a given type of file.  This metadata is used in place of the
# DEFAULT_METADATA when it is avialable.  The main use of these variable
# is to define field specific data, it is safe to leave some/all of these
# empty if the default metadata is acceptable.
##############################################################################

# Metadata for Sigmet/IRIS files
sigmet_metadata = {}

# Metadata for NEXRAD Level II files (Archive and CDM files)
nexrad_metadata = {
    reflectivity: {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Reflectivity',
        'valid_max': 94.5,
        'valid_min': -32.0,
        'coordinates': 'elevation azimuth range'},

    velocity: {
        'units': 'meters_per_second',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'long_name': 'Mean doppler Velocity',
        'valid_max': 95.0,
        'valid_min': -95.0,
        'coordinates': 'elevation azimuth range'},

    spectrum_width: {
        'units': 'meters_per_second',
        'standard_name': 'doppler_spectrum_width',
        'long_name': 'Spectrum Width',
        'valid_max': 63.0,
        'valid_min': -63.5,
        'coordinates': 'elevation azimuth range'},

    differential_reflectivity: {
        'units': 'dB',
        'standard_name': 'log_differential_reflectivity_hv',
        'long_name': 'log_differential_reflectivity_hv',
        'valid_max': 7.9375,
        'valid_min': -7.8750,
        'coordinates': 'elevation azimuth range'},

    differential_phase: {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'differential_phase_hv',
        'valid_max': 360.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    cross_correlation_ratio: {
        'units': 'ratio',
        'standard_name': 'cross_correlation_ratio_hv',
        'long_name': 'Cross correlation_ratio (RHOHV)',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},
}

# Metadata for CF/Radial files
cfradial_metadata = {}

# Metadata for MDV files
mdv_metadata = {}

# Metadata for RSL files
rsl_metadata = {}

# Metadata for CSU-CHILL, CHL files
chl_metadata = {
    'DBZ': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'equivalent_reflectivity_factor'},

    'VEL': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument'},

    'WIDTH': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'doppler_spectrum_width'},

    'ZDR': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'log_differential_reflectivity_hv'},

    'LDRH': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'log_linear_depolarization_ratio_h'},

    'LDRV': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'log_linear_depolarization_ratio_v'},

    'PHIDP': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'differential_phase_hv'},

    'KDP': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'specific_differential_phase_hv'},

    'RHOHV': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'cross_correlation_ratio_hv'},

    'NCP': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'normalized_coherent_power'},

    'H Re(lag 1)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'real_part_of_lag_1_correlation_h'},

    'V Re(lag 2)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'real_part_of_lag_2_correlation_v'},

    'VAvgQ': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'v_average_quadrature'},

    'V Im(lag 1)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'imaginary_part_of_v_at_lag_1'},

    'HAvgQ': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'h_average_quadrature'},

    'H Im(lag 2)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'imaginary_part_lag_2_correlation_h'},

    'V lag 0': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'absolute_value_of_lag_0_correlation_v'},

    'H lag 0': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'absolute_value_of_lag_0_correlation_h'},

    'H lag 0 cx': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'absolute_value_of_lag_0_cross_correlation_h'},

    'H Im(lag 1)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'imaginary_part_of_lag_1_correlation_h'},

    'H Re(lag 2)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'real_part_of_lag_2_correlation_h'},

    'V lag 0 cx': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'absolute_value_of_lag_0_cross_correlation_v'},

    'V Re(lag 1)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'real_part_of_lag_1_correlation_v'},

    'V Im(lag 2)': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'imaginary_part_of_lag_2_correlation_v'},

    'HV lag 0 I': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'real_part_of_cross_channel_correlation_at_lag_0'},

    'HV lag 0 Q': {
        'coordinates': 'elevation azimuth range',
        'standard_name':
        'imaginary_part_of_cross_channel_correlation_at_lag_0'},

    'VAvgI': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'v_average_inphase'},

    'HAvgI': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'h_average_inphase'},

    'RHOHCX': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'lag_0_h_co_to_cross_correlation'},

    'RHOVCX': {
        'coordinates': 'elevation azimuth range',
        'standard_name': 'lag_0_v_co_to_cross_correlation'},
}

FILE_SPECIFIC_METADATA = {      # Required
    'sigmet': sigmet_metadata,
    'nexrad_archive': nexrad_metadata,
    'nexrad_cdm': nexrad_metadata,
    'cfradial': cfradial_metadata,
    'mdv': mdv_metadata,
    'rsl': rsl_metadata,
    'chl': chl_metadata,
}

##############################################################################
# Field name mapping
#
# These dictionaries map file field names or data types to a radar field
# name.  These are used to populate the radar.fields dictionary during a read
# in Py-ART.  A value of None will not include that field in the radar object.
# These can be over-ridden on a per-read basis using the field_mapping
# parameter, or using setting the file_field_names parameter to True.
##############################################################################

# Sigmet/IRIS file field mapping
# Note that multiple sigmet fields map to the same radar field, if
# more than one of these fields are present the radar field will be
# overwritten with the last sigmet field.
sigmet_field_mapping = {
    # Sigmet data type :field name              # (Data_type) Description
    'XHDR': None,                               # (0) Extended Header
    'DBT': total_power,                         # (1) Total Power
    'DBZ': reflectivity,                        # (2) Reflectivity
    'VEL': velocity,                            # (3) Velocity
    'WIDTH': spectrum_width,                    # (4) Width
    'ZDR': differential_reflectivity,           # (5) Diff. reflectivity
    'DBZC': corrected_reflectivity,             # (7) Corrected reflectivity
    'DBT2': total_power,                        # (8) Total Power
    'DBZ2': reflectivity,                       # (9) Reflectivity
    'VEL2': velocity,                           # (10) Velocity
    'WIDTH2': spectrum_width,                   # (11) Width
    'ZDR2': differential_reflectivity,          # (12) Diff. reflectivity
    'RAINRATE2': radar_estimated_rain_rate,     # (13) Rainfall rate
    'KDP': specific_differential_phase,         # (14) KDP (diff. phase)
    'KDP2': specific_differential_phase,        # (15) KDP (diff. phase)
    'PHIDP': differential_phase,                # (16) PhiDP (diff. phase)
    'VELC': corrected_velocity,                 # (17) Corrected velocity
    'SQI': normalized_coherent_power,           # (18) SQI
    'RHOHV': cross_correlation_ratio,           # (19) RhoHV
    'RHOHV2': cross_correlation_ratio,          # (20) RhoHV
    'DBZC2': corrected_reflectivity,            # (21) Corrected Reflec.
    'VELC2': corrected_velocity,                # (21) Corrected Velocity
    'SQI2': normalized_coherent_power,          # (23) SQI
    'PHIDP2': differential_phase,               # (24) PhiDP (diff. phase)
    'LDRH': linear_depolarization_ratio_h,      # (25) LDR xmt H, rcv V
    'LDRH2': linear_depolarization_ratio_h,     # (26) LDR xmt H, rcv V
    'LDRV': linear_depolarization_ratio_v,      # (27) LDR xmt V, rcv H
    'LDRV2': linear_depolarization_ratio_v,     # (28) LDR xmt V, rcv H
    'HEIGHT': None,                             # (32) Height (1/10 km)
    'VIL2': None,                               # (33) Linear Liquid
    'RAW': None,                                # (34) Raw Data
    'SHEAR': None,                              # (35) Wind Shear
    'DIVERGE2': None,                           # (36) Divergence
    'FLIQUID2': None,                           # (37) Floated liquid
    'USER': None,                               # (38) User type
    'OTHER': None,                              # (39) Unspecified
    'DEFORM2': None,                            # (40) Deformation
    'VVEL2': None,                              # (41) Vertical velocity
    'HVEL2': None,                              # (42) Horizontal velocity
    'HDIR2': None,                              # (43) Horiz. wind direction
    'AXDIL2': None,                             # (44) Axis of dilation
    'TIME2': None,                              # (45) Time in seconds
    'RHOH': None,                               # (46) Rho, xmt H, rcv V
    'RHOH2': None,                              # (47) Rho, xmt H, rcv V
    'RHOV': None,                               # (48) Rho, xmt V, rcv H
    'RHOV2': None,                              # (49) Rho, xmt V, rcv H
    'PHIH': None,                               # (50) Phi, xmt H, rcv V
    'PHIH2': None,                              # (51) Phi, xmt H, rcv V
    'PHIV': None,                               # (52) Phi, xmt V, rcv H
    'PHIV2': None,                              # (53) Phi, xmt V, rcv H
    'USER2': None,                              # (54) User type
    'HCLASS': radar_echo_classification,        # (55) Hydrometeor class
    'HCLASS2': radar_echo_classification,       # (56) Hydrometeor class
    'ZDRC': corrected_differential_reflectivity,
                                                # (57) Corrected diff. refl.
    'ZDRC2': corrected_differential_reflectivity,
                                                # (58) Corrected diff. refl.
    'UNKNOWN_59': None,                         # Unknown field
    'UNKNOWN_60': None,                         # Unknown field
    'UNKNOWN_61': None,                         # Unknown field
    'UNKNOWN_62': None,                         # Unknown field
    'UNKNOWN_63': None,                         # Unknown field
    'UNKNOWN_64': None,                         # Unknown field
    'UNKNOWN_65': None,                         # Unknown field
    'UNKNOWN_66': None,                         # Unknown field
    # there may be more field, add as needed
}


# NEXRAD Level II Archive files
nexrad_archive_field_mapping = {
    # NEXRAD field: radar field name
    'REF': reflectivity,
    'VEL': velocity,
    'SW': spectrum_width,
    'ZDR': differential_reflectivity,
    'PHI': differential_phase,
    'RHO': cross_correlation_ratio
}

# NEXRAD Level II CDM files
nexrad_cdm_field_mapping = {
    # CDM variable name (without _HI): radar field name
    'Reflectivity': reflectivity,
    'RadialVelocity': velocity,
    'SpectrumWidth': spectrum_width,
    'DifferentialReflectivity': differential_reflectivity,
    'DifferentialPhase': differential_phase,
    'CorrelationCoefficient': cross_correlation_ratio
}

# MDV files
mdv_field_mapping = {
    # MDV moment: radar field name
    'DBZ_F': reflectivity,
    'VEL_F': velocity,
    'WIDTH_F': spectrum_width,
    'ZDR_F': differential_reflectivity,
    'RHOHV_F': cross_correlation_ratio,
    'NCP_F': normalized_coherent_power,
    'KDP_F': specific_differential_phase,
    'PHIDP_F': differential_phase,
    'VEL_COR': corrected_velocity,
    'PHIDP_UNF': unfolded_differential_phase,
    'KDP_SOB': corrected_specific_differential_phase,
    'DBZ_AC': corrected_reflectivity, }

# CF/Radial files
cfradial_field_mapping = {}

# RSL files
# Note that multiple RSL field map to the same radar field, if
# more than one of these fields are present in the RSL data structure
# the radar field will be overwritten with the last field.
rsl_field_mapping = {
    # RSL 2 letter field: radar field           # RSL description
    'DZ': reflectivity,                         # reflectivity
    'VR': velocity,                             # velocity
    'SW': spectrum_width,                       # spectrum width
    'CZ': corrected_reflectivity,               # corrected reflectivity
    'ZT': reflectivity,                         # uncorrected reflectivity
    'DR': differential_reflectivity,            # differential reflectivity
    'LR': differential_reflectivity,            # another diff. reflectivity
    'ZD': differential_reflectivity,            # another diff. reflectivity
    'DM': None,                                 # received power
    'RH': cross_correlation_ratio,              # RhoHV
    'PH': differential_phase,                   # PhiDP
    'XZ': None,                                 # X-band reflectivity
    'CD': corrected_differential_reflectivity,  # Corrected DR.
    'MZ': None,                                 # DZ mask
    'MD': None,                                 # DR Mask
    'ZE': corrected_reflectivity,               # edited reflectivity
    'VE': corrected_velocity,                   # edited velocity
    'KD': specific_differential_phase,          # specific diff. phase
    'TI': None,                                 # TIME (unknown)
    'DX': None,                                 # ???
    'CH': None,                                 # ???
    'AH': None,                                 # ???
    'CV': None,                                 # ???
    'AV': None,                                 # ???
    'SQ': normalized_coherent_power,            # Signal Quality Index (sigmet)
    'VS': None,                                 # Radial Vel. combined
    'VL': None,                                 # Radial Vel. combined
    'VG': None,                                 # Radial Vel. combined
    'VT': None,                                 # Radial Vel. combined
    'NP': normalized_coherent_power,            # Normalized Coherent Power
    'HC': radar_echo_classification,            # Hydroclass
    'VC': None,                                 # Radial Vel. Corrected.
    'V2': None,                                 # Radial Vel cut 2
    'S2': None,                                 # Spectrum width cut 2
    'V3': None,                                 # Radial Vel cut 3
    'S3': None,                                 # Spectrum width cut 3
}

chl_field_mapping = {
    # Chill field name : radar field name
    'Z': 'DBZ',
    'V': 'VEL',
    'W': 'WIDTH',
    'ZDR': 'ZDR',
    'LDRH': 'LDRH',
    'LDRV': 'LDRV',
    '\xce\xa8 DP': 'PHIDP',
    'KDP': 'KDP',
    '\xcf\x81 HV': 'RHOHV',
    'NCP': 'NCP',
    'H Re(lag 1)': 'H Re(lag 1)',
    'V Re(lag 2)': 'V Re(lag 2)',
    'VAvgQ': 'VAvgQ',
    'V Im(lag 1)': 'V Im(lag 1)',
    'HAvgQ': 'HAvgQ',
    'H Im(lag 2)': 'H Im(lag 2)',
    'V lag 0': 'V lag 0',
    'H lag 0': 'H lag 0',
    'H lag 0 cx': 'H lag 0 cx',
    'H Im(lag 1)': 'H Im(lag 1)',
    'H Re(lag 2)': 'H Re(lag 2)',
    'V lag 0 cx': 'V lag 0 cx',
    'V Re(lag 1)': 'V Re(lag 1)',
    'V Im(lag 2)': 'V Im(lag 2)',
    'HV lag 0 I': 'HV lag 0 I',
    'HV lag 0 Q': 'HV lag 0 Q',
    'VAvgI': 'VAvgI',
    'HAvgI': 'HAvgI',
    '\xcf\x81 HCX': 'RHOHCX',
    '\xcf\x81 VCX': 'RHOVCX',
}

FIELD_MAPPINGS = {                  # Required variable
    'sigmet': sigmet_field_mapping,
    'nexrad_archive': nexrad_archive_field_mapping,
    'nexrad_cdm': nexrad_cdm_field_mapping,
    'cfradial': cfradial_field_mapping,
    'mdv': mdv_field_mapping,
    'rsl': rsl_field_mapping,
    'chl': chl_field_mapping,
}
