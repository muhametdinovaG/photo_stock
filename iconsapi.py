import requests


def change_model(item):
    model = {
        'id': item['id'],
        'url': item['jpgAsset']['url'],
        'width': item['jpgAsset']['width'],
        'height': item['jpgAsset']['height'],
        'weight': item['weight'],
        'mp': round(item['jpgAsset']['width'] * item['jpgAsset']['height'] / 10 ** 6, 1),
        'px': item['jpgAsset']['width'] * item['jpgAsset']['height']
    }
    return model


class IconsApi:
    per_page = None

    def __init__(self, per_page=10):
        self.per_page = per_page

    def get_models(self, page=1):
        endpoint = "https://demo-photos.icons8.com/api/v1/models?related_by=folder&sort_by=weight&direction=desc" \
                   "&filter=all&page={0}&per_page={1}".format(page, self.per_page)
        response = requests.get(endpoint)
        result = response.json()
        data = map(change_model, result['models'])
        return list(data)
