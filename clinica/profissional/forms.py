from django.forms import ModelForm, fields
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profissional

#Criar o profissional
class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'endereco', 'especializacao', 'numTelefone', 'salario']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Nome'}),

            'endereco': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'endereco'}),


            'especializacao' : forms.Textarea(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','rows' : 6, 'cols' : 50, 'placeholder': 'Especialização'}),
            
            'numTelefone': forms.NumberInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Número de telefone'}),

            'salario': forms.NumberInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe salário'}),
        }
    
    # #Adiciona estilos nos campos da senha
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password1'].widget.attrs.update({
    #         'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Senha'})
    #     self.fields['password2'].widget.attrs.update({
    #         'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Confirme a senha'})


'''formulário para atualizar as informações de funcionário'''
class EditProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['endereco', 'especializacao', 'numTelefone']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Username'}),

            'endereco': forms.TextInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'endereco'}),

            'especializacao' : forms.Textarea(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','rows' : 6, 'cols' : 50, 'placeholder': 'Especialização'}),
            
            'numTelefone': forms.NumberInput(attrs={
                'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Número de telefone'}),
        }


#Formulário para alterar senha do profissional
class SenhaForm(UserChangeForm):
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Senha de confirmação',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Profissional
        fields = ['password1', 'password2']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch',)
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        if commit:
            user.save()
        return user
