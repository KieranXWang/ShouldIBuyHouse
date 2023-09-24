from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseModel, HouseRentModel

YEAR = 10

# buy house
house_model_0 = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.03, mortgage_month=30*12, n_month=YEAR*12,
                                           init_cash=2000+679)
house_model_0_list = house_model_0.net_cash_value_over_time()

house_model_1 = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.02875, mortgage_month=30*12, n_month=YEAR*12,
                                   init_cash=2000-1308)
house_model_1_list = house_model_1.net_cash_value_over_time()

boyang = HousePurchaseModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=3500,
                                 hoa=260, insurance=80, loan_interest_rate=0.0315, mortgage_month=30*12, n_month=YEAR*12,
                                   init_cash=2000)
boyang_list = boyang.net_cash_value_over_time()


plt.plot(house_model_0_list[:YEAR*12], label='better, 30-year mortgage, 0.3%')
plt.plot(house_model_1_list[:YEAR*12], label='better, 30-year mortgage, 0.2875%')
plt.plot(boyang_list[:YEAR*12], label='boyang, 3.125%')

plt.legend()
plt.show()