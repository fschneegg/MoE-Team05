import pandas as pd
import matplotlib.pyplot as plt


def read_load_profile(path):
    lp = pd.read_csv(path, sep=';', decimal=',')

    # Leere Spalten entfernen wegen ;;;;;;;
    lp = lp.dropna(axis=1, how='all')

    lp['timestamp_UTC'] = pd.to_datetime(
        lp['Ab-Datum'].astype(str) + ' ' + lp['Ab-Zeit'].astype(str),
        format='%d.%m.%Y %H:%M:%S',
        errors='coerce'
    )

    lp['kW'] = pd.to_numeric(lp['kW'], errors='coerce')
    lp['kW'] = pd.to_numeric(lp['kW'], errors='coerce')

    lp = lp.dropna(subset=['timestamp_UTC', 'kW'])

    return lp


def print_statistics(lp):
    load = lp['kW']

    lp_max = load.max()
    lp_min = load.min()
    lp_mean = load.mean()

    print(
        'Maximal:', lp_max, '\n'
        'Minimal:', lp_min, '\n'
        'Durchschnitt:', lp_mean
    )

    return lp_max, lp_min, lp_mean


def plot_load_profile(lp):
    fig, ax = plt.subplots(figsize=(12, 6))

    load = lp['kW']

    lp_max = load.max()
    lp_min = load.min()
    lp_mean = load.mean()

    ax.plot(
        lp['timestamp_UTC'],
        load,
        color='tab:red',
        linewidth=0.8,
    )

    ax.axhline(
        lp_max,
        color='black',
        linestyle='--',
        linewidth=1.2,
        label=f'Maximum: {lp_max:.2f} kW'
    )

    ax.axhline(
        lp_mean,
        color='green',
        linestyle='--',
        linewidth=1.2,
        label=f'Durchschnitt: {lp_mean:.2f} kW'
    )

    ax.axhline(
        lp_min,
        color='blue',
        linestyle='--',
        linewidth=1.2,
        label=f'Minimum: {lp_min:.2f} kW'
    )

    ax.set_title('Lastgang eines Krankenhauses')
    ax.set_xlabel('Zeit')
    ax.set_ylabel('Last [kW]')
    ax.grid(True)
    ax.legend(loc='upper right')

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()


def plot_heatmap(ax, df, value_col, title, cmap='viridis'):
    heatmap_data = df.copy()

    heatmap_data['date'] = heatmap_data['timestamp_UTC'].dt.date
    heatmap_data['hour'] = heatmap_data['timestamp_UTC'].dt.hour

    heatmap_table = heatmap_data.pivot_table(
        index='date',
        columns='hour',
        values=value_col,
        aggfunc='mean'
    )

    im = ax.imshow(
        heatmap_table,
        aspect='auto',
        cmap=cmap,
        origin='lower'
    )

    ax.set_title(title)
    ax.set_xlabel('Stunde des Tages')
    ax.set_ylabel('Datum')

    ax.set_xticks(range(0, 24, 2))
    ax.set_xticklabels(range(0, 24, 2))

    step = max(1, len(heatmap_table.index) // 10)
    ax.set_yticks(range(0, len(heatmap_table.index), step))
    ax.set_yticklabels(heatmap_table.index[::step])

    plt.colorbar(im, ax=ax, label=value_col)


def plot_load_heatmap(lp):
    fig, ax = plt.subplots(figsize=(12, 6))

    plot_heatmap(
        ax=ax,
        df=lp,
        value_col='kW',
        title='Heatmap des Lastprofils [kW]',
        cmap='viridis'
    )

    plt.tight_layout()
    plt.show()


def main():
    path = r'Stromlastgang_Krankenhaus.csv'

    lp = read_load_profile(path)

    print_statistics(lp)

    plot_load_profile(lp)
    plot_load_heatmap(lp)


if __name__ == '__main__':
    main()