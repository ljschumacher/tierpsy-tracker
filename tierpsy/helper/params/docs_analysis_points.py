'''
Dictionary of the analysis points that will be executed for a given analysis_point.
If the point is not in the dictionary the points used will be the ones in DEFAULT.
'''
valid_analysis_points = ['WORM', 'SINGLE_WORM_SHAFER', 'PHARYNX', 'ZEBRAFISH', 'MANUAL']

dflt_analysis_points = {
    'DEFAULT':
    ['COMPRESS',
    'VID_SUBSAMPLE',
    'TRAJ_CREATE',
    'TRAJ_JOIN',
    'SKE_INIT',
    'BLOB_FEATS',
    'SKE_CREATE',
    'SKE_FILT',
    'SKE_ORIENT',
    'INT_PROFILE',
    'INT_SKE_ORIENT',
    'FEAT_CREATE'
    ],

    'SINGLE_WORM_SHAFER' : 
    ['COMPRESS',
    'COMPRESS_ADD_DATA',
    'VID_SUBSAMPLE',
    'TRAJ_CREATE',
    'TRAJ_JOIN',
    'SKE_INIT',
    'BLOB_FEATS',
    'SKE_CREATE',
    'SKE_FILT',
    'SKE_ORIENT',
    'STAGE_ALIGMENT',
    'CONTOUR_ORIENT', #orientation must occur before the intensity map calculation.
    'INT_PROFILE',
    'INT_SKE_ORIENT',
    'FEAT_CREATE',
    'WCON_EXPORT'
    ],

    'MANUAL':
    ['FEAT_MANUAL_CREATE']
}
