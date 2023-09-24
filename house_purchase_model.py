from mortgage import Mortgage
from utils import annual_rate_to_monthly_rate


class ModelBase:
    def __init__(self, inflation_rate, property_tax_rate):
        self.inflation_rate = inflation_rate
        self.property_tax_rate = property_tax_rate

    def _check_cash_positive(self, cash):
        if cash < 0:
            raise ValueError("Cash is below 0.")

    def _property_tax_monthly(self, house_value):
        return house_value * self.property_tax_rate / 12

    def _monthly_inflation(self, price_dict):
        # inflation - price increase
        for item in price_dict:
            new_price = price_dict[item] * (1 + annual_rate_to_monthly_rate(self.inflation_rate))
            price_dict[item] = new_price

        return price_dict


class HousePurchaseModel(ModelBase):
    def __init__(self, down_payment_total, loan_total, monthly_cash, hoa, insurance, property_tax_rate=0.007,
                 inflation_rate=0.03, property_value_increase_rate=0.1, loan_interest_rate=0.03, mortgage_month=12 * 30,
                 cash_invest_increase_rate=0.1, n_month=12 * 30, init_cash=0, house_sell_loss=0., income_taxable=False,
                 tax_rate=0.2):
        self.init_down_payment = down_payment_total
        self.init_loan = loan_total
        self.init_house_price = down_payment_total + loan_total
        self.init_hoa = hoa
        self.init_insurance = insurance
        self.monthly_cash = monthly_cash
        self.property_tax_rate = property_tax_rate
        self.inflation_rate = inflation_rate
        self.property_value_increase_rate = property_value_increase_rate
        self.cash_invest_increase_rate = cash_invest_increase_rate
        self.loan_interest_rate = loan_interest_rate
        self.mortgage_month = mortgage_month
        self.n_month = n_month
        self.init_cash = init_cash
        self.taxable = income_taxable
        self.tax_rate = tax_rate
        self.house_sell_loss = house_sell_loss
        # mortgage
        self.mortgage = Mortgage(interest=loan_interest_rate, months=mortgage_month, amount=loan_total)
        self.mortgage_payment_monthly = self.mortgage.monthly_payment()
        self.mortgage_balance_list = list(self.mortgage.balance_schedule())

    def _expense(self, hoa, insurance, house_value, mortgage):
        # property tax
        month_property_tax = self._property_tax_monthly(house_value)

        return hoa + insurance + month_property_tax + mortgage

    def _monthly_transition(self, month, cash, house_value, price_dict):
        month += 1
        # cash invest
        cash = cash * (1 + annual_rate_to_monthly_rate(self.cash_invest_increase_rate))
        # house value increase
        house_value = house_value * (1 + annual_rate_to_monthly_rate(self.property_value_increase_rate))
        # inflation - price increase
        price_dict = self._monthly_inflation(price_dict)

        return month, cash, house_value, price_dict

    def _init_month(self):
        # deposit cash
        cash = self.monthly_cash + self.init_cash

        # expense
        expense = self._expense(hoa=self.init_hoa, insurance=self.init_insurance, house_value=self.init_house_price,
                                mortgage=self.mortgage_payment_monthly)

        cash = cash - expense

        # states
        curr_price_dict = {'hoa': self.init_hoa, 'insurance': self.init_insurance}
        curr_cash_invest = cash
        curr_house_value = self.init_house_price

        # check cash positive
        self._check_cash_positive(cash)

        return curr_house_value, curr_cash_invest, curr_price_dict, 0

    def _next_month(self, last_house_value, last_cash_invest, last_price_dict, last_month):
        # month transition
        month, cash, house_value, price_dict = self._monthly_transition(month=last_month, cash=last_cash_invest,
                                                                        house_value=last_house_value,
                                                                        price_dict=last_price_dict)

        # case deposit
        cash += self.monthly_cash

        # expense
        expense = self._expense(hoa=price_dict['hoa'], insurance=price_dict['insurance'], house_value=house_value,
                                mortgage=self.mortgage_payment_monthly)

        # clear
        cash = cash - expense

        # states
        curr_price_dict = price_dict
        curr_cash_invest = cash
        curr_house_value = house_value

        # check cash positive
        self._check_cash_positive(cash)

        return curr_house_value, curr_cash_invest, curr_price_dict, month

    def net_cash_value_over_time(self):
        net_value_list = []
        curr_house_value, curr_cash_invest, curr_price_dict, month = self._init_month()
        # net value = cash + sale house income * 0.95 - mortgage balance
        net_val = curr_cash_invest + curr_house_value * (1-self.house_sell_loss) - self.mortgage_balance_list[month]
        net_value_list.append(net_val)

        while month < self.n_month - 1:
            curr_house_value, curr_cash_invest, curr_price_dict, month = self._next_month(
                last_house_value=curr_house_value,
                last_cash_invest=curr_cash_invest,
                last_price_dict=curr_price_dict,
                last_month=month)
            # net value = cash + sale house income * 0.95 - mortgage balance
            if month < self.mortgage_month:
                net_val = curr_cash_invest + curr_house_value * (1-self.house_sell_loss) - self.mortgage_balance_list[month]
            else:
                net_val = curr_cash_invest + curr_house_value * (1-self.house_sell_loss)
            net_value_list.append(net_val)

        return net_value_list


