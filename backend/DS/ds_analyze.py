import numpy as np
import pandas as pd
import re
import spacy
import faiss
from pickle import load


def json_reading(json_parser, json_products):
    parser = pd.read_json(json_parser).loc[:,['product_key','price',
                                              'product_name',
                                              'dealer_id']]
    products = pd.read_json(json_products).rename(columns={'id_product': 'id'})
    return parser, products


def csv_reading(path='', prep=True):
    '''
    Функция загрузки данных. по умолчани берет файлы из директории и проводит начальный препроцессинг
    Выдает 4 датафрейма (возможно следует таблицу мэтчей сделать опциональным аргументом, без МО(с учителем) она не нужна)
    Если установить prep=False то загрузит сырые данные как они есть
    '''
    dealers = pd.read_csv(path + 'marketing_dealer.csv', sep=';')
    parser = pd.read_csv(path + 'marketing_dealerprice.csv', sep=';')
    products = pd.read_csv(path + 'marketing_product.csv', sep=';')
    matches = pd.read_csv(path + 'marketing_productdealerkey.csv', sep=';')
    if prep == True:

        # Сортируем диллеров по их ID, выставляем новые индексы
        dealers = (dealers
                   .sort_values('id')
                   .reset_index(drop=True))
    return dealers, parser, products, matches


def text_worker(name):
    '''
    Функция для предварительной очистки текста
    Принимает строку, возвращает строку

    Добавляет пробел на явных стыках, переходах(язык, регистр)
    и на конкретных словах
    Переводит все в нижний регистр
    Убирает название заказчика
    '''
    pattern = [r"([а-я])([a-zA-ZА-Я])",
               r"([А-Я])([A-Za-z])",
               r"([a-z])([A-Zа-яА-Я])"]
    for p in pattern:
        try:
            name = re.sub(p, "\\1 \\2", name)
        except:
            pass
    name = name.lower()
    bad = ['просепт', 'prosept50',
           'prosept50,', 'prosepteco50',
           'prosepteco50,', 'ultra',
           'crystal', '-ая',
           'prosept', 'ф/п']
    good = ['prosept', ' prosept50 ',
            ' prosept50 ', ' prosepteco50 ',
            ' prosepteco50 ', ' ultra ',
            ' crystal ', '',
            '', 'пакет']
    for o, n in zip(bad, good):
        name = name.replace(o, n)
    return name


def change_equal(name):
    '''
    Функция для разделения названия на текст и другие признаки

    Принимает текст, возвращает словарь вида
    {признак: его значение}
    Среди обнаруженных признаков:
    1)Название очищеное от следующих признаков
    2)Артитул (может выстапуть для 100% нахождения соответствующего ID продукта)
    3)Количество/объем цифрой
    4)Еденицы измерения
    Последние 2 признака переводит в общий формат (1000 г->1 кг, 600 мл->0,6 л)
    '''
    name = text_worker(name)
    dictionary = {}
    try:
        article = re.search(r' \d+-\d+/?\d?[а-я]?', name)[0].strip()
        name = name.replace(article, '')
    except:
        article = np.nan
    try:
        v = re.findall(r"\d+(?:[\.,]\d+)? ?(?:мл|кг|г|л|шт)", name)[-1]
        dimension = re.search(r'[млкгшт]+', v)[0]
        quantity = float(v.replace(dimension, '').replace(',', '.'))
        if dimension == 'мл':
            quantity = quantity / 1000
            dimension = 'л'
        elif dimension == 'г':
            quantity = quantity / 1000
            dimension = 'кг'
        name = name.replace(v, '')
    except:
        dimension = np.nan
        quantity = 0
    finally:
        dictionary['name_new'] = ' '.join(re.sub(r'\W+', ' ', name).split(r'\W+'))
        dictionary['article'] = article
        dictionary['dimension'] = dimension
        dictionary['quantity'] = quantity
        return dictionary


def lemmatizate(text, nlp, nlp_ru):
    '''
    Функция лемматизации текста,
    принимает строку и выдает так же строку но все слова в унифицированной форме
    '''

    doc = nlp(text)
    text = " ".join([token.lemma_ for token in doc])
    doc_ru = nlp_ru(text)
    return " ".join([token.lemma_ for token in doc_ru])


def parser_prep(parser):
    '''
    Функция обработки таблицы dealer_price(парсерные данные)
    Применение функции по обработке текста, разделения названия на признаки, лемматизации
    '''
    # Удаляем 3 ненужные колонки, удаляем дубликаты, переименовываем колонку ключа, и выставляем новые индексы
    parser = (parser
              .drop_duplicates()
              .rename(columns={'product_key': 'key'})
              .reset_index(drop=True))
    parser_new = (parser['product_name']
                  .apply(lambda x: change_equal(x)).apply(pd.Series))
    parser_final = (pd.concat([parser, parser_new], axis=1)
                    .drop(['product_name'], axis=1))
    parser_final['article'] = parser_final['article'].fillna('')

    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    nlp_ru = spacy.load('ru_core_news_sm', disable=['parser', 'ner'])
    parser_final['name_new'] = (parser_final['name_new']
                                .apply(lambda x: lemmatizate(x, nlp, nlp_ru)))

    return parser_final


