from pylab import *

##set figure properties
aw = 1.5
fs = 16
lw = 2.0
font = {'size'   : fs}
matplotlib.rc('font', **font)
matplotlib.rc('axes' , lw=aw)

def set_fig_properties(ax_list):
    tl = 6
    tw = 1.5
    tlm = 3

    for ax in ax_list:
        ax.tick_params(which='major', length=tl, width=tw)
        ax.tick_params(which='minor', length=tlm, width=tw)
        ax.tick_params(which='both', axis='both', direction='out', right=False, top=False)

def plot_nep(pout):
    nep = np.loadtxt("./nep.txt", skiprows=6)
    figure(figsize=(16, 7))
    plt.subplot(1,2,1)
    plt.hist(np.log(np.abs(nep)), bins=50)
    plt.subplot(1,2,2)
    plt.scatter(range(len(nep)), nep, s=0.5)
    plt.gcf().set_size_inches(9,3)
    plt.savefig(pout, dpi=300)


def com_RMSE(fin):
    nclo = int(fin.shape[1]/2)
    pids = fin[:, nclo] > -1e5
    targe = fin[pids, :nclo].reshape(-1)
    predi = fin[pids, nclo:].reshape(-1)
    return np.sqrt(((predi - targe) ** 2).mean())


loss = loadtxt('loss.out')
print("Run %s."%(len(loss)*100), end=" ")
loss[:,0] = np.arange(1, len(loss) + 1)*100
energy_train = loadtxt('energy_train.out')
force_train = loadtxt('force_train.out')
virial_train = loadtxt('virial_train.out')
stress_train = loadtxt('stress_train.out')

error_energy_train = com_RMSE(energy_train)*1000
error_force_train = com_RMSE(force_train)*1000
error_virial_train = com_RMSE(virial_train)*1000
error_stress_train = com_RMSE(stress_train)*1000
print("{:.4f} {:.4f} {:.4f} {:.4f}".format(error_energy_train,error_force_train,error_virial_train,error_stress_train), end=' ')

test_flag = 1
if test_flag == 1:
    energy_test = loadtxt('energy_test.out')
    force_test = loadtxt('force_test.out')
    virial_test = loadtxt('virial_test.out')
    stress_test = loadtxt('stress_test.out')
    error_energy_test = com_RMSE(energy_test)*1000
    error_force_test = com_RMSE(force_test)*1000
    error_virial_test = com_RMSE(virial_test)*1000
    error_stress_test = com_RMSE(stress_test)*1000
    print("{:.4f} {:.4f} {:.4f} {:.4f}".format(error_energy_test,error_force_test,error_virial_test,error_stress_test), end=' ')
print()

figure(figsize=(20, 15))
subplot(2, 2, 1)
set_fig_properties([gca()])
loglog(loss[:, 0], loss[:, 1],  ls="-", lw=lw, c = "C1", label="Total")
loglog(loss[:, 0], loss[:, 2],  ls="-", lw=lw, c = "C4", label=r"$L_{1}$")
loglog(loss[:, 0], loss[:, 3],  ls="-", lw=lw, c = "C5", label=r"$L_{2}$")
loglog(loss[:, 0], loss[:, 4],  ls="-", lw=lw, c = "C0", label="Energy_train")
loglog(loss[:, 0], loss[:, 5],  ls="-", lw=lw, c = "C2", label="Force_train")
loglog(loss[:, 0], loss[:, 6],  ls="-", lw=lw, c = "C3", label="Virial_train")

if test_flag == 1:
    loglog(loss[:, 0], loss[:, 7],  ls="--", lw=lw, c = "C6", label="Energy_test")
    loglog(loss[:, 0], loss[:, 8],  ls="--", lw=lw, c = "C7", label="Force_test")
    loglog(loss[:, 0], loss[:, 9],  ls="--", lw=lw, c = "C8", label="Virial_test")

#xlim([1e2, 10e5])
#ylim([1e-3, 5e0])
xlabel('Generation')
ylabel('Loss')
legend(loc="lower left",
        ncol = 2,
        fontsize = 14,
        frameon = False,
        columnspacing = 0.2)

subplot(2, 2, 2)
set_fig_properties([gca()])
if test_flag == 1:
    ene_min = np.min([np.min(energy_train),np.min(energy_test)])
    ene_max = np.max([np.max(energy_train),np.max(energy_test)])
else:
    ene_min = np.min(energy_train)
    ene_max = np.max(energy_train)
ene_min -= (ene_max-ene_min)*0.1
ene_max += (ene_max-ene_min)*0.1
plot([ene_min, ene_max], [ene_min, ene_max], c = "grey", lw = 3)
plot(energy_train[:, 1], energy_train[:, 0], 'o', c="C0", ms = 5, label="Train dataset (RMSE={0:4.2f} mev/atom)".format(error_energy_train))
if test_flag == 1:
    plot(energy_test[:, 1], energy_test[:, 0], 'o', c="C6", ms = 2, label="Test dataset (RMSE={0:4.2f} mev/atom)".format(error_energy_test))
xlim([ene_min, ene_max])
ylim([ene_min, ene_max])
xlabel('DFT energy (eV/atom)')
ylabel('NEP energy (eV/atom)')
legend(loc="upper left")


subplot(2, 2, 3)
set_fig_properties([gca()])
if test_flag == 1:
    for_min = np.min([np.min(force_train),np.min(force_test)])
    for_max = np.max([np.max(force_train),np.max(force_test)])
else:
    for_min = np.min(force_train)
    for_max = np.max(force_train)
