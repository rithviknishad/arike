class CustomFormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_field_style = "bg-white rounded-xl w-full py-2 px-4"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = text_field_style
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].label
