import streamlit as st
import pandas as pd
import math
from bitarray import bitarray
import os.path

#фильтр Блума
class BloomFilter(object):

    def __init__(self, size, number_expected_elements=100):
        self.size = size
        self.number_expected_elements = number_expected_elements

        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)

        self.number_hash_functions = round((self.size / self.number_expected_elements) * math.log(2))


    def _hash_djb2(self, s):
        hash = 5381
        for x in s:
            hash = ((hash << 5) + hash) + ord(x)
        return hash % self.size


    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)


    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1


    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return True
        return False

key_word_array = ["данные о инсультах", "инсульт", "гипертония", "болезнь сердца", "уровень глюкозы"]
description_array = ["Таблица хранит данные о инсультах. Она нужна для выявления людей, которые подвержены инсульту больше всего. В таблице записывается пол, возраст, гипертония, болезнь сердца, человек женат или холост, статус работы, место жительства, средний уровень глюкозы, индекс массы тела, статус курения, инсульт."]
filename_array = ["healthcare-dataset-stroke-data.csv"]

st.subheader('Добавление данных в сервис')

#добавляем ключевые слова в фильтр Блума
add_word_key = st.text_input("Введите ключевое слово из вашего набора данных")
def add_key():
    if add_word_key:
        if add_word_key in key_word_array:
            st.error("Такое ключевое слово уже есть! P.S. Ничего страшного, придумайте еще слово, которое отображает именно ваши данные. Либо просто не добавляйте ключевое слово, ваши данные все равно найдутся!")
        else:
            key_word_array.append(add_word_key)
            st.success("Ключевое слово добавлено!")

#добавляем описание в список описаний
add_description = st.text_input("Введите краткое описание вашего набора данных")
description_array.append(add_description)
def add_desk():
    if add_description:
        if add_description in description_array:
            st.error(
                "Такое описание уже есть! P.S Такого быть не должно, так как описание данных у всех различное!")
        else:
            key_word_array.append(add_word_key)
            st.success("Описание добавлено!")

#метод сохранения файлика в проекте
def save_uploaded_file(uploadedfile):
  with open(os.path.join("", uploadedfile.name), "wb") as f:
     f.write(uploadedfile.getbuffer())
  return st.success("Saved file :".format(uploadedfile.name))

#Drag-and-Drop
add_csv_file = st.file_uploader("Добавьте csv файл")
def add_csv():
    if add_csv_file is not None:
        file_details = {"FileName":add_csv_file.name,"FileType":add_csv_file.type}
        save_uploaded_file(add_csv_file)
        filename_array.append(add_csv_file.name)

if st.button('Добавить данные'):
    if add_description and add_csv_file is not None:
        add_desk()
        add_csv()
    else:
        st.error("Какие-то данные не введены!")


st.subheader('Поиск данных')
bloom_filter = BloomFilter(200, 100)

for i in range(len(key_word_array)):
    bloom_filter.add_to_filter(key_word_array[i])

#поиск данных по ключевому слову
search_word_key = st.text_input("Введите ключевое слово")
if search_word_key:
    if not bloom_filter.check_is_not_in_filter(search_word_key):
        st.write("Данные по ключевому слову ", search_word_key, " найдены.")
        for i in range(len(description_array)):
            if search_word_key.lower() in description_array[i].lower():
                st.write(pd.read_csv(filename_array[i]))
    else:
        st.write("Данные по ключевому слову ", search_word_key, " не найдены.")


st.subheader('Информационный блок')
st.write(key_word_array)
st.write(description_array)
st.write(filename_array)
