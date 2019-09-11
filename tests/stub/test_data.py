'''test_data.in as a phantomconfig'''

import datetime

from phantomconfig.phantomconfig import ConfigVariable

_datetime = datetime.datetime.strptime('01/01/1999 12:00:00.0', '%d/%m/%Y %H:%M:%S.%f')

header = [
    'Runtime options file for Phantom, written 01/01/1999 12:00:00.0',
    'Options not present assume their default values',
    'This file is updated automatically after a full dump',
]

config = {
    'logfile': ConfigVariable(
        'logfile', 'test01.log', 'file to which output is directed', 'job name'
    ),
    'dumpfile': ConfigVariable(
        'dumpfile', 'test_00000', 'dump file to start from', 'job name'
    ),
    'tmax': ConfigVariable(
        'tmax', 100.0, 'end time', 'options controlling run time and input/output'
    ),
    'dtmax': ConfigVariable(
        'dtmax',
        1.000,
        'time between dumps',
        'options controlling run time and input/output',
    ),
    'nmax': ConfigVariable(
        'nmax',
        -1,
        'maximum number of timesteps (0=just get derivs and stop)',
        'options controlling run time and input/output',
    ),
    'nout': ConfigVariable(
        'nout',
        -1,
        'number of steps between dumps (-ve=ignore)',
        'options controlling run time and input/output',
    ),
    'nmaxdumps': ConfigVariable(
        'nmaxdumps',
        -1,
        'stop after n full dumps (-ve=ignore)',
        'options controlling run time and input/output',
    ),
    'twallmax': ConfigVariable(
        'twallmax',
        datetime.timedelta(0),
        'maximum wall time (hhh:mm, 000:00=ignore)',
        'options controlling run time and input/output',
    ),
    'dtwallmax': ConfigVariable(
        'dtwallmax',
        datetime.timedelta(hours=10),
        'maximum wall time between dumps (hhh:mm, 000:00=ignore)',
        'options controlling run time and input/output',
    ),
    'nfulldump': ConfigVariable(
        'nfulldump',
        10,
        'full dump every n dumps',
        'options controlling run time and input/output',
    ),
    'iverbose': ConfigVariable(
        'iverbose',
        0,
        'verboseness of log (-1=quiet 0=default 1=allsteps 2=debug 5=max)',
        'options controlling run time and input/output',
    ),
    'C_cour': ConfigVariable(
        'C_cour', 0.300, 'Courant number', 'options controlling accuracy'
    ),
    'C_force': ConfigVariable(
        'C_force', 0.250, 'dt_force number', 'options controlling accuracy'
    ),
    'tolv': ConfigVariable(
        'tolv',
        1.000e-02,
        'tolerance on v iterations in timestepping',
        'options controlling accuracy',
    ),
    'hfact': ConfigVariable(
        'hfact',
        1.000,
        'h in units of particle spacing [h = hfact(m/rho)^(1/3)]',
        'options controlling accuracy',
    ),
    'tolh': ConfigVariable(
        'tolh',
        1.000e-04,
        'tolerance on h-rho iterations',
        'options controlling accuracy',
    ),
    'restartonshortest': ConfigVariable(
        'restartonshortest',
        False,
        'restart with all particles on shortest timestep',
        'options controlling accuracy',
    ),
    'alpha': ConfigVariable(
        'alpha',
        0.100,
        'art. viscosity parameter',
        'options controlling hydrodynamics, artificial dissipation',
    ),
    'beta': ConfigVariable(
        'beta',
        2.000,
        'beta viscosity',
        'options controlling hydrodynamics, artificial dissipation',
    ),
    'avdecayconst': ConfigVariable(
        'avdecayconst',
        0.100,
        'decay time constant for viscosity switches',
        'options controlling hydrodynamics, artificial dissipation',
    ),
    'damp': ConfigVariable(
        'damp',
        0.000,
        'artificial damping of velocities (if on, v=0 initially)',
        'options controlling hydrodynamics, artificial dissipation',
    ),
    'ieos': ConfigVariable(
        'ieos',
        3,
        'eqn of state (1=isoth;2=adiab;3=locally iso;8=barotropic)',
        'options controlling equation of state',
    ),
    'mu': ConfigVariable(
        'mu', 2.381, 'mean molecular weight', 'options controlling equation of state'
    ),
    'h_soft_sink': ConfigVariable(
        'h_soft_sink',
        0.000,
        'softening length between sink particles',
        'options controlling sink particles',
    ),
    'f_acc': ConfigVariable(
        'f_acc',
        0.800,
        'particles < f_acc*h_acc accreted without checks',
        'options controlling sink particles',
    ),
    'iexternalforce': ConfigVariable(
        'iexternalforce',
        0,
        '1=star,2=coro,3=bina,4=prdr,5=toru,6=toys,7=exte,8=spir,9=Lens,10=neut,11=Eins,',
        'options relating to external forces',
    ),
    'irealvisc': ConfigVariable(
        'irealvisc',
        0,
        'physical viscosity type (0=none,1=const,2=Shakura/Sunyaev)',
        'options controlling physical viscosity',
    ),
    'shearparam': ConfigVariable(
        'shearparam',
        0.100,
        'magnitude of shear viscosity (irealvisc=1) or alpha_SS (irealvisc=2)',
        'options controlling physical viscosity',
    ),
    'bulkvisc': ConfigVariable(
        'bulkvisc',
        0.000,
        'magnitude of bulk viscosity',
        'options controlling physical viscosity',
    ),
    'idrag': ConfigVariable(
        'idrag',
        1,
        'gas/dust drag (0=off,1=Epstein/Stokes,2=const K,3=const ts)',
        'options controlling dust',
    ),
    'grainsize': ConfigVariable(
        'grainsize', 0.100, 'Grain size in cm', 'options controlling dust'
    ),
    'graindens': ConfigVariable(
        'graindens',
        3.000,
        'Intrinsic grain density in g/cm^3',
        'options controlling dust',
    ),
    'K_code': ConfigVariable(
        'K_code',
        1.000,
        'drag constant when constant drag is used',
        'options controlling dust',
    ),
    'icut_backreaction': ConfigVariable(
        'icut_backreaction',
        0,
        'cut the drag on the gas phase (0=no, 1=yes)',
        'options controlling dust',
    ),
}

