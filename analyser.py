import pandas
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
    df_gpus = pd.read_csv(gpu_data_path, sep=';', decimal=',', index_col=0)  # dataframe of all gpu listings
    df_gpus.price = pd.to_numeric(df_gpus.price.replace(r'\.', '', regex=True).replace(',', '.', regex=True))

    with open(gpu_price_requirements) as f:
        gpu_prices = [tuple(line) for line in csv.reader(f)]

    df_gpu_deals = pd.DataFrame(data=None, columns=['title', 'price', 'link'])  # dataframe of all gpu listing that
    # match the model and price criteria

    for gpu, price in gpu_prices:
        regex = make_regex(gpu)
        gpu_model_deals = df_gpus['title'].str.contains(rf'(?i){regex}')  # (?i) -> case insensitive
        gpu_model_deals = df_gpus[gpu_model_deals]  # all listings that match specific gpu model name
        # all listings that match specific gpu model name AND are under the set max price
        gpu_model_deals = gpu_model_deals[gpu_model_deals['price'] <= float(price)]

        df_gpu_deals = pd.concat([df_gpu_deals, gpu_model_deals[['title', 'price', 'link']]], ignore_index=True, axis=0)

    return df_gpu_deals
