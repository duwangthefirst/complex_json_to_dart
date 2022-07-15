from jinja2 import Template
import json
import os
import re


class JsonToDart(object):
    def __init__(self, class_name, member_list, template_path="./dart_object_template.txt"):
        self.class_name = class_name
        self.member_list = member_list
        self.template_path = template_path

    def load_template(self):
        if not os.path.exists(self.template_path):
            print("template_path: {} 文件不存在".format(self.template_path))
            return None
        else:
            with open(self.template_path, 'r') as f:
                return Template(f.read())

    def generate_block_of_member_definition(self):
        result_list = []
        for member in self.member_list:
            if member['is_list']:
                result_list.append("List<{}>? {};".format(member['type'], member['name']))
            else:
                result_list.append("{}{} {};".format(member['type'], "" if member['type'] == "dynamic" else "?", member['name']))
        return "\n  ".join(result_list)

    def generate_block_of_construct_argument(self):
        result_list = []
        for member in self.member_list:
            result_list.append("this.{}".format(member['name']))
        return ", ".join(result_list)

    def generate_block_of_from_json(self):
        result_list = []
        for member in self.member_list:
            if member['is_list']:
                if member['type'] in ("String", "double", "bool", "int", "dynamic"):
                    result_list.append("{} = json['{}'].cast<{}>();".format(member['name'], member['name'], member['type']))
                else:
                    result_list.append("{} = (json['{}'] as List<dynamic>?)?.map((e) => {}.fromJson(e as Map<String, dynamic>)).toList();".format(member['name'], member['name'], member['type']))
            else:
                if member['type'] in ("String", "double", "bool", "int", "dynamic"):
                    result_list.append("{} = json['{}'];".format(member['name'], member['name']))
                else:
                    result_list.append("{} = json['{}']!=null ? {}.fromJson(json['{}']) : null;".format(member['name'], member['name'], member['type'], member['name']))
        return "\n    ".join(result_list)

    def generate_block_of_to_json(self):
        result_list = ["final Map<String, dynamic> data = <String, dynamic>{};"]
        for member in self.member_list:
            if member['is_list']:
                if member['type'] in ("String", "double", "bool", "int", "dynamic"):
                    result_list.append("data['{}'] = {};".format(member['name'], member['name']))
                else:
                    result_list.append("if({} != null) data['{}'] = {}!.map((e) => e.toJson()).toList();".format(member['name'], member['name'], member['name']))
            else:
                if member['type'] in ("String", "double", "bool", "int", "dynamic"):
                    result_list.append("data['{}'] = {};".format(member['name'], member['name']))
                else:
                    result_list.append("if({} != null) data['{}'] = {}!.toJson();".format(member['name'], member['name'], member['name']))
        result_list.append("return data;")
        return "\n    ".join(result_list)

    def save_dart_code(self, content):
        with open(self.class_name + ".dart", "w") as f:
            f.write(content)

    def generate(self):
        template = self.load_template()
        if template:
            block_of_member_definition = self.generate_block_of_member_definition()
            block_of_construct_argument = self.generate_block_of_construct_argument()
            block_of_from_json = self.generate_block_of_from_json()
            block_of_to_json = self.generate_block_of_to_json()
            dart_code = template.render(class_name=self.class_name,
                                        block_of_member_definition=block_of_member_definition,
                                        block_of_construct_argument=block_of_construct_argument,
                                        block_of_from_json=block_of_from_json,
                                        block_of_to_json=block_of_to_json)
            # self.save_dart_code(dart_code)
            return dart_code


