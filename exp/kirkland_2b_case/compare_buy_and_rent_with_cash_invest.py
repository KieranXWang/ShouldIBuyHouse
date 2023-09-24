from matplotlib import pyplot as plt
from house_purchase_model import HousePurchaseAndRentModel, CashInvestModel

YEAR = 10
CASH_INVEST_GAIN = 0.12

better_30_year = HousePurchaseAndRentModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=2500, hoa=260,
                                        insurance=90, rent=1900, property_tax_rate=0.007,
                                        inflation_rate=0.03, property_value_increase_rate=0.1, loan_interest_rate=0.03,
                                        mortgage_month=12 * 30,
                                        cash_invest_increase_rate=CASH_INVEST_GAIN, rent_increase_rate=0.04,
                                        rent_out_percentage=10 / 12, n_month=YEAR*12, init_cash=2000+679)
better_30_year_list = better_30_year.net_cash_value_over_time()

better_30_year_point = HousePurchaseAndRentModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=2500, hoa=260,
                                        insurance=80, rent=1900, property_tax_rate=0.007,
                                        inflation_rate=0.03, property_value_increase_rate=0.1, loan_interest_rate=0.02875,
                                        mortgage_month=12 * 30,
                                        cash_invest_increase_rate=CASH_INVEST_GAIN, rent_increase_rate=0.04,
                                        rent_out_percentage=10 / 12, n_month=YEAR*12, init_cash=2000-1308)
better_30_year_point_list = better_30_year_point.net_cash_value_over_time()

better_15_year = HousePurchaseAndRentModel(down_payment_total=454000*0.2, loan_total=454000*0.8, monthly_cash=2500, hoa=260,
                                        insurance=80, rent=1900, property_tax_rate=0.007,
                                        inflation_rate=0.03, property_value_increase_rate=0.1, loan_interest_rate=0.02,
                                        mortgage_month=12 * 15,
                                        cash_invest_increase_rate=CASH_INVEST_GAIN, rent_increase_rate=0.04,
                                        rent_out_percentage=10 / 12, n_month=YEAR*12, init_cash=2000-912)
better_15_year_list = better_15_year.net_cash_value_over_time()

cash_model = CashInvestModel(init_cash=454000*0.2 + 2000, monthly_cash=2500, cash_invest_increase_rate=0.1, n_month=YEAR*12)
cash_net_val_list = cash_model.net_cash_value_over_time()

plt.plot(better_30_year_list[:YEAR*12], label='house invest, 30 year mortgage')
plt.plot(better_15_year_list[:YEAR*12], label='house invest, 15 year mortgage')
plt.plot(cash_net_val_list[:YEAR*12], label='cash invest')
plt.legend()
plt.show()