def products_prep(products):
    '''
    Функция обработки таблицы продукции
    Принимает исходную таблицу с проведенной предподготовкой
    Выдает винальный вариант таблицы, который можно использовать в МО

    Заполняет пропуски, собирает в одну колонку уникальные слова из 4 колонок названий, и собирает дополнительные фичи из названий
    '''
    # Удаляем 7 ненужных колонок
    products = (products
                .drop(['ean_13',
                       'category_id', 'ozon_article',
                       'wb_article', 'ym_article',
                       'wb_article_td'], axis=1))
    # заполняем пропуски
    name_columns = ['name_1c', 'ozon_name', 'name', 'wb_name']
    products['name_1c'] = products['name_1c'].fillna(products['name'])
    products['ozon_name'] = products['ozon_name'].fillna(products['name_1c'])
    products[name_columns] = products[name_columns].fillna('')

    # Из субъективно лучшей колонки названия вытаскиваем количество и ед.измерения из остальных только очищеное имя
    name_1c = (products['name_1c']
    .apply(change_equal).apply(pd.Series)
    .rename(columns={'name_new': 'name_1c_new'})['name_1c_new'])
    ozon_name = (products['ozon_name']
                 .apply(change_equal).apply(pd.Series)
                 .drop(['article'], axis=1)
                 .rename(columns={'name_new': 'ozon_name_new'}))
    name_1 = (products['name']
    .apply(change_equal).apply(pd.Series)
    .rename(columns={'name_new': 'name_new'})['name_new'])
    wb_name = (products['wb_name']
    .apply(change_equal).apply(pd.Series)
    .rename(columns={'name_new': 'wb_name_new'})['wb_name_new'])
    products1 = pd.concat([products, ozon_name, name_1c, wb_name, name_1], axis=1)

    # Соединяем названия из 4х колонок в full name (только уникальные слова в том же порядке)
    products1['full_name'] = (products1
                              .apply(lambda x: ' '.join(list(dict.fromkeys((x['name_1c_new'] + ' '
                                                                            + x['ozon_name_new'] + ' '
                                                                            + x['name_new'] + ' '
                                                                            + x['wb_name_new']).split()))), axis=1))

    # лемматизируем
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    nlp_ru = spacy.load('ru_core_news_sm', disable=['parser', 'ner'])
    products1['full_name'] = (products1['full_name']
                              .apply(lambda x: lemmatizate(x, nlp, nlp_ru)))

    products1['article'] = products1['article'].apply(lambda x: str(x).lower())

    # Собираем финальную версию таблицы продукции
    products_final = products1.loc[:, ['id', 'article',
                                       'cost', 'recommended_price',
                                       'full_name', 'dimension',
                                       'quantity']]

    # заполняем пропуски рекомендованной цены медианой
    #products_final['recommended_price'] = (products_final['recommended_price']
    #                                       .fillna(products_final['recommended_price'].median()))
    return products_final


def find_product_id_by_article(article, products_final):
    '''
    Фанкция нахождения id товара по артикулу

    Принимает на вход артикул строкой,
    возвращает id товара из таблицы продукции списком из 1 числа
    '''
    id = []
    if article == '':
        return np.nan
    else:
        try:
            id.append(int(list(
                products_final.loc[products_final['article'] == article].id)[0]))
        except:
            return np.nan
        return id

def accuracy_check(target, dict_of_preds,n):
    '''
    Функция промежуточной проверки точности
    Принимает правильные соответствия в виде словаря, словарь предсказаний и рассматривание количество первы предсказаний
    Выводит текст с оценкой, в переменную никакую не записывается
    '''
    acc = 0
    n_empty = 0
    for key in list(target.keys()):
        n_empty +=int((key not in dict_of_preds)
                      or (dict_of_preds[key]==[]))
        acc += int((key in dict_of_preds)
                   and (target[key] in dict_of_preds[key][:n]))
    try:
        result = round(100 * acc / (len(list(target.keys()))-n_empty),2)
        return (f'В {result}% случаев правильный ответ среди первых {n} предсказаний.'
                f' Количество сравнений: {(len(list(target.keys()))-n_empty)}')
    except ZeroDivisionError:
        return 'Метрика не подсчитана, деление на 0, необходимо проверить условие в функции "accuracy_check"'


