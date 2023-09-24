from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseModel, HouseRentModel

# buy house
house_model = HousePurchaseModel(down_payment_total=1500000*0.2, loan_total=1500000*0.8, monthly_cash=6000,
                                 hoa=200, insurance=100, property_value_increase_rate=0.12)
buy_net_val_list = house_model.net_cash_value_over_time()

rent_model = HouseRentModel(init_cash=1500000*0.2, rent=1700, monthly_cash=6000, utility=70, rent_increase_rate=0.04,
                            cash_invest_increase_rate=0.1)
rent_net_val_list = rent_model.net_cash_value_over_time()

plt.plot(buy_net_val_list[:10*12], label='buy')
plt.plot(rent_net_val_list[:10*12], label='rent')
plt.legend()
plt.show()