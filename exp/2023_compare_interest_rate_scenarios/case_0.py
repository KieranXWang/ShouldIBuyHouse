from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseAndRentModel, CashInvestModel


SHOW_MONTH = 3 * 12

# buy house and rend out
house_purchase_and_rent_model = HousePurchaseAndRentModel(down_payment_total=400000,
                                                          loan_total=1600000,
                                                          monthly_cash=10000,
                                                          hoa=0,
                                                          insurance=100,
                                                          rent=6000,
                                                          inflation_rate=0.02,
                                                          property_value_increase_rate=0.0,
                                                          loan_interest_rate=0.07,
                                                          cash_invest_increase_rate=0.05,
                                                          rent_increase_rate=0.02,
                                                          rent_out_percentage=1,
                                                          init_cash=0)
house_purchase_and_rent_model_net_val_list = house_purchase_and_rent_model.net_cash_value_over_time()

# cash invest
cash_model = CashInvestModel(init_cash=400000, monthly_cash=10000, cash_invest_increase_rate=0.05)
cash_model_net_val_list = cash_model.net_cash_value_over_time()

plt.plot(house_purchase_and_rent_model_net_val_list[:SHOW_MONTH], label='buy house and rent out')
plt.plot(cash_model_net_val_list[:SHOW_MONTH], label='invest')
plt.legend()
plt.savefig('./case_0.png')

print('db')