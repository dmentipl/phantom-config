'''test_data.in as a phantomconfig'''

import datetime

from phantomconfig.phantomconfig import ConfigVariable

test_datetime = datetime.datetime.strptime(
    '01/01/1999 12:00:00.0', '%d/%m/%Y %H:%M:%S.%f'
)

test_header = [
    'Runtime options file for Phantom, written 01/01/1999 12:00:00.0',
    'Options not present assume their default values',
    'This file is updated automatically after a full dump',
]

test_config = {
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
        datetime.timedelta(0),
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
    'h_soft_sinksink': ConfigVariable(
        'h_soft_sinksink',
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

test_dict = {
    '__header__': test_header,
    '__datetime__': test_datetime,
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
        datetime.timedelta(0),
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
    'h_soft_sinksink': [
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