for_min -= (for_max-for_min)*0.1
for_max += (for_max-for_min)*0.1
plot([for_min, for_max], [for_min, for_max], c = "grey", lw = 3)
plot(force_train[:, 3], force_train[:, 0], 'o', c="C2", ms = 5, label="Train dataset (RMSE={0:4.2f} mev/atom)".format(error_force_train))
plot(force_train[:, 4:6], force_train[:, 1:3], 'o', c="C2", ms = 5)
if test_flag == 1:
    plot(force_test[:, 3], force_test[:, 0], 'o', c="C7", ms = 2, label="Test dataset (RMSE={0:4.2f} mev/atom)".format(error_force_test))
    plot(force_test[:, 4:6], force_test[:, 1:3], 'o', c="C7", ms = 2)
xlim([for_min, for_max])
ylim([for_min, for_max])
xlabel(r'DFT force (eV/$\rm{\AA}$)')
ylabel(r'NEP force (eV/$\rm{\AA}$)')
legend(loc="upper left")


# subplot(2, 2, 4)
# set_fig_properties([gca()])
# if test_flag == 1:
#     ptra = virial_train[:,-1] > -1e-5
#     ptes = virial_test[:,-1] > -1e-5
#     vir_min = np.min([np.min(virial_train[ptra, :]),np.min(virial_test[ptes, :])])
#     vir_max = np.max([np.max(virial_train[ptra, :]),np.max(virial_test[ptes, :])])
# else:
#     ptra = virial_train[:,-1] > -1e-5
#     vir_min = np.min(virial_train[ptra, :])
#     vir_max = np.max(virial_train[ptra, :])
# vir_min -= (vir_max-vir_min)*0.1
# vir_max += (vir_max-vir_min)*0.1
# #vir_min = -0.09
# #vir_max =  0.04
# plot([vir_min, vir_max], [vir_min, vir_max], c = "grey", lw = 1)
# if virial_train.shape[1] == 2:
#     plot(virial_train[ptra, 1], virial_train[ptra, 0], 'o', c="C3", ms = 5, label="Train dataset (RMSE={0:4.2f} mev/atom)".format(error_virial_train))
# elif virial_train.shape[1] == 12:
#     plot(virial_train[ptra, 6], virial_train[ptra, 0], 'o', c="C3", ms = 5, label="Train dataset (RMSE={0:4.2f} mev/atom)".format(error_virial_train))
#     plot(virial_train[ptra, 7:12], virial_train[ptra, 1:6], 'o', c="C3", ms = 5)
# if test_flag == 1:
#     if virial_test.shape[1] == 2:
#         plot(virial_test[ptes, 1], virial_test[ptes, 0], 'o', c="C3", ms = 2, label="Train dataset (RMSE={0:4.2f} mev/atom)".format(error_virial_test))
#     elif virial_test.shape[1] == 12:
#         plot(virial_test[ptes, 6], virial_test[ptes, 0], 'o', c="C8", ms = 2, label="Test dataset (RMSE={0:4.2f} mev/atom)".format(error_virial_test))
#         plot(virial_test[ptes, 7:12], virial_test[ptes, 1:6], 'o', c="C8", ms = 2)
# xlim([vir_min, vir_max])
# ylim([vir_min, vir_max])
# xlabel('DFT virial (eV/atom)')
# ylabel('NEP virial (eV/atom)')
# legend(loc="upper left")

subplot(2, 2, 4)
set_fig_properties([gca()])
if test_flag == 1:
    ptra = stress_train[:,-1] > -1e-5
    ptes = stress_test[:,-1] > -1e-5
    vir_min = np.min([np.min(stress_train[ptra, :]),np.min(stress_test[ptes, :])])
    vir_max = np.max([np.max(stress_train[ptra, :]),np.max(stress_test[ptes, :])])
else:
    ptra = stress_train[:,-1] > -1e-5
    vir_min = np.min(stress_train[ptra, :])
    vir_max = np.max(stress_train[ptra, :])
vir_min -= (vir_max-vir_min)*0.1
vir_max += (vir_max-vir_min)*0.1
#vir_min = -0.09
#vir_max =  0.04
plot([vir_min, vir_max], [vir_min, vir_max], c = "grey", lw = 1)
if stress_train.shape[1] == 2:
    plot(stress_train[ptra, 1], stress_train[ptra, 0], 'o', c="C3", ms = 5, label="Train dataset (RMSE={0:4.2f} MPa)".format(error_stress_train))
elif stress_train.shape[1] == 12:
    plot(stress_train[ptra, 6], stress_train[ptra, 0], 'o', c="C3", ms = 5, label="Train dataset (RMSE={0:4.2f} MPa)".format(error_stress_train))
    plot(stress_train[ptra, 7:12], stress_train[ptra, 1:6], 'o', c="C3", ms = 5)
if test_flag == 1:
    if stress_test.shape[1] == 2:
        plot(stress_test[ptes, 1], stress_test[ptes, 0], 'o', c="C3", ms = 2, label="Train dataset (RMSE={0:4.2f} MPa)".format(error_stress_test))
    elif stress_test.shape[1] == 12:
        plot(stress_test[ptes, 6], stress_test[ptes, 0], 'o', c="C8", ms = 2, label="Test dataset (RMSE={0:4.2f} MPa)".format(error_stress_test))
        plot(stress_test[ptes, 7:12], stress_test[ptes, 1:6], 'o', c="C8", ms = 2)
xlim([vir_min, vir_max])
ylim([vir_min, vir_max])
xlabel('DFT stress (GPa)')
ylabel('NEP stress (GPa)')
legend(loc="upper left")

subplots_adjust(wspace=0.35, hspace=0.3)
savefig("RMSE.png", bbox_inches='tight')
plt.close()

plot_nep("nep_txt.png")