variables = [
    'logfile',
    'dumpfile',
    'tmax',
    'dtmax',
    'nmax',
    'nout',
    'nmaxdumps',
    'twallmax',
    'dtwallmax',
    'nfulldump',
    'iverbose',
    'C_cour',
    'C_force',
    'tolv',
    'hfact',
    'tolh',
    'restartonshortest',
    'alpha',
    'beta',
    'avdecayconst',
    'damp',
    'ieos',
    'mu',
    'h_soft_sink',
    'f_acc',
    'iexternalforce',
    'irealvisc',
    'shearparam',
    'bulkvisc',
    'idrag',
    'grainsize',
    'graindens',
    'K_code',
    'icut_backreaction',
]

values = [
    'test01.log',
    'test_00000',
    100.0,
    1.0,
    -1,
    -1,
    -1,
    datetime.timedelta(0),
    datetime.timedelta(hours=10),
    10,
    0,
    0.3,
    0.25,
    0.01,
    1.0,
    0.0001,
    False,
    0.1,
    2.0,
    0.1,
    0.0,
    3,
    2.381,
    0.0,
    0.8,
    0,
    0,
    0.1,
    0.0,
    1,
    0.1,
    3.0,
    1.0,
    0,
]

comments = [
    'file to which output is directed',
    'dump file to start from',
    'end time',
    'time between dumps',
    'maximum number of timesteps (0=just get derivs and stop)',
    'number of steps between dumps (-ve=ignore)',
    'stop after n full dumps (-ve=ignore)',
    'maximum wall time (hhh:mm, 000:00=ignore)',
    'maximum wall time between dumps (hhh:mm, 000:00=ignore)',
    'full dump every n dumps',
    'verboseness of log (-1=quiet 0=default 1=allsteps 2=debug 5=max)',
    'Courant number',
    'dt_force number',
    'tolerance on v iterations in timestepping',
    'h in units of particle spacing [h = hfact(m/rho)^(1/3)]',
    'tolerance on h-rho iterations',
    'restart with all particles on shortest timestep',
    'art. viscosity parameter',
    'beta viscosity',
    'decay time constant for viscosity switches',
    'artificial damping of velocities (if on, v=0 initially)',
    'eqn of state (1=isoth;2=adiab;3=locally iso;8=barotropic)',
    'mean molecular weight',
    'softening length between sink particles',
    'particles < f_acc*h_acc accreted without checks',
    '1=star,2=coro,3=bina,4=prdr,5=toru,6=toys,7=exte,8=spir,9=Lens,10=neut,11=Eins,',
    'physical viscosity type (0=none,1=const,2=Shakura/Sunyaev)',
    'magnitude of shear viscosity (irealvisc=1) or alpha_SS (irealvisc=2)',
    'magnitude of bulk viscosity',
    'gas/dust drag (0=off,1=Epstein/Stokes,2=const K,3=const ts)',
    'Grain size in cm',
    'Intrinsic grain density in g/cm^3',
    'drag constant when constant drag is used',
    'cut the drag on the gas phase (0=no, 1=yes)',
]

