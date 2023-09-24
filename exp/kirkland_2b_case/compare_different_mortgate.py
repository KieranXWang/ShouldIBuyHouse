from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseModel, HouseRentModel

YEAR = 10

# buy house
house_model_30 = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.03, mortgage_month=30*12, n_month=YEAR*12)
house_model_30_list = house_model_30.net_cash_value_over_time()

house_model_20 = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.0275, mortgage_month=20*12, n_month=YEAR*12)
house_model_20_list = house_model_20.net_cash_value_over_time()

house_model_15 = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.02, mortgage_month=15*12, n_month=YEAR*12)
house_model_15_list = house_model_15.net_cash_value_over_time()


rent_model = HouseRentModel(init_cash=454000*0.2, rent=1800, monthly_cash=3500, utility=70, rent_increase_rate=0.04,
                            n_month=YEAR*12)
rent_net_val_list = rent_model.net_cash_value_over_time()

plt.plot(house_model_30_list[:YEAR*12], label='buy, 30-year mortgage')
plt.plot(house_model_20_list[:YEAR*12], label='buy, 20-year mortgage')
plt.plot(house_model_15_list[:YEAR*12], label='buy, 15-year mortgage')
plt.plot(rent_net_val_list[:YEAR*12], label='rent')
plt.legend()
plt.show()