'use client'

import { useRouter } from 'next/navigation'
import Layout from '@/components/layout/Layout'
import { catalogService } from '@/lib/api/catalog'
import { CreateServiceData } from '@/types/service'
import { useForm } from 'react-hook-form'
import Input from '@/components/common/Input'
import Button from '@/components/common/Button'
import Alert from '@/components/common/Alert'
import { useState } from 'react'

export default function NewServicePage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateServiceData>()

  const onSubmit = async (data: CreateServiceData) => {
    setError(null)
    setLoading(true)

    try {
      await catalogService.create(data)
      router.push('/admin/services')
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Error al crear el servicio. Intenta nuevamente.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout requireAdmin>
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Nuevo Servicio</h1>
          <p className="mt-2 text-gray-600">
            Crea un nuevo servicio en el catálogo
          </p>
        </div>

        {error && (
          <Alert type="error" message={error} onClose={() => setError(null)} />
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-6">
          <Input
            label="Nombre del Servicio"
            {...register('name', {
              required: 'El nombre es requerido',
            })}
            error={errors.name?.message}
          />

          <Input
            label="Categoría"
            {...register('category', {
              required: 'La categoría es requerida',
            })}
            error={errors.category?.message}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Descripción
            </label>
            <textarea
              {...register('description', {
                required: 'La descripción es requerida',
              })}
              className="input"
              rows={4}
            />
            {errors.description && (
              <p className="mt-1 text-sm text-red-600">
                {errors.description.message}
              </p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Precio Estudiante"
              type="number"
              step="0.01"
              {...register('prices.student', {
                required: 'El precio es requerido',
                valueAsNumber: true,
              })}
              error={errors.prices?.student?.message}
            />

            <Input
              label="Precio General"
              type="number"
              step="0.01"
              {...register('prices.general', {
                required: 'El precio es requerido',
                valueAsNumber: true,
              })}
              error={errors.prices?.general?.message}
            />
          </div>

          <div className="flex space-x-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => router.back()}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="primary"
              loading={loading}
              className="flex-1"
            >
              Crear Servicio
            </Button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
