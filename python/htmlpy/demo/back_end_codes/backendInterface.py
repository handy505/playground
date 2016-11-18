import htmlPy
import json


class BackEnd(htmlPy.Object):
    # @htmlPy.Slot(arg1_type, arg2_type, ..., result=return_type)
    @htmlPy.Slot(str, result=str)
    def say_hello_world(self,arg1):
        print("say_hello_world"+arg1)
        # self.app.html = "Hello, world"
        return "123"

    @htmlPy.Slot()
    def method(self):        
        self.app.html = "method"

    @htmlPy.Slot()
    def function_name(self):
        # This is the function exposed to GUI events.
        # You can change app HTML from here.
        # Or, you can do pretty much any python from here.
        #
        # NOTE: @htmlPy.Slot decorater needs argument and return data-types.
        # Refer to API documentation.
        print("function name")
        s = "{}, {}".format(self.app.width, self.app.height)
        print(s)
        return

    @htmlPy.Slot(str, result=str)
    def form_function_name(self, json_data):
        # @htmlPy.Slot(arg1_type, arg2_type, ..., result=return_type)
        # This function can be used for GUI forms.
        #
        print(json_data)

        d = json.loads(json_data)
        print(d)
        d["val"] = 100
        print(d)

        jsonstr = json.dumps(d)
        jscode = 'document.getElementById("d1").innerHTML="{val}";'.format(val=d["name"])
        print(jscode)
        self.app.evaluate_javascript(jscode)
        return json.dumps(d)

    @htmlPy.Slot()
    def javascript_function(self):
        # Any function decorated with @htmlPy.Slot decorater can be called
        # using javascript in GUI
        print("javascript_function")
        return        