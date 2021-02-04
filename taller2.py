# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:42:19 2021

@author: Lenovo
"""

"""
Spyder Editor

This is a temporary script file.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import flopy

name = "ejercicio1"
h1 = 100
h2 = 90
Nlay = 10
N = 101
L = 400.0
H = 50.0
k = 1.0

sim = flopy.mf6.MFSimulation(
    sim_name=name, exe_name=
    "C:/Users/Lenovo/Desktop/Diapositivas PyS/DIPLOMADO/mf6.2.0/bin/mf6",
    version="mf6", sim_ws="workspace"
) 

#guarda mf6 en la carpeta especfica y guarada los archivos

tdis = flopy.mf6.ModflowTdis(
    sim, pname="tdis", time_units="DAYS", nper=1, perioddata=[(1.0, 1, 1.0)]
)

#Crea el TDISobjeto Flopy
ims = flopy.mf6.ModflowIms(sim, pname="ims", complexity="SIMPLE")

#Crea el IMSobjeto Flopy Package



model_nam_file = "{}.nam".format(name)
gwf = flopy.mf6.ModflowGwf(sim, modelname=name, model_nam_file=model_nam_file)

#Crear el objeto de modelo de flujo de agua subterránea Flopy (gwf)

#Crear el DISpaquete de discretización

bot = np.linspace(-H / Nlay, -H, Nlay)
delrow = delcol = L / (N - 1) #espesro de filas
dis = flopy.mf6.ModflowGwfdis(  #paquete de discretizacion
    gwf,
    nlay=Nlay,
    nrow=N,
    ncol=N,
    delr=delrow,
    delc=delcol,
    top=0.0,
    botm=bot,
)

#Crear el ICpaquete de condiciones iniciales ( )
start = h1 * np.ones((Nlay, N, N))
ic = flopy.mf6.ModflowGwfic(gwf, pname="ic", strt=start)

#Crear el NPFpaquete de flujo de propiedades de nodo


k=np.ones([10,N,N])
k[1,:,:]=5e-1

#river
riv_period = {}
riv_period_array = [((0,2,0),'river_stage_1',1001.0,35.9,None),
                    ((0,3,1),'river_stage_1',1002.0,35.8,None),
                    ((0,4,2),'river_stage_1',1003.0,35.7,None),
                    ((0,4,3),'river_stage_1',1004.0,35.6,None),
                    ((0,5,4),'river_stage_1',1005.0,35.5,None),
                    ((0,5,5),'river_stage_1',1006.0,35.4,'riv1_c6'),
                    ((0,5,6),'river_stage_1',1007.0,35.3,'riv1_c7'),
                    ((0,4,7),'river_stage_1',1008.0,35.2,None),
                    ((0,4,8),'river_stage_1',1009.0,35.1,None),
                    ((0,4,9),'river_stage_1',1010.0,35.0,None),
                    ((0,9,0),'river_stage_2',1001.0,36.9,'riv2_upper'),
                    ((0,8,1),'river_stage_2',1002.0,36.8,'riv2_upper'),
                    ((0,7,2),'river_stage_2',1003.0,36.7,'riv2_upper'),
                    ((0,6,3),'river_stage_2',1004.0,36.6,None),
                    ((0,6,4),'river_stage_2',1005.0,36.5,None),
                    ((0,5,5),'river_stage_2',1006.0,36.4,'riv2_c6'),
                    ((0,5,6),'river_stage_2',1007.0,36.3,'riv2_c7'),
                    ((0,6,7),'river_stage_2',1008.0,36.2,None),
                    ((0,6,8),'river_stage_2',1009.0,36.1),
                    ((0,6,9),'river_stage_2',1010.0,36.0)]
riv_period[0] = riv_period_array
riv = flopy.mf6.ModflowGwfriv(gwf, pname='riv', print_input=True, print_flows=True, 
                              save_flows='{}.cbc'.format("mymodel"),
                              boundnames=True, maxbound=20, 
                              stress_period_data=riv_period)
ts_recarray=[(0.0,40.0,41.0),(1.0,41.0,41.5),
             (2.0,43.0,42.0),(3.0,45.0,42.8),
             (4.0,44.0,43.0),(6.0,43.0,43.1),
             (9.0,42.0,42.4),(11.0,41.0,41.5),
             (31.0,40.0,41.0)]
riv.ts.initialize(filename='river_stages.ts', timeseries=ts_recarray,
                  time_series_namerecord=[('river_stage_1', 'river_stage_2')],
                  interpolation_methodrecord=[('linear', 'stepwise')])
