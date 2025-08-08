from django import forms
from .models import Evento, Participante

class EventoForm(forms.ModelForm):
    data = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'type': 'text',
                'placeholder': 'dd/mm/aaaa hh:mm',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        ),
        label='Data e Hora do Evento'
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'tipo', 'data', 'local', 'descricao',
                  'observacao_organizador', 'capacidade', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do evento'}),
            'observacao_organizador': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Informações úteis aos participantes (aparece na inscrição)',
                'rows': 3
            }),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidade máxima'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_capacidade(self):
        capacidade = self.cleaned_data.get('capacidade')
        if capacidade is not None and capacidade <= 0:
            raise forms.ValidationError("A capacidade deve ser maior que zero.")
        return capacidade


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email', 'telefone', 'assistencia', 'assistencia_detalhes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com', 'autocomplete': 'off'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX', 'autocomplete': 'off'}),
            'assistencia': forms.RadioSelect(attrs={'id': 'id_assistencia'}),
            'assistencia_detalhes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'id': 'id_assistencia_detalhes',
                'placeholder': 'Descreva a assistência necessária'
            }),
        }

    def clean(self):
        cleaned = super().clean()
        assistencia = cleaned.get('assistencia')
        detalhes = (cleaned.get('assistencia_detalhes') or '').strip()

        if assistencia == 'OUTRA' and not detalhes:
            self.add_error('assistencia_detalhes', 'Descreva a assistência necessária.')
        if assistencia != 'OUTRA':
            cleaned['assistencia_detalhes'] = ''  
        return cleaned
