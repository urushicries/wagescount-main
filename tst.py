import numpy as np
import matplotlib.pyplot as plt


# Напряжение источника (прямое смещение)
U1 = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4])
I1 = np.array([0, 0, 0, 16.9, 30.8, 45.65, 60.9,
              76.6, 108.3, 140.4])  # Ток диода (мА)
U_d1 = np.array([0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9,
                1.0, 1.1, 1.2])  # Напряжение на диоде

# Напряжение источника (обратное смещение)
U2 = np.array([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12])
I2 = np.array([0, 0, 0, 0, 0, -122.8, -284.9, -449.5, -
              614.8, -780.7, -946.7, -1130])  # Ток диода (мА)
U_d2 = np.array([-1.0, -2.0, -3.0, -4.0, -5.0, -5.9, -6.7, -
                7.5, -8.4, -9.2, -10.1, -10.9])  # Напряжение на диоде

# Строим график ВАХ для прямого смещения
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(U_d1, I1, marker='o', linestyle='-',
         color='b', label="Прямое смещение")
plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
plt.xlabel("Uист, В")
plt.ylabel("Iд, мА")
plt.title("Прямое смещение")
plt.legend()
plt.grid()


# Строим график ВАХ для обратного смещения
plt.subplot(1, 2, 2)
plt.plot(U_d2, I2, marker='o', linestyle='-',
         color='r', label="Обратное смещение")
plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
plt.xlabel("Uист, В")
plt.ylabel("Iд, мА")
plt.title("Обратное смещение")
plt.legend()
plt.grid()

# Отображаем графики
plt.tight_layout()
plt.show()
