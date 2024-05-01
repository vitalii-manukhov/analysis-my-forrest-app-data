import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
from utils import get_df_from_table_from_db
import numpy as np


def build_histograms():
    times_df = get_df_from_table_from_db()

    # Группировка данных по месяцу
    monthly_data = times_df.groupby(times_df['date'].dt.month)

    # Построение гистограмм для каждого месяца
    for month, month_data in monthly_data:
        plt.figure(figsize=(10, 6))
        plt.bar(month_data['date'].dt.day,
                month_data['time'],
                color='skyblue')
        plt.title(f"Гистограмма времени по дням для месяца {month}")
        plt.xlabel("День месяца")
        plt.ylabel("Потраченное время")
        plt.xticks(month_data['date'].dt.day)
        plt.grid(True)
        plt.savefig(f"hist_{month}")


def build_histograms_with_density_of_distribution():
    times_df = get_df_from_table_from_db()

    # Группировка данных по месяцу
    monthly_data = times_df.groupby(times_df['date'].dt.month)

    # Построение гистограмм и графика плотности
    # распределения для каждого месяца
    for month, month_data in monthly_data:
        plt.figure(figsize=(10, 6))
        sns.histplot(month_data['time'], kde=True, color='skyblue', bins=10)
        plt.title(
            f"Гистограмма и плотность распределения времени для месяца {month}"
        )
        plt.xlabel("Потраченное время")
        plt.ylabel("Частота")
        plt.grid(True)
        plt.savefig(f"histograms_with_density_of_distribution/hist_{month}")


def build_hists_and_curves():
    times_df = get_df_from_table_from_db()

    # Группировка данных по месяцу
    monthly_data = times_df.groupby(times_df['date'].dt.month)

    for month, month_data in monthly_data:
        plt.figure(figsize=(10, 6))
        plt.plot(month_data['date'].dt.day,
                 month_data['time'],
                 marker='o',
                 linestyle='-')
        plt.bar(month_data['date'].dt.day,
                month_data['time'],
                color='skyblue',
                alpha=0.5)
        plt.title(f"Кривая зависимости для месяца {month}")
        plt.xlabel("День месяца")
        plt.ylabel("Потраченное время")
        plt.xticks(month_data['date'].dt.day)
        plt.grid(True)
        plt.savefig(f"hists_and_curves/hist_{month}")


def build_hists_and_curves_2():
    times_df = get_df_from_table_from_db()

    # Группировка данных по месяцу
    monthly_data = times_df.groupby(times_df['date'].dt.month)

    for month, month_data in monthly_data:
        plt.figure(figsize=(10, 6))

        # Применение скользящего среднего
        window_size = 5
        smoothed_time = month_data['time'].rolling(window=window_size,
                                                   min_periods=1).mean()

        # Построение кривой зависимости времени от дня
        plt.plot(month_data['date'].dt.day,
                 smoothed_time,
                 # marker='o',
                 linestyle='-')
        plt.bar(month_data['date'].dt.day,
                month_data['time'],
                color='skyblue',
                alpha=0.3)

        plt.title(f"Сглаженная кривая для месяца {month}")
        plt.xlabel("День месяца")
        plt.ylabel("Потраченное время")
        plt.xticks(month_data['date'].dt.day)
        plt.grid(True)
        plt.savefig(f"hists_and_curves_2/hist_{month}")


def build_hists_and_interpolate():
    times_df = get_df_from_table_from_db()

    monthly_data = times_df.groupby(times_df['date'].dt.month)

    for month, month_data in monthly_data:
        plt.figure(figsize=(10, 6))

        # Применение скользящего среднего
        window_size = 3
        smoothed_time = month_data['time'].rolling(window=window_size,
                                                   min_periods=1).mean()

        # Кубическая интерполяция
        f = interp1d(month_data['date'].dt.day, smoothed_time, kind='cubic')
        x_new = np.linspace(month_data['date'].dt.day.min(),
                            month_data['date'].dt.day.max(), 300)
        y_smooth = f(x_new)

        # Построение кривой с использованием кубической интерполяции
        plt.plot(x_new, y_smooth, color='red', linestyle='-', linewidth=2)
        plt.bar(month_data['date'].dt.day,
                month_data['time'],
                color='skyblue',
                alpha=0.5)

        plt.title(f"Сглаженная кривая для месяца {month}")
        plt.xlabel("День месяца")
        plt.ylabel("Потраченное время")
        plt.xticks(month_data['date'].dt.day)
        plt.grid(True)
        plt.savefig(f"hists_and_interpolate/hist_{month}")


def main():
    # build_histograms()
    # build_histograms_with_density_of_distribution()
    # build_hists_and_curves()
    # build_hists_and_curves_2()
    build_hists_and_interpolate()


if __name__ == "__main__":
    main()
