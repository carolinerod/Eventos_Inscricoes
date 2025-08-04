from django import forms
from .models import Evento, Participante

class EventoForm(forms.ModelForm):
    data = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'type': 'text',
                'placeholder': 'dd/mm/aaaa',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'data', 'local', 'descricao', 'capacidade', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do evento'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade máxima'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_capacidade(self):
        capacidade = self.cleaned_data.get('capacidade')
        if capacidade <= 0:
            raise forms.ValidationError("A capacidade deve ser maior que zero.")
        return capacidade


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email', 'telefone', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com', 'autocomplete': 'off'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX', 'autocomplete': 'off'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alguma observação?', 'rows': 3}),
        }