class HouseRentModel(ModelBase):
    def __init__(self, init_cash, rent, monthly_cash, utility, inflation_rate=0.03, rent_increase_rate=0.05, n_month=12*30,
                 cash_invest_increase_rate=0.1):
        self.init_cash = init_cash
        self.init_rent = rent
        self.monthly_cash = monthly_cash
        # utility is the expense typically covered by hoa when buying a home
        self.init_utility = utility
        self.inflation_rate = inflation_rate
        self.rent_increase_rate = rent_increase_rate
        self.n_month = n_month
        self.cash_invest_increase_rate = cash_invest_increase_rate

    def _expense(self, rent, utility):
        return rent + utility

    def _monthly_transition(self, month, cash, rent, price_dict):
        month += 1
        # cash invest
        cash = cash * (1 + annual_rate_to_monthly_rate(self.cash_invest_increase_rate))
        # rent increase
        rent = rent * (1 + self.rent_increase_rate / 12)
        # price inflation
        price_dict = self._monthly_inflation(price_dict)

        return month, cash, rent, price_dict

    def _init_month(self):
        # deposit cash
        cash = self.init_cash + self.monthly_cash

        # expense
        expense = self._expense(rent=self.init_rent, utility=self.init_utility)

        # clear
        cash = cash - expense

        # states
        curr_price_dict = {'utility': self.init_utility}
        curr_cash_invest = cash
        curr_rent = self.init_rent

        # check cash positive
        self._check_cash_positive(cash)

        return curr_rent, curr_cash_invest, curr_price_dict, 0

    def _next_month(self, last_rent, last_cash_invest, last_price_dict, last_month):
        month, cash, rent, price_dict = self._monthly_transition(month=last_month, cash=last_cash_invest, rent=last_rent, price_dict=last_price_dict)

        # deposit cash
        cash += self.monthly_cash

        # expense
        expense = self._expense(rent=rent, utility=price_dict['utility'])

        # clear
        cash = cash - expense

        # states
        curr_price_dict = price_dict
        curr_cash_invest = cash
        curr_rent = rent

        # check cash positive
        self._check_cash_positive(cash)

        return curr_rent, curr_cash_invest, curr_price_dict, month

    def net_cash_value_over_time(self):
        net_value_list = []
        curr_rent, curr_cash_invest, curr_price_dict, month = self._init_month()
        # net val = curr_cash_invest
        net_value_list.append(curr_cash_invest)

        while month < self.n_month - 1:
            curr_house_value, curr_cash_invest, curr_price_dict, month = self._next_month(last_rent=curr_rent,
                                                                                          last_cash_invest=curr_cash_invest,
                                                                                          last_price_dict=curr_price_dict,
                                                                                          last_month=month)
            net_value_list.append(curr_cash_invest)

        return net_value_list


