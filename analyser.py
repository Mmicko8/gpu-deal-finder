import pandas as pd
import csv


def make_regex(gpu_model):
    """
    Makes a regex that matches the specified gpu model
    :param gpu_model: name of the gpu model
    :return: the regex that matches the specified gpu model
    """
    regex = ''
    for x in gpu_model.split():
        regex += rf'[ ]?{x}'
    regex += rf'(?![ ]?ti|[ ]?super)'  # so that gtx 1080 doesn't match gtx 1080 ti or super
    return regex


def analyse(gpu_data_path, gpu_price_requirements):
    """
    Returns gpu listings which fit the model and price requirements.

    :param gpu_data_path: path of the file where all the gpu_listings are stored
    :param gpu_price_requirements: path of the file where the GPU model and price requirements are stored
    :return: Pandas DataFrame that contains gpu listings which fit the model and price requirements.
    """
    df = pd.read_csv(gpu_data_path, sep=';', decimal=',', index_col=0)
    df.price = pd.to_numeric(df.price.replace(r'\.', '', regex=True).replace(',', '.', regex=True))

    with open(gpu_price_requirements) as f:
        gpu_prices = [tuple(line) for line in csv.reader(f)]

    df_analysed = pd.DataFrame(data=None, columns=['title', 'price', 'link'])

    for gpu, price in gpu_prices:
        regex = make_regex(gpu)
        gpu_deals = df['title'].str.contains(rf'(?i){regex}')
        gpu_deals = df[gpu_deals]
        gpu_deals = gpu_deals[gpu_deals['price'] <= float(price)]
        df_analysed = df_analysed.append(gpu_deals[['title', 'price', 'link']], ignore_index=True)  # TODO replace with concat

        print("\n\n")
        print(df_analysed)

    print("\n\n######################################################\n")
    print(df_analysed)
    return df_analysed


# print(analyse('data/mainTest.csv'))
