'use client'

import { useEffect, useState } from 'react'
import Layout from '@/components/layout/Layout'
import { profileService } from '@/lib/api/profile'
import { Profile, UpdateProfileData } from '@/types/profile'
import { useForm } from 'react-hook-form'
import Input from '@/components/common/Input'
import Button from '@/components/common/Button'
import Alert from '@/components/common/Alert'
import Loading from '@/components/common/Loading'
import { useAuth } from '@/contexts/AuthContext'

export default function ProfilePage() {
  const { user } = useAuth()
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<UpdateProfileData>()

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      setLoading(true)
      const data = await profileService.getMyProfile()
      setProfile(data)
      reset({
        full_name: data.full_name,
        faculty: data.faculty || '',
        career: data.career || '',
        phone: data.phone || '',
      })
    } catch (err: any) {
      setError('Error al cargar el perfil. Intenta nuevamente.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const onSubmit = async (data: UpdateProfileData) => {
    setError(null)
    setSuccess(null)
    setSaving(true)

    try {
      const updated = await profileService.update(data)
      setProfile(updated)
      setSuccess('Perfil actualizado correctamente')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Error al actualizar el perfil. Intenta nuevamente.'
      )
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <Layout>
        <Loading />
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Mi Perfil</h1>
          <p className="mt-2 text-gray-600">
            Actualiza tu información personal
          </p>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        {success && (
          <Alert
            type="success"
            message={success}
            onClose={() => setSuccess(null)}
          />
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              value={profile?.email || user?.email || ''}
              disabled
              className="input bg-gray-100 cursor-not-allowed"
            />
            <p className="mt-1 text-sm text-gray-500">
              El email no se puede modificar
            </p>
          </div>

          <Input
            label="Nombre Completo"
            {...register('full_name', {
              required: 'El nombre es requerido',
            })}
            error={errors.full_name?.message}
          />

          <Input
            label="Facultad"
            {...register('faculty')}
            error={errors.faculty?.message}
          />

          <Input
            label="Carrera"
            {...register('career')}
            error={errors.career?.message}
          />

          <Input
            label="Teléfono"
            type="tel"
            {...register('phone')}
            error={errors.phone?.message}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tipo de Usuario
            </label>
            <input
              type="text"
              value={
                profile?.user_type === 'STUDENT' ? 'Estudiante' : 'General'
              }
              disabled
              className="input bg-gray-100 cursor-not-allowed"
            />
          </div>

          <Button type="submit" variant="primary" loading={saving}>
            Guardar Cambios
          </Button>
        </form>
      </div>
    </Layout>
  )
}