obs_recarray = {'riv_obs.csv':[('rv1-3-1', 'RIV', (0,2,0)), ('rv1-4-2', 'RIV', (0,3,1)),
                               ('rv1-5-3', 'RIV', (0,4,2)), ('rv1-5-4', 'RIV', (0,4,3)),
                               ('rv1-6-5', 'RIV', (0,5,4)), ('rv1-c6', 'RIV', 'riv1_c6'),
                               ('rv1-c7', 'RIV', 'riv1_c7'), ('rv2-upper', 'RIV', 'riv2_upper'),
                               ('rv-2-7-4', 'RIV', (0,6,3)), ('rv2-8-5', 'RIV', (0,6,4)),
                               ('rv-2-9-6', 'RIV', (0,5,5,))],
                'riv_flowsA.csv':[('riv1-3-1', 'RIV', (0,2,0)), ('riv1-4-2', 'RIV', (0,3,1)),
                                  ('riv1-5-3', 'RIV', (0,4,2))],
                'riv_flowsB.csv':[('riv2-10-1', 'RIV', (0,9,0)), ('riv-2-9-2', 'RIV', (0,8,1)),
                                  ('riv2-8-3', 'RIV', (0,7,2))]}
riv.obs.initialize(filename='{}.riv.obs'.format("mymodel"), digits=10,
                   print_input=True, continuous=obs_recarray)



npf = flopy.mf6.ModflowGwfnpf(gwf, icelltype=1, k=k, save_flows=True)



#Crear el CHDpaquete de cabeza constante ( )

chd_rec = []
chd_rec.append(((0, int(N / 4), int(N / 4)), h2))
chd_rec.append(((1, int(3*N / 4), int(3*N / 4)), h2-3))
for layer in range(0, Nlay):
    for row_col in range(0, N):
        chd_rec.append(((layer, row_col, 0), h1))
        chd_rec.append(((layer, row_col, N - 1), h1))
        if row_col != 0 and row_col != N - 1:
            chd_rec.append(((layer, 0, row_col), h1))
            chd_rec.append(((layer, N - 1, row_col), h1))
chd = flopy.mf6.ModflowGwfchd(
    gwf,
    maxbound=len(chd_rec),
    stress_period_data=chd_rec,
    save_flows=True,
)

#l CHDpaquete almacenaba las cabezas constantes en una matriz estructurada, también llamada numpy.recarray. Podemos obtener un puntero al recarray para el primer período de estrés (iper = 0) de la siguiente manera.
iper = 0
ra = chd.stress_period_data.get_data(key=iper)
ra


# Create the output control (`OC`) Package
headfile = "{}.hds".format(name)
head_filerecord = [headfile]
budgetfile = "{}.cbb".format(name)
budget_filerecord = [budgetfile]
saverecord = [("HEAD", "ALL"), ("BUDGET", "ALL")]
printrecord = [("HEAD", "LAST")]
oc = flopy.mf6.ModflowGwfoc(
    gwf,
    saverecord=saverecord,
    head_filerecord=head_filerecord,
    budget_filerecord=budget_filerecord,
    printrecord=printrecord,
)

#Escribe los conjuntos de datos

sim.write_simulation()

#Ejecuta la simulación

success, buff = sim.run_simulation()
if not success:
    raise Exception("MODFLOW 6 did not terminate normally.")
    
#Trazar un mapa de la capa 1
headfile=  'Workspace' +'/'+headfile
hds = flopy.utils.binaryfile.HeadFile(headfile)
h = hds.get_data(kstpkper=(0, 0))
x = y = np.linspace(0, L, N)
y = y[::-1]
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1, 1, 1, aspect="equal")
c = ax.contour(x, y, h[0], np.arange(90, 100.1, 0.2), colors="red")
plt.clabel(c, fmt="%2.1f")


#Trazar un mapa de la capa 10

x = y = np.linspace(0, L, N)
y = y[::-1]
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1, 1, 1, aspect="equal")
c = ax.contour(x, y, h[-1], np.arange(90, 100.1, 0.2), colors="red")
plt.clabel(c, fmt="%1.1f")


z = np.linspace(-H / Nlay / 2, -H + H / Nlay / 2, Nlay)
fig = plt.figure(figsize=(5, 2.5))
ax = fig.add_subplot(1, 1, 1, aspect="auto")
c = ax.contour(x, z, h[:, 50, :], np.arange(90, 100.1, 0.2), colors="red")
plt.clabel(c, fmt="%1.1f")

