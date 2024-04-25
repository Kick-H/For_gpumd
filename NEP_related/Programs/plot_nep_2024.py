import numpy as np
from pylab import *
import sys


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
    subplot(1,2,1)
    hist(np.log(np.abs(nep)), bins=50)
    subplot(1,2,2)
    scatter(range(len(nep)), nep, s=0.5)
    gcf().set_size_inches(9,3)
    savefig(pout, dpi=300)


def plot_loss(loss, test=True):
    loss_title = "gen total l1 l2 e_train f_train v_train e_test f_test v_test".split(' ')
    loss[:,0] = np.arange(1, len(loss)+1)
    for i in range(1, 7):
        loglog(loss[:, 0], loss[:, i], ls="-", lw=lw, label=loss_title[i])
    if test:
        for i in range(7, 10):
            loglog(loss[:, 0], loss[:, i], ls="-", lw=lw, label=loss_title[i])
    xlabel('Generation/100')
    ylabel('Loss')
    legend(loc="lower left", ncol=2, fontsize=14, frameon=False, columnspacing=0.2)
    # tight_layout()


def find_units(name):
    if name == "force": return ['eV/A/atom', 'meV/A/atom', 4]
    elif name == "energy": return ['eV/atom', 'meV/atom', 3]
    elif name == "virial": return ['eV/atom', 'meV/atom', 5]
    elif name == "stress": return ['GPa', 'MPa', 5]


def plot_nep_dft(data, title):
    # title = [name, type, units]
    # example: title = ['force', 'eV/A/atom', 'train']
    nclo = int(data.shape[1]/2)
    targe = data[:, :nclo].reshape(-1)
    predi = data[:, nclo:].reshape(-1)
    pids = np.abs(targe - predi) < 1e4
    if np.sum(pids) != len(targe):
        print(f"WARNING: There are {len(targe)-np.sum(pids)} frams mismatch in {title[0]} {title[1]}")
    targe = targe[pids]
    predi = predi[pids]
    units = find_units(title[0])

    data_min = np.min([np.min(targe),np.min(predi)])
    data_max = np.max([np.max(targe),np.max(predi)])
    data_min -= (data_max-data_min)*0.1
    data_max += (data_max-data_min)*0.1
    plot([data_min, data_max], [data_min, data_max], c="grey", lw=3)
    xlim([data_min, data_max])
    ylim([data_min, data_max])

    RMSE = np.sqrt(((predi - targe) ** 2).mean())
    color = f"C{units[2]}"
    if title[1] == 'test': color = f"C{units[2]+3}"
    plot(targe, predi, '.', color=color)
    xlabel(f'DFT {title[0]} ({units[0]})')
    ylabel(f'NEP {title[0]} ({units[0]})')
    legend([f'{title[1]} RMSE:{1000*RMSE:.4f} {units[1]}'], loc="upper left")
    if print_rmse:
        print(" >>", title[0], title[1], f'{1000*RMSE:.4f}', units[1])
    # tight_layout()


def plot_nep_nep(data_train, data_test, title):
    # title = [name, type, units]
    # example: title = ['force', 'eV/A/atom', 'train']
    nclo  = int(data_train.shape[1]/2)
    train = data_train[:, nclo:].reshape(-1)
    test  = data_test[:, nclo:].reshape(-1)
    train = np.select([np.logical_and(train>-1e5, train<1e5)], [train])
    test  = np.select([np.logical_and(test>-1e5,  test<1e5)],  [test])
    units = find_units(title[0])

    data_min = np.min([np.min(train),np.min(test)])
    data_max = np.max([np.max(train),np.max(test)])
    data_min -= (data_max-data_min)*0.1
    data_max += (data_max-data_min)*0.1
    plot([data_min, data_max], [data_min, data_max], c="grey", lw=3)
    xlim([data_min, data_max])
    ylim([data_min, data_max])

    RMSE = np.sqrt(((test - train) ** 2).mean())
    color = f"C{units[2]}"
    if title[1] == 'test': color = f"C{units[2]+3}"
    plot(train, test, '.', color=color)
    xlabel(f'Train {title[0]} ({units[0]})')
    ylabel(f'Test {title[0]} ({units[0]})')
    legend([f'{title[1]} RMSE:{1000*RMSE:.4f} {units[1]}'], loc="upper left")
    # tight_layout()


