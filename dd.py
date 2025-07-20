# scraped_prices = [
#     "",
#     "",
#     "100,50",
#     "5,80",
#     "",
#     "",
#     "25,99",
#     "",
#     "17,50",
#     "",
#     "0,95",
#     "99,00",
#     "",
# ]
#
# i = 0
#
# while i < len(scraped_prices):
#
#     item = scraped_prices[i]
#
#     if item:
#         scraped_prices[i] = float(item.replace(",", "."))
#         i += 1
#     else:
#         scraped_prices.pop(i)
#
#
# print(scraped_prices)
from api.api_v1.dependencies import basic_auth_for_unsafe_methods

numbers = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]


for number in numbers:
    short = numbers.index(number)
    if short % 3 == 0 and short != 0:
        print()

    print(number.center(3), end="")
