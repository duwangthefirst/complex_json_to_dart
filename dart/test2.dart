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