class HousePurchaseAndRentModel(ModelBase):
    def __init__(self, down_payment_total, loan_total, monthly_cash, hoa, insurance, rent, property_tax_rate=0.007,
                 inflation_rate=0.03, property_value_increase_rate=0.1, loan_interest_rate=0.03, mortgage_month=12*30,
                 cash_invest_increase_rate=0.1, rent_increase_rate=0.05, rent_out_percentage=10/12, n_month=12*30,
                 init_cash=0, house_sell_loss=0.0):
        self.init_down_payment = down_payment_total
        self.init_loan = loan_total
        self.init_house_price = down_payment_total + loan_total
        self.init_hoa = hoa
        self.init_insurance = insurance
        self.monthly_cash = monthly_cash
        self.init_rent = rent
        self.property_tax_rate = property_tax_rate
        self.inflation_rate = inflation_rate
        self.property_value_increase_rate = property_value_increase_rate
        self.loan_interest_rate = loan_interest_rate
        self.mortgage_month = mortgage_month
        self.cash_invest_increase_rate = cash_invest_increase_rate
        self.rent_increase_rate = rent_increase_rate
        self.rent_out_percentage = rent_out_percentage
        self.n_month = n_month
        self.init_cash = init_cash
        self.house_sell_loss = house_sell_loss
        # mortgage
        self.mortgage = Mortgage(interest=loan_interest_rate, months=mortgage_month, amount=loan_total)
        self.mortgage_payment_monthly = self.mortgage.monthly_payment()
        self.mortgage_balance_list = list(self.mortgage.balance_schedule())

    def _income(self, rent):
        # consider the fact that you may not be able to rent out the house full time
        return rent * self.rent_out_percentage

    def _expense(self, hoa, insurance, house_value, mortgage):
        # property tax
        month_property_tax = self._property_tax_monthly(house_value)

        return hoa + insurance + month_property_tax + mortgage

    def _monthly_transition(self, month, cash, house_value, rent, price_dict):
        month += 1
        # cash invest
        cash = cash * (1 + annual_rate_to_monthly_rate(self.cash_invest_increase_rate))
        # house value increase
        house_value = house_value * (1 + annual_rate_to_monthly_rate(self.property_value_increase_rate))
        # inflation - price increase
        price_dict = self._monthly_inflation(price_dict)
        # rent increase
        rent = rent * (1 + annual_rate_to_monthly_rate(self.rent_increase_rate))

        return month, cash, house_value, rent, price_dict

    def _init_month(self):
        # deposit cash
        cash = self.monthly_cash + self.init_cash

        # income: rent
        income = self._income(rent=self.init_rent)

        # expense
        expense = self._expense(hoa=self.init_hoa, insurance=self.init_insurance, house_value=self.init_house_price,
                                mortgage=self.mortgage_payment_monthly)

        # clear
        cash = cash + income - expense

        # states
        curr_price_dict = {'hoa': self.init_hoa, 'insurance': self.init_insurance}
        curr_cash_invest = cash
        curr_house_value = self.init_house_price
        curr_rent = self.init_rent

        # check cash positive
        self._check_cash_positive(cash)

        return curr_house_value, curr_cash_invest, curr_price_dict, curr_rent, 0

    def _next_month(self, last_house_value, last_cash_invest, last_price_dict, last_rent, last_month):
        month, cash, house_value, rent, price_dict = self._monthly_transition(month=last_month, cash=last_cash_invest,
                                                                              house_value=last_house_value,
                                                                              rent=last_rent,
                                                                              price_dict=last_price_dict)

        # deposit cash
        cash += self.monthly_cash

        # income
        income = self._income(rent=rent)

        # expense
        expense = self._expense(hoa=price_dict['hoa'], insurance=price_dict['insurance'], house_value=house_value,
                                mortgage=self.mortgage_payment_monthly)

        # clear
        cash = cash + income - expense

        # states
        curr_price_dict = price_dict
        curr_cash_invest = cash
        curr_house_value = house_value
        curr_rent = rent

        # check cash positive
        self._check_cash_positive(cash)

        return curr_house_value, curr_cash_invest, curr_price_dict, curr_rent, month

    def net_cash_value_over_time(self):
        net_value_list = []
        curr_house_value, curr_cash_invest, curr_price_dict, curr_rent, month = self._init_month()
        # net value = cash + sale house income * 0.95 - mortgage balance - (return last month rent)
        net_val = curr_cash_invest + curr_house_value * (1 - self.house_sell_loss) - self.mortgage_balance_list[
            month] - curr_rent
        net_value_list.append(net_val)

        while month < self.n_month - 1:
            curr_house_value, curr_cash_invest, curr_price_dict, curr_rent, month = self._next_month(
                last_house_value=curr_house_value, last_cash_invest=curr_cash_invest, last_price_dict=curr_price_dict,
                last_rent=curr_rent, last_month=month)
            # net value = cash + sale house income * 0.95 - mortgage balance - return last month rent
            if month < self.mortgage_month:
                net_val = curr_cash_invest + curr_house_value * (1 - self.house_sell_loss) - self.mortgage_balance_list[
                    month] - curr_rent
            else:
                net_val = curr_cash_invest + curr_house_value * (1-self.house_sell_loss) - curr_rent

            net_value_list.append(net_val)

        return net_value_list


class CashInvestModel:
    def __init__(self, init_cash, monthly_cash, cash_invest_increase_rate=0.1, n_month=30*12):
        self.init_cash = init_cash
        self.monthly_cash = monthly_cash
        self.cash_invest_increase_rate = cash_invest_increase_rate
        self.n_month = n_month

    def _init_month(self):
        # income
        cash = self.init_cash + self.monthly_cash

        # states
        return cash

    def _next_mont(self, last_cash_invest):
        # cash invest
        cash = last_cash_invest * (1 + annual_rate_to_monthly_rate(self.cash_invest_increase_rate))

        # income
        cash += self.monthly_cash

        # states
        return cash

    def net_cash_value_over_time(self):
        month = 0
        net_val_list = []
        curr_cash_invest = self._init_month()
        # net val = cash invest
        net_val_list.append(curr_cash_invest)

        while month < self.n_month - 1:
            month += 1
            curr_cash_invest = self._next_mont(last_cash_invest=curr_cash_invest)
            net_val_list.append(curr_cash_invest)

        return net_val_list






















