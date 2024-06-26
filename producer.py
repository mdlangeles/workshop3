from kafka import KafkaProducer
from json import dumps
import pandas as pd
from time import sleep
import datetime as dt
from service.transformationsFS import continent, delete_columns, convert_to_dummy


def test_data():
    df_test = pd.read_csv("Data/x_test.csv")
    if 'country' in df_test.columns:
        df_test['continent'] = df_test['country'].apply(continent) 
    else:
        raise ValueError("Column 'country' not found in DataFrame.")
    
    df_test= delete_columns(df_test)
    df_test = convert_to_dummy(df_test)

    y_test = pd.read_csv("Data/y_test.csv")
    df_test['happiness_score'] = y_test

    return df_test


def producer_kafka(df_test):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )
    for i in range(len(df_test)):
        row_json = df_test.iloc[i].to_json()
        producer.send("test-data", value=row_json)
        print(f"Message sent at {dt.datetime.utcnow()}")
        sleep(2)

    print("The rows were sent successfully!")


if __name__ == '__main__':
    df_test = test_data()
    producer_kafka(df_test)
