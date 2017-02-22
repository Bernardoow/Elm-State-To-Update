# -*- coding: utf-8 -*-

'''
Created on 2016/11/27
Updated on 2016/01/14
__author__ = "Bernardo Gomes de Abreu"
__email__ = "bgomesdeabreu@gmail.com"
'''

import sublime, sublime_plugin
import re


class BaseConvertCommand(sublime_plugin.TextCommand):
    pattern_file = re.compile(r"(.*).py$")
    TO_CLIPBOARD = False

    def run(self, edit):
        self.find_class_and_fields(self.view, edit)

    def is_enabled(self):
        return True
        # return self.view.file_name() is None \
        #     or re.search(self.pattern_file, self.view.file_name() or "") is not None

    def check_pattern(self, string, patterns):
        for pattern in patterns:
            matchObj = re.match(pattern, string)
            if matchObj:
                return "'" + matchObj.group(1).strip() + "', "
        return ''

    def _return_params(self, list_of_params):
        text = " "
        dict_params = {
            "String": {'name': 'string', 'count': 0},
            "Int": {'name': 'int', 'count': 0},
            "Bool": {'name': 'bool', 'count': 0},
            "Float": {'name': 'float', 'count': 0},
            "Char": {'name': 'char', 'count': 0},
            "Number": {'name': 'number', 'count': 0}

        }
        for param in list_of_params:
            if param not in dict_params:
                dict_params.update({param : {'name': param.lower(), 'count': 0}})
            _param = dict_params[param]
            text += _param['name'] + str(_param['count']) + " "
            dict_params[param]['count'] += 1
        return text

    def _check_http(self, text):
        return "Result Http.Error " in text

    def _return_params_http(self, text):
        #"TODO"
        #if was tuple?

        return ""

    def _finish_text(self, text, params=None):
        if params:
            return text + params +" ->\n model ! []" + "\n"
        return text +" ->\n model ! []" + "\n"

    def find_class_and_fields(self, view, edit):
        for region in view.sel():
            if not region.empty():
                region_text = view.substr(region)
                region_text_splited = region_text.split("=")
                if len(region_text_splited) > 1:
                    text_to_return = " "
                    for index, text in enumerate(region_text_splited[1].split('|')):
                        if self._check_http(text):
                            pass
                        else: 
                            text_splited = text.strip().split(" ")
                            if text_splited:
                                if len(text_splited) > 1:
                                    text_to_return += self._finish_text(text_splited[0], self._return_params(text_splited[1:]))
                                else:
                                    text_to_return += self._finish_text(text_splited[0])
                    
                    if self.TO_CLIPBOARD:
                        sublime.set_clipboard(text_to_return)
                    else:
                        view.insert(edit, region.end(), "\n")
                        view.insert(edit, region.end(), text_to_return)



class BaseConvertToClipboardCommand(BaseConvertCommand):
    TO_CLIPBOARD = True



class ConvertStateToModel(BaseConvertCommand):
    pass

class ConvertStateToModelClipboard(ConvertStateToModel, BaseConvertToClipboardCommand):
    pass
