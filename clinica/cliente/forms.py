# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from servico.models import Servico

# from.models import Cliente,AgendarServico
# from django import forms

# #Formulário de cadastro de clientes
# class ClienteForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = ['nome', 'endereco', 'telefone']
#         widgets = {
#             'nome' : forms.TextInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu nome'}),
#             'endereco' : forms.TextInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu nome'}),
#             'telefone' : forms.NumberInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu nome'})
#         }

# #formulario para editar dados do Cliente
# class EditClienteForm(forms.ModelForm):
#     class Meta:
#         model = Cliente
#         fields = ['nome', 'endereco', 'telefone']
#         widgets = {
#             'nome' : forms.TextInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu nome completo'}),
#             'endereco' : forms.TextInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu endereço'}),
#             'telefone' : forms.NumberInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu telefone'})
#         }


# #Formulário para alterar senha do cliente
# class SenhaForm(UserChangeForm):
#     password1 = forms.CharField(
#         label='Senha',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
#     password2 = forms.CharField(
#         label='Senha de confirmação',
#         widget=forms.PasswordInput(attrs={'class': 'form-control'})
#     )
#     class Meta:
#         model = Cliente
#         fields = ['password1', 'password2']
    
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch',)
#         return password2
    
#     def save(self, commit=True):
#         cliente = super().save(commit=False)
#         cliente.user.set_password(self.cleaned_data['password1'])
#         cliente.user.save()
#         if commit:
#             cliente.save()
#         return cliente

# #Agendar Servico
# class AgendarServicoForm(forms.ModelForm):
#         #criar o campo com mutiplas seleções
#     servico = forms.ModelMultipleChoiceField(
#         queryset=Servico.objects.all(),
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'select-multiple'})
#     )
#     class Meta:
#         model = AgendarServico
#         fields = ['nomeCliente', 'servico', 'data', 'horario']
#         widgets = {
#             'nomeCliente' : forms.TextInput(attrs={
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50','placeholder': 'Informe seu nome completo'}),
#             'data': forms.TextInput(attrs={
#                 'type': 'date',
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50'
#             }),
#             'horario': forms.TextInput(attrs={
#                 'type': 'time',
#                 'class': 'form-control py-3 border-white bg-transparent text-white w-50'
#             }),
#         }
#     # Cria uma função clean para verificar se já tem um serviço agendado para o mesmo horário
#     # Se caso tiver não deixar agendar o serviço.
#     def clean(self):
#         limpahora = super().clean()
#         servicosMarcados = limpahora.get('servico')
#         hora = limpahora.get('horario')

#         if servicosMarcados and hora:
#             for servicos in servicosMarcados:
#                 horarioIgual = self._meta.model.objects.filter(
#                     servico = servicos,
#                     horario = hora
#                 )
#                 if self.instance.pk:
#                     horarioIgual = horarioIgual.exclude(pk=self.instance.pk)

#                 if horarioIgual.exists():
#                     raise forms.ValidationError(
#                         f"Serviço '{servicos.servico}' já está agendado para este horario {hora}"
#                     )
#         return limpahora