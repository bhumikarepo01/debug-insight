from django import forms
from .models import ErrorSolution, Tag


class ErrorSolutionForm(forms.ModelForm):
    # Custom field for user input (comma-separated)
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. django, python, api'
        })
    )

    class Meta:
        model = ErrorSolution
        fields = ['error_title', 'error_description', 'solution', 'tags']

        widgets = {
            'error_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter error title'
            }),
            'error_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the error',
                'rows': 3
            }),
            'solution': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write the solution',
                'rows': 3
            }),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user:
            instance.user = user

        if commit:
            instance.save()

        # ✅ Always reset tags (important for edit)
            tags_input = self.cleaned_data.get('tags', '')

            tag_names = [
                tag.strip().lower()
                for tag in tags_input.split(',')
                if tag.strip()
            ]

            tag_objects = []
            for name in tag_names:
                tag_obj, _ = Tag.objects.get_or_create(name=name)
                tag_objects.append(tag_obj)

            # 🔥 THIS LINE IS KEY (replaces clear + set combo)
            instance.tags.set(tag_objects)

        return instance