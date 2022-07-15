class Test1 {

  Apple? a;
  List<int>? e;
  List<Product>? product_list;

  Test1({
    this.a, this.e, this.product_list
  });

  Test1.fromJson(Map<String, dynamic> json) {
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