import os
import flopy
ws = './mymodel'
name = 'mymodel'
sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=ws, exe_name='C:/Users/Lenovo/Desktop/Diapositivas PyS/DIPLOMADO/mf6.2.0/bin/mf6')
tdis = flopy.mf6.ModflowTdis(sim)
ims = flopy.mf6.ModflowIms(sim)
gwf = flopy.mf6.ModflowGwf(sim, modelname=name, save_flows=True)
dis = flopy.mf6.ModflowGwfdis(gwf, nrow=10, ncol=10)
ic = flopy.mf6.ModflowGwfic(gwf)
# River
riv_period = {}
riv_period_array = [((0,2,0),'river_stage_1',1001.0,35.9,None),
                    ((0,3,1),'river_stage_1',1002.0,35.8,None),
                    ((0,4,2),'river_stage_1',1003.0,35.7,None),
                    ((0,4,3),'river_stage_1',1004.0,35.6,None),
                    ((0,5,4),'river_stage_1',1005.0,35.5,None),
                    ((0,5,5),'river_stage_1',1006.0,35.4,'riv1_c6'),
                    ((0,5,6),'river_stage_1',1007.0,35.3,'riv1_c7'),
                    ((0,4,7),'river_stage_1',1008.0,35.2,None),
                    ((0,4,8),'river_stage_1',1009.0,35.1,None),
                    ((0,4,9),'river_stage_1',1010.0,35.0,None),
                    ((0,9,0),'river_stage_2',1001.0,36.9,'riv2_upper'),
                    ((0,8,1),'river_stage_2',1002.0,36.8,'riv2_upper'),
                    ((0,7,2),'river_stage_2',1003.0,36.7,'riv2_upper'),
                    ((0,6,3),'river_stage_2',1004.0,36.6,None),
                    ((0,6,4),'river_stage_2',1005.0,36.5,None),
                    ((0,5,5),'river_stage_2',1006.0,36.4,'riv2_c6'),
                    ((0,5,6),'river_stage_2',1007.0,36.3,'riv2_c7'),
                    ((0,6,7),'river_stage_2',1008.0,36.2,None),
                    ((0,6,8),'river_stage_2',1009.0,36.1),
                    ((0,6,9),'river_stage_2',1010.0,36.0)]
riv_period[0] = riv_period_array
riv = flopy.mf6.ModflowGwfriv(gwf, pname='riv', print_input=True, print_flows=True, 
                              save_flows='{}.cbc'.format("mymodel"),
                              boundnames=True, maxbound=20, 
                              stress_period_data=riv_period)
ts_recarray=[(0.0,40.0,41.0),(1.0,41.0,41.5),
             (2.0,43.0,42.0),(3.0,45.0,42.8),
             (4.0,44.0,43.0),(6.0,43.0,43.1),
             (9.0,42.0,42.4),(11.0,41.0,41.5),
             (31.0,40.0,41.0)]
riv.ts.initialize(filename='river_stages.ts', timeseries=ts_recarray,
                  time_series_namerecord=[('river_stage_1', 'river_stage_2')],
                  interpolation_methodrecord=[('linear', 'stepwise')])
obs_recarray = {'riv_obs.csv':[('rv1-3-1', 'RIV', (0,2,0)), ('rv1-4-2', 'RIV', (0,3,1)),
                               ('rv1-5-3', 'RIV', (0,4,2)), ('rv1-5-4', 'RIV', (0,4,3)),
                               ('rv1-6-5', 'RIV', (0,5,4)), ('rv1-c6', 'RIV', 'riv1_c6'),
                               ('rv1-c7', 'RIV', 'riv1_c7'), ('rv2-upper', 'RIV', 'riv2_upper'),
                               ('rv-2-7-4', 'RIV', (0,6,3)), ('rv2-8-5', 'RIV', (0,6,4)),
                               ('rv-2-9-6', 'RIV', (0,5,5,))],
                'riv_flowsA.csv':[('riv1-3-1', 'RIV', (0,2,0)), ('riv1-4-2', 'RIV', (0,3,1)),
                                  ('riv1-5-3', 'RIV', (0,4,2))],
                'riv_flowsB.csv':[('riv2-10-1', 'RIV', (0,9,0)), ('riv-2-9-2', 'RIV', (0,8,1)),
                                  ('riv2-8-3', 'RIV', (0,7,2))]}
riv.obs.initialize(filename='{}.riv.obs'.format("mymodel"), digits=10,
                   print_input=True, continuous=obs_recarray)



npf = flopy.mf6.ModflowGwfnpf(gwf, save_specific_discharge=True)
chd = flopy.mf6.ModflowGwfchd(gwf, stress_period_data=[[(0, 0, 0), 1.],
                                                       [(0, 9, 9), 0.]])



budget_file = name + '.bud'
head_file = name + '.hds'
oc = flopy.mf6.ModflowGwfoc(gwf,
                            budget_filerecord=budget_file,
                            head_filerecord=head_file,
                            saverecord=[('HEAD', 'ALL'), ('BUDGET', 'ALL')])
sim.write_simulation()
sim.run_simulation()
head = flopy.utils.HeadFile(os.path.join(ws, head_file)).get_data()
bud = flopy.utils.CellBudgetFile(os.path.join(ws, budget_file),
                                 precision='double')
spdis = bud.get_data(text='DATA-SPDIS')[0]
pmv = flopy.plot.PlotMapView(gwf)
pmv.plot_array(head)
pmv.plot_grid(colors='red')
pmv.contour_array(head, levels=[.2, .4, .6, .8], linewidths=3.)
pmv.plot_specific_discharge(spdis, color='white')

