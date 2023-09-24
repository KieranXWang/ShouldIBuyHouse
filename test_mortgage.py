from mortgage import Mortgage

test_mortgage = Mortgage(interest=0.03, months=12*30, amount=450000*0.8)

i = 0
for principle, interest, balance in test_mortgage.monthly_payment_schedule():
    print(f"{i} \t {principle} \t {interest} \t {balance}")
    i += 1

