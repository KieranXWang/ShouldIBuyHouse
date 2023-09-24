from matplotlib import pyplot as plt
from utils import annual_rate_to_monthly_rate

class CarPurchaseModel:
    def __init__(self, car_price_full: float, monthly_depreciation: float = 300., monthly_insurance: float = 200.,
                 monthly_maintenance: float = 50., yearly_price_increase: float = 0.03):
        self.car_price_full = car_price_full
        self.monthly_depreciation = monthly_depreciation
        self.monthly_insurance = monthly_insurance
        self.monthly_maintenance = monthly_maintenance
        self.yearly_price_increase = yearly_price_increase
        self.monthly_price_increase = annual_rate_to_monthly_rate(yearly_price_increase)
        # states at beginning
        self.down_payment = 0.
        self.begin_net_value = 0.
        # states during holding period
        self.payment_by_month = []
        self.net_value_by_month = []

    def get_current_value(self):
        if len(self.net_value_by_month) == 0:
            return self.begin_net_value
        else:
            return self.net_value_by_month[-1]

    def get_current_payment(self):
        if len(self.payment_by_month) == 0:
            return self.monthly_insurance + self.monthly_maintenance
        else:
            return self.payment_by_month[-1]

    def down_payment_time(self, down_payment: float, additional_fee:float=0):
        self.down_payment = down_payment + additional_fee
        self.begin_net_value = self.car_price_full

    def one_month_time(self):
        # payment = insurance + maintenance
        # considering inflation， payment = last month payment * (1 + monthly price increase)
        month_payment = self.get_current_payment() * (1 + self.monthly_price_increase)
        # net value = current value - monthly depreciation
        month_net_value = self.get_current_value() - self.monthly_depreciation
        self.payment_by_month.append(month_payment)
        self.net_value_by_month.append(month_net_value)

    def hold(self, months:int):
        for i in range(months):
            self.one_month_time()

    def output_data(self):
        return self.down_payment, self.begin_net_value, self.payment_by_month, self.net_value_by_month


class CarRentalModel:
    def __init__(self, month_rent_now: float, yearly_price_increase: float = 0.03, yearly_invest_increase:float = 0.1):
        self.month_rent_now = month_rent_now
        self.yearly_price_increase = yearly_price_increase
        self.monthly_price_increase = annual_rate_to_monthly_rate(yearly_price_increase)
        self.yearly_invest_increase = yearly_invest_increase
        self.monthly_invest_increase = annual_rate_to_monthly_rate(yearly_invest_increase)
        # states at beginning
        self.begin_cash = 0.
        self.begin_net_value = 0.
        self.begin_rent = month_rent_now
        # states during holding period
        self.rent_by_month = []
        self.payment_by_month = []
        self.net_value_by_month = []
        self.cash_by_month = []

    def get_current_rent(self):
        if len(self.rent_by_month) == 0:
            return self.begin_rent
        else:
            return self.rent_by_month[-1]

    def get_current_cash(self):
        if len(self.cash_by_month) == 0:
            return self.begin_cash
        else:
            return self.cash_by_month[-1]

    def start_time(self, cash: float):
        self.begin_cash = cash
        self.begin_net_value = cash

    def one_month_time(self, cash_add: float):
        # payment = current month rent
        month_rent = self.get_current_rent() * (1 + self.monthly_price_increase)
        month_payment = month_rent
        # net value = (pre value - month payment + cash add) * (1 + monthly invest rate)
        month_cash = (self.get_current_cash() - month_payment + cash_add) * (1 + self.monthly_invest_increase)
        month_net_value = month_cash
        # update
        self.rent_by_month.append(month_rent)
        self.payment_by_month.append(month_payment)
        self.cash_by_month.append(month_cash)
        self.net_value_by_month.append(month_net_value)

    def hold(self, months: int, cash_add_schedule:list):
        for i in range(months):
            month_cash = cash_add_schedule[i]
            self.one_month_time(month_cash)

    def output_data(self):
        return 0., 0., self.payment_by_month, self.net_value_by_month


# test
honda_hrv = CarPurchaseModel(car_price_full=30000, monthly_depreciation=225., monthly_insurance=120.,
                             monthly_maintenance=30., yearly_price_increase=0.0)
honda_hrv.down_payment_time(30000, additional_fee=1000.)
honda_hrv.hold(months=36)
down_payment, _, purchase_payment_by_month, purchase_net_value_by_month = honda_hrv.output_data()

# compare with rental
rental_car = CarRentalModel(month_rent_now=620., yearly_price_increase=0.03, yearly_invest_increase=0.1)
rental_car.start_time(cash=down_payment)
rental_car.hold(months=36, cash_add_schedule=purchase_payment_by_month)
_, _, rental_payment_by_month, rental_net_value_by_month = rental_car.output_data()

plt.plot(purchase_net_value_by_month, label='purchase')
plt.plot(rental_net_value_by_month, label='rental')
plt.legend()
plt.show()

print('db')