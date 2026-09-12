import pandas as pd
import matplotlib.pyplot as plt


def read_load_profile(path):
    # CSV einlesen
    lp = pd.read_csv(path)

    # Erste Spalte = alter Index / Snapshot
    # Zweite Spalte = Leistung
    if len(lp.columns) >= 2:
        lp = lp.iloc[:, :2]
        lp.columns = ['old_index', 'kW']

    else:
        lp.columns = ['kW']

    # Leistung sicher numerisch machen
    lp['kW'] = pd.to_numeric(lp['kW'], errors='coerce')

    # Ungültige Werte entfernen
    lp = lp.dropna(subset=['kW']).reset_index(drop=True)

    # -----------------------------------------------------
    # Neue Zeitachse:
    # 01.01.2026 bis 31.12.2026
    # -----------------------------------------------------

    start = pd.Timestamp('2026-01-01 00:00:00')
    end = pd.Timestamp('2027-01-01 00:00:00')

    # Zeitschritt automatisch aus Anzahl der Werte bestimmen
    timestep = (end - start) / len(lp)

    lp['timestamp_UTC'] = pd.date_range(
        start=start,
        periods=len(lp),
        freq=timestep
    )

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

    ax.set_title('Lastgang mit konventionellen Tarifen & FRC')
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
        title='Heatmap des Lastprofils mit konventionellen Tarifen & ohne FCR [kW]',
        cmap='viridis'
    )

    plt.tight_layout()
    plt.show()


def main():
    path = r'Last Krankenhaus ohne FCR & konv. Stromtarife2026-09-12.csv'

    lp = read_load_profile(path)

    print_statistics(lp)

#    plot_load_profile(lp)
    plot_load_heatmap(lp)


if __name__ == '__main__':
    main()