dict_flat = {
    '__header__': header,
    '__datetime__': _datetime,
    'logfile': ['test01.log', 'file to which output is directed', 'job name'],
    'dumpfile': ['test_00000', 'dump file to start from', 'job name'],
    'tmax': [100.0, 'end time', 'options controlling run time and input/output'],
    'dtmax': [
        1.000,
        'time between dumps',
        'options controlling run time and input/output',
    ],
    'nmax': [
        -1,
        'maximum number of timesteps (0=just get derivs and stop)',
        'options controlling run time and input/output',
    ],
    'nout': [
        -1,
        'number of steps between dumps (-ve=ignore)',
        'options controlling run time and input/output',
    ],
    'nmaxdumps': [
        -1,
        'stop after n full dumps (-ve=ignore)',
        'options controlling run time and input/output',
    ],
    'twallmax': [
        datetime.timedelta(0),
        'maximum wall time (hhh:mm, 000:00=ignore)',
        'options controlling run time and input/output',
    ],
    'dtwallmax': [
        datetime.timedelta(hours=10),
        'maximum wall time between dumps (hhh:mm, 000:00=ignore)',
        'options controlling run time and input/output',
    ],
    'nfulldump': [
        10,
        'full dump every n dumps',
        'options controlling run time and input/output',
    ],
    'iverbose': [
        0,
        'verboseness of log (-1=quiet 0=default 1=allsteps 2=debug 5=max)',
        'options controlling run time and input/output',
    ],
    'C_cour': [0.300, 'Courant number', 'options controlling accuracy'],
    'C_force': [0.250, 'dt_force number', 'options controlling accuracy'],
    'tolv': [
        1.000e-02,
        'tolerance on v iterations in timestepping',
        'options controlling accuracy',
    ],
    'hfact': [
        1.000,
        'h in units of particle spacing [h = hfact(m/rho)^(1/3)]',
        'options controlling accuracy',
    ],
    'tolh': [
        1.000e-04,
        'tolerance on h-rho iterations',
        'options controlling accuracy',
    ],
    'restartonshortest': [
        False,
        'restart with all particles on shortest timestep',
        'options controlling accuracy',
    ],
    'alpha': [
        0.100,
        'art. viscosity parameter',
        'options controlling hydrodynamics, artificial dissipation',
    ],
    'beta': [
        2.000,
        'beta viscosity',
        'options controlling hydrodynamics, artificial dissipation',
    ],
    'avdecayconst': [
        0.100,
        'decay time constant for viscosity switches',
        'options controlling hydrodynamics, artificial dissipation',
    ],
    'damp': [
        0.000,
        'artificial damping of velocities (if on, v=0 initially)',
        'options controlling hydrodynamics, artificial dissipation',
    ],
    'ieos': [
        3,
        'eqn of state (1=isoth;2=adiab;3=locally iso;8=barotropic)',
        'options controlling equation of state',
    ],
    'mu': [2.381, 'mean molecular weight', 'options controlling equation of state'],
    'h_soft_sink': [
        0.000,
        'softening length between sink particles',
        'options controlling sink particles',
    ],
    'f_acc': [
        0.800,
        'particles < f_acc*h_acc accreted without checks',
        'options controlling sink particles',
    ],
    'iexternalforce': [
        0,
        '1=star,2=coro,3=bina,4=prdr,5=toru,6=toys,7=exte,8=spir,9=Lens,10=neut,11=Eins,',
        'options relating to external forces',
    ],
    'irealvisc': [
        0,
        'physical viscosity type (0=none,1=const,2=Shakura/Sunyaev)',
        'options controlling physical viscosity',
    ],
    'shearparam': [
        0.100,
        'magnitude of shear viscosity (irealvisc=1) or alpha_SS (irealvisc=2)',
        'options controlling physical viscosity',
    ],
    'bulkvisc': [
        0.000,
        'magnitude of bulk viscosity',
        'options controlling physical viscosity',
    ],
    'idrag': [
        1,
        'gas/dust drag (0=off,1=Epstein/Stokes,2=const K,3=const ts)',
        'options controlling dust',
    ],
    'grainsize': [0.100, 'Grain size in cm', 'options controlling dust'],
    'graindens': [
        3.000,
        'Intrinsic grain density in g/cm^3',
        'options controlling dust',
    ],
    'K_code': [
        1.000,
        'drag constant when constant drag is used',
        'options controlling dust',
    ],
    'icut_backreaction': [
        0,
        'cut the drag on the gas phase (0=no, 1=yes)',
        'options controlling dust',
    ],
}

