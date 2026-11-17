from django.forms.widgets import MultiWidget, NumberInput
from django.utils.safestring import mark_safe


class SliderRangeWidget(MultiWidget):
    def __init__(self, min_value=0, max_value=10000, step=50, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

        widgets = [
            NumberInput(attrs={'type': 'hidden'}),
            NumberInput(attrs={'type': 'hidden'}),
        ]

        super().__init__(widgets, **kwargs)

    def decompress(self, value):
        if hasattr(value, "start") and hasattr(value, "stop"):
            return [value.start, value.stop]
        if isinstance(value, slice):
            return [value.start, value.stop]
        if isinstance(value, (list, tuple)) and len(value) == 2:
            return value
        return [self.min_value, self.max_value]

    def render(self, name, value, attrs=None, renderer=None):
        v0, v1 = self.decompress(value)
        hidden_html = super().render(name, [v0, v1], attrs, renderer)

        return mark_safe(hidden_html)
