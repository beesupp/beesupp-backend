import iyzipay
import json

options = {
    'api_key': "sandbox-6jKATeTIvudx0u0duGF1QxDL1zKY4C2u",
    'secret_key': "sandbox-yagJo0AZzSaDVGG3ekuGhRS11gCRvPJc",
    'base_url': iyzipay.base_url
}

payment_card = {
    'cardHolderName': 'John Doe',
    'cardNumber': '5528790000000008',
    'expireMonth': '12',
    'expireYear': '2030',
    'cvc': '123',
    'registerCard': '0'
}

buyer = {
    'id': 'BY789',
    'name': 'Ertan',
    'surname': 'Uysal',
    'gsmNumber': '+905350000000',
    'email': 'email@email.com',
    'identityNumber': '74300864791',
    'lastLoginDate': '2015-10-05 12:43:35',
    'registrationDate': '2013-04-21 15:12:09',
    'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
    'ip': '85.34.78.112',
    'city': 'Istanbul',
    'country': 'Turkey',
    'zipCode': '34732'
}

address = {
    'contactName': 'Jane Doe',
    'city': 'Istanbul',
    'country': 'Turkey',
    'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
    'zipCode': '34732'
}

def buy(item_name):
    basket_items = [
        {
            'id': 'BI101',
            'name': item_name,
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '1000'
        }
    ]
    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': '1000',
        'currency': 'USD',
        'installment': '1',
        'basketId': 'B67832',
        'paymentChannel': 'WEB',
        'paymentGroup': 'PRODUCT',
        'paymentCard': payment_card,
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items
    }
    payment = iyzipay.Payment().create(request, options)
    payment_result = json.loads(payment.read().decode('utf-8'))
    if payment_result['status'] == "success":
        return True
    else:
        return False