def plot_out(plot_model, out_name="nep_out.png"):

    nep_out_files = ['loss.out',
                     'energy_train.out', 'energy_test.out',
                     'force_train.out',  'force_test.out']
    try:
        open('stress_train.out', 'r')
        nep_out_files += ['stress_train.out', 'stress_test.out']
        stress_flag = 1
    except FileNotFoundError:
        nep_out_files += ['virial_train.out', 'virial_test.out']
        print('WARNING: There is no stress file, use the virial file.')
        stress_flag = 0
    except:
        print('WARNING: There is no virial and stress files.')
        stress_flag = -1

    data_list = {}
    for file in nep_out_files:
        try:
            data_list[file] = np.loadtxt(file)
        except:
            data_list[file] = None

    if   plot_model == 0: plot_data = [1, 1, 0, 1, 0, 1, 0]
    elif plot_model == 1: plot_data = [1, 0, 1, 0, 1, 0, 1]
    elif plot_model == 2: plot_data = [1, 1, 1, 1, 1, 1, 1]
    elif plot_model == 3: plot_data = [0, 1, 0, 1, 0, 1, 0]
    elif plot_model == 4: plot_data = [0, 0, 1, 0, 1, 0, 1]
    elif plot_model == 5: plot_data = [0, 1, 1, 1, 1, 1, 1]

    plot_sum = np.sum(plot_data)
    if plot_sum in [4, 7]:  # plot train_test with loss.

        figure(figsize=(16, 14))
        subplot(2,2,1)
        set_fig_properties([gca()])
        # plot_loss
        plot_loss(data_list[nep_out_files[0]], test=plot_data[2])

        for i in range(3):   #  plot_train_test
            subplot(2,2,i+2)
            set_fig_properties([gca()])

            file_train_ids = 1+2*i
            if plot_data[file_train_ids] == 1:  # plot_train
                file_name = nep_out_files[file_train_ids]
                title = file_name.split('.')[0].split('_')
                plot_nep_dft(data_list[file_name], title)

            file_test_ids = 2+2*i
            if plot_data[file_test_ids] == 1:  # plot_test
                file_name = nep_out_files[file_test_ids]
                title = file_name.split('.')[0].split('_')
                plot_nep_dft(data_list[file_name], title)

    elif plot_sum in [3]:

        figure(figsize=(24, 7))
        for i in range(3):
            subplot(1,3,i+1)

            file_train_ids = 1+2*i
            if plot_data[file_train_ids] == 1:
                file_name = nep_out_files[file_train_ids]
                title = file_name.split('.')[0].split('_')
                plot_nep_dft(data_list[file_name], title)

            file_test_ids = 2+2*i
            if plot_data[file_test_ids] == 1:
                file_name = nep_out_files[file_test_ids]
                title = file_name.split('.')[0].split('_')
                plot_nep_dft(data_list[file_name], title)

    elif plot_sum in [6]:

        figure(figsize=(24, 7))
        for i in range(3):
            subplot(1,3,i+1)

            file_train_ids = 1+2*i
            file_test_ids = 2+2*i
            if plot_data[file_train_ids] == 1 and plot_data[file_test_ids] == 1:
                file_train_name = nep_out_files[file_train_ids]
                file_test_name = nep_out_files[file_test_ids]
                title = file_train_name.split('.')[0].split('_')
                plot_nep_nep(data_list[file_train_name], data_list[file_test_name], title)

    savefig(out_name, dpi=150, bbox_inches='tight')

    # plot_model = 0 # 0, train: loss+train
    # plot_model = 1 # 1, test: loss+test
    # plot_model = 2 # 2, train+test: loss+train+test
    # plot_model = 3 # 3, predict: train
    # plot_model = 4 # 4, predict: test
    # plot_model = 5 # 5, compare: train_nep:test_nep

name_list = ["nep_train.png", "nep_test.png", "nep_train_test.png", "train.png", "test.png", "compare.png"]

plot_model = int(sys.argv[1])
print_rmse = True

plot_out(plot_model, out_name=name_list[plot_model])
if plot_model in [0, 1, 2]:
    plot_nep("nep_txt.png")
