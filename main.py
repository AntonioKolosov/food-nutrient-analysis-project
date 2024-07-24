import pandas as pd


def convert_col_int(df):
    '''Convert the specified column to int'''
    for col in df.columns:
        if col == 'gtin_upc':
            df[col] = pd.to_numeric(df[col],
                                    errors='coerce').fillna(0).astype(int)
    return df


def convert_col_str(df):
    '''Convert all columns with object format to string'''
    exclude_col = 'gtin_upc'
    for col in df.select_dtypes(include=['object']).columns:
        if col != exclude_col:
            df[col] = df[col].astype('string')
    return df


def convert_col_dt(df):
    '''Convert specified columns to date format'''
    date_col = ['modified_date', 'available_date']
    for col in date_col:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col],
                                         format='%Y-%m-%d',
                                         errors='coerce')
            except Exception as e:
                print(f"Error during processing {col}: {e}")
    return df


def main():
    '''Main flow'''
    df = pd.read_csv('food.csv', parse_dates=True, low_memory=False)
    print(f"DataFrame загружен, количество строк: {len(df)}")
    print(df.head())

    # Преобразование столбцов в формат даты
    df = convert_col_dt(df)
    print("Типы данных после преобразования в дату:")
    print(df.dtypes)

    # Преобразование столбцов в строковый формат
    df = convert_col_str(df)

    # Преобразование столбца в целочисленный формат
    df = convert_col_int(df)

    # Вывод первых строк до очистки
    print("Первые строки до очистки:")
    print(df.head())

    # Проверка количества NaN в каждом столбце
    print("Количество NaN в каждом столбце до очистки:")
    print(df.isna().sum())

    # Проверка количества дубликатов
    print("Количество дубликатов до очистки:", df.duplicated().sum())

    # Удаление строк с NaN только в критичных столбцах
    critical_columns = ['fdc_id',
                        'gtin_upc',
                        'modified_date',
                        'available_date']
    df.dropna(subset=critical_columns,
              inplace=True)

    # Проверка строк после удаления NaN в критичных столбцах
    print(f"После удаления NaN в критичных столбцах: {len(df)}")

    # Удаление дубликатов
    df.drop_duplicates(inplace=True)
    print(f"Количество строк после удаления дубликатов: {len(df)}")

    if not df.empty:
        cleaned_file_path = 'cleaned_food.csv'
        df.to_csv(cleaned_file_path, index=False)
        print(f"Очищенные данные сохранены в файл: {cleaned_file_path}")
    else:
        print("После удаления NaN и дубликатов ничего не сохранено.")

    # Вывод результатов для проверки
    print("Типы данных после всех преобразований:")
    print(df.dtypes)
    print("Первые строки после всех преобразований:")
    print(df.head())


if __name__ == '__main__':
    main()
