# Печатные газеты использовали свой формат дат для каждого выпуска. Для каждой газеты из списка напишите формат указанной даты для перевода в объект datetime:
# The Moscow Times — Wednesday, October 2, 2002
# The Guardian — Friday, 11.10.13
# Daily News — Thursday, 18 August 1970

from datetime import datetime

moscow_times_date = "Wednesday, October 2, 2002"
moscow_times_format = "%A, %B %d, %Y"
moscow_times_dt = datetime.strptime(moscow_times_date, moscow_times_format)

guardian_date = "Friday, 11.10.13"
guardian_format = "%A, %d.%m.%y"
guardian_dt = datetime.strptime(guardian_date, guardian_format)

daily_news_date = "Thursday, 18 August 1970"
daily_news_format = "%A, %d %B %Y"
daily_news_dt = datetime.strptime(daily_news_date, daily_news_format)

print("Форматы:")
print(f"The Moscow Times: {moscow_times_dt}")
print(f"The Guardian: {guardian_dt}")
print(f"Daily News: {daily_news_dt}")