def search_neighbors(base_tfidf, query_tfidf):
    '''
    Функция ранжирования и отбора ближайших соседей
    по расстоянию между векторизированными текстами

    Принимает на вход 2 таблицы векторизированного текста
    выдает (base_index) словарь соответствия индекса с id продукта,
    (vecs) список списков расстояний между векторами по возрастанию (n ближайших)
    (idx) список списков ближайших n id продукции в соответствии с (vecs)

    '''
    dims = base_tfidf.shape[1]
    n_cells = 1  # количество центроидов
    quantizer = faiss.IndexFlatL2(dims)
    idx_l2 = faiss.IndexIVFFlat(quantizer, dims, n_cells)
    # подготовка к поиску
    idx_l2.train(np.ascontiguousarray(base_tfidf.values).astype('float32'))
    idx_l2.add(np.ascontiguousarray(base_tfidf.values).astype('float32'))
    # создание словаря для нахождения индекса товара в базовом наборе данных
    base_index = {k: v for k, v in enumerate(base_tfidf.index.to_list())}
    vecs, idx = idx_l2.search(
        np.ascontiguousarray(query_tfidf.values).astype('float32'),
        10)
    return base_index, vecs, idx


def get_neighbors(products_final, parser_final):
    '''
    Функция поиска ближайших соседей
    (включает использование функций обучения векторайзера и самого поиска соседей)
    Если передаем таблицу мэтчей - значит в работу берем только данные с известным ответом и будет показана метрика

    Принимает 2 обработанные таблицы(продукция и парсерные данные) и опционально таблицу мэтчей
    Выдает словарь соответствия ключа предполагаемым 10 id и при зарузке таблицы мэтчей - таргет
    '''
    # Создадим две таблицы. Первая: base - данные производителя, где индексы - это id товаров.
    # Вторая: query - соответствие запроса к парсеру и правильного ответа к продукции
    base = products_final.copy().set_index('id').drop(['cost'], axis=1)
    query = (parser_final
    .groupby('key').first()
    .reset_index()[['key', 'price',
                    'name_new', 'article',
                    'quantity', 'dimension']])

    #загрузка обученного TF-IDF
    with open('DS/korpus_tfidf.pkl', 'rb') as fid:
        count_tf_idf = load(fid)

    base_tfidf = pd.DataFrame(count_tf_idf.transform(base['full_name'])
                              .toarray()).set_index(base.index)
    query_tfidf = pd.DataFrame(count_tf_idf.transform(query['name_new'])
                               .toarray())
    base_tfidf.columns = base_tfidf.columns.astype('str')
    query_tfidf.columns = query_tfidf.columns.astype('str')
    # Поиск соседей функцией
    base_index, vecs, idx = search_neighbors(base_tfidf, query_tfidf)

    # Сборка словаря предсказаний
    dict_of_neighbors = {}
    for k, v in zip(query['key'], idx.tolist()):
        list_of_preds = [base_index[i] for i in v]
        dict_of_neighbors[k] = list_of_preds

    return dict_of_neighbors


def dict_join(dict_all, dict_small):
    '''
    Функция объединения значений двух словарей
    с учетом позиций

    На входе основной и дополнительный словари
    На выходе обновленные основной словарь
    '''
    for key in dict_small.keys():
        # print('Ключ',key)
        # print('Список для этого ключа в исходном словаре',dict_of_neigh[key])
        l1 = dict_all[key]
        l2 = dict_small[key]
        # в этот момент происходит слияние с учетом позиции
        l_all = list(dict.fromkeys(l1 + l2))
        # print(f'В общем словаре по ключу {key} значения: {l1}, в новом такие:{l2}, вместе: {l_all}')
        # print('Замена в этом списке:',dict_of_neigh[key])
        dict_all[key] = l_all
        # print('После замены:',dict_of_neigh[key])
    return dict_all


def main_function(json_parser=0, json_products=0, path=''):
    '''
    Главная функция которая задействует все остальные функции,
    Принимает на вход путь к файлам,
    выдает словарь соответствия ключа предложения диллера с 10 id продукции заказчика

    '''

    # загрузка документов
    parser, products = json_reading(json_parser, json_products)
    #dilers, parser, products, matches = csv_reading(path)
    # преобразование текста(обе таблицы, лемматизация)
    parser_final = parser_prep(parser)
    products_final = products_prep(products)
    # Составляем макет словаря
    dict_of_neigh = dict.fromkeys(parser_final['key'], [])

    # Поиск по артикулу
    dict_of_article_neigh = (pd.DataFrame(parser_final['article']
                                          .apply(lambda x: find_product_id_by_article(x, products_final)))
                                          .set_index(parser_final['key'])
                                          .dropna().to_dict()['article'])
    # Заносим найденное в основной словарь
    dict_of_neigh.update(dict_of_article_neigh)
    # поиск с помощью Tf-idf и faiss
    dict_of_tfidf_neighbors = get_neighbors(products_final,
                                                     parser_final)
    '''
    Эти этапы не реализованы, но предполагают возможное внедрение для улучшения точности
    # сборка каждый к каждому(query-base)

    #train-test split

    # классификация через модель

    # отбор топ-n по predict-proba
    '''

    # Сбрка финального словаря предсказаний
    dict_of_neighbors = dict_join(dict_of_neigh, dict_of_tfidf_neighbors)
    return dict_of_neighbors