class ComplexJsonToDart(object):
    def __init__(self, json_path, dart_path):
        self.json_path = json_path
        class_name, root_json_object = self.load_json()
        self.id_to_member_list, self.id_to_class_name = self.analysis_json(root_json_object, class_name)

        self.dart_path = dart_path

    def load_json(self):
        if not os.path.exists(self.json_path):
            print('json_path对应的文件不存在：{}'.format(self.json_path))
            return
        _, filename = os.path.split(self.json_path)
        filename_splits = filename.split('.')
        if len(filename_splits) != 2:
            print('json文件名必须只含一个"."')
            return
        file, ext = filename_splits
        class_name = self.normalize_name(file)
        # 获取json对象
        with open(self.json_path, 'r') as f:
            json_obj = json.load(f)
        return class_name, json_obj

    def construct_member(self, name, type, is_list=False):
        if self.is_custom_name(name):
            type = self.extract_custom_class_name(name)
            name = self.remove_custom_ext(name)
        elif type == "dynamic":
            type = self.normalize_name(name)
        return {
            "name": name,
            "type": type,
            "is_list": is_list,
        }

    # 判断是否自定义了字段对应的子类名称
    def is_custom_name(self, input):
        return "__DICT_OF_" in input

    # 获取自定义类名
    def extract_custom_class_name(self, input):
        return self.normalize_name(self.get_custom_dict_class_name(input) if self.is_custom_name(input) else input)

    def remove_custom_ext(self, input):
        return re.sub(r'__DICT_OF_[a-zA-Z_]+', '', input)

    def normalize_name(self, input):
        # 将包含下划线的文件名改成驼峰格式，作为类名
        output = input
        # 首字母大写
        output = re.sub(r'^[a-z]', lambda x: x[0].upper(), output)
        # _a改为A, ..., _z改为Z
        output = re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), output) if '_' in output else output
        return output

    def get_custom_dict_class_name(self, input):
        output = re.search(r'__DICT_OF_([a-zA-Z_]+)$', input)
        if output is None:
            return input
        else:
            return output.group(1)

    def get_dict_id(self, json_obj):
        key_list = [self.remove_custom_ext(k) for k in json_obj.keys()]
        sorted(key_list)
        id = "__".join(key_list)
        return id

    def analysis_json(self, json_node, class_name):
        if type(json_node) is not dict:
            print("json_node必须是dict类型")
            return
        id_to_member_list = dict()
        id_to_class_name = dict()
        dict_id = self.get_dict_id(json_node)
        id_to_member_list[dict_id] = []
        id_to_class_name[dict_id] = class_name
        for k, v in json_node.items():
            node_type = type(v)
            if v is None:
                id_to_member_list[dict_id].append(self.construct_member(k, "dynamic"))
            elif node_type is str:
                id_to_member_list[dict_id].append(self.construct_member(k, "String"))
            elif node_type is bool:
                id_to_member_list[dict_id].append(self.construct_member(k, "bool"))
            elif node_type is int:
                id_to_member_list[dict_id].append(self.construct_member(k, "int"))
            elif node_type is float:
                id_to_member_list[dict_id].append(self.construct_member(k, "double"))
            elif node_type is dict:
                v_id = self.get_dict_id(v)
                if v_id not in id_to_class_name.keys():
                    v_id_to_member_list, v_id_to_class_name = self.analysis_json(v, self.extract_custom_class_name(k))
                    for m, n in v_id_to_member_list.items():
                        if m not in id_to_member_list:
                            id_to_member_list[m] = n
                    for p, q in v_id_to_class_name.items():
                        if p not in id_to_class_name:
                            id_to_class_name[p] = q
                    id_to_member_list[dict_id].append(self.construct_member(k, v_id_to_class_name[v_id]))
                else:
                    id_to_member_list[dict_id].append(self.construct_member(k, id_to_class_name[v_id]))
            elif node_type is list or node_type is tuple:
                if len(v) > 0:
                    if all(isinstance(x, str) for x in v):
                        id_to_member_list[dict_id].append(self.construct_member(k, "String", is_list=True))
                    elif all(isinstance(x, int) for x in v):
                        id_to_member_list[dict_id].append(self.construct_member(k, "int", is_list=True))
                    elif all(isinstance(x, float) for x in v):
                        id_to_member_list[dict_id].append(self.construct_member(k, "double", is_list=True))
                    elif all(isinstance(x, bool) for x in v):
                        id_to_member_list[dict_id].append(self.construct_member(k, "bool", is_list=True))
                    elif all(isinstance(x, dict) for x in v):
                        v_id = self.get_dict_id(v[0])
                        if v_id not in id_to_class_name.keys():
                            v_id_to_member_list, v_id_to_class_name = self.analysis_json(v[0], self.extract_custom_class_name(k))
                            for m, n in v_id_to_member_list.items():
                                if m not in id_to_member_list:
                                    id_to_member_list[m] = n
                            for p, q in v_id_to_class_name.items():
                                if p not in id_to_class_name:
                                    id_to_class_name[p] = q
                            id_to_member_list[dict_id].append(self.construct_member(k, v_id_to_class_name[v_id], is_list=True))
                        else:
                            id_to_member_list[dict_id].append(self.construct_member(k, id_to_class_name[v_id], is_list=True))
                    else:
                        print("错误：数组的元素类型不一致")
                        id_to_member_list[dict_id].append(self.construct_member(k, "dynamic", is_list=True))
                else:
                    id_to_member_list[dict_id].append(self.construct_member(k, "dynamic", is_list=True))
        return id_to_member_list, id_to_class_name

    def generate(self):
        result_list = []
        if self.id_to_class_name.keys() != self.id_to_member_list.keys():
            print("错误：self.id_to_class_name.keys() != self.id_to_member_list.keys():")
            return None
        else:
            for id in self.id_to_class_name:
                class_name = self.id_to_class_name[id]
                member_list = self.id_to_member_list[id]
                result_list.append(JsonToDart(class_name, member_list).generate())
        content = "\n\n".join(result_list)
        with open(self.dart_path, "w") as f:
            f.write(content)


def batch_transform(json_dir, dart_dir):
    if not os.path.exists(dart_dir):
        os.makedirs(dart_dir)
    for json_file in os.listdir(json_dir):
        if json_file.endswith(".json"):
            dart_file = json_file.replace(".json", ".dart")
            dart_path = os.path.join(dart_dir, dart_file)
            json_path = os.path.join(json_dir, json_file)
            print("正在处理{}，结果将保存至{}".format(json_path, dart_path))
            ComplexJsonToDart(json_path, dart_path).generate()


if __name__ == '__main__':
    batch_transform("./json/", "./dart/")
