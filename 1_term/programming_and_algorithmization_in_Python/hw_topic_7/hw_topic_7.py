import csv

class Client:
  def __init__(self, name, device_type, browser, sex, age, bill, region):
    self.name = name
    self.device_type = device_type
    self.browser = browser
    self.sex = sex
    self.age = age
    self.bill = bill
    self.region = region

  def translate_gender(self):
    return 'мужского пола' if self.sex == 'male' else 'женского пола'

  def translate_verb(self):
    return 'совершил' if self.sex == 'male' else 'совершила'

  def translate_device(self):
    devices = {
      'mobile': 'мобильного',
      'tablet': 'планшетного',
      'laptop': 'ноутбучного',
      'desktop': 'стационарного'
    }
    return devices.get(self.device_type, self.device_type)

  def generate_description(self):
    gender_text = self.translate_gender()
    verb = self.translate_verb()
    device_text = self.translate_device()

    description = f'Пользователь {self.name} {gender_text}, {self.age} лет {verb} покупку на {self.bill} у.е. с {device_text} браузера {self.browser}. Регион, из которого совершалась покупка: {self.region}.'

    return description


class ClientProcessor:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def load_clients(self):
    with open(self.input_file) as f:
      reader = csv.reader(f)
      next(reader)
      for row in reader:
        name, device_type, browser, sex, age, bill, region = row
        yield Client(name, device_type, browser, sex, age, bill, region)
        #Решил сделать через генератор, если большие файлы с клиентами - не хочется хранить их в памяти) 

  def process(self):
    with open(self.output_file, 'w') as f:
      for client in self.load_clients():
        description = client.generate_description()
        f.write(description + '\n')


def main():
  processor = ClientProcessor('web_clients_correct.csv', 'web_clients_correct.txt')
  processor.process()

main()
