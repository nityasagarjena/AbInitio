&CONTROL
  calculation = 'cp',
  title = 'Si 64 atoms'
  restart_mode = 'restart',
  ndr = 51,
  ndw = 52,
  dt = 15,
  nstep  = 2000,
  iprint = 10,
  pseudo_dir = './',
  outdir = '$ESPRESSO_TMPDIR'
/

&SYSTEM
  ibrav = 1,
  celldm(1) = 20.52
  nat  = 64,
  ntyp = 1,
  ecutwfc = 6,
  ecutrho = 24,
  nr1b = 30, nr2b = 30, nr3b = 30
/

&ELECTRONS
  electron_dynamics = 'verlet'
  emass = 700.d0,
  emass_cutoff = 4.d0,
/

&IONS
  ion_dynamics = 'verlet',
  ion_temperature = 'nose',
  tempw = 500,
  fnosep = 13
/

ATOMIC_SPECIES
 Si 28.0855 Si.pbe-rrkj.UPF

ATOMIC_POSITIONS (bohr)
Si  -10.260000   -10.260000   -10.260000
Si  -7.695000    -7.695000    -7.695000
Si  -5.130000    -5.130000   -10.260000
Si  -2.565000    -2.565000    -7.695000
Si  -10.260000    -5.130000    -5.130000
Si  -7.695000    -2.565000    -2.565000
Si  -5.130000   -10.260000    -5.130000
Si  -2.565000    -7.695000    -2.565000
Si  -10.260000   -10.260000     0.000000
Si  -7.695000    -7.695000     2.565000
Si  -5.130000    -5.130000     0.000000
Si  -2.565000    -2.565000     2.565000
Si  -10.260000    -5.130000     5.130000
Si  -7.695000    -2.565000     7.695000
Si  -5.130000   -10.260000     5.130000
Si  -2.565000    -7.695000     7.695000
Si  -10.260000     0.000000   -10.260000
Si  -7.695000     2.565000    -7.695000
Si  -5.130000     5.130000   -10.260000
Si  -2.565000     7.695000    -7.695000
Si  -10.260000     5.130000    -5.130000
Si  -7.695000     7.695000    -2.565000
Si  -5.130000     0.000000    -5.130000
Si  -2.565000     2.565000    -2.565000
Si  -10.260000     0.000000     0.000000
Si  -7.695000     2.565000     2.565000
Si  -5.130000     5.130000     0.000000
Si  -2.565000     7.695000     2.565000
Si  -10.260000     5.130000     5.130000
Si  -7.695000     7.695000     7.695000
Si  -5.130000     0.000000     5.130000
Si  -2.565000     2.565000     7.695000
Si  0.000000   -10.260000   -10.260000
Si  2.565000    -7.695000    -7.695000
Si  5.130000    -5.130000   -10.260000
Si  7.695000    -2.565000    -7.695000
Si  0.000000    -5.130000    -5.130000
Si  2.565000    -2.565000    -2.565000
Si  5.130000   -10.260000    -5.130000
Si  7.695000    -7.695000    -2.565000
Si  0.000000   -10.260000     0.000000
Si  2.565000    -7.695000     2.565000
Si  5.130000    -5.130000     0.000000
Si  7.695000    -2.565000     2.565000
Si  0.000000    -5.130000     5.130000
Si  2.565000    -2.565000     7.695000
Si  5.130000   -10.260000     5.130000
Si  7.695000    -7.695000     7.695000
Si  0.000000     0.000000   -10.260000
Si  2.565000     2.565000    -7.695000
Si  5.130000     5.130000   -10.260000
Si  7.695000     7.695000    -7.695000
Si  0.000000     5.130000    -5.130000
Si  2.565000     7.695000    -2.565000
Si  5.130000     0.000000    -5.130000
Si  7.695000     2.565000    -2.565000
Si  0.000000     0.000000     0.000000
Si  2.565000     2.565000     2.565000
Si  5.130000     5.130000     0.000000
Si  7.695000     7.695000     2.565000
Si  0.000000     5.130000     5.130000
Si  2.565000     7.695000     7.695000
Si  5.130000     0.000000     5.130000
Si  7.695000     2.565000     7.695000