dict_nested = {
    '__header__': header,
    '__datetime__': _datetime,
    'job name': {
        'logfile': ('test01.log', 'file to which output is directed'),
        'dumpfile': ('test_00000', 'dump file to start from'),
    },
    'options controlling run time and input/output': {
        'tmax': (100.0, 'end time'),
        'dtmax': (1.000, 'time between dumps'),
        'nmax': (-1, 'maximum number of timesteps (0=just get derivs and stop)'),
        'nout': (-1, 'number of steps between dumps (-ve=ignore)'),
        'nmaxdumps': (-1, 'stop after n full dumps (-ve=ignore)'),
        'twallmax': (
            datetime.timedelta(0),
            'maximum wall time (hhh:mm, 000:00=ignore)',
        ),
        'dtwallmax': (
            datetime.timedelta(hours=10),
            'maximum wall time between dumps (hhh:mm, 000:00=ignore)',
        ),
        'nfulldump': (10, 'full dump every n dumps'),
        'iverbose': (
            0,
            'verboseness of log (-1=quiet 0=default 1=allsteps 2=debug 5=max)',
        ),
    },
    'options controlling accuracy': {
        'C_cour': (0.300, 'Courant number'),
        'C_force': (0.250, 'dt_force number'),
        'tolv': (1.000e-02, 'tolerance on v iterations in timestepping'),
        'hfact': (1.000, 'h in units of particle spacing [h = hfact(m/rho)^(1/3)]'),
        'tolh': (1.000e-04, 'tolerance on h-rho iterations'),
        'restartonshortest': (False, 'restart with all particles on shortest timestep'),
    },
    'options controlling hydrodynamics, artificial dissipation': {
        'alpha': (0.100, 'art. viscosity parameter'),
        'beta': (2.000, 'beta viscosity'),
        'avdecayconst': (0.100, 'decay time constant for viscosity switches'),
        'damp': (0.000, 'artificial damping of velocities (if on, v=0 initially)'),
    },
    'options controlling equation of state': {
        'ieos': (3, 'eqn of state (1=isoth;2=adiab;3=locally iso;8=barotropic)'),
        'mu': (2.381, 'mean molecular weight'),
    },
    'options controlling sink particles': {
        'h_soft_sink': (0.000, 'softening length between sink particles'),
        'f_acc': (0.800, 'particles < f_acc*h_acc accreted without checks'),
    },
    'options relating to external forces': {
        'iexternalforce': (
            0,
            '1=star,2=coro,3=bina,4=prdr,5=toru,6=toys,7=exte,8=spir,9=Lens,10=neut,11=Eins,',
        )
    },
    'options controlling physical viscosity': {
        'irealvisc': (0, 'physical viscosity type (0=none,1=const,2=Shakura/Sunyaev)'),
        'shearparam': (
            0.100,
            'magnitude of shear viscosity (irealvisc=1) or alpha_SS (irealvisc=2)',
        ),
        'bulkvisc': (0.000, 'magnitude of bulk viscosity'),
    },
    'options controlling dust': {
        'idrag': (1, 'gas/dust drag (0=off,1=Epstein/Stokes,2=const K,3=const ts)'),
        'grainsize': (0.100, 'Grain size in cm'),
        'graindens': (3.000, 'Intrinsic grain density in g/cm^3'),
        'K_code': (1.000, 'drag constant when constant drag is used'),
        'icut_backreaction': (0, 'cut the drag on the gas phase (0=no, 1=yes)'),
    },
}
