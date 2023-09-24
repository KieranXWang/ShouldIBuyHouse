from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseModel, HouseRentModel

# buy house
house_model = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=2500,
                                 hoa=260, insurance=80)
buy_net_val_list = house_model.net_cash_value_over_time()

rent_model = HouseRentModel(init_cash=454000*0.2, rent=1800, monthly_cash=2500, utility=70, rent_increase_rate=0.04)
rent_net_val_list = rent_model.net_cash_value_over_time()

plt.plot(buy_net_val_list[:10*12], label='buy')
plt.plot(rent_net_val_list[:10*12], label='rent')
plt.legend()
plt.show()

