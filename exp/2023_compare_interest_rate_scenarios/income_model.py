from mortgage import Mortgage


def calculate_yearly_net_income_buy_house(house_price: float, interest_rate: float,
                                          mortgage_payment_interest_ratio: float,
                                          house_price_increase_rate: float = 0.0, mortgage_percentage: float = 0.2):
    # mortgage
    mortgage = Mortgage(interest=interest_rate, months=12*30, amount=house_price*mortgage_percentage)

    # rent income, 3.5%
    rent_income = house_price * 0.035
    # house price increase
    house_value_increase = house_price * house_price_increase_rate

    # property tax
    property_tax = house_price * 0.01
    # interest payment
    interest_payment = mortgage.monthly_payment() * 12 * mortgage_payment_interest_ratio

    total = rent_income + house_value_increase - property_tax - interest_payment

    return total


def calculate_yearly_net_income_invest(amount: float, gain_rate: float):
    return amount * gain_rate


if __name__ == '__main__':
    # 3% interest, 57% payment goes to interest, 100w house
    buy_house_year_income = calculate_yearly_net_income_buy_house(house_price=1000000,
                                                                  interest_rate=0.03,
                                                                  mortgage_payment_interest_ratio=0.57)
    print(f"Year income 3% interest rate buy house case = {buy_house_year_income}")
    # invest, 1%
    invest_year_income = calculate_yearly_net_income_invest(amount=200000, gain_rate=0.01)
    print(f"Year income 1% gain rate invest = {invest_year_income}")
    # invest, 5%
    invest_year_income = calculate_yearly_net_income_invest(amount=200000, gain_rate=0.05)
    print(f"Year income 5% gain rate invest = {invest_year_income}")

    # 7.6% interest, 88% payment goes to interest, 100w house
    buy_house_year_income = calculate_yearly_net_income_buy_house(house_price=1000000,
                                                                  interest_rate=0.076,
                                                                  mortgage_payment_interest_ratio=0.88)
    print(f"Year income 7.6% interest rate buy house case = {buy_house_year_income}")

