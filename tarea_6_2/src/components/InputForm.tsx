import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Label } from '@/components/ui/label';

const RegistrationForm = ({ setIsLogin, setIsEmployee }: { setIsLogin: (value: boolean) => void, setIsEmployee: (value: boolean) => void }) => {
  const [formData, setFormData] = useState({
    email: '',
    age: '',
    employeeCode: ''
  });

  const [errors, setErrors] = useState({
    email: '',
    age: '',
    employeeCode: ''
  });

  const [submitError, setSubmitError] = useState('');

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return 'El formato del correo electrónico no es válido';
    }
    return '';
  };

  const validateAge = (age: string) => {
    const ageNum = parseInt(age);
    if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) {
      return 'La edad debe ser un número entre 1 y 120';
    }
    if (ageNum < 18) {
      return 'Lo sentimos, no tienes edad suficiente para registrarte';
    }
    return '';
  };

  const validateEmployeeCode = (code: string, isEmployeeDomain: boolean) => {
    console.log(code, isEmployeeDomain);
    if (isEmployeeDomain && (!code || code.length !== 6)) {
      return 'El código de empleado debe tener exactamente 6 caracteres';
    }
    return '';
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Limpiar errores al escribir
    setErrors(prev => ({ ...prev, [name]: '' }));
    setSubmitError('');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const isEmployeeDomain = formData.email.endsWith('umg.com');
    
    // Validar todos los campos
    const newErrors = {
      email: validateEmail(formData.email),
      age: validateAge(formData.age),
      employeeCode: validateEmployeeCode(formData.employeeCode, isEmployeeDomain)
    };

    setErrors(newErrors);

    // Verificar si hay errores
    if (Object.values(newErrors).some(error => error !== '')) {
      setSubmitError('Por favor, corrige los errores en el formulario');
      return;
    }

    setIsLogin(true);
    setIsEmployee(isEmployeeDomain);
    // Aquí iría la lógica para enviar el formulario
    console.log('Formulario enviado:', formData);
  };

  const isEmployeeDomain = formData.email.endsWith('umg.com');

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Registro de Usuario</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Correo Electrónico</Label>
            <Input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'border-red-500' : ''}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="age">Edad</Label>
            <Input
              id="age"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              className={errors.age ? 'border-red-500' : ''}
            />
            {errors.age && (
              <p className="text-sm text-red-500">{errors.age}</p>
            )}
          </div>

          {isEmployeeDomain && (
            <div className="space-y-2">
              <Label htmlFor="employeeCode">Código de Empleado</Label>
              <Input
                id="employeeCode"
                name="employeeCode"
                value={formData.employeeCode}
                onChange={handleChange}
                className={errors.employeeCode ? 'border-red-500' : ''}
                maxLength={6}
              />
              {errors.employeeCode && (
                <p className="text-sm text-red-500">{errors.employeeCode}</p>
              )}
            </div>
          )}

          {submitError && (
            <Alert variant="destructive">
              <AlertDescription>{submitError}</AlertDescription>
            </Alert>
          )}

          <Button type="submit" className="w-full">
            Registrarse
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default RegistrationForm;