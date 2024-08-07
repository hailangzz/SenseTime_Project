import numpy as np
import matplotlib.pyplot as plt

def simulate_price(initial_price, avg_growth_rate, growth_std, annual_growth, days=365):
    prices = [initial_price]
    for _ in range(days):
        daily_growth = np.random.normal(avg_growth_rate, growth_std)
        prices.append(prices[-1] + daily_growth)
    prices = np.array(prices)
    prices += np.linspace(0, annual_growth, days+1)
    return prices

def calculate_total_return(initial_money, price, strategy_day):
    units = initial_money // price[strategy_day]
    remaining_money = initial_money - units * price[strategy_day]
    final_money = remaining_money + units * price[-1]
    return final_money, units

def analyze_strategies(initial_money, initial_price, avg_growth_rate, growth_std, annual_growth, days=365, simulations=1000):
    avg_prices = np.zeros(days + 1)
    avg_units = np.zeros(days + 1)
    avg_returns = np.zeros(days + 1)

    for _ in range(simulations):
        prices = simulate_price(initial_price, avg_growth_rate, growth_std, annual_growth, days)
        avg_prices += prices
        for day in range(days + 1):
            final_money, units = calculate_total_return(initial_money, prices, day)
            avg_units[day] += units
            avg_returns[day] += final_money

    avg_prices /= simulations
    avg_units /= simulations
    avg_returns /= simulations

    return avg_prices, avg_units, avg_returns

# Parameters
initial_money = 10000
initial_price = 60
avg_growth_rate = 2
growth_std = 0.2
annual_growth = 9

avg_prices, avg_units, avg_returns = analyze_strategies(initial_money, initial_price, avg_growth_rate, growth_std, annual_growth)

# Plotting the results
plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
plt.plot(avg_prices)
plt.title('Average Prices Over a Year')
plt.xlabel('Day')
plt.ylabel('Price (Yuan)')

plt.subplot(3, 1, 2)
plt.plot(avg_units)
plt.title('Average Units Bought Over a Year')
plt.xlabel('Day')
plt.ylabel('Units')

plt.subplot(3, 1, 3)
plt.plot(avg_returns)
plt.title('Average Returns Over a Year')
plt.xlabel('Day')
plt.ylabel('Total Returns (Yuan)')

plt.tight_layout()
plt.show()

# Finding the optimal strategy
best_strategy_day = np.argmax(avg_returns)
best_final_money = avg_returns[best_strategy_day]
best_units = avg_units[best_strategy_day]

print(f"最佳购买策略是在第 {best_strategy_day} 天买入，最终收益为 {best_final_money:.2f} 元，买入量为 {best_units:.2f} 单位。")
