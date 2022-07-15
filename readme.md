### complex json to dart

#### 1. feature
- I wrote this script to generate dart model from json files in my flutter project, just run `batch_transform("path/to/flutter_project/assets/json/", "path/to/flutter_project/lib/model/")` and boom~~~ the code will be generated for you.
- suport custom bean name(including sub object) with simple `__DICT_OF_` annotation
  - `"f__DICT_OF_Bean": { "text": "blablabla" }` will generate a field named "f" with type "`Bean`"
  - `"f_list__DICT_OF_Bean": [{ "text": "blablabla" }, { "text": "blablabla" }]` will generate a field named "f_list" with type "`List<Bean>`"
- support complex json, for example:
  - embedded object:
    - ```json
      {
        "a": {
          "b": {
            "c": {
              "name": "complex json with embedded object"
            }
          }
        }
      }
      ```
  - list of object:
    - ```json
      {
        "product_list__DICT_OF_Product": [
          {
            "name": "product 1",
            "is_on_sale": true,
            "available": 18,
            "price": 13.33,
            "other": null
          },
          {
            "name": "product 2",
            "is_on_sale": true,
            "available": 99,
            "price": 10.33,
            "other": null
          }
        ]
      }
      ```


#### 2. usage
just one single main.py file.
just edit the following block of code: (will transform all the json file in ./json/, and save all generated dart file to ./dart/ )
```python

if __name__ == '__main__':
    batch_transform("./json/", "./dart/")

# the end of main.py file
```

and then create venv and run the script:

```bash
cd complex_json_to_dart
python3 -m venv ./venv
# for mac
source ./venv/bin/activate
# for windows
./venv/ben/activate.bat

pip install -r requirements.txt

python main.py
```

#### 3. demo
##### 3.1 demo 1: complex json with custom bean name
**input test1.json:**
```json
{
  "a__DICT_OF_Apple": {
    "b__DICT_OF_Banana": {
      "c__DICT_OF_Cocktail": {
        "name": "complex json with embedded object"
      }
    }
  },
  "e": [1, 2, 3],
  "product_list__DICT_OF_Product": [
    {
      "name": "product 1",
      "is_on_sale": true,
      "available": 18,
      "price": 13.33,
      "other": null
    },
    {
      "name": "product 2",
      "is_on_sale": true,
      "available": 99,
      "price": 10.33,
      "other": null
    }
  ]
}
```
**output test1.dart:**
```dart
class Test2 {

  Apple? a;
  List<int>? e;
  List<Product>? product_list;

  Test2({
    this.a, this.e, this.product_list
  });

  Test2.fromJson(Map<String, dynamic> json) {
    a = json['a']!=null ? Apple.fromJson(json['a']) : null;
    e = json['e'].cast<int>();
    product_list = (json['product_list'] as List<dynamic>?)?.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(a != null) data['a'] = a!.toJson();
    data['e'] = e;
    if(product_list != null) data['product_list'] = product_list!.map((e) => e.toJson()).toList();
    return data;
  }
}

class Apple {

  Banana? b;

  Apple({
    this.b
  });

  Apple.fromJson(Map<String, dynamic> json) {
    b = json['b']!=null ? Banana.fromJson(json['b']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(b != null) data['b'] = b!.toJson();
    return data;
  }
}

class Banana {

  Cocktail? c;

  Banana({
    this.c
  });

  Banana.fromJson(Map<String, dynamic> json) {
    c = json['c']!=null ? Cocktail.fromJson(json['c']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(c != null) data['c'] = c!.toJson();
    return data;
  }
}

class Cocktail {

  String? name;

  Cocktail({
    this.name
  });

  Cocktail.fromJson(Map<String, dynamic> json) {
    name = json['name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['name'] = name;
    return data;
  }
}

class Product {

  String? name;
  bool? is_on_sale;
  int? available;
  double? price;
  Other? other;

  Product({
    this.name, this.is_on_sale, this.available, this.price, this.other
  });

  Product.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    is_on_sale = json['is_on_sale'];
    available = json['available'];
    price = json['price'];
    other = json['other']!=null ? Other.fromJson(json['other']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['name'] = name;
    data['is_on_sale'] = is_on_sale;
    data['available'] = available;
    data['price'] = price;
    if(other != null) data['other'] = other!.toJson();
    return data;
  }
}
```

##### 3.2 demo2: complex json without custom bean name

**input test2.json:**
```json
{
  "a": {
    "b": {
      "c": {
        "name": "complex json with embedded object"
      }
    }
  },
  "e": [1, 2, 3],
  "product_list": [
    {
      "name": "product 1",
      "is_on_sale": true,
      "available": 18,
      "price": 13.33,
      "other": null
    },
    {
      "name": "product 2",
      "is_on_sale": true,
      "available": 99,
      "price": 10.33,
      "other": null
    }
  ]
}

```
**output test2.dart:**
```dart
class Test2 {

  A? a;
  List<int>? e;
  List<ProductList>? product_list;

  Test2({
    this.a, this.e, this.product_list
  });

  Test2.fromJson(Map<String, dynamic> json) {
    a = json['a']!=null ? A.fromJson(json['a']) : null;
    e = json['e'].cast<int>();
    product_list = (json['product_list'] as List<dynamic>?)?.map((e) => ProductList.fromJson(e as Map<String, dynamic>)).toList();
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(a != null) data['a'] = a!.toJson();
    data['e'] = e;
    if(product_list != null) data['product_list'] = product_list!.map((e) => e.toJson()).toList();
    return data;
  }
}

class A {

  B? b;

  A({
    this.b
  });

  A.fromJson(Map<String, dynamic> json) {
    b = json['b']!=null ? B.fromJson(json['b']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(b != null) data['b'] = b!.toJson();
    return data;
  }
}

class B {

  C? c;

  B({
    this.c
  });

  B.fromJson(Map<String, dynamic> json) {
    c = json['c']!=null ? C.fromJson(json['c']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    if(c != null) data['c'] = c!.toJson();
    return data;
  }
}

class C {

  String? name;

  C({
    this.name
  });

  C.fromJson(Map<String, dynamic> json) {
    name = json['name'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['name'] = name;
    return data;
  }
}

class ProductList {

  String? name;
  bool? is_on_sale;
  int? available;
  double? price;
  Other? other;

  ProductList({
    this.name, this.is_on_sale, this.available, this.price, this.other
  });

  ProductList.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    is_on_sale = json['is_on_sale'];
    available = json['available'];
    price = json['price'];
    other = json['other']!=null ? Other.fromJson(json['other']) : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['name'] = name;
    data['is_on_sale'] = is_on_sale;
    data['available'] = available;
    data['price'] = price;
    if(other != null) data['other'] = other!.toJson();
    return data;
  }
}

```