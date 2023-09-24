from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseModel, HouseRentModel

YEAR = 30

# buy house
house_model_30_20down = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.0325, mortgage_month=30*12, n_month=YEAR*12,
                                           init_cash=454000*0.05)
house_model_30_list_20 = house_model_30_20down.net_cash_value_over_time()

house_model_30_25down = HousePurchaseModel(down_payment_total=454000*0.25, loan_total=454000*0.75, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.03, mortgage_month=30*12, n_month=YEAR*12)
house_model_30_list_25 = house_model_30_25down.net_cash_value_over_time()

plt.plot(house_model_30_list_20[:YEAR*12], label='buy, 30-year mortgage, 20% down')
plt.plot(house_model_30_list_25[:YEAR*12], label='buy, 30-year mortgage, 25% down')

plt.legend()
plt.show()
