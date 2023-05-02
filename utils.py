import csv
import json

CATEGORIES_MODEL = "ads.Category"
CSV_FILE_CATEGORIES = 'datasets/category.csv'
JSON_FILE_CATEGORIES = 'datasets/category.json'

AD_MODEL = "ads.Ad"
CSV_FILE_AD = 'datasets/ad.csv'
JSON_FILE_AD = 'datasets/ad.json'

LOCATION_MODEL = "users.Location"
CSV_FILE_LOCATION = 'datasets/location.csv'
JSON_FILE_LOCATION = 'datasets/location.json'

USER_MODEL = "users.User"
CSV_FILE_USER = 'datasets/user.csv'
JSON_FILE_USER = 'datasets/user.json'


def csv_to_json(file_csv, file_json, model):
    json_list = []
    with open(file_csv, encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv)
        for row in reader:
            record_dict = {"model": model}
            if model == AD_MODEL:
                del row['Id']
                row['price'] = float(row['price'])
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            else:
                del row['id']
            record_dict['fields'] = row

            json_list.append(record_dict)

    json_object = json.dumps(json_list, indent=4, ensure_ascii=False)
    with open(file_json, 'w', encoding='utf-8') as file:
        file.write(json_object)


csv_to_json(CSV_FILE_CATEGORIES, JSON_FILE_CATEGORIES, CATEGORIES_MODEL)
csv_to_json(CSV_FILE_AD, JSON_FILE_AD, AD_MODEL)
csv_to_json(CSV_FILE_LOCATION, JSON_FILE_LOCATION, LOCATION_MODEL)
csv_to_json(CSV_FILE_USER, JSON_FILE_USER, USER_MODEL)